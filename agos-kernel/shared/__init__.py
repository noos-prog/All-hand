"""Shared types for AGOS Kernel."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ResultStatus(Enum):
    """Result status."""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


@dataclass
class Result:
    """Base result type."""
    status: ResultStatus
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def is_success(self) -> bool:
        return self.status == ResultStatus.SUCCESS
    
    @property
    def is_failure(self) -> bool:
        return self.status == ResultStatus.FAILURE


@dataclass
class Metadata:
    """Metadata for any component."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    version: str = "0.1.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


class SkillInput:
    """Base class for skill inputs."""
    pass


class SkillOutput:
    """Base class for skill outputs."""
    pass
