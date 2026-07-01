"""Provider SDK - Every provider must use this SDK."""
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ProviderState(Enum):
    """Provider lifecycle states."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


@dataclass
class ProviderDescriptor:
    """Descriptor for a provider."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    skills: List[str] = field(default_factory=list)
    health_status: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


class ProviderHealth:
    """Health check result for a provider."""
    
    def __init__(self, healthy: bool, message: str = "", details: Dict[str, Any] = None):
        self.healthy = healthy
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class ProviderCapabilities:
    """Capabilities of a provider."""
    
    def __init__(self):
        self._skills: List[str] = []
        self._features: List[str] = []
    
    def add_skill(self, skill: str) -> None:
        """Add a skill."""
        self._skills.append(skill)
    
    def add_skills(self, skills: List[str]) -> None:
        """Add multiple skills."""
        self._skills.extend(skills)
    
    def add_feature(self, feature: str) -> None:
        """Add a feature."""
        self._features.append(feature)
    
    @property
    def skills(self) -> List[str]:
        """Get all skills."""
        return self._skills.copy()
    
    @property
    def features(self) -> List[str]:
        """Get all features."""
        return self._features.copy()


class ProviderLifecycle:
    """Lifecycle hooks for providers."""
    
    def on_initialize(self) -> None:
        """Called when provider is initialized."""
        pass
    
    def on_health_check(self) -> ProviderHealth:
        """Called for health check."""
        return ProviderHealth(healthy=True)
    
    def on_start(self) -> None:
        """Called when provider starts."""
        pass
    
    def on_stop(self) -> None:
        """Called when provider stops."""
        pass


class ProviderBase:
    """
    Base class for all providers.
    
    Rules:
    ❌ No business logic
    ❌ No mission logic
    ❌ No decision logic
    
    ✅ Automatic discovery
    ✅ Automatic registration
    ✅ Health reporting
    ✅ Version reporting
    ✅ Capability compatibility
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self._state = ProviderState.CREATED
        self._descriptor = self._create_descriptor()
        self._capabilities = ProviderCapabilities()
        self._lifecycle = ProviderLifecycle()
        self._lifecycle.provider = self
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the provider name."""
        pass
    
    @abstractmethod
    def get_skills(self) -> List[str]:
        """Return the list of supported skills."""
        pass
    
    @abstractmethod
    def execute(self, skill_name: str, input_data: Any) -> Any:
        """Execute a skill."""
        pass
    
    @abstractmethod
    def supports_skill(self, skill_name: str) -> bool:
        """Check if provider supports a skill."""
        pass
    
    def get_description(self) -> str:
        """Return the provider description."""
        return f"Provider: {self.get_name()}"
    
    def _create_descriptor(self) -> ProviderDescriptor:
        """Create provider descriptor."""
        return ProviderDescriptor(
            name=self.get_name(),
            version=self.VERSION,
            description=self.get_description(),
            skills=self.get_skills(),
            health_status="unknown"
        )
    
    @property
    def descriptor(self) -> ProviderDescriptor:
        """Get the provider descriptor."""
        return self._descriptor
    
    @property
    def name(self) -> str:
        """Get the provider name."""
        return self.get_name()
    
    @property
    def version(self) -> str:
        """Get the provider version."""
        return self.VERSION
    
    @property
    def state(self) -> ProviderState:
        """Get the provider state."""
        return self._state
    
    @property
    def capabilities(self) -> ProviderCapabilities:
        """Get the provider capabilities."""
        return self._capabilities
    
    def initialize(self) -> None:
        """Initialize the provider."""
        if self._state == ProviderState.CREATED:
            self._capabilities.add_skills(self.get_skills())
            self._lifecycle.on_initialize()
            self._state = ProviderState.INITIALIZED
    
    def start(self) -> None:
        """Start the provider."""
        if self._state == ProviderState.INITIALIZED:
            self._lifecycle.on_start()
            self._state = ProviderState.READY
            self._check_health()
    
    def stop(self) -> None:
        """Stop the provider."""
        if self._state in [ProviderState.READY, ProviderState.HEALTHY]:
            self._lifecycle.on_stop()
            self._state = ProviderState.CREATED
    
    def health_check(self) -> ProviderHealth:
        """Perform health check."""
        health = self._lifecycle.on_health_check()
        
        if health.healthy:
            self._state = ProviderState.HEALTHY
            self._descriptor.health_status = "healthy"
        else:
            self._state = ProviderState.UNHEALTHY
            self._descriptor.health_status = "unhealthy"
        
        return health
    
    def _check_health(self) -> None:
        """Internal health check."""
        self.health_check()
    
    def validate(self) -> List[str]:
        """Validate the provider contract."""
        errors = []
        
        if not self.get_name():
            errors.append("Name is required")
        
        if not self.get_skills():
            errors.append("At least one skill is required")
        
        return errors


class ProviderBuilder:
    """Builder for providers."""
    
    def __init__(self):
        self._name = ""
        self._description = ""
        self._skills: List[str] = []
        self._version = "1.0.0"
        self._metadata: Dict[str, Any] = {}
    
    def with_name(self, name: str) -> 'ProviderBuilder':
        """Set the name."""
        self._name = name
        return self
    
    def with_description(self, description: str) -> 'ProviderBuilder':
        """Set the description."""
        self._description = description
        return self
    
    def with_skills(self, skills: List[str]) -> 'ProviderBuilder':
        """Set the skills."""
        self._skills = skills
        return self
    
    def with_version(self, version: str) -> 'ProviderBuilder':
        """Set the version."""
        self._version = version
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> 'ProviderBuilder':
        """Set the metadata."""
        self._metadata = metadata
        return self
    
    def build(self) -> ProviderDescriptor:
        """Build the descriptor."""
        return ProviderDescriptor(
            name=self._name,
            version=self._version,
            description=self._description,
            skills=self._skills,
            metadata=self._metadata
        )
