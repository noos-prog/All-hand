"""
Universal Runtime Platform.

Integrates all runtime subsystems:
- Workspace Runtime
- Session Runtime
- Artifact Runtime
- Environment Runtime
- Resource Runtime
- Scheduler Runtime
- Queue Runtime
- State Runtime
- Recovery Runtime

EXECUTION-000051 to EXECUTION-000060: Runtime Foundation
"""

# Workspace
from .workspace.models import (
    WorkspaceStatus, WorkspaceType, WorkspaceResources, WorkspaceContext,
    WorkspaceSnapshot, Workspace, WorkspaceTemplate
)
from .workspace.runtime import WorkspaceRuntime

# Session
from .session.models import (
    SessionStatus, SessionType, SessionEvent, SessionTimeline,
    SessionMetrics, Session
)
from .session.runtime import SessionRuntime

# Artifact
from .artifact.models import (
    ArtifactType, ArtifactStatus, ArtifactVersion, ArtifactMetadata, Artifact
)
from .artifact.runtime import ArtifactRuntime

# Environment
from .environment.models import (
    EnvironmentType, EnvironmentStatus, EnvironmentHealth,
    EnvironmentConfig, Environment
)
from .environment.runtime import EnvironmentRuntime

# Resource
from .resource.models import (
    ResourceType, ResourceStatus, ResourceAllocation, ResourceUsage,
    ResourceQuota, Resource
)
from .resource.runtime import ResourceRuntime

# Scheduler
from .scheduler.models import (
    ScheduleType, ScheduleStatus, Schedule, ExecutionCalendar
)
from .scheduler.runtime import SchedulerRuntime

# Queue
from .queue.models import (
    QueueType, QueueStatus, QueueItem, Queue
)
from .queue.runtime import QueueRuntime

# State
from .state.models import (
    StateType, StateStatus, StateTransition, StateSnapshot, State
)
from .state.runtime import StateRuntime

# Recovery
from .recovery.models import (
    RecoveryType, RecoveryStatus, Checkpoint, RollbackPlan,
    FailureAnalysis, RecoveryPlan, Recovery
)
from .recovery.runtime import RecoveryRuntime

# Platform
from .platform import (
    RuntimeStats, UniversalRuntimePlatform, get_platform,
    create_mission_workspace, health_check
)

__version__ = "1.0.0"

__all__ = [
    # Workspace
    "WorkspaceStatus", "WorkspaceType", "WorkspaceResources",
    "WorkspaceContext", "WorkspaceSnapshot", "Workspace", "WorkspaceTemplate",
    "WorkspaceRuntime",
    # Session
    "SessionStatus", "SessionType", "SessionEvent", "SessionTimeline",
    "SessionMetrics", "Session", "SessionRuntime",
    # Artifact
    "ArtifactType", "ArtifactStatus", "ArtifactVersion", "ArtifactMetadata",
    "Artifact", "ArtifactRuntime",
    # Environment
    "EnvironmentType", "EnvironmentStatus", "EnvironmentHealth",
    "EnvironmentConfig", "Environment", "EnvironmentRuntime",
    # Resource
    "ResourceType", "ResourceStatus", "ResourceAllocation", "ResourceUsage",
    "ResourceQuota", "Resource", "ResourceRuntime",
    # Scheduler
    "ScheduleType", "ScheduleStatus", "Schedule", "ExecutionCalendar",
    "SchedulerRuntime",
    # Queue
    "QueueType", "QueueStatus", "QueueItem", "Queue", "QueueRuntime",
    # State
    "StateType", "StateStatus", "StateTransition", "StateSnapshot",
    "State", "StateRuntime",
    # Recovery
    "RecoveryType", "RecoveryStatus", "Checkpoint", "RollbackPlan",
    "FailureAnalysis", "RecoveryPlan", "Recovery", "RecoveryRuntime",
    # Platform
    "RuntimeStats", "UniversalRuntimePlatform", "get_platform",
    "create_mission_workspace", "health_check",
]
