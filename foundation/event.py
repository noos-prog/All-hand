"""
Foundation Event Module
====================

Universal event management system for the AGOS civilization.
Provides event-driven architecture with immutable event stores.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


EVENT_FIELDS = [
    "Identity", "Timestamp", "Producer", "Consumer", "Mission",
    "Context", "Evidence", "Version", "Correlation ID", "Causation ID"
]


class EventType(Enum):
    """Types of events in the system."""
    MISSION_CREATED = "mission_created"
    MISSION_STARTED = "mission_started"
    MISSION_COMPLETED = "mission_completed"
    MISSION_FAILED = "mission_failed"
    AGENT_REGISTERED = "agent_registered"
    AGENT_ACTIVATED = "agent_activated"
    CAPABILITY_ADDED = "capability_added"
    CAPABILITY_REMOVED = "capability_removed"
    KNOWLEDGE_UPDATED = "knowledge_updated"
    ERROR_OCCURRED = "error_occurred"
    CUSTOM = "custom"


class EventPriority(Enum):
    """Priority levels for events."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class EventStatus(Enum):
    """Status of event processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


@dataclass
class Event:
    """
    Universal event for the AGOS system.
    
    Every meaningful change becomes an immutable event.
    """
    event_id: str
    timestamp: str
    producer: str
    event_type: EventType = EventType.CUSTOM
    consumer: Optional[str] = None
    mission: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    status: EventStatus = EventStatus.PENDING
    
    @classmethod
    def create(
        cls,
        producer: str,
        event_type: EventType,
        payload: Dict[str, Any],
        mission: Optional[str] = None,
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> Event:
        """Factory method to create a new event."""
        return cls(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            timestamp=datetime.utcnow().isoformat(),
            producer=producer,
            event_type=event_type,
            mission=mission,
            payload=payload,
            correlation_id=correlation_id or str(uuid.uuid4()),
            causation_id=causation_id,
            priority=priority,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "producer": self.producer,
            "event_type": self.event_type.value,
            "consumer": self.consumer,
            "mission": self.mission,
            "context": self.context,
            "evidence": self.evidence,
            "version": self.version,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "payload": self.payload,
            "priority": self.priority.value,
            "status": self.status.value,
        }


class EventFilter:
    """Filter for selecting events."""
    
    def __init__(
        self,
        event_types: Optional[List[EventType]] = None,
        producers: Optional[List[str]] = None,
        missions: Optional[List[str]] = None,
        priority_min: Optional[EventPriority] = None,
        since: Optional[datetime] = None,
    ):
        self.event_types = set(event_types) if event_types else None
        self.producers = set(producers) if producers else None
        self.missions = set(missions) if missions else None
        self.priority_min = priority_min
        self.since = since
    
    def matches(self, event: Event) -> bool:
        """Check if event matches the filter."""
        if self.event_types and event.event_type not in self.event_types:
            return False
        if self.producers and event.producer not in self.producers:
            return False
        if self.missions and event.mission not in self.missions:
            return False
        if self.priority_min and event.priority.value < self.priority_min.value:
            return False
        if self.since:
            event_time = datetime.fromisoformat(event.timestamp)
            if event_time < self.since:
                return False
        return True


class EventSubscriber:
    """Subscriber for event notifications."""
    
    def __init__(self, subscriber_id: str, callback: Callable):
        self.subscriber_id = subscriber_id
        self.callback = callback
        self.filter: Optional[EventFilter] = None
        self.active = True
    
    def receive(self, event: Event) -> None:
        """Receive and process an event."""
        if not self.active:
            return
        if self.filter and not self.filter.matches(event):
            return
        try:
            self.callback(event)
        except Exception:
            pass


class GlobalEventStore:
    """Immutable store for all events."""
    
    def __init__(self):
        self._events: Dict[str, Event] = {}
        self._by_mission: Dict[str, List[str]] = {}
        self._by_producer: Dict[str, List[str]] = {}
        self._by_type: Dict[str, List[str]] = {}
        self._by_correlation: Dict[str, List[str]] = {}
    
    def store(self, event: Event) -> bool:
        """Store an event."""
        self._events[event.event_id] = event
        
        if event.mission:
            if event.mission not in self._by_mission:
                self._by_mission[event.mission] = []
            self._by_mission[event.mission].append(event.event_id)
        
        if event.producer:
            if event.producer not in self._by_producer:
                self._by_producer[event.producer] = []
            self._by_producer[event.producer].append(event.event_id)
        
        if event.event_type:
            type_key = event.event_type.value
            if type_key not in self._by_type:
                self._by_type[type_key] = []
            self._by_type[type_key].append(event.event_id)
        
        if event.correlation_id:
            if event.correlation_id not in self._by_correlation:
                self._by_correlation[event.correlation_id] = []
            self._by_correlation[event.correlation_id].append(event.event_id)
        
        return True
    
    def get(self, event_id: str) -> Optional[Event]:
        """Get an event by ID."""
        return self._events.get(event_id)
    
    def get_by_mission(self, mission_id: str) -> List[Event]:
        """Get all events for a mission."""
        event_ids = self._by_mission.get(mission_id, [])
        return [self._events[eid] for eid in event_ids if eid in self._events]
    
    def get_by_producer(self, producer: str) -> List[Event]:
        """Get all events from a producer."""
        event_ids = self._by_producer.get(producer, [])
        return [self._events[eid] for eid in event_ids if eid in self._events]
    
    def get_by_correlation(self, correlation_id: str) -> List[Event]:
        """Get all events with the same correlation ID."""
        event_ids = self._by_correlation.get(correlation_id, [])
        return sorted(
            [self._events[eid] for eid in event_ids if eid in self._events],
            key=lambda e: e.timestamp,
        )
    
    def query(self, event_filter: EventFilter) -> List[Event]:
        """Query events matching a filter."""
        return [e for e in self._events.values() if event_filter.matches(e)]
    
    def replay(
        self,
        from_timestamp: Optional[str] = None,
        event_filter: Optional[EventFilter] = None,
    ) -> List[Event]:
        """Replay events from a timestamp."""
        events = []
        for event in self._events.values():
            if from_timestamp and event.timestamp < from_timestamp:
                continue
            if event_filter and not event_filter.matches(event):
                continue
            events.append(event)
        return sorted(events, key=lambda e: e.timestamp)


class EventBus:
    """Publish-subscribe event bus."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[EventSubscriber]] = {}
        self._all_subscribers: List[EventSubscriber] = []
        self._event_store: Optional[GlobalEventStore] = None
    
    def set_store(self, store: GlobalEventStore) -> None:
        """Set the event store."""
        self._event_store = store
    
    def subscribe(
        self,
        consumer: str,
        event_types: Optional[List[EventType]] = None,
        missions: Optional[List[str]] = None,
    ) -> EventSubscriber:
        """Subscribe to events."""
        callback = lambda e: None
        subscriber = EventSubscriber(consumer, callback)
        subscriber.filter = EventFilter(
            event_types=event_types,
            missions=missions,
        )
        
        if event_types is None and missions is None:
            self._all_subscribers.append(subscriber)
        else:
            for et in (event_types or []):
                if et.value not in self._subscribers:
                    self._subscribers[et.value] = []
                self._subscribers[et.value].append(subscriber)
        
        return subscriber
    
    def unsubscribe(self, subscriber: EventSubscriber) -> bool:
        """Unsubscribe from events."""
        if subscriber in self._all_subscribers:
            self._all_subscribers.remove(subscriber)
            return True
        
        for subscribers in self._subscribers.values():
            if subscriber in subscribers:
                subscribers.remove(subscriber)
                return True
        
        return False
    
    def publish(self, event: Event) -> int:
        """Publish an event to all subscribers."""
        notified = 0
        
        for subscriber in self._all_subscribers:
            subscriber.receive(event)
            notified += 1
        
        type_subscribers = self._subscribers.get(event.event_type.value, [])
        for subscriber in type_subscribers:
            if subscriber not in self._all_subscribers:
                subscriber.receive(event)
                notified += 1
        
        if self._event_store:
            self._event_store.store(event)
        
        return notified


