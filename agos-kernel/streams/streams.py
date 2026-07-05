"""AGOS Streams."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class StreamStatus(Enum):
    """Stream status."""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class StreamType(Enum):
    """Stream type."""
    EVENT = "event"
    DATA = "data"
    LOG = "log"
    METRICS = "metrics"


@dataclass
class StreamEvent:
    """A stream event."""
    id: str
    stream_id: str
    event_type: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Stream:
    """A stream."""
    id: str
    name: str
    stream_type: StreamType
    status: StreamStatus = StreamStatus.CREATED
    events: List[StreamEvent] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class StreamProcessor:
    """
    Stream Processor.
    
    Processes streams of events.
    
    Usage:
        processor = StreamProcessor()
        stream = processor.create_stream("events", StreamType.EVENT)
        processor.subscribe("events", my_handler)
    """
    
    def __init__(self):
        """Initialize stream processor."""
        self._streams: Dict[str, Stream] = {}
        self._handlers: Dict[str, List[Callable]] = {}
    
    def create_stream(
        self,
        name: str,
        stream_type: StreamType,
    ) -> Stream:
        """Create a stream."""
        stream = Stream(
            id=f"stream-{uuid.uuid4().hex[:8]}",
            name=name,
            stream_type=stream_type,
        )
        self._streams[name] = stream
        self._handlers[name] = []
        return stream
    
    def get_stream(self, name: str) -> Optional[Stream]:
        """Get a stream by name."""
        return self._streams.get(name)
    
    def publish(self, stream_name: str, event_type: str, data: Any) -> bool:
        """Publish an event to a stream."""
        stream = self._streams.get(stream_name)
        if not stream:
            return False
        
        event = StreamEvent(
            id=f"evt-{uuid.uuid4().hex[:8]}",
            stream_id=stream.id,
            event_type=event_type,
            data=data,
        )
        
        stream.events.append(event)
        
        # Notify handlers
        if stream_name in self._handlers:
            for handler in self._handlers[stream_name]:
                handler(event)
        
        return True
    
    def subscribe(self, stream_name: str, handler: Callable) -> None:
        """Subscribe to a stream."""
        if stream_name not in self._handlers:
            self._handlers[stream_name] = []
        self._handlers[stream_name].append(handler)
    
    def unsubscribe(self, stream_name: str, handler: Callable) -> None:
        """Unsubscribe from a stream."""
        if stream_name in self._handlers:
            self._handlers[stream_name].remove(handler)
    
    def start(self, stream_name: str) -> bool:
        """Start a stream."""
        stream = self._streams.get(stream_name)
        if stream:
            stream.status = StreamStatus.RUNNING
            return True
        return False
    
    def stop(self, stream_name: str) -> bool:
        """Stop a stream."""
        stream = self._streams.get(stream_name)
        if stream:
            stream.status = StreamStatus.STOPPED
            return True
        return False


_stream_processor: Optional[StreamProcessor] = None


def get_stream_processor() -> StreamProcessor:
    """Get the global stream processor."""
    global _stream_processor
    if _stream_processor is None:
        _stream_processor = StreamProcessor()
    return _stream_processor
