"""Universal Scheduler Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ScheduleType(Enum):
    """Schedule type."""
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    SCHEDULED = "scheduled"
    RECURRING = "recurring"
    PRIORITY = "priority"
    EVENT_DRIVEN = "event_driven"
    DEPENDENCY_DRIVEN = "dependency_driven"
    MANUAL_APPROVAL = "manual_approval"


class ScheduleStatus(Enum):
    """Schedule status."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


@dataclass
class Schedule:
    """Universal Schedule."""
    id: str
    name: str
    schedule_type: ScheduleType
    
    # Timing
    execute_at: datetime
    duration_seconds: Optional[float] = None
    
    # Recurrence
    is_recurring: bool = False
    interval_seconds: Optional[float] = None
    max_runs: Optional[int] = None
    run_count: int = 0
    
    # Priority
    priority: int = 0  # Higher = more priority
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)  # Other schedule IDs
    
    # Status
    status: ScheduleStatus = ScheduleStatus.PENDING
    
    # Payload
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # Retry
    retry_enabled: bool = True
    max_retries: int = 3
    retry_count: int = 0
    retry_delay_seconds: float = 60
    
    # Calendar
    cron_expression: Optional[str] = None
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionCalendar:
    """Calendar of scheduled executions."""
    schedules: List[Schedule] = field(default_factory=list)
    current_time: datetime = field(default_factory=datetime.now)
