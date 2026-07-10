"""Deliberation engine: multi-round reasoning with pruning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Mapping, Sequence

from cognition.model import Alternative, Decision

from .decision import DecisionEngine
from .evaluation import EvaluationEngine, EvaluationResult


@dataclass
class DeliberationResult:
    rounds: int
    decisions: List[Decision] = field(default_factory=list)
    evaluations: List[EvaluationResult] = field(default_factory=list)
    final: Decision | None = None


@dataclass
class DeliberationEngine:
    decision: DecisionEngine = field(default_factory=DecisionEngine)
    evaluation: EvaluationEngine = field(default_factory=EvaluationEngine)
    max_rounds: int = 3
    min_confidence: float = 0.75

    def deliberate(
        self,
        alternatives: Sequence[Alternative],
        context: Mapping[str, Any],
        criteria: Mapping[str, float],
    ) -> DeliberationResult:
        result = DeliberationResult(rounds=0)
        pool: List[Alternative] = list(alternatives)
        ctx = dict(context)

        for _ in range(self.max_rounds):
            if not pool:
                break
            result.rounds += 1
            decision = self.decision.decide(pool, ctx)
            evaluation = self.evaluation.evaluate(decision.chosen, criteria)
            result.decisions.append(decision)
            result.evaluations.append(evaluation)
            result.final = decision

            if decision.confidence >= self.min_confidence and evaluation.approved:
                break

            # prune lowest-scoring half and continue with a boost on remaining
            ranked = sorted(pool, key=lambda a: a.score, reverse=True)
            pool = ranked[: max(1, len(ranked) // 2)]
            ctx = {**ctx, f"boost:{decision.chosen.name}": ctx.get(f"boost:{decision.chosen.name}", 0.0) + 0.1}

        return result
