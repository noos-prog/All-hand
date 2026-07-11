#!/usr/bin/env python3
"""
AgentFactory — the top-level orchestrator the rest of the civilization talks to.

Everything the civilization needs from "produce agents on demand" boils
down to three operations exposed here:

    spawn(specialization)                    -> one FactoryAgent, ready to use
    run(specialization, task)                 -> execute one task through the pool
    spawn_batch(specialization, prompts)      -> stream results for N tasks,
                                                  N unbounded in principle
    scale_to(specialization, n)               -> explicit capacity override

An `Autoscaler` runs continuously in the background (via `start_autoscaling`)
so pools track real demand without an operator manually retuning
`AGENTS_PER_SPEC` the way `server.py`'s `create_civilization()` does today.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, AsyncIterator, Dict, Iterable, Optional

from .autoscaler import Autoscaler, AutoscalerPolicy
from .blueprint import BlueprintRegistry
from .metrics import FactoryMetrics
from .pool import AgentPool

logger = logging.getLogger("agos_factory.factory")


class AgentFactory:
    """Produces and runs civilization agents on demand, at any scale."""

    def __init__(
        self,
        registry: BlueprintRegistry,
        *,
        autoscaler: Optional[Autoscaler] = None,
        autoscale_interval_s: float = 5.0,
        llm: Optional[Any] = None,
    ) -> None:
        self.registry = registry
        self.metrics = FactoryMetrics()
        self.autoscaler = autoscaler or Autoscaler()
        self._autoscale_interval_s = autoscale_interval_s
        self._llm = llm
        self._pools: Dict[str, AgentPool] = {}
        self._pools_lock = asyncio.Lock()
        self._autoscale_task: Optional[asyncio.Task] = None

    async def _pool_for(self, specialization: str) -> AgentPool:
        pool = self._pools.get(specialization)
        if pool is not None:
            return pool
        async with self._pools_lock:
            pool = self._pools.get(specialization)
            if pool is None:
                blueprint = self.registry.get(specialization)
                pool = AgentPool(blueprint, metrics=self.metrics, llm=self._llm)
                self._pools[specialization] = pool
                logger.info("pool created for '%s' (max_concurrency=%d)",
                            specialization, pool.capacity)
            return pool

    async def spawn(self, specialization: str):
        """Return one ready-to-use `FactoryAgent` for `specialization`.

        Prefer `run()` for actual task execution — it enforces the pool's
        concurrency budget. `spawn()` is exposed for callers that need a
        direct handle (e.g. multi-step conversations with one agent).
        """
        pool = await self._pool_for(specialization)
        agent = await pool._acquire_agent()  # noqa: SLF001 - factory is pool's trusted owner
        async with pool._lock:  # noqa: SLF001
            pool._active += 1  # noqa: SLF001
        await self.metrics.record_spawn(specialization, active_now=pool.active)
        return agent

    async def run(self, specialization: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one task on a pooled agent of `specialization`."""
        pool = await self._pool_for(specialization)
        return await pool.run(task)

    async def spawn_batch(
        self,
        specialization: str,
        prompts: Iterable[str],
        *,
        data: Optional[Any] = None,
        concurrency: Optional[int] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream outcomes for a (potentially huge) batch of prompts.

        This is the "millions of agents" entry point: `prompts` can be a
        generator producing millions of items lazily. Work is fanned out
        across the pool with an explicit `asyncio.Semaphore` so at most
        `concurrency` tasks run at once regardless of batch size, and
        results are yielded as they complete rather than collected into one
        giant list.
        """
        pool = await self._pool_for(specialization)
        limit = concurrency or pool.capacity
        semaphore = asyncio.Semaphore(limit)
        queue: asyncio.Queue = asyncio.Queue(maxsize=limit * 2)
        SENTINEL = object()

        async def _worker(prompt: str) -> None:
            async with semaphore:
                outcome = await pool.run({"prompt": prompt, "data": data})
                await queue.put(outcome)

        async def _producer() -> None:
            tasks = []
            try:
                for prompt in prompts:
                    tasks.append(asyncio.create_task(_worker(prompt)))
                if tasks:
                    await asyncio.gather(*tasks)
            finally:
                await queue.put(SENTINEL)

        producer_task = asyncio.create_task(_producer())
        try:
            while True:
                item = await queue.get()
                if item is SENTINEL:
                    break
                yield item
        finally:
            await producer_task

    async def scale_to(self, specialization: str, max_concurrency: int) -> None:
        """Explicitly set a pool's concurrency ceiling, bypassing the autoscaler."""
        pool = await self._pool_for(specialization)
        await pool.resize(max_concurrency)

    def set_autoscale_policy(self, specialization: str, policy: AutoscalerPolicy) -> None:
        self.autoscaler.set_policy(specialization, policy)

    async def start_autoscaling(self) -> None:
        """Start a background loop that re-tunes every known pool's capacity."""
        if self._autoscale_task is not None:
            return
        self._autoscale_task = asyncio.create_task(self._autoscale_loop())

    async def _autoscale_loop(self) -> None:
        try:
            while True:
                await asyncio.sleep(self._autoscale_interval_s)
                for pool in list(self._pools.values()):
                    await self.autoscaler.tick(pool)
        except asyncio.CancelledError:
            pass

    async def snapshot(self) -> Dict[str, Any]:
        return {
            "pools": {spec: pool.snapshot() for spec, pool in self._pools.items()},
            "metrics": await self.metrics.snapshot(),
        }

    async def shutdown(self) -> None:
        """Stop autoscaling and drain every pool. Safe to call multiple times."""
        if self._autoscale_task is not None:
            self._autoscale_task.cancel()
            try:
                await self._autoscale_task
            except asyncio.CancelledError:
                pass
            self._autoscale_task = None
        for pool in self._pools.values():
            await pool.drain_and_close()
