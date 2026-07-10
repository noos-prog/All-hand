"""Enterprise graph with typed traversal and dependency resolution."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple

from .entities import Entity, EntityKind, Relationship, RelationshipKind


class EnterpriseGraphError(Exception):
    """Base error for enterprise graph operations."""


class EnterpriseGraph:
    def __init__(self) -> None:
        self._entities: Dict[str, Entity] = {}
        self._out: Dict[str, List[Relationship]] = defaultdict(list)
        self._in: Dict[str, List[Relationship]] = defaultdict(list)
        self._edges: Set[Tuple[str, str, str]] = set()

    # -------------------------------------------------------------- entities
    def add_entity(self, entity: Entity) -> Entity:
        if entity.entity_id in self._entities:
            raise EnterpriseGraphError(f"duplicate entity {entity.entity_id}")
        self._entities[entity.entity_id] = entity
        return entity

    def get(self, entity_id: str) -> Entity:
        try:
            return self._entities[entity_id]
        except KeyError as exc:
            raise EnterpriseGraphError(f"unknown entity {entity_id}") from exc

    def entities(self, *, kind: Optional[EntityKind] = None) -> List[Entity]:
        values = list(self._entities.values())
        if kind is not None:
            values = [e for e in values if e.kind == kind]
        return sorted(values, key=lambda e: (e.kind.value, e.name))

    # ------------------------------------------------------------------ edges
    def relate(self, rel: Relationship) -> Relationship:
        self.get(rel.source)
        self.get(rel.target)
        key = rel.key()
        if key in self._edges:
            return rel
        self._edges.add(key)
        self._out[rel.source].append(rel)
        self._in[rel.target].append(rel)
        return rel

    def outgoing(self, entity_id: str, *, kind: Optional[RelationshipKind] = None) -> List[Relationship]:
        rels = list(self._out.get(entity_id, ()))
        return [r for r in rels if kind is None or r.kind == kind]

    def incoming(self, entity_id: str, *, kind: Optional[RelationshipKind] = None) -> List[Relationship]:
        rels = list(self._in.get(entity_id, ()))
        return [r for r in rels if kind is None or r.kind == kind]

    # ------------------------------------------------------------- traversal
    def neighbors(self, entity_id: str, *, kind: Optional[RelationshipKind] = None) -> List[Entity]:
        return [self.get(r.target) for r in self.outgoing(entity_id, kind=kind)]

    def bfs(self, start: str) -> Iterator[Entity]:
        self.get(start)
        seen: Set[str] = {start}
        queue: deque[str] = deque([start])
        while queue:
            nid = queue.popleft()
            yield self.get(nid)
            for rel in self._out.get(nid, ()):
                if rel.target not in seen:
                    seen.add(rel.target)
                    queue.append(rel.target)

    def topo_order(self, kind: RelationshipKind = RelationshipKind.DEPENDS_ON) -> List[Entity]:
        indeg: Dict[str, int] = {eid: 0 for eid in self._entities}
        adj: Dict[str, List[str]] = defaultdict(list)
        for rels in self._out.values():
            for r in rels:
                if r.kind is kind:
                    adj[r.source].append(r.target)
                    indeg[r.target] = indeg.get(r.target, 0) + 1

        queue = deque(sorted(eid for eid, d in indeg.items() if d == 0))
        order: List[Entity] = []
        while queue:
            eid = queue.popleft()
            order.append(self.get(eid))
            for nxt in sorted(adj[eid]):
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        if len(order) != len(self._entities):
            raise EnterpriseGraphError("cycle detected on kind={}".format(kind.value))
        return order

    # ------------------------------------------------------------------ stats
    def statistics(self) -> Dict[str, int]:
        by_kind: Dict[str, int] = defaultdict(int)
        for e in self._entities.values():
            by_kind[e.kind.value] += 1
        return {
            "entities": len(self._entities),
            "relationships": len(self._edges),
            **{f"kind:{k}": v for k, v in by_kind.items()},
        }

    def __len__(self) -> int:
        return len(self._entities)


@dataclass
class UniversalAutonomousEnterprise:
    """Facade over an :class:`EnterpriseGraph` with convenience helpers."""

    graph: EnterpriseGraph = field(default_factory=EnterpriseGraph)

    def register(self, entities: Iterable[Entity]) -> List[Entity]:
        return [self.graph.add_entity(e) for e in entities]

    def link(self, rels: Iterable[Relationship]) -> List[Relationship]:
        return [self.graph.relate(r) for r in rels]

    def execution_order(self) -> List[Entity]:
        return self.graph.topo_order()

    def summary(self) -> Dict[str, int]:
        return self.graph.statistics()
