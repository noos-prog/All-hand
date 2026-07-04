"""Universal Environment Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class EnvironmentType(Enum):
    """Environment type."""
    LOCAL = "local"
    CONTAINER = "container"
    VIRTUAL_MACHINE = "vm"
    CLOUD = "cloud"
    REMOTE = "remote"
    BROWSER = "browser"
    SANDBOX = "sandbox"
    CI = "ci"
    EPHEMERAL = "ephemeral"
    PERSISTENT = "persistent"


class EnvironmentStatus(Enum):
    """Environment status."""
    CREATING = "creating"
    INITIALIZING = "initializing"
    READY = "ready"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class EnvironmentHealth:
    """Environment health status."""
    status: EnvironmentStatus = EnvironmentStatus.HEALTHY
    checks: Dict[str, bool] = field(default_factory=dict)
    last_check: datetime = field(default_factory=datetime.now)
    uptime_seconds: float = 0.0
    error_count: int = 0


@dataclass
class EnvironmentConfig:
    """Environment configuration."""
    image: str = ""
    command: str = ""
    args: List[str] = field(default_factory=list)
    env_vars: Dict[str, str] = field(default_factory=dict)
    ports: List[int] = field(default_factory=list)
    volumes: List[str] = field(default_factory=list)
    resources: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Environment:
    """Universal Environment."""
    id: str
    name: str
    environment_type: EnvironmentType
    
    # Status
    status: EnvironmentStatus = EnvironmentStatus.CREATING
    
    # Configuration
    config: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    health: EnvironmentHealth = field(default_factory=EnvironmentHealth)
    
    # Connection
    endpoint: str = ""
    connection_info: Dict[str, Any] = field(default_factory=dict)
    
    # Relationships
    workspace_id: Optional[str] = None
    provider_id: Optional[str] = None
    
    # Compatibility
    compatible_with: List[str] = field(default_factory=list)
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.environment_type.value,
            "status": self.status.value,
            "endpoint": self.endpoint,
            "created_at": self.created_at.isoformat(),
        }
