"""Time-based decay policies for episodic and semantic importance."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol


class DecayPolicy(Protocol):
    def decay(self, importance: float, age_seconds: float) -> float: ...


@dataclass
class ExponentialDecay:
    half_life_seconds: float = 7 * 24 * 3600.0

    def decay(self, importance: float, age_seconds: float) -> float:
        if self.half_life_seconds <= 0:
            return importance
        factor = 0.5 ** (max(0.0, age_seconds) / self.half_life_seconds)
        return max(0.0, min(1.0, importance * factor))


@dataclass
class LinearDecay:
    zero_after_seconds: float = 30 * 24 * 3600.0

    def decay(self, importance: float, age_seconds: float) -> float:
        if self.zero_after_seconds <= 0:
            return importance
        ratio = 1.0 - (max(0.0, age_seconds) / self.zero_after_seconds)
        return max(0.0, min(1.0, importance * ratio))


def age_seconds(t: datetime, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return (now - t).total_seconds()
