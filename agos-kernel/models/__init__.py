"""Universal Object Model - Every runtime object inherits from the same system model."""
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ObjectState(Enum):
    """Object state."""
    CREATED = "created"
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class BaseObject:
    """
    Base class for all runtime objects.
    
    Common fields:
    - ID (immutable)
    - Version
    - Type
    - State
    - CreatedAt
    - UpdatedAt
    - Metadata
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    version: str = "1.0.0"
    type: str = ""
    state: ObjectState = ObjectState.CREATED
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "version": self.version,
            "type": self.type,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Mission(BaseObject):
    """Mission object."""
    name: str = ""
    description: str = ""
    capability: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.type = "mission"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description,
            "capability": self.capability,
            "parameters": self.parameters
        })
        return data


@dataclass
class Capability(BaseObject):
    """Capability object."""
    name: str = ""
    description: str = ""
    skills: List[str] = field(default_factory=list)
    priority: int = 1
    
    def __post_init__(self):
        self.type = "capability"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
            "priority": self.priority
        })
        return data


@dataclass
class Provider(BaseObject):
    """Provider object."""
    name: str = ""
    description: str = ""
    skills: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    
    def __post_init__(self):
        self.type = "provider"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description,
            "skills": self.skills
        })
        return data


@dataclass
class Skill(BaseObject):
    """Skill object."""
    name: str = ""
    description: str = ""
    input_type: str = ""
    output_type: str = ""
    
    def __post_init__(self):
        self.type = "skill"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "name": self.name,
            "description": self.description,
            "input_type": self.input_type,
            "output_type": self.output_type
        })
        return data


@dataclass
class Decision(BaseObject):
    """Decision object."""
    mission_id: str = ""
    capability: str = ""
    provider: str = ""
    reason: str = ""
    score: float = 0.0
    
    def __post_init__(self):
        self.type = "decision"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "mission_id": self.mission_id,
            "capability": self.capability,
            "provider": self.provider,
            "reason": self.reason,
            "score": self.score
        })
        return data


@dataclass
class Event(BaseObject):
    """Event object."""
    event_type: str = ""
    mission_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.type = "event"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "event_type": self.event_type,
            "mission_id": self.mission_id,
            "data": self.data
        })
        return data


@dataclass
class Knowledge(BaseObject):
    """Knowledge object."""
    name: str = ""
    content: Any = None
    source: str = ""
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.type = "knowledge"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "name": self.name,
            "content": self.content,
            "source": self.source,
            "tags": self.tags
        })
        return data


@dataclass
class Execution(BaseObject):
    """Execution object."""
    mission_id: str = ""
    capability: str = ""
    provider: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: int = 0
    result: Any = None
    error: Optional[str] = None
    
    def __post_init__(self):
        self.type = "execution"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "mission_id": self.mission_id,
            "capability": self.capability,
            "provider": self.provider,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "result": self.result,
            "error": self.error
        })
        return data


@dataclass
class Context(BaseObject):
    """Context object."""
    mission_id: str = ""
    execution_id: str = ""
    correlation_id: str = ""
    configuration: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.type = "context"
        if not self.execution_id:
            self.execution_id = str(uuid4())
        if not self.correlation_id:
            self.correlation_id = str(uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "mission_id": self.mission_id,
            "execution_id": self.execution_id,
            "correlation_id": self.correlation_id,
            "configuration": self.configuration,
            "constraints": self.constraints,
            "inputs": self.inputs
        })
        return data


@dataclass
class Result(BaseObject):
    """Result object."""
    success: bool = False
    data: Any = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    
    def __post_init__(self):
        self.type = "result"
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms
        })
        return data
