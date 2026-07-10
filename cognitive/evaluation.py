"""Evaluation engine: score a candidate against weighted criteria."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping


@dataclass
class EvaluationResult:
    candidate: Any
    score: float
    breakdown: Dict[str, float]
    approved: bool
    threshold: float


class EvaluationEngine:
    def __init__(self, threshold: float = 0.5) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be within [0, 1]")
        self.threshold = threshold

    def evaluate(self, candidate: Any, criteria: Mapping[str, float]) -> EvaluationResult:
        payload = getattr(candidate, "payload", candidate)
        breakdown: Dict[str, float] = {}
        for key, weight in criteria.items():
            raw = _extract(payload, key)
            breakdown[key] = float(raw) * float(weight)
        total_weight = sum(abs(w) for w in criteria.values()) or 1.0
        score = sum(breakdown.values()) / total_weight
        score = max(0.0, min(1.0, score))
        return EvaluationResult(
            candidate=candidate,
            score=score,
            breakdown=breakdown,
            approved=score >= self.threshold,
            threshold=self.threshold,
        )


def _extract(payload: Any, key: str) -> float:
    if isinstance(payload, Mapping):
        return float(payload.get(key, 0.0))
    return float(getattr(payload, key, 0.0))
