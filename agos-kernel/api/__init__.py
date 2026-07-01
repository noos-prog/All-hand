"""
AGOS Kernel API Specification v1.0

This document defines the public API for AGOS Kernel.
All future development must use these APIs only.

AFTER COMPLETION:
- Lock Public API
- Reject Breaking Changes
- Reject Direct Internal Access
- Future Development Must Use Public APIs Only
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# =============================================================================
# PUBLIC ENUMS
# =============================================================================

class KernelState(Enum):
    """Kernel states."""
    STOPPED = "stopped"
    STARTING = "starting"
    READY = "ready"
    STOPPING = "stopping"
    ERROR = "error"


class MissionState(Enum):
    """Mission states."""
    CREATED = "created"
    VALIDATED = "validated"
    PLANNED = "planned"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CapabilityState(Enum):
    """Capability states."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class ProviderState(Enum):
    """Provider states."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


# =============================================================================
# PUBLIC DATA CLASSES
# =============================================================================

@dataclass
class MissionInput:
    """Input for creating a mission."""
    name: str
    capability: str
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MissionOutput:
    """Output from mission execution."""
    mission_id: str
    state: MissionState
    result: Any = None
    error: Optional[str] = None
    duration_ms: int = 0
    events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CapabilityDescriptor:
    """Descriptor for a capability."""
    name: str
    version: str
    description: str
    skills: List[str]
    priority: int = 1


@dataclass
class ProviderDescriptor:
    """Descriptor for a provider."""
    name: str
    version: str
    description: str
    skills: List[str]
    health_status: str = "unknown"


@dataclass
class DecisionResult:
    """Result from decision."""
    capability: str
    provider: str
    score: float
    reasons: List[str]


@dataclass
class ExecutionResult:
    """Result from execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    duration_ms: int = 0


@dataclass
class HealthReport:
    """Health report."""
    status: str
    components: List[Dict[str, Any]]
    uptime_ms: int
    timestamp: datetime


@dataclass
class BootstrapResult:
    """Bootstrap result."""
    success: bool
    kernel_version: str
    capabilities: List[str]
    providers: List[str]
    duration_ms: int
    errors: List[str]


# =============================================================================
# KERNEL API (PUBLIC)
# =============================================================================

class IKernelAPI:
    """
    Public Kernel API.
    
    Methods:
    - start() -> BootstrapResult
    - stop()
    - execute_mission(input: MissionInput) -> MissionOutput
    - get_health() -> HealthReport
    - get_capabilities() -> List[CapabilityDescriptor]
    - get_providers() -> List[ProviderDescriptor]
    """
    
    def start(self) -> BootstrapResult:
        """Start the kernel."""
        raise NotImplementedError()
    
    def stop(self) -> None:
        """Stop the kernel."""
        raise NotImplementedError()
    
    def execute_mission(self, input: MissionInput) -> MissionOutput:
        """Execute a mission."""
        raise NotImplementedError()
    
    def get_health(self) -> HealthReport:
        """Get kernel health."""
        raise NotImplementedError()
    
    def get_capabilities(self) -> List[CapabilityDescriptor]:
        """Get registered capabilities."""
        raise NotImplementedError()
    
    def get_providers(self) -> List[ProviderDescriptor]:
        """Get registered providers."""
        raise NotImplementedError()


# =============================================================================
# CAPABILITY API (PUBLIC)
# =============================================================================

