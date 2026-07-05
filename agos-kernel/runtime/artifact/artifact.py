"""
AGOS Artifact Manager
===================

Manages artifacts - files, code, documents, and other outputs.
"""

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ArtifactType(Enum):
    """Artifact type."""
    FILE = "file"
    CODE = "code"
    DOCUMENT = "document"
    IMAGE = "image"
    MODEL = "model"
    DATA = "data"
    ARCHIVE = "archive"
    OTHER = "other"


class ArtifactStatus(Enum):
    """Artifact status."""
    CREATED = "created"
    VALIDATED = "validated"
    STORED = "stored"
    ARCHIVED = "archived"
    DELETED = "deleted"


@dataclass
class Artifact:
    """An artifact."""
    id: str
    name: str
    artifact_type: ArtifactType
    path: str
    size: int = 0
    checksum: str = ""
    status: ArtifactStatus = ArtifactStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    owner_id: Optional[str] = None
    parent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.artifact_type.value,
            "path": self.path,
            "size": self.size,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }


class ArtifactManager:
    """
    Artifact Manager.
    
    Manages artifacts throughout their lifecycle.
    
    Usage:
        manager = ArtifactManager()
        
        artifact = manager.create_artifact(
            name="report.pdf",
            artifact_type=ArtifactType.DOCUMENT,
            path="/workspace/reports/report.pdf",
        )
        
        artifacts = manager.list_artifacts(tags=["important"])
    """
    
    def __init__(self, storage_path: str = "/tmp/agos-artifacts"):
        """Initialize artifact manager."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._artifacts: Dict[str, Artifact] = {}
    
    def create_artifact(
        self,
        name: str,
        artifact_type: ArtifactType,
        path: str,
        size: int = 0,
        checksum: str = "",
        owner_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Artifact:
        """Create an artifact."""
        # Calculate checksum if not provided
        if not checksum and Path(path).exists():
            with open(path, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
        
        # Get size if not provided
        if size == 0 and Path(path).exists():
            size = Path(path).stat().st_size
        
        artifact = Artifact(
            id=f"art-{uuid.uuid4().hex[:8]}",
            name=name,
            artifact_type=artifact_type,
            path=path,
            size=size,
            checksum=checksum,
            owner_id=owner_id,
            parent_id=parent_id,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        self._artifacts[artifact.id] = artifact
        return artifact
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get an artifact by ID."""
        return self._artifacts.get(artifact_id)
    
    def list_artifacts(
        self,
        artifact_type: Optional[ArtifactType] = None,
        status: Optional[ArtifactStatus] = None,
        owner_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[Artifact]:
        """List artifacts with filtering."""
        artifacts = list(self._artifacts.values())
        
        if artifact_type:
            artifacts = [a for a in artifacts if a.artifact_type == artifact_type]
        
        if status:
            artifacts = [a for a in artifacts if a.status == status]
        
        if owner_id:
            artifacts = [a for a in artifacts if a.owner_id == owner_id]
        
        if tags:
            artifacts = [
                a for a in artifacts
                if any(tag in a.tags for tag in tags)
            ]
        
        # Sort by creation date, newest first
        artifacts.sort(key=lambda a: a.created_at, reverse=True)
        
        return artifacts[:limit]
    
    def update_artifact(
        self,
        artifact_id: str,
        status: Optional[ArtifactStatus] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Artifact]:
        """Update an artifact."""
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return None
        
        if status:
            artifact.status = status
        
        if tags:
            artifact.tags.extend([t for t in tags if t not in artifact.tags])
        
        if metadata:
            artifact.metadata.update(metadata)
        
        artifact.updated_at = datetime.now()
        return artifact
    
    def delete_artifact(self, artifact_id: str) -> bool:
        """Delete an artifact."""
        if artifact_id in self._artifacts:
            artifact = self._artifacts[artifact_id]
            artifact.status = ArtifactStatus.DELETED
            return True
        return False
    
    def validate_artifact(self, artifact_id: str) -> bool:
        """Validate an artifact."""
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            return False
        
        # Check if file exists
        if not Path(artifact.path).exists():
            return False
        
        # Verify checksum
        if artifact.checksum:
            with open(artifact.path, 'rb') as f:
                actual_checksum = hashlib.md5(f.read()).hexdigest()
            if actual_checksum != artifact.checksum:
                return False
        
        artifact.status = ArtifactStatus.VALIDATED
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        total_size = sum(a.size for a in self._artifacts.values())
        
        return {
            "total_artifacts": len(self._artifacts),
            "total_size_bytes": total_size,
            "by_type": {
                atype.value: sum(1 for a in self._artifacts.values() if a.artifact_type == atype)
                for atype in ArtifactType
            },
            "by_status": {
                status.value: sum(1 for a in self._artifacts.values() if a.status == status)
                for status in ArtifactStatus
            },
        }


# Global instance
_artifact_manager: Optional[ArtifactManager] = None


def get_artifact_manager() -> ArtifactManager:
    """Get the global artifact manager."""
    global _artifact_manager
    if _artifact_manager is None:
        _artifact_manager = ArtifactManager()
    return _artifact_manager
