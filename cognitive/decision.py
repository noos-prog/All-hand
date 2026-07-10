"""Decision engine: pick the best alternative under a scoring policy."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from cognition.model import Alternative, CognitiveError, Decision


ScoringFn = Callable[[Alternative, Mapping[str, Any]], float]


def _default_score(alt: Alternative, context: Mapping[str, Any]) -> float:
    boost = float(context.get(f"boost:{alt.name}", 0.0))
    return alt.score + boost


@dataclass
class DecisionEngine:
    scoring: ScoringFn = _default_score
    tie_breaker: Callable[[Sequence[Alternative]], Alternative] = field(
        default=lambda alts: sorted(alts, key=lambda a: a.name)[0]
    )

    def decide(
        self, alternatives: Sequence[Alternative], context: Mapping[str, Any]
    ) -> Decision:
        if not alternatives:
            raise CognitiveError("no alternatives to decide over")
        scored = [
            Alternative(
                name=alt.name,
                payload=alt.payload,
                score=self.scoring(alt, context),
                rationale=alt.rationale,
            )
            for alt in alternatives
        ]
        top_score = max(a.score for a in scored)
        top = [a for a in scored if math.isclose(a.score, top_score)]
        chosen = top[0] if len(top) == 1 else self.tie_breaker(top)
        total = sum(math.exp(a.score - top_score) for a in scored)
        confidence = 1.0 / total if total > 0 else 1.0
        return Decision(
            chosen=chosen,
            considered=tuple(sorted(scored, key=lambda a: a.score, reverse=True)),
            rationale=chosen.rationale or f"top score {chosen.score:.3f}",
            confidence=confidence,
        )
