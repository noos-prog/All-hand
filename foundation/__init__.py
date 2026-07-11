"""AGOS Foundation - Universal civilization foundation."""

from .identity import (
    Identity, IdentityManager, IdentityType, IdentityStatus,
    GlobalIDGenerator, NamespaceManager, ObjectLocator, AliasManager, ReferenceManager,
    UniversalIdentityPlatform
)
from .relationship import Relationship, RelationshipManager, RelationshipType
from .time import TimeManager, TimeZone, TemporalContext
from .truth import Truth, TruthEngine, TruthLevel
from .validation import Validator, ValidationResult, ValidationRule, ValidationRuleType
from .policy import Policy, PolicyManager, PolicyType
from .dependency import Dependency, DependencyGraph, DependencyType
from .evidence import Evidence, EvidenceManager, EvidenceChain, EvidenceStatus
from .object import UniversalObject, ObjectManager, ObjectType
from .event import (
    Event, EventBus, EventType, EventPriority, EventStatus,
    GlobalEventStore, EventFilter, EventSubscriber,
    UniversalEventCivilization
)

__all__ = [
    # Identity
    "Identity", "IdentityManager", "IdentityType", "IdentityStatus",
    "GlobalIDGenerator", "NamespaceManager", "ObjectLocator", "AliasManager", "ReferenceManager",
    "UniversalIdentityPlatform",
    # Relationship
    "Relationship", "RelationshipManager", "RelationshipType",
    # Time
    "TimeManager", "TimeZone", "TemporalContext",
    # Truth
    "Truth", "TruthEngine", "TruthLevel",
    # Validation
    "Validator", "ValidationResult", "ValidationRule", "ValidationRuleType",
    # Policy
    "Policy", "PolicyManager", "PolicyType",
    # Dependency
    "Dependency", "DependencyGraph", "DependencyType",
    # Evidence
    "Evidence", "EvidenceManager", "EvidenceChain", "EvidenceStatus",
    # Object
    "UniversalObject", "ObjectManager", "ObjectType",
    # Event
    "Event", "EventBus", "EventType", "EventPriority", "EventStatus",
    "GlobalEventStore", "EventFilter", "EventSubscriber",
    "UniversalEventCivilization",
]

__version__ = "1.0.0"
