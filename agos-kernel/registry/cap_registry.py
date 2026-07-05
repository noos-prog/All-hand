"""
AGOS Capability Registry
====================

Registry for all AGOS capabilities.
Every capability must be registered to be discoverable by the Kernel.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type
import threading


class CapabilityType(Enum):
    """Type of capability."""
    REPOSITORY = "repository"
    ANALYSIS = "analysis"
    EXECUTION = "execution"
    KNOWLEDGE = "knowledge"
    GOVERNANCE = "governance"
    ORCHESTRATION = "orchestration"


class CapabilityStatus(Enum):
    """Capability status."""
    REGISTERED = "registered"
    LOADED = "loaded"
    ACTIVE = "active"
    DISABLED = "disabled"
    FAILED = "failed"


@dataclass
class Capability:
    """
    A registered AGOS capability.
    
    Attributes:
        id: Unique identifier (e.g., CAPABILITY-000001)
        name: Human-readable name
        capability_type: Type of capability
        description: What this capability does
        version: Semantic version
        status: Current status
        handler: The capability handler function/class
        input_schema: JSON schema for input validation
        output_schema: JSON schema for output validation
        skills: List of skills this capability provides
        providers: List of provider types this capability uses
        metadata: Additional metadata
        registered_at: When this was registered
    """
    id: str
    name: str
    capability_type: CapabilityType
    description: str = ""
    version: str = "1.0.0"
    status: CapabilityStatus = CapabilityStatus.REGISTERED
    handler: Optional[Any] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)
    providers: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    activated_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def execute(self, input_data: Any) -> Any:
        """Execute this capability."""
        if self.handler is None:
            raise RuntimeError(f"Capability {self.id} has no handler")
        return self.handler(input_data)
    
    def activate(self) -> bool:
        """Activate this capability."""
        try:
            if self.handler is not None:
                self.status = CapabilityStatus.ACTIVE
                self.activated_at = datetime.utcnow()
                return True
            return False
        except Exception as e:
            self.status = CapabilityStatus.FAILED
            self.error = str(e)
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "capability_type": self.capability_type.value,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "skills": self.skills,
            "providers": self.providers,
            "metadata": self.metadata,
            "registered_at": self.registered_at.isoformat(),
            "activated_at": self.activated_at.isoformat() if self.activated_at else None,
        }


class CapabilityRegistry:
    """
    Thread-safe singleton registry for all AGOS capabilities.
    
    Usage:
        registry = CapabilityRegistry.get_instance()
        registry.register(
            id="CAPABILITY-000001",
            name="Repository Discovery",
            capability_type=CapabilityType.REPOSITORY,
            handler=my_handler,
        )
        capability = registry.get("CAPABILITY-000001")
        result = capability.execute(input_data)
    """
    
    _instance: Optional['CapabilityRegistry'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        """Initialize registry."""
        self._capabilities: Dict[str, Capability] = {}
        self._lock = threading.RLock()
    
    @classmethod
    def get_instance(cls) -> 'CapabilityRegistry':
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
        capability_type: CapabilityType,
        description: str = "",
        handler: Optional[Any] = None,
        version: str = "1.0.0",
        skills: Optional[List[str]] = None,
        providers: Optional[List[str]] = None,
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a capability.
        
        Args:
            id: Unique identifier (e.g., CAPABILITY-000001)
            name: Human-readable name
            capability_type: Type of capability
            description: What this capability does
            handler: The capability handler
            version: Semantic version
            skills: List of skills this provides
            providers: List of provider types needed
            input_schema: JSON schema for input
            output_schema: JSON schema for output
            metadata: Additional metadata
            
        Returns:
            The capability ID
        """
        with self._lock:
            if id in self._capabilities:
                return id  # Already registered
            
            capability = Capability(
                id=id,
                name=name,
                capability_type=capability_type,
                description=description,
                handler=handler,
                version=version,
                skills=skills or [],
                providers=providers or [],
                input_schema=input_schema or {},
                output_schema=output_schema or {},
                metadata=metadata or {},
            )
            
            self._capabilities[id] = capability
            return id
    
    def unregister(self, id: str) -> bool:
        """Unregister a capability."""
        with self._lock:
            if id in self._capabilities:
                del self._capabilities[id]
                return True
            return False
    
    def get(self, id: str) -> Optional[Capability]:
        """Get a registered capability."""
        return self._capabilities.get(id)
    
    def list_all(self) -> List[Capability]:
        """List all registered capabilities."""
        return list(self._capabilities.values())
    
    def list_by_type(self, capability_type: CapabilityType) -> List[Capability]:
        """List capabilities by type."""
        return [c for c in self._capabilities.values() if c.capability_type == capability_type]
    
    def list_active(self) -> List[Capability]:
        """List active capabilities."""
        return [c for c in self._capabilities.values() if c.status == CapabilityStatus.ACTIVE]
    
    def search(self, query: str) -> List[Capability]:
        """Search capabilities by name or description."""
        query_lower = query.lower()
        return [
            c for c in self._capabilities.values()
            if query_lower in c.name.lower() or query_lower in c.description.lower()
        ]
    
    def activate_all(self) -> Dict[str, bool]:
        """Activate all capabilities."""
        results = {}
        for id, capability in self._capabilities.items():
            results[id] = capability.activate()
        return results
    
    def check_health(self) -> Dict[str, Any]:
        """Check health of all capabilities."""
        return {
            "total": len(self._capabilities),
            "active": len(self.list_active()),
            "failed": len([c for c in self._capabilities.values() if c.status == CapabilityStatus.FAILED]),
            "capabilities": {c.id: {"name": c.name, "status": c.status.value} for c in self._capabilities.values()},
        }
    
    def reset(self) -> None:
        """Reset registry (for testing)."""
        with self._lock:
            self._capabilities.clear()


# Decorator for easy registration
def register_capability(
    id: str,
    name: str,
    capability_type: CapabilityType,
    description: str = "",
    skills: Optional[List[str]] = None,
    providers: Optional[List[str]] = None,
):
    """
    Decorator to register a capability.
    
    Usage:
        @register_capability(
            id="CAPABILITY-000001",
            name="Repository Discovery",
            capability_type=CapabilityType.REPOSITORY,
        )
        def my_capability(input_data):
            return result
    """
    def decorator(func: Callable) -> Callable:
        registry = CapabilityRegistry.get_instance()
        registry.register(
            id=id,
            name=name,
            capability_type=capability_type,
            description=description,
            handler=func,
            skills=skills,
            providers=providers,
        )
        return func
    
    return decorator

# Add singleton function
_capability_registry_instance = None
_capability_registry_lock = threading.Lock()

def get_capability_registry() -> CapabilityRegistry:
    global _capability_registry_instance
    if _capability_registry_instance is None:
        with _capability_registry_lock:
            if _capability_registry_instance is None:
                _capability_registry_instance = CapabilityRegistry()
    return _capability_registry_instance

