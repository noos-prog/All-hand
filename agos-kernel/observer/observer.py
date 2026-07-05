"""AGOS Observer Pattern."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """An event."""
    type: str
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class Observer:
    """Observer interface."""
    
    def update(self, event: Event) -> None:
        """Handle an event."""
        pass


class Observable:
    """
    Observable subject.
    
    Usage:
        observable = Observable()
        observable.attach(my_observer)
        observable.notify(Event("message", {"key": "value"}))
    """
    
    def __init__(self):
        """Initialize observable."""
        self._observers: List[Observer] = []
        self._handlers: Dict[str, List[Callable]] = {}
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)
    
    def notify(self, event: Event) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(event)
        
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                handler(event)


class Subject(Observable):
    """Alias for Observable."""
    pass


_observable: Optional[Observable] = None


def get_observable() -> Observable:
    """Get the global observable."""
    global _observable
    if _observable is None:
        _observable = Observable()
    return _observable
