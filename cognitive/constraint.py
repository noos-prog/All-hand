"""Constraint engine: declarative predicates over a working context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Mapping, Sequence


@dataclass(frozen=True)
class Constraint:
    name: str
    predicate: Callable[[Mapping[str, Any]], bool]
    severity: str = "hard"  # "hard" | "soft"
    description: str = ""


@dataclass(frozen=True)
class ConstraintViolation:
    constraint: Constraint
    context_snapshot: Mapping[str, Any]

    def is_hard(self) -> bool:
        return self.constraint.severity == "hard"


class ConstraintEngine:
    def __init__(self, constraints: Sequence[Constraint] = ()) -> None:
        self._constraints: List[Constraint] = list(constraints)

    def register(self, constraint: Constraint) -> None:
        self._constraints.append(constraint)

    def check(self, context: Mapping[str, Any]) -> List[ConstraintViolation]:
        violations: List[ConstraintViolation] = []
        for c in self._constraints:
            try:
                ok = bool(c.predicate(context))
            except Exception:
                ok = False
            if not ok:
                violations.append(ConstraintViolation(constraint=c, context_snapshot=dict(context)))
        return violations

    def is_feasible(self, context: Mapping[str, Any]) -> bool:
        return not any(v.is_hard() for v in self.check(context))

    def hard(self) -> List[Constraint]:
        return [c for c in self._constraints if c.severity == "hard"]

    def soft(self) -> List[Constraint]:
        return [c for c in self._constraints if c.severity == "soft"]
