"""UniversalDomain: cross-vertical, cross-industry domain adapter.

Bundles an :class:`EnterpriseGraph`, a :class:`DomainFramework` and a
:class:`DomainBuilder` with a default policy pack that fits any domain
(finance, healthcare, manufacturing, software, government).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .entities import EntityKind
from .enterprise import EnterpriseGraph
from .framework import DomainFramework, DomainPolicy, PolicyResult
from .sdk import DomainBuilder


def _has_owner(entity, ctx: Mapping[str, Any]) -> bool:  # noqa: ARG001
    return bool(entity.properties.get("owner"))


def _budget_positive(entity, ctx: Mapping[str, Any]) -> bool:  # noqa: ARG001
    amount = entity.properties.get("amount", 0)
    try:
        return float(amount) >= 0
    except (TypeError, ValueError):
        return False


def _risk_mitigated(entity, ctx: Mapping[str, Any]) -> bool:  # noqa: ARG001
    return bool(entity.properties.get("mitigation"))


DEFAULT_POLICIES = (
    DomainPolicy(
        name="every_project_has_owner",
        applies_to=EntityKind.PROJECT,
        check=_has_owner,
        message="project must declare an 'owner' property",
    ),
    DomainPolicy(
        name="budget_amount_non_negative",
        applies_to=EntityKind.BUDGET,
        check=_budget_positive,
        message="budget amount must be non-negative",
    ),
    DomainPolicy(
        name="risk_has_mitigation",
        applies_to=EntityKind.RISK,
        check=_risk_mitigated,
        message="risk must declare a 'mitigation' property",
    ),
)


@dataclass
class UniversalDomain:
    graph: EnterpriseGraph = field(default_factory=EnterpriseGraph)
    framework: DomainFramework = field(default_factory=DomainFramework)

    def __post_init__(self) -> None:
        self.framework.register_many(DEFAULT_POLICIES)

    @classmethod
    def from_builder(cls, builder: DomainBuilder) -> "UniversalDomain":
        return cls(graph=builder.build())

    def validate(self, context: Mapping[str, Any] | None = None) -> list[PolicyResult]:
        return self.framework.evaluate(self.graph, context)

    def is_healthy(self) -> bool:
        results = self.validate()
        return not self.framework.failing(results)
