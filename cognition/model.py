"""Core data model for the cognition layer.

Everything is a frozen dataclass so cognitive steps stay pure and safely
shareable across threads and agent boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Protocol, Sequence, Tuple


class CognitiveError(Exception):
    """Raised when a cognitive step cannot produce a result."""


@dataclass(frozen=True)
class Observation:
    """A raw signal presented to cognition."""
    source: str
    payload: Any
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Evidence:
    """A weighted, provenance-tagged piece of support for a belief."""
    statement: str
    weight: float
    source: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be within [0, 1]")


@dataclass(frozen=True)
class Belief:
    statement: str
    confidence: float
    evidence: Tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class Intent:
    verb: str
    target: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass(frozen=True)
class Goal:
    name: str
    description: str
    success_criteria: Tuple[str, ...] = ()
    priority: int = 0


@dataclass(frozen=True)
class Hypothesis:
    statement: str
    prior: float = 0.5

    def posterior(self, likelihood: float, evidence_weight: float) -> float:
        """Return a Bayesian posterior given a likelihood and evidence weight."""
        if not 0.0 <= likelihood <= 1.0:
            raise ValueError("likelihood must be within [0, 1]")
        if evidence_weight < 0:
            raise ValueError("evidence_weight must be non-negative")
        numerator = likelihood * self.prior
        denominator = numerator + (1 - likelihood) * (1 - self.prior)
        if denominator == 0:
            return self.prior
        base = numerator / denominator
        # Damp the update by evidence weight in [0, 1].
        w = min(1.0, evidence_weight)
        return self.prior * (1 - w) + base * w


@dataclass(frozen=True)
class Alternative:
    name: str
    payload: Any
    score: float = 0.0
    rationale: str = ""


@dataclass(frozen=True)
class PlanStep:
    index: int
    action: str
    inputs: Mapping[str, Any] = field(default_factory=dict)
    expected_outcome: str = ""
    depends_on: Tuple[int, ...] = ()


@dataclass(frozen=True)
class Plan:
    goal: Goal
    steps: Tuple[PlanStep, ...]

    def is_dag(self) -> bool:
        indices = {step.index for step in self.steps}
        return all(all(d in indices and d < s.index for d in s.depends_on) for s in self.steps)


@dataclass(frozen=True)
class Decision:
    chosen: Alternative
    considered: Tuple[Alternative, ...]
    rationale: str
    confidence: float = 1.0


class Reasoner(Protocol):
    """Anything that can score and pick among alternatives."""

    def score(self, alt: Alternative, context: Mapping[str, Any]) -> float: ...

    def choose(
        self, alternatives: Sequence[Alternative], context: Mapping[str, Any]
    ) -> Decision: ...
