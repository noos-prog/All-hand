"""Event Bus for AGOS Kernel."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class EventType(Enum):
    """Event types in the system."""
    # Mission Events
    MISSION_CREATED = "mission_created"
    MISSION_STARTED = "mission_started"
    MISSION_COMPLETED = "mission_completed"
    MISSION_FAILED = "mission_failed"
    
    # Selection Events
    CAPABILITY_SELECTED = "capability_selected"
    PROVIDER_SELECTED = "provider_selected"
    
    # Execution Events
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETED = "execution_completed"
    EXECUTION_FAILED = "execution_failed"
    
    # Skill Events
    SKILL_STARTED = "skill_started"
    SKILL_COMPLETED = "skill_completed"
    SKILL_FAILED = "skill_failed"


@dataclass
class Event:
    """Base event type."""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: EventType = EventType.MISSION_CREATED
    timestamp: datetime = field(default_factory=datetime.utcnow)
    mission_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "mission_id": self.mission_id,
            "data": self.data
        }


class EventBus:
    """
    Simple event bus that publishes events.
    No subscriptions - just logging for now.
    """
    
    def __init__(self):
        self._events: List[Event] = []
    
    def publish(self, event: Event) -> None:
        """Publish an event."""
        self._events.append(event)
        print(f"[EVENT] {event.type.value}: {event.data}")
    
    def get_events(self, mission_id: Optional[str] = None) -> List[Event]:
        """Get events, optionally filtered by mission."""
        if mission_id is None:
            return self._events.copy()
        return [e for e in self._events if e.mission_id == mission_id]
    
    def clear(self) -> None:
        """Clear all events."""
        self._events.clear()
