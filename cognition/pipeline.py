"""The cognitive pipeline: Observe -> Understand -> Reason -> Decide.

Pure functions only: no network I/O, no filesystem access, no logging
side effects. All state lives in the caller-provided ``WorkingMemory``
and ``BeliefStore``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Sequence

from .memory import BeliefStore, WorkingMemory
from .model import (
    Alternative,
    CognitiveError,
    Decision,
    Evidence,
    Goal,
    Intent,
    Observation,
    Plan,
    PlanStep,
    Reasoner,
)
from .reasoners import WeightedReasoner


@dataclass
class PipelineTrace:
    """Structured record of a full pipeline execution — useful for audit."""

    intent: Optional[Intent] = None
    beliefs: List[str] = field(default_factory=list)
    alternatives: List[Alternative] = field(default_factory=list)
    decision: Optional[Decision] = None
    plan: Optional[Plan] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class CognitivePipeline:
    """Cohesive orchestration of the individual cognitive engines."""

    reasoner: Reasoner = field(default_factory=WeightedReasoner)
    memory: WorkingMemory = field(default_factory=WorkingMemory)
    beliefs: BeliefStore = field(default_factory=BeliefStore)

    # ------------------------------------------------------------------ steps
    def observe(self, observations: Sequence[Observation]) -> None:
        for i, obs in enumerate(observations):
            self.memory.remember(f"{obs.source}:{i}", obs)

    def understand(self, observations: Sequence[Observation]) -> Intent:
        if not observations:
            raise CognitiveError("cannot infer intent without observations")
        primary = observations[0]
        verb, _, target = str(primary.payload).partition(" ")
        return Intent(
            verb=verb or "process",
            target=target or primary.source,
            parameters={"tag_count": len(primary.tags)},
            confidence=min(1.0, 0.5 + 0.1 * len(observations)),
        )

    def hypothesize(self, intent: Intent) -> List[Evidence]:
        return [
            Evidence(
                statement=f"agent should {intent.verb} {intent.target}",
                weight=1.0,
                source="cognition.hypothesize",
                confidence=intent.confidence,
            )
        ]

    def evaluate(
        self, alternatives: Sequence[Alternative], context: Mapping[str, Any]
    ) -> Decision:
        return self.reasoner.choose(alternatives, context)

    def plan(self, goal: Goal, decision: Decision) -> Plan:
        steps = _plan_from_decision(decision)
        plan = Plan(goal=goal, steps=steps)
        if not plan.is_dag():
            raise CognitiveError("planner produced a cyclic step graph")
        return plan

    # ------------------------------------------------------------------ full
    def run(
        self,
        observations: Sequence[Observation],
        alternatives: Sequence[Alternative],
        goal: Goal,
        context: Optional[Mapping[str, Any]] = None,
    ) -> PipelineTrace:
        ctx = dict(context or {})
        trace = PipelineTrace()
        self.observe(observations)

        intent = self.understand(observations)
        trace.intent = intent

        for ev in self.hypothesize(intent):
            belief = self.beliefs.upsert(ev.statement, ev)
            trace.beliefs.append(belief.statement)

        trace.alternatives = list(alternatives)
        decision = self.evaluate(alternatives, ctx)
        trace.decision = decision

        trace.plan = self.plan(goal, decision)
        return trace


class UniversalCognitiveCore(CognitivePipeline):
    """Convenience alias mirroring the historical AGOS name."""

    version = "10.0.0"


def _plan_from_decision(decision: Decision) -> tuple[PlanStep, ...]:
    steps: List[PlanStep] = []
    for i, alt in enumerate(decision.considered):
        depends = (i - 1,) if i else ()
        steps.append(
            PlanStep(
                index=i,
                action=f"consider:{alt.name}",
                inputs={"score": alt.score},
                expected_outcome=alt.rationale,
                depends_on=depends,
            )
        )
    steps.append(
        PlanStep(
            index=len(steps),
            action=f"execute:{decision.chosen.name}",
            inputs={"confidence": decision.confidence},
            expected_outcome="apply chosen alternative",
            depends_on=tuple(range(len(steps))),
        )
    )
    return tuple(steps)
