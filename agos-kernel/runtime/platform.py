"""Universal Runtime Platform - Integrates all runtime subsystems."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .workspace.runtime import WorkspaceRuntime
from .workspace.models import Workspace, WorkspaceType, WorkspaceStatus
from .session.runtime import SessionRuntime
from .session.models import Session, SessionType, SessionStatus
from .artifact.runtime import ArtifactRuntime
from .artifact.models import Artifact, ArtifactType, ArtifactStatus
from .environment.runtime import EnvironmentRuntime
from .environment.models import Environment, EnvironmentType, EnvironmentStatus
from .resource.runtime import ResourceRuntime
from .resource.models import Resource, ResourceType, ResourceStatus
from .scheduler.runtime import SchedulerRuntime
from .scheduler.models import Schedule, ScheduleType, ScheduleStatus
from .queue.runtime import QueueRuntime
from .queue.models import Queue, QueueItem, QueueType, QueueStatus
from .state.runtime import StateRuntime
from .state.models import State, StateType, StateStatus
from .recovery.runtime import RecoveryRuntime
from .recovery.models import Recovery, RecoveryType, RecoveryStatus, Checkpoint


@dataclass
class RuntimeStats:
    """Runtime statistics."""
    workspaces_count: int = 0
    sessions_count: int = 0
    artifacts_count: int = 0
    environments_count: int = 0
    resources_count: int = 0
    schedules_count: int = 0
    queues_count: int = 0
    states_count: int = 0
    checkpoints_count: int = 0


@dataclass
class UniversalRuntimePlatform:
    """
    Universal Runtime Platform v1.
    
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
    """
    
    # Subsystems
    workspace: WorkspaceRuntime = field(default_factory=WorkspaceRuntime)
    session: SessionRuntime = field(default_factory=SessionRuntime)
    artifact: ArtifactRuntime = field(default_factory=ArtifactRuntime)
    environment: EnvironmentRuntime = field(default_factory=EnvironmentRuntime)
    resource: ResourceRuntime = field(default_factory=ResourceRuntime)
    scheduler: SchedulerRuntime = field(default_factory=SchedulerRuntime)
    queue: QueueRuntime = field(default_factory=QueueRuntime)
    state: StateRuntime = field(default_factory=StateRuntime)
    recovery: RecoveryRuntime = field(default_factory=RecoveryRuntime)
    
    # Metadata
    started_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    # Statistics
    stats: RuntimeStats = field(default_factory=RuntimeStats)
    
    def update_stats(self) -> RuntimeStats:
        """Update runtime statistics."""
        self.stats = RuntimeStats(
            workspaces_count=len(self.workspace.workspaces),
            sessions_count=len(self.session.sessions),
            artifacts_count=len(self.artifact.artifacts),
            environments_count=len(self.environment.environments),
            resources_count=len(self.resource.resources),
            schedules_count=len(self.scheduler.schedules),
            queues_count=len(self.queue.queues),
            states_count=len(self.state.states),
            checkpoints_count=len(self.recovery.checkpoints),
        )
        return self.stats
    
    def get_stats(self) -> RuntimeStats:
        """Get runtime statistics."""
        return self.update_stats()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all subsystems."""
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "subsystems": {},
        }
        
        # Check each subsystem
        checks = {
            "workspace": len(self.workspace.workspaces) >= 0,
            "session": len(self.session.sessions) >= 0,
            "artifact": len(self.artifact.artifacts) >= 0,
            "environment": len(self.environment.environments) >= 0,
            "resource": len(self.resource.resources) >= 0,
            "scheduler": len(self.scheduler.schedules) >= 0,
            "queue": len(self.queue.queues) >= 0,
            "state": len(self.state.states) >= 0,
            "recovery": len(self.recovery.checkpoints) >= 0,
        }
        
        health["subsystems"] = checks
        health["healthy_subsystems"] = sum(1 for v in checks.values() if v)
        health["total_subsystems"] = len(checks)
        
        if health["healthy_subsystems"] < len(checks):
            health["status"] = "degraded"
        
        return health
    
    # ============ Convenience Methods ============
    
    def create_mission_workspace(
        self,
        mission_id: str,
        name: str,
    ) -> Workspace:
        """Create a workspace for a mission."""
        workspace = self.workspace.create_workspace(
            name=name,
            workspace_type=WorkspaceType.MISSION,
            mission_id=mission_id,
        )
        
        # Create associated session
        session = self.session.create_session(
            name=f"session-{name}",
            session_type=SessionType.MISSION,
            mission_id=mission_id,
            workspace_id=workspace.id,
        )
        
        # Create associated state
        state = self.state.create_state(
            name=f"state-{name}",
            state_type=StateType.MISSION,
            mission_id=mission_id,
            workspace_id=workspace.id,
        )
        
        return workspace
    
    def create_checkpoint_for_workspace(self, workspace_id: str) -> Checkpoint:
        """Create a checkpoint for a workspace."""
        workspace = self.workspace.get_workspace(workspace_id)
        if not workspace:
            raise ValueError(f"Workspace not found: {workspace_id}")
        
        # Create checkpoint
        checkpoint = self.recovery.create_checkpoint(
            entity_type="workspace",
            entity_id=workspace_id,
            data={
                "name": workspace.name,
                "workspace_type": workspace.workspace_type.value,
                "status": workspace.status.value,
            },
            state={
                "context": workspace.context.__dict__,
                "resources": workspace.resources.__dict__,
            },
        )
        
        # Create snapshot
        self.workspace.snapshot_workspace(workspace_id)
        
        return checkpoint
    
    def recover_workspace(self, workspace_id: str) -> bool:
        """Recover a workspace from its latest checkpoint."""
        checkpoint = self.recovery.restore_from_checkpoint(workspace_id)
        if not checkpoint:
            return False
        
        workspace = self.workspace.get_workspace(workspace_id)
        if not workspace:
            return False
        
        # Create recovery operation
        recovery = self.recovery.create_recovery(
            recovery_type=RecoveryType.RESTORE,
            entity_id=workspace_id,
            entity_type="workspace",
        )
        
        self.recovery.start_recovery(recovery.id)
        
        # Restore workspace
        from .workspace.models import WorkspaceSnapshot
        snapshot = WorkspaceSnapshot(
            id=checkpoint.id,
            workspace_id=workspace_id,
            created_at=checkpoint.created_at,
            state=checkpoint.state,
        )
        
        success = self.workspace.restore_workspace(workspace_id, snapshot)
        
        self.recovery.complete_recovery(recovery.id, success=success)
        
        return success
    
    def get_workspace_summary(self, workspace_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of a workspace."""
        workspace = self.workspace.get_workspace(workspace_id)
        if not workspace:
            return {}
        
        # Gather related data
        sessions = self.session.list_sessions(workspace_id=workspace_id)
        states = self.state.list_states(workspace_id=workspace_id)
        checkpoints = self.recovery.list_checkpoints(entity_id=workspace_id)
        
        return {
            "workspace": workspace.to_dict(),
            "sessions": [s.to_dict() for s in sessions],
            "states_count": len(states),
            "checkpoints_count": len(checkpoints),
            "telemetry": workspace.telemetry,
        }


# Global instance
_platform: Optional[UniversalRuntimePlatform] = None


def get_platform() -> UniversalRuntimePlatform:
    """Get the global runtime platform instance."""
    global _platform
    if _platform is None:
        _platform = UniversalRuntimePlatform()
    return _platform


def create_mission_workspace(mission_id: str, name: str) -> Workspace:
    """Convenience function to create a mission workspace."""
    return get_platform().create_mission_workspace(mission_id, name)


def health_check() -> Dict[str, Any]:
    """Convenience function to check platform health."""
    return get_platform().health_check()
