"""AGOS Adapter Base."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class AdapterStatus(Enum):
    """Adapter status."""
    DRAFT = "draft"
    DEVELOPMENT = "development"
    TESTING = "testing"
    CERTIFIED = "certified"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"


@dataclass
class AdapterMetadata:
    """Adapter metadata."""
    id: str
    name: str
    technology: str
    version: str = "1.0.0"
    description: str = ""
    auth_types: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AdapterConfig:
    """Adapter configuration."""
    endpoint: str = ""
    credentials: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    retry_count: int = 3


class Adapter:
    """Base adapter class."""
    
    def __init__(self, name: str, technology: str, description: str = ""):
        """Initialize adapter."""
        self.metadata = AdapterMetadata(
            id=f"adapter-{uuid.uuid4().hex[:8]}",
            name=name,
            technology=technology,
            description=description,
        )
        self.status = AdapterStatus.DRAFT
        self.config = AdapterConfig()
    
    def discover(self) -> List[Dict]:
        """Discover resources."""
        return []
    
    def validate(self, config: Dict) -> bool:
        """Validate configuration."""
        return True
    
    def health_check(self) -> Dict[str, Any]:
        """Check adapter health."""
        return {"healthy": True, "latency_ms": 0}
    
    def authenticate(self, credentials: Dict) -> bool:
        """Authenticate with target."""
        return True
    
    def negotiate_capability(self, capability: str) -> Optional[Dict]:
        """Negotiate capability."""
        return None
    
    def get_capabilities(self) -> List[str]:
        """Get adapter capabilities."""
        return self.metadata.capabilities


class AdapterRegistry:
    """Registry for all adapters."""
    
    def __init__(self):
        """Initialize registry."""
        self.adapters: Dict[str, Adapter] = {}
    
    def register(self, adapter: Adapter) -> None:
        """Register an adapter."""
        self.adapters[adapter.metadata.id] = adapter
    
    def get(self, adapter_id: str) -> Optional[Adapter]:
        """Get an adapter."""
        return self.adapters.get(adapter_id)
    
    def list_all(self) -> List[Adapter]:
        """List all adapters."""
        return list(self.adapters.values())
    
    def list_by_technology(self, technology: str) -> List[Adapter]:
        """List adapters by technology."""
        return [a for a in self.adapters.values() if a.metadata.technology == technology]


# Global registry
_registry = AdapterRegistry()


def get_registry() -> AdapterRegistry:
    """Get the global adapter registry."""
    return _registry