"""Universal Artifact Runtime - Data Models."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ArtifactType(Enum):
    """Artifact type."""
    FILE = "file"
    DIRECTORY = "directory"
    REPOSITORY = "repository"
    ARCHIVE = "archive"
    REPORT = "report"
    PLAN = "plan"
    KNOWLEDGE = "knowledge"
    DNA = "dna"
    GRAPH = "graph"
    BENCHMARK = "benchmark"
    LOG = "log"
    PACKAGE = "package"
    IMAGE = "image"
    CONTAINER = "container"
    EXECUTABLE = "executable"
    MODEL = "model"
    DATASET = "dataset"
    CONFIG = "config"


class ArtifactStatus(Enum):
    """Artifact status."""
    CREATED = "created"
    VALIDATING = "validating"
    VALID = "valid"
    INVALID = "invalid"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass
class ArtifactVersion:
    """Artifact version."""
    version: str
    created_at: datetime
    created_by: str
    changelog: str = ""
    size_bytes: int = 0
    checksum: str = ""


@dataclass
class ArtifactMetadata:
    """Artifact metadata."""
    name: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    license: str = ""
    source_repository: str = ""
    source_commit: str = ""
    dependencies: List[str] = field(default_factory=list)


@dataclass
class Artifact:
    """Universal Artifact."""
    id: str
    name: str
    artifact_type: ArtifactType
    
    # Versions
    current_version: str = "1.0.0"
    versions: List[ArtifactVersion] = field(default_factory=list)
    
    # Status
    status: ArtifactStatus = ArtifactStatus.CREATED
    
    # Content
    path: str = ""
    size_bytes: int = 0
    checksum: str = ""
    mime_type: str = ""
    
    # Metadata
    metadata: ArtifactMetadata = field(default_factory=ArtifactMetadata)
    
    # Relationships
    workspace_id: Optional[str] = None
    mission_id: Optional[str] = None
    execution_id: Optional[str] = None
    parent_id: Optional[str] = None
    
    # Lifecycle
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    
    # Validation
    validation_errors: List[str] = field(default_factory=list)
    validation_warnings: List[str] = field(default_factory=list)
    
    # Storage
    storage_backend: str = "local"
    storage_path: str = ""
    
    # Diff
    diff_enabled: bool = True
    previous_version: Optional[str] = None
    
    # Metadata
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.artifact_type.value,
            "status": self.status.value,
            "version": self.current_version,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat(),
        }
