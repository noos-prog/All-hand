"""Universal Recovery Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RecoveryType(Enum):
    """Recovery type."""
    CHECKPOINT = "checkpoint"
    ROLLBACK = "rollback"
    FAILOVER = "failover"
    RESTORE = "restore"
    REPLAY = "replay"


class RecoveryStatus(Enum):
    """Recovery status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Checkpoint:
    """Checkpoint for recovery."""
    id: str
    entity_type: str  # mission, execution, workspace, etc.
    entity_id: str
    created_at: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RollbackPlan:
    """Plan for rollback."""
    id: str
    entity_id: str
    created_at: datetime = field(default_factory=datetime.now)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    estimated_duration_seconds: float = 0.0


@dataclass
class FailureAnalysis:
    """Analysis of a failure."""
    id: str
    entity_id: str
    error_type: str
    error_message: str
    root_cause: str = ""
    affected_components: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class RecoveryPlan:
    """Plan for recovery."""
    id: str
    recovery_type: RecoveryType
    entity_id: str
    created_at: datetime = field(default_factory=datetime.now)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    estimated_duration_seconds: float = 0.0


@dataclass
class Recovery:
    """Recovery operation."""
    id: str
    recovery_type: RecoveryType
    entity_id: str
    entity_type: str
    
    # Status
    status: RecoveryStatus = RecoveryStatus.PENDING
    
    # Planning
    plan: Optional[RecoveryPlan] = None
    
    # Execution
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    
    # Result
    success: bool = False
    error: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
