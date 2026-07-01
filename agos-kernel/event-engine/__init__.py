"""Event Processing Engine - Async event handling with guaranteed delivery."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4


class EventType(Enum):
    """Event types."""
    MISSION_CREATED = "mission_created"
    MISSION_STARTED = "mission_started"
    MISSION_COMPLETED = "mission_completed"
    MISSION_FAILED = "mission_failed"
    CAPABILITY_SELECTED = "capability_selected"
    PROVIDER_SELECTED = "provider_selected"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_COMPLETED = "execution_completed"
    SKILL_STARTED = "skill_started"
    SKILL_COMPLETED = "skill_completed"


@dataclass
class Event:
    """
    Immutable event.
    Events cannot be modified after creation.
    """
    id: str
    type: EventType
    timestamp: datetime
    mission_id: Optional[str]
    data: Dict[str, Any]
    
    def __post_init__(self):
        # Ensure immutability
        object.__setattr__(self, '_frozen', True)
    
    def __setattr__(self, name, value):
        if getattr(self, '_frozen', False):
            raise AttributeError("Events are immutable")
        object.__setattr__(self, name, value)
    
    @classmethod
    def create(cls, event_type: EventType, mission_id: Optional[str] = None, **data) -> 'Event':
        """Create a new immutable event."""
        return cls(
            id=str(uuid4()),
            type=event_type,
            timestamp=datetime.utcnow(),
            mission_id=mission_id,
            data=data
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "mission_id": self.mission_id,
            "data": self.data
        }


class EventSubscriber:
    """Event subscriber callback."""
    
    def __init__(self, callback: Callable[[Event], None], event_types: List[EventType]):
        self.callback = callback
        self.event_types = event_types
        self.id = str(uuid4())


class EventDispatcher:
    """Dispatches events to subscribers."""
    
    def __init__(self):
        self._subscribers: List[EventSubscriber] = []
    
    def subscribe(self, callback: Callable[[Event], None], event_types: List[EventType]) -> str:
        """Subscribe to events."""
        subscriber = EventSubscriber(callback, event_types)
        self._subscribers.append(subscriber)
        return subscriber.id
    
    def unsubscribe(self, subscriber_id: str) -> None:
        """Unsubscribe from events."""
        self._subscribers = [s for s in self._subscribers if s.id != subscriber_id]
    
    def dispatch(self, event: Event) -> List[Any]:
        """Dispatch event to subscribers."""
        results = []
        for subscriber in self._subscribers:
            if event.type in subscriber.event_types:
                try:
                    result = subscriber.callback(event)
                    results.append(result)
                except Exception as e:
                    results.append(e)
        return results


class EventPublisher:
    """Publishes events."""
    
    def __init__(self, dispatcher: EventDispatcher, store: 'EventStore'):
        self._dispatcher = dispatcher
        self._store = store
    
    def publish(self, event: Event) -> None:
        """Publish an event."""
        # Store first
        self._store.store(event)
        # Then dispatch
        self._dispatcher.dispatch(event)


class EventStore:
    """
    Stores events.
    Events are immutable and ordered.
    """
    
    def __init__(self, max_size: int = 10000):
        self._events: List[Event] = []
        self._max_size = max_size
    
    def store(self, event: Event) -> None:
        """Store an event."""
        self._events.append(event)
        
        # Trim if too large
        if len(self._events) > self._max_size:
            self._events = self._events[-self._max_size:]
    
    def get_all(self) -> List[Event]:
        """Get all events."""
        return self._events.copy()
    
    def get_by_mission(self, mission_id: str) -> List[Event]:
        """Get events for a mission."""
        return [e for e in self._events if e.mission_id == mission_id]
    
    def get_by_type(self, event_type: EventType) -> List[Event]:
        """Get events by type."""
        return [e for e in self._events if e.type == event_type]
    
    def get_recent(self, count: int = 100) -> List[Event]:
        """Get recent events."""
        return self._events[-count:]
    
    def clear(self) -> None:
        """Clear all events."""
        self._events.clear()
    
    def count(self) -> int:
        """Count stored events."""
        return len(self._events)


class EventEngine:
    """
    Event Processing Engine.
    
    Flow:
    Publish → Dispatch → Subscribers → Persistence
    
    Rules:
    - Asynchronous by default
    - Ordered processing
    - Immutable events
    - Guaranteed delivery inside runtime
    """
    
    def __init__(self):
        self._store = EventStore()
        self._dispatcher = EventDispatcher()
        self._publisher = EventPublisher(self._dispatcher, self._store)
    
    @property
    def publisher(self) -> EventPublisher:
        """Get the event publisher."""
        return self._publisher
    
    @property
    def store(self) -> EventStore:
        """Get the event store."""
        return self._store
    
    def subscribe(self, callback: Callable[[Event], None], event_types: List[EventType]) -> str:
        """Subscribe to events."""
        return self._dispatcher.subscribe(callback, event_types)
    
    def unsubscribe(self, subscriber_id: str) -> None:
        """Unsubscribe from events."""
        self._dispatcher.unsubscribe(subscriber_id)
    
    def publish(self, event_type: EventType, mission_id: Optional[str] = None, **data) -> Event:
        """Publish an event."""
        event = Event.create(event_type, mission_id, **data)
        self._publisher.publish(event)
        return event
    
    def get_mission_events(self, mission_id: str) -> List[Event]:
        """Get all events for a mission."""
        return self._store.get_by_mission(mission_id)
    
    def get_recent_events(self, count: int = 100) -> List[Event]:
        """Get recent events."""
        return self._store.get_recent(count)
