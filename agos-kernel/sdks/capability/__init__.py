"""Capability SDK - Every capability must use this SDK."""
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type


class CapabilityState(Enum):
    """Capability lifecycle states."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class CapabilityDescriptor:
    """Descriptor for a capability."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    skills: List[str] = field(default_factory=list)
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CapabilityContext:
    """Context for capability execution."""
    mission_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CapabilityResult:
    """Result of capability execution."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class CapabilityBase:
    """
    Base class for all capabilities.
    
    Rules:
    ❌ No direct kernel access
    ❌ No global state
    ❌ No filesystem access outside providers
    
    ✅ Automatic registration
    ✅ Automatic validation
    ✅ Automatic metadata
    ✅ Automatic event publishing
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self._state = CapabilityState.CREATED
        self._descriptor = self._create_descriptor()
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the capability name."""
        pass
    
    @abstractmethod
    def get_skills(self) -> List[str]:
        """Return the list of required skills."""
        pass
    
    def get_description(self) -> str:
        """Return the capability description."""
        return f"Capability: {self.get_name()}"
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the capability."""
        pass
    
    def _create_descriptor(self) -> CapabilityDescriptor:
        """Create capability descriptor."""
        return CapabilityDescriptor(
            name=self.get_name(),
            version=self.VERSION,
            description=self.get_description(),
            skills=self.get_skills(),
            priority=getattr(self, "PRIORITY", 1),
            metadata=getattr(self, "METADATA", {})
        )
    
    @property
    def descriptor(self) -> CapabilityDescriptor:
        """Get the capability descriptor."""
        return self._descriptor
    
    @property
    def name(self) -> str:
        """Get the capability name."""
        return self.get_name()
    
    @property
    def description(self) -> str:
        """Get the capability description."""
        return self.get_description()
    
    @property
    def skills(self) -> List[str]:
        """Get the required skills."""
        return self.get_skills()
    
    @property
    def state(self) -> CapabilityState:
        """Get the capability state."""
        return self._state
    
    def initialize(self) -> None:
        """Initialize the capability."""
        if self._state == CapabilityState.CREATED:
            self._state = CapabilityState.INITIALIZED
    
    def prepare(self) -> None:
        """Prepare the capability for execution."""
        if self._state == CapabilityState.INITIALIZED:
            self._state = CapabilityState.READY
    
    def start(self) -> None:
        """Start the capability."""
        if self._state == CapabilityState.READY:
            self._state = CapabilityState.RUNNING
    
    def stop(self) -> None:
        """Stop the capability."""
        if self._state == CapabilityState.RUNNING:
            self._state = CapabilityState.STOPPED
    
    def validate(self) -> List[str]:
        """Validate the capability contract."""
        errors = []
        
        if not self.get_name():
            errors.append("Name is required")
        
        if not self.get_skills():
            errors.append("At least one skill is required")
        
        return errors


class CapabilityBuilder:
    """Builder for capabilities."""
    
    def __init__(self):
        self._name = ""
        self._description = ""
        self._skills: List[str] = []
        self._version = "1.0.0"
        self._priority = 1
        self._metadata: Dict[str, Any] = {}
    
    def with_name(self, name: str) -> 'CapabilityBuilder':
        """Set the name."""
        self._name = name
        return self
    
    def with_description(self, description: str) -> 'CapabilityBuilder':
        """Set the description."""
        self._description = description
        return self
    
    def with_skills(self, skills: List[str]) -> 'CapabilityBuilder':
        """Set the skills."""
        self._skills = skills
        return self
    
    def with_version(self, version: str) -> 'CapabilityBuilder':
        """Set the version."""
        self._version = version
        return self
    
    def with_priority(self, priority: int) -> 'CapabilityBuilder':
        """Set the priority."""
        self._priority = priority
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> 'CapabilityBuilder':
        """Set the metadata."""
        self._metadata = metadata
        return self
    
    def build(self) -> CapabilityDescriptor:
        """Build the descriptor."""
        return CapabilityDescriptor(
            name=self._name,
            version=self._version,
            description=self._description,
            skills=self._skills,
            priority=self._priority,
            metadata=self._metadata
        )


class CapabilityLifecycle:
    """Lifecycle hooks for capabilities."""
    
    def on_initialize(self) -> None:
        """Called when capability is initialized."""
        pass
    
    def on_prepare(self) -> None:
        """Called when capability is prepared."""
        pass
    
    def on_execute(self, parameters: Dict[str, Any]) -> None:
        """Called before capability execution."""
        pass
    
    def on_complete(self, result: Any) -> None:
        """Called after capability execution."""
        pass
    
    def on_error(self, error: Exception) -> None:
        """Called when capability execution fails."""
        pass
    
    def on_stop(self) -> None:
        """Called when capability is stopped."""
        pass
