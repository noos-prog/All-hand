"""Execution Context - Every execution must receive an immutable execution context."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ExecutionState(Enum):
    """Execution state."""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class ExecutionContext:
    """
    Immutable execution context.
    
    Context includes:
    - Mission
    - Capability
    - Provider
    - Configuration
    - Constraints
    - Inputs
    - Execution ID
    - Correlation ID
    
    Rules:
    ❌ No hidden state
    ❌ No global variables
    ❌ No runtime mutation
    ✅ Immutable
    ✅ Serializable
    ✅ Traceable
    """
    # Core IDs
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    
    # Mission info
    mission_id: str = ""
    mission_name: str = ""
    capability: str = ""
    
    # Configuration
    configuration: tuple = field(default_factory=tuple)  # frozen=True requires immutable
    
    # Constraints
    constraints: tuple = field(default_factory=tuple)
    
    # Inputs
    inputs: tuple = field(default_factory=tuple)
    
    # Timing
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # State
    state: ExecutionState = ExecutionState.CREATED
    
    def with_state(self, new_state: ExecutionState) -> 'ExecutionContext':
        """Create new context with updated state (immutable)."""
        return ExecutionContext(
            execution_id=self.execution_id,
            correlation_id=self.correlation_id,
            mission_id=self.mission_id,
            mission_name=self.mission_name,
            capability=self.capability,
            configuration=self.configuration,
            constraints=self.constraints,
            inputs=self.inputs,
            created_at=self.created_at,
            state=new_state
        )
    
    def with_capability(self, capability: str) -> 'ExecutionContext':
        """Create new context with updated capability."""
        return ExecutionContext(
            execution_id=self.execution_id,
            correlation_id=self.correlation_id,
            mission_id=self.mission_id,
            mission_name=self.mission_name,
            capability=capability,
            configuration=self.configuration,
            constraints=self.constraints,
            inputs=self.inputs,
            created_at=self.created_at,
            state=self.state
        )
    
    def with_provider(self, provider: str) -> 'ExecutionContext':
        """Create new context with updated provider."""
        # Store provider in inputs
        new_inputs = dict(self.inputs) if self.inputs else {}
        new_inputs["provider"] = provider
        return ExecutionContext(
            execution_id=self.execution_id,
            correlation_id=self.correlation_id,
            mission_id=self.mission_id,
            mission_name=self.mission_name,
            capability=self.capability,
            configuration=self.configuration,
            constraints=self.constraints,
            inputs=tuple(sorted(new_inputs.items())),
            created_at=self.created_at,
            state=self.state
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "execution_id": self.execution_id,
            "correlation_id": self.correlation_id,
            "mission_id": self.mission_id,
            "mission_name": self.mission_name,
            "capability": self.capability,
            "configuration": dict(self.configuration) if self.configuration else {},
            "constraints": list(self.constraints) if self.constraints else [],
            "inputs": dict(self.inputs) if self.inputs else {},
            "created_at": self.created_at.isoformat(),
            "state": self.state.value
        }
    
    @classmethod
    def from_mission(
        cls,
        mission_id: str,
        mission_name: str,
        capability: str,
        inputs: Dict[str, Any] = None,
        configuration: Dict[str, Any] = None,
        constraints: List[str] = None
    ) -> 'ExecutionContext':
        """Create context from mission."""
        return cls(
            mission_id=mission_id,
            mission_name=mission_name,
            capability=capability,
            inputs=tuple(sorted((inputs or {}).items())),
            configuration=tuple(sorted((configuration or {}).items())),
            constraints=tuple(constraints or [])
        )
    
    def get_input(self, key: str, default: Any = None) -> Any:
        """Get input value."""
        if not self.inputs:
            return default
        inputs_dict = dict(self.inputs)
        return inputs_dict.get(key, default)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        if not self.configuration:
            return default
        config_dict = dict(self.configuration)
        return config_dict.get(key, default)


class ExecutionContextBuilder:
    """Builder for execution context."""
    
    def __init__(self):
        self._execution_id: Optional[str] = None
        self._correlation_id: Optional[str] = None
        self._mission_id: str = ""
        self._mission_name: str = ""
        self._capability: str = ""
        self._configuration: Dict[str, Any] = {}
        self._constraints: List[str] = []
        self._inputs: Dict[str, Any] = {}
    
    def with_execution_id(self, execution_id: str) -> 'ExecutionContextBuilder':
        """Set execution ID."""
        self._execution_id = execution_id
        return self
    
    def with_correlation_id(self, correlation_id: str) -> 'ExecutionContextBuilder':
        """Set correlation ID."""
        self._correlation_id = correlation_id
        return self
    
    def with_mission(self, mission_id: str, mission_name: str) -> 'ExecutionContextBuilder':
        """Set mission info."""
        self._mission_id = mission_id
        self._mission_name = mission_name
        return self
    
    def with_capability(self, capability: str) -> 'ExecutionContextBuilder':
        """Set capability."""
        self._capability = capability
        return self
    
    def with_configuration(self, configuration: Dict[str, Any]) -> 'ExecutionContextBuilder':
        """Set configuration."""
        self._configuration = configuration
        return self
    
    def with_constraints(self, constraints: List[str]) -> 'ExecutionContextBuilder':
        """Set constraints."""
        self._constraints = constraints
        return self
    
    def with_inputs(self, inputs: Dict[str, Any]) -> 'ExecutionContextBuilder':
        """Set inputs."""
        self._inputs = inputs
        return self
    
    def build(self) -> ExecutionContext:
        """Build the context."""
        return ExecutionContext(
            execution_id=self._execution_id or str(uuid4()),
            correlation_id=self._correlation_id or str(uuid4()),
            mission_id=self._mission_id,
            mission_name=self._mission_name,
            capability=self._capability,
            configuration=tuple(sorted(self._configuration.items())),
            constraints=tuple(self._constraints),
            inputs=tuple(sorted(self._inputs.items()))
        )


class ContextRegistry:
    """Registry for execution contexts."""
    
    def __init__(self):
        self._contexts: Dict[str, ExecutionContext] = {}
    
    def register(self, context: ExecutionContext) -> None:
        """Register a context."""
        self._contexts[context.execution_id] = context
    
    def get(self, execution_id: str) -> Optional[ExecutionContext]:
        """Get a context."""
        return self._contexts.get(execution_id)
    
    def remove(self, execution_id: str) -> None:
        """Remove a context."""
        if execution_id in self._contexts:
            del self._contexts[execution_id]
    
    def list_all(self) -> List[ExecutionContext]:
        """List all contexts."""
        return list(self._contexts.values())
