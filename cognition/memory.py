"""In-memory working memory and belief store used by the cognitive pipeline."""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Iterator, List, Optional, Tuple

from .model import Belief, Evidence, Observation


class WorkingMemory:
    """A bounded LRU cache of recent observations."""

    def __init__(self, capacity: int = 1024) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._lock = threading.Lock()
        self._store: "OrderedDict[str, Observation]" = OrderedDict()

    def remember(self, key: str, observation: Observation) -> None:
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = observation
            while len(self._store) > self._capacity:
                self._store.popitem(last=False)

    def recall(self, key: str) -> Optional[Observation]:
        with self._lock:
            obs = self._store.get(key)
            if obs is not None:
                self._store.move_to_end(key)
            return obs

    def recent(self, n: int = 16) -> List[Tuple[str, Observation]]:
        with self._lock:
            items = list(self._store.items())
        return items[-n:]

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)

    def __iter__(self) -> Iterator[str]:
        with self._lock:
            return iter(list(self._store.keys()))


class BeliefStore:
    """Additive belief store with evidence-weighted confidence updates."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._beliefs: Dict[str, Belief] = {}

    def upsert(self, statement: str, evidence: Evidence) -> Belief:
        with self._lock:
            current = self._beliefs.get(statement)
            if current is None:
                belief = Belief(
                    statement=statement,
                    confidence=max(0.0, min(1.0, evidence.weight * evidence.confidence)),
                    evidence=(evidence,),
                )
            else:
                combined = list(current.evidence) + [evidence]
                total_weight = sum(e.weight for e in combined) or 1.0
                new_conf = sum(e.weight * e.confidence for e in combined) / total_weight
                belief = Belief(
                    statement=statement,
                    confidence=max(0.0, min(1.0, new_conf)),
                    evidence=tuple(combined),
                )
            self._beliefs[statement] = belief
            return belief

    def get(self, statement: str) -> Optional[Belief]:
        with self._lock:
            return self._beliefs.get(statement)

    def top(self, n: int = 10) -> List[Belief]:
        with self._lock:
            values = list(self._beliefs.values())
        values.sort(key=lambda b: b.confidence, reverse=True)
        return values[:n]

    def __len__(self) -> int:
        with self._lock:
            return len(self._beliefs)