class ICapabilityAPI:
    """
    Public Capability API.
    
    Methods:
    - execute(parameters: Dict) -> Any
    - get_descriptor() -> CapabilityDescriptor
    - validate() -> List[str]
    """
    
    def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the capability."""
        raise NotImplementedError()
    
    def get_descriptor(self) -> CapabilityDescriptor:
        """Get capability descriptor."""
        raise NotImplementedError()
    
    def validate(self) -> List[str]:
        """Validate capability contract."""
        raise NotImplementedError()


# =============================================================================
# PROVIDER API (PUBLIC)
# =============================================================================

class IProviderAPI:
    """
    Public Provider API.
    
    Methods:
    - execute(skill_name: str, input: Any) -> Any
    - supports_skill(skill_name: str) -> bool
    - get_descriptor() -> ProviderDescriptor
    - health_check() -> bool
    """
    
    def execute(self, skill_name: str, input: Any) -> Any:
        """Execute a skill."""
        raise NotImplementedError()
    
    def supports_skill(self, skill_name: str) -> bool:
        """Check if skill is supported."""
        raise NotImplementedError()
    
    def get_descriptor(self) -> ProviderDescriptor:
        """Get provider descriptor."""
        raise NotImplementedError()
    
    def health_check(self) -> bool:
        """Check provider health."""
        raise NotImplementedError()


# =============================================================================
# MISSION API (PUBLIC)
# =============================================================================

class IMissionAPI:
    """
    Public Mission API.
    
    Methods:
    - create(input: MissionInput) -> MissionOutput
    - get(mission_id: str) -> MissionOutput
    - cancel(mission_id: str) -> bool
    - list() -> List[MissionOutput]
    """
    
    def create(self, input: MissionInput) -> MissionOutput:
        """Create and execute a mission."""
        raise NotImplementedError()
    
    def get(self, mission_id: str) -> MissionOutput:
        """Get mission output."""
        raise NotImplementedError()
    
    def cancel(self, mission_id: str) -> bool:
        """Cancel a mission."""
        raise NotImplementedError()
    
    def list(self) -> List[MissionOutput]:
        """List all missions."""
        raise NotImplementedError()


# =============================================================================
# EXECUTION API (PUBLIC)
# =============================================================================

class IExecutionAPI:
    """
    Public Execution API.
    
    Methods:
    - execute(context: ExecutionContext) -> ExecutionResult
    - get(execution_id: str) -> ExecutionResult
    - list() -> List[ExecutionResult]
    """
    
    def execute(self, capability: str, inputs: Dict[str, Any]) -> ExecutionResult:
        """Execute a capability."""
        raise NotImplementedError()
    
    def get(self, execution_id: str) -> ExecutionResult:
        """Get execution result."""
        raise NotImplementedError()
    
    def list(self) -> List[ExecutionResult]:
        """List all executions."""
        raise NotImplementedError()


# =============================================================================
# KNOWLEDGE API (PUBLIC)
# =============================================================================

class IKnowledgeAPI:
    """
    Public Knowledge API.
    
    Methods:
    - read(collection: str, id: str) -> Any
    - write(collection: str, data: Dict) -> str
    - update(collection: str, id: str, data: Dict) -> bool
    - delete(collection: str, id: str) -> bool
    - search(collection: str, query: str) -> List[Any]
    """
    
    def read(self, collection: str, id: str) -> Optional[Any]:
        """Read data."""
        raise NotImplementedError()
    
    def write(self, collection: str, data: Dict[str, Any]) -> str:
        """Write data."""
        raise NotImplementedError()
    
    def update(self, collection: str, id: str, data: Dict[str, Any]) -> bool:
        """Update data."""
        raise NotImplementedError()
    
    def delete(self, collection: str, id: str) -> bool:
        """Delete data."""
        raise NotImplementedError()
    
    def search(self, collection: str, query: str) -> List[Any]:
        """Search data."""
        raise NotImplementedError()


# =============================================================================
# API SPECIFICATION SUMMARY
# =============================================================================

PUBLIC_APIS = {
    "IKernelAPI": IKernelAPI,
    "ICapabilityAPI": ICapabilityAPI,
    "IProviderAPI": IProviderAPI,
    "IMissionAPI": IMissionAPI,
    "IExecutionAPI": IExecutionAPI,
    "IKnowledgeAPI": IKnowledgeAPI,
}

API_VERSION = "1.0"
SPEC_VERSION = "1.0.0"

"""
API SPECIFICATION v1.0
=====================

Rules:
1. Lock Public API
2. Reject Breaking Changes
3. Reject Direct Internal Access
4. Future Development Must Use Public APIs Only

All public interfaces are defined above.
Internal access is prohibited.
"""
