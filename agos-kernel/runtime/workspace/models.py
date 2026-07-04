"""Universal Workspace Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class WorkspaceStatus(Enum):
    """Workspace status."""
    CREATING = "creating"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    SUSPENDED = "suspended"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    ERROR = "error"
    SNAPSHOTTING = "snapshotting"
    RESTORING = "restoring"


class WorkspaceType(Enum):
    """Workspace type."""
    MISSION = "mission"
    USER = "user"
    AGENT = "agent"
    PROVIDER = "provider"
    SYSTEM = "system"
    TEMPLATE = "template"
    EPHEMERAL = "ephemeral"
    PERSISTENT = "persistent"


@dataclass
class WorkspaceResources:
    """Resources allocated to workspace."""
    cpu_cores: float = 1.0
    memory_mb: int = 512
    disk_mb: int = 1024
    network_enabled: bool = True
    gpu_enabled: bool = False
    timeout_seconds: Optional[int] = None


@dataclass
class WorkspaceContext:
    """Workspace execution context."""
    filesystem_root: str = ""
    repositories: List[str] = field(default_factory=list)
    knowledge_base: str = ""
    policies: List[str] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)
    secrets_refs: Dict[str, str] = field(default_factory=dict)
    working_directory: str = ""


@dataclass
class WorkspaceSnapshot:
    """Snapshot of workspace state."""
    id: str
    workspace_id: str
    created_at: datetime = field(default_factory=datetime.now)
    files: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Workspace:
    """Universal Workspace."""
    id: str
    name: str
    mission_id: Optional[str] = None
    
    # Type and status
    workspace_type: WorkspaceType = WorkspaceType.MISSION
    status: WorkspaceStatus = WorkspaceStatus.CREATING
    
    # Resources
    resources: WorkspaceResources = field(default_factory=WorkspaceResources)
    
    # Context
    context: WorkspaceContext = field(default_factory=WorkspaceContext)
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Telemetry
    telemetry: Dict[str, Any] = field(default_factory=dict)
    
    # Parent/clone
    parent_id: Optional[str] = None
    clone_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.workspace_type.value,
            "status": self.status.value,
            "mission_id": self.mission_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class WorkspaceTemplate:
    """Template for creating workspaces."""
    id: str
    name: str
    description: str = ""
    
    # Template content
    workspace_type: WorkspaceType = WorkspaceType.MISSION
    resources: WorkspaceResources = field(default_factory=WorkspaceResources)
    
    # Pre-configured context
    default_repositories: List[str] = field(default_factory=list)
    default_policies: List[str] = field(default_factory=list)
    default_environment: Dict[str, str] = field(default_factory=dict)
    init_script: Optional[str] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
