"""Universal Queue Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class QueueType(Enum):
    """Queue type."""
    MISSION = "mission"
    EXECUTION = "execution"
    PROVIDER = "provider"
    ARTIFACT = "artifact"
    KNOWLEDGE = "knowledge"
    VALIDATION = "validation"
    ANALYSIS = "analysis"
    INDEXING = "indexing"
    DEAD_LETTER = "dead_letter"
    PRIORITY = "priority"
    RETRY = "retry"
    REPLAY = "replay"


class QueueStatus(Enum):
    """Queue status."""
    CREATED = "created"
    ACTIVE = "active"
    PAUSED = "paused"
    DRAINING = "draining"
    CLOSED = "closed"


@dataclass
class QueueItem:
    """Item in a queue."""
    id: str
    queue_type: QueueType
    priority: int = 0
    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    retries: int = 0
    max_retries: int = 3
    error: Optional[str] = None


@dataclass
class Queue:
    """Universal Queue."""
    id: str
    name: str
    queue_type: QueueType
    
    # Configuration
    status: QueueStatus = QueueStatus.CREATED
    max_size: int = 10000
    timeout_seconds: int = 300
    
    # Items
    items: List[QueueItem] = field(default_factory=list)
    processed_count: int = 0
    failed_count: int = 0
    
    # Priority
    priority_enabled: bool = False
    priority_levels: int = 10
    
    # DLQ (Dead Letter Queue)
    dlq_enabled: bool = False
    dlq_id: Optional[str] = None
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
