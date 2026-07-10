"""Lightweight, thread-safe telemetry counters per workspace."""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TelemetryCounter:
    name: str
    value: int = 0


class WorkspaceTelemetry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def incr(self, workspace_id: str, name: str, amount: int = 1) -> int:
        with self._lock:
            self._counters[workspace_id][name] += amount
            return self._counters[workspace_id][name]

    def get(self, workspace_id: str, name: str) -> int:
        with self._lock:
            return self._counters[workspace_id].get(name, 0)

    def snapshot(self, workspace_id: str) -> Dict[str, int]:
        with self._lock:
            return dict(self._counters.get(workspace_id, {}))

    def all(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {ws: dict(counters) for ws, counters in self._counters.items()}
