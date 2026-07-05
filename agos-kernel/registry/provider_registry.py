"""
AGOS Provider Registry
==================

Registry for all AGOS providers.
Every provider must be registered to be discoverable by capabilities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type
import threading


class ProviderStatus(Enum):
    """Provider status."""
    REGISTERED = "registered"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


class ProviderType(Enum):
    """Type of provider."""
    FILESYSTEM = "filesystem"
    GIT = "git"
    LLM = "llm"
    HTTP = "http"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    STORAGE = "storage"
    COMPUTE = "compute"


@dataclass
class Provider:
    """
    A registered AGOS provider.
    
    Attributes:
        id: Unique identifier (e.g., PROVIDER-000001)
        name: Human-readable name
        provider_type: Type of provider
        description: What this provider does
        version: Semantic version
        status: Current status
        handler: The provider handler instance
        capabilities: List of capabilities this provider supports
        config: Provider configuration
        health_check: Health check function
        metadata: Additional metadata
        registered_at: When this was registered
    """
    id: str
    name: str
    provider_type: ProviderType
    description: str = ""
    version: str = "1.0.0"
    status: ProviderStatus = ProviderStatus.REGISTERED
    handler: Optional[Any] = None
    capabilities: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_health_check: Optional[datetime] = None
    error: Optional[str] = None
    
    def execute(self, operation: str, **kwargs) -> Any:
        """Execute a provider operation."""
        if self.handler is None:
            raise RuntimeError(f"Provider {self.id} has no handler")
        return self.handler.execute(operation, **kwargs)
    
    def health_check(self) -> bool:
        """Perform health check."""
        try:
            if self.handler and hasattr(self.handler, 'health_check'):
                result = self.handler.health_check()
                self.status = ProviderStatus.AVAILABLE if result else ProviderStatus.UNAVAILABLE
                self.last_health_check = datetime.utcnow()
                return result
            self.status = ProviderStatus.AVAILABLE
            return True
        except Exception as e:
            self.status = ProviderStatus.ERROR
            self.error = str(e)
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "provider_type": self.provider_type.value,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "config": self.config,
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat(),
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "error": self.error,
        }


class ProviderRegistry:
    """
    Thread-safe singleton registry for all AGOS providers.
    
    Usage:
        registry = ProviderRegistry.get_instance()
        registry.register(
            id="PROVIDER-000001",
            name="GitHub Provider",
            provider_type=ProviderType.GIT,
            handler=github_handler,
        )
        provider = registry.get("PROVIDER-000001")
        result = provider.execute("clone", url="...")
    """
    
    _instance: Optional['ProviderRegistry'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        """Initialize registry."""
        self._providers: Dict[str, Provider] = {}
        self._lock = threading.RLock()
    
    @classmethod
    def get_instance(cls) -> 'ProviderRegistry':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def register(
        self,
        id: str,
        name: str,
        provider_type: ProviderType,
        description: str = "",
        handler: Optional[Any] = None,
        version: str = "1.0.0",
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a provider.
        
        Args:
            id: Unique identifier
            name: Human-readable name
            provider_type: Type of provider
            description: What this provider does
            handler: The provider handler
            version: Semantic version
            capabilities: List of capabilities supported
            config: Provider configuration
            metadata: Additional metadata
            
        Returns:
            The provider ID
        """
        with self._lock:
            if id in self._providers:
                return id  # Already registered
            
            provider = Provider(
                id=id,
                name=name,
                provider_type=provider_type,
                description=description,
                handler=handler,
                version=version,
                capabilities=capabilities or [],
                config=config or {},
                metadata=metadata or {},
            )
            
            self._providers[id] = provider
            return id
    
    def unregister(self, id: str) -> bool:
        """Unregister a provider."""
        with self._lock:
            if id in self._providers:
                del self._providers[id]
                return True
            return False
    
    def get(self, id: str) -> Optional[Provider]:
        """Get a registered provider."""
        return self._providers.get(id)
    
    def list_all(self) -> List[Provider]:
        """List all registered providers."""
        return list(self._providers.values())
    
    def list_by_type(self, provider_type: ProviderType) -> List[Provider]:
        """List providers by type."""
        return [p for p in self._providers.values() if p.provider_type == provider_type]
    
    def list_available(self) -> List[Provider]:
        """List available providers."""
        return [p for p in self._providers.values() if p.status == ProviderStatus.AVAILABLE]
    
    def find_by_capability(self, capability: str) -> List[Provider]:
        """Find providers supporting a capability."""
        return [p for p in self._providers.values() if capability in p.capabilities]
    
    def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all providers."""
        results = {}
        for id, provider in self._providers.items():
            results[id] = provider.health_check()
        return results
    
    def check_health(self) -> Dict[str, Any]:
        """Check health of all providers."""
        return {
            "total": len(self._providers),
            "available": len(self.list_available()),
            "error": len([p for p in self._providers.values() if p.status == ProviderStatus.ERROR]),
            "providers": {p.id: {"name": p.name, "status": p.status.value} for p in self._providers.values()},
        }
    
    def reset(self) -> None:
        """Reset registry (for testing)."""
        with self._lock:
            self._providers.clear()

_provider_registry_instance = None
_provider_registry_lock = threading.Lock()
def get_provider_registry() -> ProviderRegistry:
    global _provider_registry_instance
    if _provider_registry_instance is None:
        with _provider_registry_lock:
            if _provider_registry_instance is None:
                _provider_registry_instance = ProviderRegistry()
    return _provider_registry_instance

