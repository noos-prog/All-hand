"""AGOS Capability Registry."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class CapabilityType(Enum):
    """Capability type."""
    ANALYSIS = "analysis"
    EXECUTION = "execution"
    GENERATION = "generation"
    TRANSFORMATION = "transformation"
    VALIDATION = "validation"


class CapabilityStatus(Enum):
    """Capability status."""
    AVAILABLE = "available"
    BUSY = "busy"
    DISABLED = "disabled"


@dataclass
class Capability:
    """A capability."""
    id: str
    name: str
    capability_type: CapabilityType
    handler: Callable
    description: str = ""
    version: str = "1.0.0"
    parameters: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    status: CapabilityStatus = CapabilityStatus.AVAILABLE
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CapabilityRegistry:
    """
    Capability Registry.
    
    Manages all capabilities available in the system.
    
    Usage:
        registry = CapabilityRegistry()
        cap = registry.register(
            name="repository_analysis",
            capability_type=CapabilityType.ANALYSIS,
            handler=analyze_repo,
            description="Analyzes repositories"
        )
        result = registry.execute("repository_analysis", url="https://github.com/org/repo")
    """
    
    def __init__(self):
        """Initialize capability registry."""
        self._capabilities: Dict[str, Capability] = {}
        self._by_type: Dict[CapabilityType, List[str]] = {}
    
    def register(
        self,
        name: str,
        capability_type: CapabilityType,
        handler: Callable,
        description: str = "",
        version: str = "1.0.0",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Capability:
        """Register a capability."""
        capability = Capability(
            id=f"cap-{uuid.uuid4().hex[:8]}",
            name=name,
            capability_type=capability_type,
            handler=handler,
            description=description,
            version=version,
            parameters=parameters or {},
        )
        
        self._capabilities[name] = capability
        
        if capability_type not in self._by_type:
            self._by_type[capability_type] = []
        self._by_type[capability_type].append(name)
        
        return capability
    
    def get(self, name: str) -> Optional[Capability]:
        """Get a capability by name."""
        return self._capabilities.get(name)
    
    def execute(self, name: str, **kwargs) -> Any:
        """Execute a capability."""
        capability = self._capabilities.get(name)
        if not capability:
            raise ValueError(f"Capability not found: {name}")
        
        capability.status = CapabilityStatus.BUSY
        capability.usage_count += 1
        
        try:
            result = capability.handler(**kwargs)
            return result
        finally:
            capability.status = CapabilityStatus.AVAILABLE
    
    def list_all(self) -> List[Capability]:
        """List all capabilities."""
        return list(self._capabilities.values())
    
    def list_by_type(self, capability_type: CapabilityType) -> List[Capability]:
        """List capabilities by type."""
        names = self._by_type.get(capability_type, [])
        return [self._capabilities[n] for n in names]
    
    def enable(self, name: str) -> bool:
        """Enable a capability."""
        capability = self._capabilities.get(name)
        if capability:
            capability.status = CapabilityStatus.AVAILABLE
            return True
        return False
    
    def disable(self, name: str) -> bool:
        """Disable a capability."""
        capability = self._capabilities.get(name)
        if capability:
            capability.status = CapabilityStatus.DISABLED
            return True
        return False
    
    def unregister(self, name: str) -> bool:
        """Unregister a capability."""
        if name in self._capabilities:
            cap = self._capabilities[name]
            del self._capabilities[name]
            if cap.capability_type in self._by_type:
                if name in self._by_type[cap.capability_type]:
                    self._by_type[cap.capability_type].remove(name)
            return True
        return False


_capability_registry: Optional[CapabilityRegistry] = None


def get_capability_registry() -> CapabilityRegistry:
    """Get the global capability registry."""
    global _capability_registry
    if _capability_registry is None:
        _capability_registry = CapabilityRegistry()
    return _capability_registry
