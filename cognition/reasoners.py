"""Concrete, deterministic reasoners.

These are pure functions with no external calls, safe to use as
defaults, in tests, and as fallbacks when an LLM-backed reasoner is
unavailable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .model import Alternative, CognitiveError, Decision


@dataclass
class WeightedReasoner:
    """Scores alternatives by a weighted sum over context features."""

    weights: Mapping[str, float] = field(default_factory=dict)
    bias: float = 0.0

    def score(self, alt: Alternative, context: Mapping[str, Any]) -> float:
        if alt.score:
            base = float(alt.score)
        else:
            base = 0.0
        features = {**context, **_flatten(getattr(alt.payload, "__dict__", {}) or {})}
        weighted = sum(float(features.get(k, 0.0)) * w for k, w in self.weights.items())
        return base + weighted + self.bias

    def choose(
        self, alternatives: Sequence[Alternative], context: Mapping[str, Any]
    ) -> Decision:
        if not alternatives:
            raise CognitiveError("no alternatives to choose from")
        scored = [
            Alternative(
                name=alt.name,
                payload=alt.payload,
                score=self.score(alt, context),
                rationale=alt.rationale,
            )
            for alt in alternatives
        ]
        scored.sort(key=lambda a: a.score, reverse=True)
        chosen = scored[0]
        total = sum(math.exp(a.score) for a in scored) or 1.0
        confidence = math.exp(chosen.score) / total
        return Decision(
            chosen=chosen,
            considered=tuple(scored),
            rationale=chosen.rationale or f"top score {chosen.score:.3f}",
            confidence=confidence,
        )


class DeterministicReasoner:
    """Always picks the first alternative — useful for stable test paths."""

    def score(self, alt: Alternative, context: Mapping[str, Any]) -> float:  # noqa: ARG002
        return alt.score

    def choose(
        self, alternatives: Sequence[Alternative], context: Mapping[str, Any]  # noqa: ARG002
    ) -> Decision:
        if not alternatives:
            raise CognitiveError("no alternatives to choose from")
        chosen = alternatives[0]
        return Decision(chosen=chosen, considered=tuple(alternatives), rationale="deterministic", confidence=1.0)


def _flatten(d: Mapping[str, Any], prefix: str = "") -> Mapping[str, Any]:
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, Mapping):
            out.update(_flatten(v, prefix=f"{key}."))
        elif isinstance(v, (int, float, bool)):
            out[key] = float(v)
    return out
