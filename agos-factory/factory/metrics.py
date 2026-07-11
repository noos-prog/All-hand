#!/usr/bin/env python3
"""
Async-safe factory metrics.

Every counter here is a real, live measurement of factory activity — not a
static claim. `total_spawned` is the number that actually answers "how many
agents has this civilization produced", including ones that have since been
recycled and no longer exist as objects.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class _SpecializationCounters:
    spawned: int = 0
    recycled: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_time_s: float = 0.0
    peak_active: int = 0


class FactoryMetrics:
    """Thread-safe-within-asyncio counters for the whole factory.

    A single `asyncio.Lock` protects all mutations. Contention is not a
    concern here: increments are O(1) dict/int operations, dwarfed by the
    LLM call latency that dominates real agent execution time.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._by_spec: Dict[str, _SpecializationCounters] = {}
        self._started_at = time.time()

    def _bucket(self, specialization: str) -> _SpecializationCounters:
        bucket = self._by_spec.get(specialization)
        if bucket is None:
            bucket = _SpecializationCounters()
            self._by_spec[specialization] = bucket
        return bucket

    async def record_spawn(self, specialization: str, *, active_now: int) -> None:
        async with self._lock:
            bucket = self._bucket(specialization)
            bucket.spawned += 1
            bucket.peak_active = max(bucket.peak_active, active_now)

    async def record_recycle(self, specialization: str) -> None:
        async with self._lock:
            self._bucket(specialization).recycled += 1

    async def record_task(self, specialization: str, *, ok: bool, elapsed_s: float) -> None:
        async with self._lock:
            bucket = self._bucket(specialization)
            bucket.total_time_s += elapsed_s
            if ok:
                bucket.tasks_completed += 1
            else:
                bucket.tasks_failed += 1

    async def snapshot(self) -> Dict[str, Any]:
        async with self._lock:
            total_spawned = sum(b.spawned for b in self._by_spec.values())
            total_tasks = sum(b.tasks_completed + b.tasks_failed for b in self._by_spec.values())
            return {
                "uptime_s": round(time.time() - self._started_at, 3),
                "total_spawned": total_spawned,
                "total_tasks_processed": total_tasks,
                "by_specialization": {
                    spec: {
                        "spawned": b.spawned,
                        "recycled": b.recycled,
                        "peak_active": b.peak_active,
                        "tasks_completed": b.tasks_completed,
                        "tasks_failed": b.tasks_failed,
                        "total_time_s": round(b.total_time_s, 3),
                    }
                    for spec, b in self._by_spec.items()
                },
            }
