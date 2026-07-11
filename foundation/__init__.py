"""AGOS Foundation - Universal civilization foundation."""

from .identity import (
    Identity, IdentityManager, IdentityType, IdentityStatus,
    GlobalIDGenerator, NamespaceManager, ObjectLocator, AliasManager, ReferenceManager,
    UniversalIdentityPlatform
)
from .relationship import Relationship, RelationshipManager, RelationshipType
from .time_ import TimeManager, TimeZone, TemporalContext
from .truth import Truth, TruthEngine, TruthLevel
from .validation import Validator, ValidationResult, ValidationRule, ValidationRuleType
from .policy import Policy, PolicyManager, PolicyType
from .dependency import Dependency, DependencyGraph, DependencyType
from .evidence import Evidence, EvidenceManager, EvidenceChain, EvidenceStatus
from .object import UniversalObject, ObjectManager, ObjectType
from .event import Event, EventBus, EventType, EventPriority, EventStatus

__all__ = [
    "Identity", "IdentityManager", "IdentityType", "IdentityStatus",
    "GlobalIDGenerator", "NamespaceManager", "ObjectLocator", "AliasManager", "ReferenceManager",
    "UniversalIdentityPlatform",
    "Relationship", "RelationshipManager", "RelationshipType",
    "TimeManager", "TimeZone", "TemporalContext",
    "Truth", "TruthEngine", "TruthLevel",
    "Validator", "ValidationResult", "ValidationRule", "ValidationRuleType",
    "Policy", "PolicyManager", "PolicyType",
    "Dependency", "DependencyGraph", "DependencyType",
    "Evidence", "EvidenceManager", "EvidenceChain", "EvidenceStatus",
    "UniversalObject", "ObjectManager", "ObjectType",
    "Event", "EventBus", "EventType", "EventPriority", "EventStatus",
]

__version__ = "1.0.0"
