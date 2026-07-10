"""Small declarative SDK for building an enterprise graph in code."""

from __future__ import annotations

from typing import Any, Dict, List

from .entities import Entity, EntityKind, Relationship, RelationshipKind
from .enterprise import EnterpriseGraph


class DomainBuilder:
    """Chainable builder that produces an :class:`EnterpriseGraph`."""

    def __init__(self) -> None:
        self._graph = EnterpriseGraph()
        self._by_name: Dict[str, Entity] = {}

    # ---------------------------------------------------------------- factory
    def entity(self, kind: EntityKind, name: str, **props: Any) -> "DomainBuilder":
        if name in self._by_name:
            raise ValueError(f"duplicate entity name {name!r}")
        ent = Entity.new(kind, name, **props)
        self._graph.add_entity(ent)
        self._by_name[name] = ent
        return self

    def department(self, name: str, **props: Any) -> "DomainBuilder":
        return self.entity(EntityKind.DEPARTMENT, name, **props)

    def employee(self, name: str, **props: Any) -> "DomainBuilder":
        return self.entity(EntityKind.EMPLOYEE, name, **props)

    def agent(self, name: str, **props: Any) -> "DomainBuilder":
        return self.entity(EntityKind.AGENT, name, **props)

    def project(self, name: str, **props: Any) -> "DomainBuilder":
        return self.entity(EntityKind.PROJECT, name, **props)

    def objective(self, name: str, **props: Any) -> "DomainBuilder":
        return self.entity(EntityKind.OBJECTIVE, name, **props)

    # ---------------------------------------------------------------- edges
    def link(self, source: str, kind: RelationshipKind, target: str, **props: Any) -> "DomainBuilder":
        s = self._resolve(source)
        t = self._resolve(target)
        self._graph.relate(Relationship(source=s.entity_id, target=t.entity_id, kind=kind, properties=props))
        return self

    def part_of(self, source: str, parent: str) -> "DomainBuilder":
        return self.link(source, RelationshipKind.PART_OF, parent)

    def reports_to(self, source: str, manager: str) -> "DomainBuilder":
        return self.link(source, RelationshipKind.REPORTS_TO, manager)

    def depends_on(self, source: str, dependency: str) -> "DomainBuilder":
        return self.link(source, RelationshipKind.DEPENDS_ON, dependency)

    def owns(self, source: str, asset: str) -> "DomainBuilder":
        return self.link(source, RelationshipKind.OWNS, asset)

    # --------------------------------------------------------------- output
    def build(self) -> EnterpriseGraph:
        return self._graph

    def names(self) -> List[str]:
        return sorted(self._by_name.keys())

    def _resolve(self, name: str) -> Entity:
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise ValueError(f"unknown entity name {name!r}") from exc
