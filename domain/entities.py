"""Typed entities and relationships for the enterprise graph."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class EntityKind(str, Enum):
    DEPARTMENT = "department"
    EMPLOYEE = "employee"
    AGENT = "agent"
    PROJECT = "project"
    PROCESS = "process"
    POLICY = "policy"
    OBJECTIVE = "objective"
    RISK = "risk"
    BUDGET = "budget"
    INFRASTRUCTURE = "infrastructure"
    PRODUCT = "product"
    SERVICE = "service"
    KNOWLEDGE = "knowledge"


class RelationshipKind(str, Enum):
    PART_OF = "part_of"
    REPORTS_TO = "reports_to"
    OWNS = "owns"
    OPERATES = "operates"
    DEPENDS_ON = "depends_on"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    MITIGATES = "mitigates"
    FUNDS = "funds"
    APPLIES_TO = "applies_to"
    KNOWS = "knows"


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class Entity:
    entity_id: str
    kind: EntityKind
    name: str
    properties: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def new(cls, kind: EntityKind, name: str, **properties: Any) -> "Entity":
        return cls(entity_id=_new_id(kind.value), kind=kind, name=name, properties=properties)


@dataclass(frozen=True)
class Relationship:
    source: str
    target: str
    kind: RelationshipKind
    properties: Mapping[str, Any] = field(default_factory=dict)

    def key(self) -> tuple[str, str, str]:
        return (self.source, self.target, self.kind.value)
