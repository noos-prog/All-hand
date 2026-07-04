"""Universal State Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class StateType(Enum):
    """State type."""
    MISSION = "mission"
    EXECUTION = "execution"
    WORKSPACE = "workspace"
    PROVIDER = "provider"
    CAPABILITY = "capability"
    WORKFLOW = "workflow"
    ARTIFACT = "artifact"
    KNOWLEDGE = "knowledge"


class StateStatus(Enum):
    """State status."""
    CREATED = "created"
    ACTIVE = "active"
    PERSISTED = "persisted"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass
class StateTransition:
    """State transition record."""
    id: str
    from_state: str
    to_state: str
    timestamp: datetime
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateSnapshot:
    """State snapshot."""
    id: str
    state_id: str
    created_at: datetime
    data: Dict[str, Any]
    checksum: str = ""


@dataclass
class State:
    """Universal State."""
    id: str
    name: str
    state_type: StateType
    
    # Content
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Status
    status: StateStatus = StateStatus.CREATED
    
    # History
    transitions: List[StateTransition] = field(default_factory=list)
    snapshots: List[StateSnapshot] = field(default_factory=list)
    
    # Versioning
    version: int = 1
    previous_versions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Relationships
    mission_id: Optional[str] = None
    execution_id: Optional[str] = None
    workspace_id: Optional[str] = None
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Validation
    schema: Optional[Dict[str, Any]] = None
    validation_errors: List[str] = field(default_factory=list)
    
    # Diff
    diff_enabled: bool = True
    last_diff: Optional[Dict[str, Any]] = None
    
    def transition_to(self, new_state: str, reason: str = "", metadata: Dict[str, Any] = None) -> StateTransition:
        """Transition to a new state."""
        transition = StateTransition(
            id=f"{self.id}-trans-{len(self.transitions)}",
            from_state=self.status.value,
            to_state=new_state,
            timestamp=datetime.now(),
            reason=reason,
            metadata=metadata or {},
        )
        self.transitions.append(transition)
        self.status = StateStatus(new_state)
        self.updated_at = datetime.now()
        return transition
    
    def create_snapshot(self, data: Dict[str, Any]) -> StateSnapshot:
        """Create a snapshot of current state."""
        snapshot = StateSnapshot(
            id=f"{self.id}-snap-{len(self.snapshots)}",
            state_id=self.id,
            created_at=datetime.now(),
            data=data.copy(),
        )
        self.snapshots.append(snapshot)
        return snapshot
    
    def validate(self) -> bool:
        """Validate state against schema."""
        if not self.schema:
            return True
        
        self.validation_errors = []
        # Simple validation - would use jsonschema in production
        for key, spec in self.schema.items():
            if spec.get("required") and key not in self.data:
                self.validation_errors.append(f"Missing required field: {key}")
        
        return len(self.validation_errors) == 0
