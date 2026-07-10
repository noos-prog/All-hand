"""Compose multiple :class:`EnterpriseGraph` instances into one."""

from __future__ import annotations

from typing import Iterable

from .enterprise import EnterpriseGraph, EnterpriseGraphError


def compose(*graphs: EnterpriseGraph) -> EnterpriseGraph:
    """Merge graphs. Duplicate entity ids raise EnterpriseGraphError."""
    out = EnterpriseGraph()
    for g in graphs:
        for e in g.entities():
            out.add_entity(e)
        for eid in list(g.entities()):
            for r in g.outgoing(eid.entity_id):
                out.relate(r)
    return out


def compose_all(graphs: Iterable[EnterpriseGraph]) -> EnterpriseGraph:
    return compose(*list(graphs))
