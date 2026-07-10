"""
AGOS Domain
===========

Structured representation of an entire enterprise as an AGOS-native
knowledge graph: departments, employees, agents, projects, processes,
policies, objectives, risks, budgets, infrastructure, products,
services and knowledge assets.

The graph supports typed entities, typed relationships, deterministic
traversal, policy application, dependency resolution (topological sort),
and a small declarative SDK/DSL for building domains in code.
"""

from .entities import (
    Entity,
    EntityKind,
    Relationship,
    RelationshipKind,
)
from .enterprise import EnterpriseGraph, UniversalAutonomousEnterprise
from .framework import DomainFramework, DomainPolicy, PolicyResult
from .composition import compose, compose_all
from .sdk import DomainBuilder
from .universal import UniversalDomain

__all__ = [
    "DomainBuilder",
    "DomainFramework",
    "DomainPolicy",
    "Entity",
    "EntityKind",
    "EnterpriseGraph",
    "PolicyResult",
    "Relationship",
    "RelationshipKind",
    "UniversalAutonomousEnterprise",
    "UniversalDomain",
    "compose",
    "compose_all",
]
