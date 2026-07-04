"""
Task Model
PHASE-02: EXECUTION-000005 - Universal Mission Planner

Every Task must contain:
- Task ID
- Mission ID
- Objective
- Inputs
- Outputs
- Dependencies
- Required Capabilities
- Required Skills
- Required Providers
- Estimated Cost
- Estimated Duration
- Priority
- Retry Policy
- Timeout Policy
- Rollback Strategy
- Validation Rules
- Evidence Requirements
- Completion Criteria
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ROLLED_BACK = "rolled_back"


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class RetryPolicy(Enum):
    """Retry policies."""
    NO_RETRY = "no_retry"
    RETRY_1 = "retry_1"
    RETRY_2 = "retry_2"
    RETRY_3 = "retry_3"
    INFINITE = "infinite"


@dataclass
class TaskInput:
    """Task input."""
    name: str = ""
    type: str = ""
    source: str = ""  # previous task, external, constant
    required: bool = True


@dataclass
class TaskOutput:
    """Task output."""
    name: str = ""
    type: str = ""
    destination: str = ""  # next task, external
    required: bool = True


@dataclass
class ValidationRule:
    """Validation rule."""
    name: str = ""
    type: str = ""  # assert, check, compare
    condition: str = ""
    expected: Any = None


@dataclass
class Task:
    """
    Task Model.
    
    Fundamental unit of execution in the mission planner.
    """
    
    # Identification
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mission_id: str = ""
    name: str = ""
    description: str = ""
    
    # Objective
    objective: str = ""
    
    # I/O
    inputs: List[TaskInput] = field(default_factory=list)
    outputs: List[TaskOutput] = field(default_factory=list)
    
    # Dependencies
    depends_on: List[str] = field(default_factory=list)  # Task IDs
    depends_on_names: List[str] = field(default_factory=list)
    
    # Requirements
    required_capabilities: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    required_providers: List[str] = field(default_factory=list)
    
    # Planning
    estimated_cost: float = 0.0  # computational cost
    estimated_duration: int = 60  # seconds
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # Policies
    retry_policy: RetryPolicy = RetryPolicy.NO_RETRY
    timeout_seconds: int = 300
    rollback_strategy: str = ""
    
    # Validation
    validation_rules: List[ValidationRule] = field(default_factory=list)
    evidence_requirements: List[str] = field(default_factory=list)
    completion_criteria: List[str] = field(default_factory=list)
    
    # Execution state
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 0
    error: str = ""
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: str = ""
    completed_at: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'task_id': self.task_id,
            'mission_id': self.mission_id,
            'name': self.name,
            'description': self.description,
            'objective': self.objective,
            'inputs': [i.__dict__ for i in self.inputs],
            'outputs': [o.__dict__ for o in self.outputs],
            'depends_on': self.depends_on,
            'depends_on_names': self.depends_on_names,
            'required_capabilities': self.required_capabilities,
            'required_skills': self.required_skills,
            'required_providers': self.required_providers,
            'estimated_cost': self.estimated_cost,
            'estimated_duration': self.estimated_duration,
            'priority': self.priority.value if isinstance(self.priority, TaskPriority) else self.priority,
            'retry_policy': self.retry_policy.value if isinstance(self.retry_policy, RetryPolicy) else self.retry_policy,
            'timeout_seconds': self.timeout_seconds,
            'rollback_strategy': self.rollback_strategy,
            'validation_rules': [v.__dict__ for v in self.validation_rules],
            'evidence_requirements': self.evidence_requirements,
            'completion_criteria': self.completion_criteria,
            'status': self.status.value if isinstance(self.status, TaskStatus) else self.status,
            'retry_count': self.retry_count,
            'error': self.error,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
        }
    
    def is_ready(self, completed_tasks: List[str]) -> bool:
        """Check if task is ready to execute."""
        if self.status != TaskStatus.PENDING:
            return False
        return all(dep in completed_tasks for dep in self.depends_on)
    
    def can_retry(self) -> bool:
        """Check if task can be retried."""
        if self.retry_policy == RetryPolicy.NO_RETRY:
            return False
        if self.retry_policy == RetryPolicy.INFINITE:
            return True
        return self.retry_count < self.max_retries