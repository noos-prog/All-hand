"""Domain framework: policy application over an :class:`EnterpriseGraph`."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Mapping, Sequence

from .entities import Entity, EntityKind
from .enterprise import EnterpriseGraph


@dataclass(frozen=True)
class DomainPolicy:
    name: str
    applies_to: EntityKind
    check: Callable[[Entity, Mapping[str, object]], bool]
    message: str = ""


@dataclass
class PolicyResult:
    entity: Entity
    policy: DomainPolicy
    passed: bool
    message: str


class DomainFramework:
    """Register and evaluate declarative domain policies."""

    def __init__(self) -> None:
        self._policies: List[DomainPolicy] = []

    def register(self, policy: DomainPolicy) -> None:
        self._policies.append(policy)

    def register_many(self, policies: Iterable[DomainPolicy]) -> None:
        for p in policies:
            self.register(p)

    def evaluate(
        self, graph: EnterpriseGraph, context: Mapping[str, object] | None = None
    ) -> List[PolicyResult]:
        ctx = dict(context or {})
        out: List[PolicyResult] = []
        for policy in self._policies:
            for entity in graph.entities(kind=policy.applies_to):
                try:
                    ok = bool(policy.check(entity, ctx))
                except Exception as exc:  # pragma: no cover - defensive
                    ok = False
                    msg = f"{policy.message or policy.name}: {exc}"
                else:
                    msg = policy.message or policy.name
                out.append(PolicyResult(entity=entity, policy=policy, passed=ok, message=msg))
        return out

    def failing(self, results: Sequence[PolicyResult]) -> List[PolicyResult]:
        return [r for r in results if not r.passed]