class UniversalEventCivilization:
    """
    Universal Event Civilization.
    
    Every meaningful change becomes an immutable event.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.event_store = GlobalEventStore()
        self.event_bus = EventBus()
        self.event_bus.set_store(self.event_store)
    
    def emit(
        self,
        producer: str,
        event_type: EventType,
        payload: Dict[str, Any],
        mission: Optional[str] = None,
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> Event:
        """Emit a new event."""
        event = Event.create(
            producer=producer,
            event_type=event_type,
            payload=payload,
            mission=mission,
            correlation_id=correlation_id,
            causation_id=causation_id,
            priority=priority,
        )
        self.event_bus.publish(event)
        return event
    
    def subscribe(
        self,
        consumer: str,
        event_types: Optional[List[EventType]] = None,
        missions: Optional[List[str]] = None,
    ) -> EventSubscriber:
        """Subscribe to events."""
        return self.event_bus.subscribe(consumer, event_types, missions)
    
    def query_events(
        self,
        event_types: Optional[List[EventType]] = None,
        producers: Optional[List[str]] = None,
        missions: Optional[List[str]] = None,
        since: Optional[datetime] = None,
    ) -> List[Event]:
        """Query events with filters."""
        event_filter = EventFilter(
            event_types=event_types,
            producers=producers,
            missions=missions,
            since=since,
        )
        return self.event_store.query(event_filter)
    
    def replay_events(
        self,
        from_timestamp: Optional[str] = None,
        event_types: Optional[List[EventType]] = None,
    ) -> List[Event]:
        """Replay events from a point in time."""
        event_filter = EventFilter(event_types=event_types) if event_types else None
        return self.event_store.replay(from_timestamp, event_filter)
    
    def get_timeline(self, mission_id: str) -> List[Event]:
        """Get the event timeline for a mission."""
        return self.event_store.get_by_mission(mission_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get event statistics."""
        return {
            "version": self.version,
            "event_fields": EVENT_FIELDS,
            "total_events": len(self.event_store._events),
            "by_type": {
                et: len(events) for et, events in self.event_store._by_type.items()
            },
            "total_producers": len(self.event_store._by_producer),
            "total_missions": len(self.event_store._by_mission),
        }


# Backwards compatibility
Event = Event
