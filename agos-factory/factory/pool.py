#!/usr/bin/env python3
"""
AgentPool — a bounded, recyclable pool of live `FactoryAgent` instances.

This is the component that makes "millions of agents" a throughput claim
instead of a memory claim: a pool for a given specialization never holds
more than `blueprint.max_concurrency` *concurrently executing* agents, no
matter how many tasks are pushed through it over the civilization's
lifetime. Idle agents older than `blueprint.idle_ttl_s` are dropped so a
burst of traffic does not leave a permanently oversized pool behind.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from typing import Any, Deque, Dict, Optional

from .agent import FactoryAgent
from .blueprint import AgentBlueprint
from .metrics import FactoryMetrics

logger = logging.getLogger("agos_factory.pool")


class AgentPool:
    """Bounded pool of `FactoryAgent` instances for exactly one specialization."""

    def __init__(
        self,
        blueprint: AgentBlueprint,
        *,
        metrics: FactoryMetrics,
        llm: Optional[Any] = None,
    ) -> None:
        self.blueprint = blueprint
        self._metrics = metrics
        self._llm = llm
        self._idle: Deque[tuple[FactoryAgent, float]] = deque()
        self._active = 0
        self._current_capacity = blueprint.max_concurrency
        self._semaphore = asyncio.Semaphore(blueprint.max_concurrency)
        self._lock = asyncio.Lock()
        self._closed = False

    @property
    def specialization(self) -> str:
        return self.blueprint.specialization

    @property
    def active(self) -> int:
        return self._active

    @property
    def idle_count(self) -> int:
        return len(self._idle)

    @property
    def capacity(self) -> int:
        """Current concurrency ceiling — starts at the blueprint's default
        and moves independently once `resize()` is called, since the
        blueprint itself stays immutable and shared across pools."""
        return self._current_capacity

    async def _acquire_agent(self) -> FactoryAgent:
        async with self._lock:
            self._evict_expired_locked()
            if self._idle:
                agent, _ = self._idle.pop()
                return agent
        return FactoryAgent(self.blueprint, llm=self._llm)

    def _evict_expired_locked(self) -> None:
        """Drop idle agents that outlived `idle_ttl_s`. Caller holds `_lock`."""
        cutoff = time.time() - self.blueprint.idle_ttl_s
        while self._idle and self._idle[0][1] < cutoff:
            self._idle.popleft()

    async def _release_agent(self, agent: FactoryAgent) -> None:
        async with self._lock:
            if self._closed:
                return
            # Recycle bound: never keep more idle agents than the concurrency
            # cap — anything beyond that is simply garbage-collected.
            if len(self._idle) < self._current_capacity:
                self._idle.append((agent, time.time()))
            else:
                await self._metrics.record_recycle(self.specialization)

    async def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one task on a pooled agent, respecting the concurrency cap.

        This is the only way tasks should reach a `FactoryAgent` — it
        guarantees the specialization never exceeds its configured resource
        budget regardless of how many callers request work concurrently.
        """
        if self._closed:
            raise RuntimeError(f"pool for '{self.specialization}' is closed")

        async with self._semaphore:
            agent = await self._acquire_agent()
            async with self._lock:
                self._active += 1
            await self._metrics.record_spawn(self.specialization, active_now=self._active)
            try:
                outcome = await agent.execute(task)
                await self._metrics.record_task(
                    self.specialization, ok=bool(outcome.get("ok")), elapsed_s=outcome.get("elapsed_s", 0.0)
                )
                return outcome
            finally:
                async with self._lock:
                    self._active -= 1
                await self._release_agent(agent)

    async def resize(self, max_concurrency: int) -> None:
        """Adjust the concurrency ceiling at runtime (used by the autoscaler).

        Growing simply widens the semaphore. Shrinking lets in-flight work
        finish naturally — the semaphore's internal counter is corrected by
        acquiring the delta so it can never go negative.
        """
        if max_concurrency <= 0:
            raise ValueError("max_concurrency must be > 0")
        current = self._current_capacity
        delta = max_concurrency - current
        self._resize_semaphore(delta)
        self._current_capacity = max_concurrency
        logger.info("pool '%s' resized: %d -> %d", self.specialization, current, max_concurrency)

    def _resize_semaphore(self, delta: int) -> None:
        if delta > 0:
            for _ in range(delta):
                self._semaphore.release()
        elif delta < 0:
            for _ in range(-delta):
                # Best-effort tightening: only takes effect once currently
                # held permits are released; never blocks the caller.
                if self._semaphore._value > 0:  # noqa: SLF001 - intentional, no public API for this
                    self._semaphore._value -= 1  # noqa: SLF001

    async def drain_and_close(self) -> None:
        """Stop accepting new idle agents and release references for GC."""
        async with self._lock:
            self._closed = True
            self._idle.clear()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "specialization": self.specialization,
            "active": self._active,
            "idle": len(self._idle),
            "max_concurrency": self._current_capacity,
        }
