"""Universal Session Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class SessionStatus(Enum):
    """Session status."""
    CREATED = "created"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    PAUSED = "paused"
    ENDING = "ending"
    ENDED = "ended"
    ERROR = "error"
    RECOVERING = "recovering"


class SessionType(Enum):
    """Session type."""
    MISSION = "mission"
    USER = "user"
    AGENT = "agent"
    PROVIDER = "provider"
    WORKSPACE = "workspace"
    MODEL = "model"
    CLI = "cli"
    BROWSER = "browser"
    API = "api"
    WEBHOOK = "webhook"


@dataclass
class SessionEvent:
    """A single event in the session timeline."""
    id: str
    timestamp: datetime
    event_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionTimeline:
    """Timeline of session events."""
    events: List[SessionEvent] = field(default_factory=list)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: float = 0.0


@dataclass
class SessionMetrics:
    """Session metrics."""
    interactions: int = 0
    messages_sent: int = 0
    messages_received: int = 0
    tokens_used: int = 0
    tokens_generated: int = 0
    api_calls: int = 0
    errors: int = 0
    latency_ms_avg: float = 0.0
    cost: float = 0.0


@dataclass
class Session:
    """Universal Session."""
    id: str
    name: str
    session_type: SessionType
    
    # Relationships
    mission_id: Optional[str] = None
    workspace_id: Optional[str] = None
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Status
    status: SessionStatus = SessionStatus.CREATED
    
    # Timeline
    timeline: SessionTimeline = field(default_factory=SessionTimeline)
    
    # Metrics
    metrics: SessionMetrics = field(default_factory=SessionMetrics)
    
    # State
    state: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_activity: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Replay
    replay_enabled: bool = True
    replay_data: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_event(self, event_type: str, data: Dict[str, Any] = None, metadata: Dict[str, Any] = None) -> SessionEvent:
        """Add an event to the timeline."""
        event = SessionEvent(
            id=f"{self.id}-evt-{len(self.timeline.events)}",
            timestamp=datetime.now(),
            event_type=event_type,
            data=data or {},
            metadata=metadata or {},
        )
        self.timeline.events.append(event)
        self.timeline.duration_seconds = (event.timestamp - (self.timeline.started_at or event.timestamp)).total_seconds()
        self.last_activity = datetime.now()
        return event
    
    def update_metrics(self, **kwargs) -> None:
        """Update session metrics."""
        for key, value in kwargs.items():
            if hasattr(self.metrics, key):
                setattr(self.metrics, key, value)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.session_type.value,
            "status": self.status.value,
            "mission_id": self.mission_id,
            "workspace_id": self.workspace_id,
            "created_at": self.created_at.isoformat(),
            "duration_seconds": self.timeline.duration_seconds,
            "metrics": {
                "interactions": self.metrics.interactions,
                "tokens_used": self.metrics.tokens_used,
            },
        }
