"""
AGOS Specification Module
========================

Official specifications for AGOS components.
Specifications are the source of truth.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import hashlib
import json


class SpecType(Enum):
    """Types of specifications."""
    INTERFACE = "interface"
    CONTRACT = "contract"
    SCHEMA = "schema"
    EVENT = "event"
    CAPABILITY = "capability"


class SpecStatus(Enum):
    """Status of a specification."""
    DRAFT = "draft"
    STABLE = "stable"
    DEPRECATED = "deprecated"


@dataclass(frozen=True)
class Specification:
    """
    Immutable specification definition.
    
    Specifications define the contract between components.
    Once published, specifications are immutable.
    """
    spec_id: str                        # Unique identifier
    spec_type: SpecType                 # Type of specification
    name: str                           # Human-readable name
    version: str                         # Version (e.g., "1.0")
    description: str                     # What this spec defines
    interface: Tuple[str, ...]          # Public interface methods
    requirements: Tuple[str, ...]       # Requirements
    examples: Tuple[str, ...]           # Usage examples
    related_specs: Tuple[str, ...]      # Related specification IDs
    status: SpecStatus = SpecStatus.DRAFT
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "spec_id": self.spec_id,
            "spec_type": self.spec_type.value,
            "name": self.name,
            "version": self.version,
            "interface": self.interface,
        }
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "spec_id": self.spec_id,
            "spec_type": self.spec_type.value,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "interface": list(self.interface),
            "requirements": list(self.requirements),
            "examples": list(self.examples),
            "related_specs": list(self.related_specs),
            "status": self.status.value,
            "hash": self.compute_hash(),
        }


class SpecificationRegistry:
    """
    Registry of all AGOS specifications.
    """
    
    def __init__(self):
        self._specs: Dict[str, Specification] = {}
    
    def register(self, spec: Specification) -> None:
        """Register a specification."""
        key = f"{spec.spec_id}_{spec.version}"
        self._specs[key] = spec
    
    def get(self, spec_id: str, version: Optional[str] = None) -> Optional[Specification]:
        """Get a specification."""
        if version:
            return self._specs.get(f"{spec_id}_{version}")
        
        # Get latest version
        matching = [
            (k, v) for k, v in self._specs.items()
            if k.startswith(f"{spec_id}_")
        ]
        if matching:
            matching.sort(key=lambda x: x[0], reverse=True)
            return matching[0][1]
        return None
    
    def list_all(self) -> List[Specification]:
        """List all specifications."""
        return list(self._specs.values())


# ============ CORE SPECIFICATIONS ============

# Task Contract Specification
SPEC_TASK_V1_0 = Specification(
    spec_id="contract_task",
    spec_type=SpecType.CONTRACT,
    name="Task Contract",
    version="1.0",
    description="Contract for submitting and managing tasks",
    interface=(
        "submit(task: TaskInput) -> TaskId",
        "status(task_id: TaskId) -> TaskStatus",
        "cancel(task_id: TaskId) -> bool",
        "result(task_id: TaskId) -> TaskResult",
    ),
    requirements=(
        "All tasks have unique ID",
        "Tasks transition through states",
        "Results are immutable",
    ),
    examples=(
        "task_id = contract.submit(task)",
        "status = contract.status(task_id)",
    ),
    related_specs=("contract_event", "schema_task"),
)

# Event Contract Specification
SPEC_EVENT_V1_0 = Specification(
    spec_id="contract_event",
    spec_type=SpecType.CONTRACT,
    name="Event Contract",
    version="1.0",
    description="Contract for event emission and subscription",
    interface=(
        "emit(event: Event) -> EventId",
        "subscribe(event_type: str, handler: Handler) -> SubscriptionId",
        "unsubscribe(subscription_id: SubscriptionId) -> bool",
    ),
    requirements=(
        "Events are immutable once emitted",
        "All events have timestamps",
        "Event delivery is at-least-once",
    ),
    examples=(
        "event_id = emit(Event(type='task.completed'))",
        "sub_id = subscribe('task.*', handler)",
    ),
    related_specs=("contract_task", "schema_event"),
)


__all__ = [
    "Specification",
    "SpecType",
    "SpecStatus",
    "SpecificationRegistry",
]
