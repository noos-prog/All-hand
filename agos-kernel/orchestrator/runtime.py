"""Universal Multi-Workspace Orchestrator."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class WorkspaceState(Enum):
    """Workspace state."""
    PENDING = "pending"
    ALLOCATED = "allocated"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    RECOVERING = "recovering"
    TERMINATED = "terminated"


@dataclass
class Workspace:
    """A managed workspace."""
    id: str
    name: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    
    # State
    state: WorkspaceState = WorkspaceState.PENDING
    
    # Resources
    cpu: float = 1.0
    memory: float = 1024
    storage: float = 10240
    
    # Shared resources (read-only)
    shared_readonly: List[str] = field(default_factory=list)
    
    # Template
    template_id: Optional[str] = None
    
    # Checkpoints
    checkpoints: List[str] = field(default_factory=list)
    last_checkpoint: Optional[datetime] = None
    
    # Timeline
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Migration
    migrated_from: Optional[str] = None
    migrated_to: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkspaceTemplate:
    """Workspace template."""
    id: str
    name: str
    description: str = ""
    resources: Dict[str, float] = field(default_factory=dict)
    shared_resources: List[str] = field(default_factory=list)
    inherited_from: Optional[str] = None


class WorkspacePool:
    """Pool of available workspaces."""
    
    def __init__(self, max_size: int = 1000):
        """Initialize pool."""
        self.max_size = max_size
        self.available: Set[str] = set()
        self.in_use: Set[str] = set()
    
    def acquire(self) -> Optional[str]:
        """Acquire workspace from pool."""
        if self.available:
            ws_id = self.available.pop()
            self.in_use.add(ws_id)
            return ws_id
        return None
    
    def release(self, ws_id: str) -> None:
        """Release workspace back to pool."""
        self.in_use.discard(ws_id)
        if len(self.available) < self.max_size:
            self.available.add(ws_id)
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        return {
            "available": len(self.available),
            "in_use": len(self.in_use),
            "total": len(self.available) + len(self.in_use),
        }


class WorkspaceOrchestrator:
    """Universal Multi-Workspace Orchestrator."""
    
    def __init__(self):
        """Initialize orchestrator."""
        self.workspaces: Dict[str, Workspace] = {}
        self.templates: Dict[str, WorkspaceTemplate] = {}
        self.pool = WorkspacePool()
        
        # Router
        self.router = WorkspaceRouter()
        
        # Scheduler
        self.scheduler = WorkspaceScheduler()
        
        # Sync
        self.synchronizer = WorkspaceSynchronizer()
        
        # Analytics
        self.analytics = WorkspaceAnalytics()
    
    def create_workspace(
        self,
        name: str,
        parent_id: Optional[str] = None,
        template_id: Optional[str] = None,
        resources: Optional[Dict[str, float]] = None,
    ) -> Workspace:
        """Create a new workspace."""
        ws_id = self._generate_id(name)
        
        workspace = Workspace(
            id=ws_id,
            name=name,
            parent_id=parent_id,
            template_id=template_id,
        )
        
        if resources:
            workspace.cpu = resources.get("cpu", workspace.cpu)
            workspace.memory = resources.get("memory", workspace.memory)
            workspace.storage = resources.get("storage", workspace.storage)
        
        self.workspaces[ws_id] = workspace
        
        # Add to parent's children
        if parent_id and parent_id in self.workspaces:
            self.workspaces[parent_id].children.append(ws_id)
        
        # Add to pool
        self.pool.available.add(ws_id)
        
        return workspace
    
    def clone_workspace(
        self,
        source_id: str,
        new_name: str,
    ) -> Optional[Workspace]:
        """Clone an existing workspace."""
        source = self.workspaces.get(source_id)
        if not source:
            return None
        
        # Create new workspace
        cloned = self.create_workspace(
            name=new_name,
            parent_id=source.parent_id,
            resources={"cpu": source.cpu, "memory": source.memory, "storage": source.storage},
        )
        
        # Copy shared resources
        cloned.shared_readonly = source.shared_readonly.copy()
        
        return cloned
    
    def allocate(self, ws_id: str) -> bool:
        """Allocate a workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return False
        
        workspace.state = WorkspaceState.ALLOCATED
        self.pool.release(ws_id)
        
        return True
    
    def start(self, ws_id: str) -> bool:
        """Start a workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return False
        
        workspace.state = WorkspaceState.RUNNING
        workspace.started_at = datetime.now()
        
        return True
    
    def pause(self, ws_id: str) -> bool:
        """Pause a workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace or workspace.state != WorkspaceState.RUNNING:
            return False
        
        workspace.state = WorkspaceState.PAUSED
        return True
    
    def resume(self, ws_id: str) -> bool:
        """Resume a workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace or workspace.state != WorkspaceState.PAUSED:
            return False
        
        workspace.state = WorkspaceState.RUNNING
        return True
    
    def terminate(self, ws_id: str) -> bool:
        """Terminate a workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return False
        
        workspace.state = WorkspaceState.TERMINATED
        workspace.completed_at = datetime.now()
        
        # Terminate children
        for child_id in workspace.children:
            self.terminate(child_id)
        
        return True
    
    def create_checkpoint(self, ws_id: str) -> str:
        """Create a checkpoint."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return ""
        
        checkpoint_id = self._generate_id(f"checkpoint-{ws_id}")
        workspace.checkpoints.append(checkpoint_id)
        workspace.last_checkpoint = datetime.now()
        
        return checkpoint_id
    
    def recover(self, ws_id: str, checkpoint_id: str) -> bool:
        """Recover from checkpoint."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return False
        
        if checkpoint_id not in workspace.checkpoints:
            return False
        
        workspace.state = WorkspaceState.RECOVERING
        # In a real implementation, would restore state from checkpoint
        
        return True
    
    def migrate(self, ws_id: str, target: str) -> bool:
        """Migrate workspace."""
        workspace = self.workspaces.get(ws_id)
        if not workspace:
            return False
        
        workspace.migrated_to = target
        return True
    
    def sync(self, ws_ids: List[str]) -> bool:
        """Synchronize workspaces."""
        return self.synchronizer.sync(ws_ids)
    
    def route(self, mission_id: str) -> Optional[str]:
        """Route mission to appropriate workspace."""
        return self.router.route(mission_id, self.workspaces)
    
    def schedule(self, ws_id: str, when: datetime) -> bool:
        """Schedule workspace execution."""
        return self.scheduler.schedule(ws_id, when)
    
    def auto_cleanup(self, max_age_hours: int = 24) -> int:
        """Auto cleanup old workspaces."""
        cleaned = 0
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        for ws in self.workspaces.values():
            if ws.state in [WorkspaceState.COMPLETED, WorkspaceState.TERMINATED, WorkspaceState.FAILED]:
                if ws.completed_at and ws.completed_at < cutoff:
                    self.terminate(ws.id)
                    cleaned += 1
        
        return cleaned
    
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "total_workspaces": len(self.workspaces),
            "by_state": {
                s.value: sum(1 for w in self.workspaces.values() if w.state.value == s.value)
                for s in WorkspaceState
            },
            "pool": self.pool.get_stats(),
            "nested_count": sum(1 for w in self.workspaces.values() if w.parent_id),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class WorkspaceRouter:
    """Route missions to workspaces."""
    
    def route(self, mission_id: str, workspaces: Dict[str, Workspace]) -> Optional[str]:
        """Route mission to workspace."""
        # Find available workspace
        for ws in workspaces.values():
            if ws.state == WorkspaceState.RUNNING:
                return ws.id
        return None


class WorkspaceScheduler:
    """Schedule workspace execution."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduled: Dict[str, datetime] = {}
    
    def schedule(self, ws_id: str, when: datetime) -> bool:
        """Schedule workspace."""
        self.scheduled[ws_id] = when
        return True


class WorkspaceSynchronizer:
    """Synchronize workspace state."""
    
    def sync(self, ws_ids: List[str]) -> bool:
        """Sync workspaces."""
        return True
        # Would implement actual synchronization


class WorkspaceAnalytics:
    """Workspace analytics."""
    
    def get_metrics(self, ws_id: str) -> Dict[str, Any]:
        """Get workspace metrics."""
        return {
            "id": ws_id,
            "timestamp": datetime.now().isoformat(),
        }
