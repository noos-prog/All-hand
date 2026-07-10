"""Episode and semantic record data model + append-only episodic stream."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Tuple


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Episode:
    episode_id: str
    agent_id: str
    content: str
    tags: Tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utcnow)
    importance: float = 0.5


@dataclass
class SemanticRecord:
    record_id: str
    summary: str
    supports: Tuple[str, ...]  # episode ids
    tags: Tuple[str, ...]
    importance: float
    updated_at: datetime = field(default_factory=_utcnow)


class EpisodicStream:
    """Bounded, thread-safe append-only stream of episodes."""

    def __init__(self, capacity: int = 100_000) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._lock = threading.Lock()
        self._episodes: List[Episode] = []

    def append(self, episode: Episode) -> None:
        with self._lock:
            self._episodes.append(episode)
            if len(self._episodes) > self._capacity:
                overflow = len(self._episodes) - self._capacity
                del self._episodes[:overflow]

    def extend(self, episodes: Iterable[Episode]) -> None:
        for ep in episodes:
            self.append(ep)

    def snapshot(self) -> List[Episode]:
        with self._lock:
            return list(self._episodes)

    def drain(self) -> List[Episode]:
        with self._lock:
            out, self._episodes = self._episodes, []
            return out

    def __len__(self) -> int:
        with self._lock:
            return len(self._episodes)
