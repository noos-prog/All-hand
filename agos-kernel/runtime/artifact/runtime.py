"""Universal Artifact Runtime."""
import hashlib
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    Artifact, ArtifactType, ArtifactStatus, ArtifactVersion, ArtifactMetadata
)


class ArtifactRuntime:
    """Universal Artifact Runtime."""
    
    def __init__(self, storage_path: str = "/tmp/agos-artifacts"):
        """Initialize artifact runtime."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.artifacts: Dict[str, Artifact] = {}
    
    def create_artifact(
        self,
        name: str,
        artifact_type: ArtifactType,
        path: str = "",
        workspace_id: Optional[str] = None,
        mission_id: Optional[str] = None,
        metadata: Optional[ArtifactMetadata] = None,
    ) -> Artifact:
        """Create a new artifact."""
        artifact_id = self._generate_id(name)
        
        artifact = Artifact(
            id=artifact_id,
            name=name,
            artifact_type=artifact_type,
            path=path,
            workspace_id=workspace_id,
            mission_id=mission_id,
            metadata=metadata or ArtifactMetadata(name=name),
            versions=[ArtifactVersion(
                version="1.0.0",
                created_at=datetime.now(),
                created_by="system",
            )],
        )
        
        # Calculate size and checksum
        if path and Path(path).exists():
            artifact.size_bytes = Path(path).stat().st_size
            artifact.checksum = self._calculate_checksum(path)
            artifact.storage_path = str(self.storage_path / artifact_id)
        
        # Store artifact
        self.artifacts[artifact_id] = artifact
        return artifact
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID."""
        return self.artifacts.get(artifact_id)
    
    def list_artifacts(
        self,
        artifact_type: Optional[ArtifactType] = None,
        status: Optional[ArtifactStatus] = None,
        workspace_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Artifact]:
        """List artifacts with optional filtering."""
        artifacts = list(self.artifacts.values())
        
        if artifact_type:
            artifacts = [a for a in artifacts if a.artifact_type == artifact_type]
        
        if status:
            artifacts = [a for a in artifacts if a.status == status]
        
        if workspace_id:
            artifacts = [a for a in artifacts if a.workspace_id == workspace_id]
        
        if tags:
            artifacts = [a for a in artifacts if any(t in a.metadata.tags for t in tags)]
        
        return artifacts
    
    def update_artifact(self, artifact_id: str, **kwargs) -> Optional[Artifact]:
        """Update artifact attributes."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return None
        
        for key, value in kwargs.items():
            if hasattr(artifact, key):
                setattr(artifact, key, value)
        
        artifact.updated_at = datetime.now()
        return artifact
    
    def version_artifact(self, artifact_id: str, version: str, changelog: str = "") -> Optional[Artifact]:
        """Create a new version of an artifact."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return None
        
        # Store previous version info
        artifact.previous_version = artifact.current_version
        
        # Create new version
        artifact.versions.append(ArtifactVersion(
            version=version,
            created_at=datetime.now(),
            created_by="system",
            changelog=changelog,
        ))
        artifact.current_version = version
        artifact.updated_at = datetime.now()
        
        return artifact
    
    def validate_artifact(self, artifact_id: str) -> bool:
        """Validate an artifact."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return False
        
        artifact.validation_errors = []
        artifact.validation_warnings = []
        
        # Check if path exists
        if artifact.path:
            if not Path(artifact.path).exists():
                artifact.validation_errors.append(f"Path does not exist: {artifact.path}")
        
        # Check size
        if artifact.size_bytes == 0:
            artifact.validation_warnings.append("Artifact has zero size")
        
        # Set status
        if artifact.validation_errors:
            artifact.status = ArtifactStatus.INVALID
            return False
        
        artifact.status = ArtifactStatus.VALID
        return True
    
    def publish_artifact(self, artifact_id: str) -> bool:
        """Publish an artifact."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return False
        
        # Validate first
        if not self.validate_artifact(artifact_id):
            return False
        
        artifact.status = ArtifactStatus.PUBLISHED
        artifact.published_at = datetime.now()
        artifact.updated_at = datetime.now()
        return True
    
    def delete_artifact(self, artifact_id: str, soft: bool = True) -> bool:
        """Delete an artifact."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return False
        
        if soft:
            artifact.status = ArtifactStatus.DELETED
        else:
            # Hard delete
            if artifact.storage_path and Path(artifact.storage_path).exists():
                shutil.rmtree(artifact.storage_path, ignore_errors=True)
            del self.artifacts[artifact_id]
        
        return True
    
    def archive_artifact(self, artifact_id: str) -> bool:
        """Archive an artifact."""
        artifact = self.artifacts.get(artifact_id)
        if not artifact:
            return False
        
        artifact.status = ArtifactStatus.ARCHIVED
        artifact.updated_at = datetime.now()
        return True
    
    def search_artifacts(self, query: str) -> List[Artifact]:
        """Search artifacts by name or tags."""
        query_lower = query.lower()
        results = []
        
        for artifact in self.artifacts.values():
            if query_lower in artifact.name.lower():
                results.append(artifact)
            elif any(query_lower in tag.lower() for tag in artifact.metadata.tags):
                results.append(artifact)
            elif query_lower in artifact.metadata.description.lower():
                results.append(artifact)
        
        return results
    
    def diff_artifacts(self, artifact_id1: str, artifact_id2: str) -> Dict[str, Any]:
        """Compare two artifacts."""
        a1 = self.artifacts.get(artifact_id1)
        a2 = self.artifacts.get(artifact_id2)
        
        if not a1 or not a2:
            return {"error": "One or both artifacts not found"}
        
        return {
            "artifact1": a1.to_dict(),
            "artifact2": a2.to_dict(),
            "differences": {
                "size_bytes": a2.size_bytes - a1.size_bytes,
                "version": f"{a1.current_version} -> {a2.current_version}",
                "type_same": a1.artifact_type == a2.artifact_type,
            },
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
    
    def _calculate_checksum(self, path: str) -> str:
        """Calculate file checksum."""
        if not Path(path).exists():
            return ""
        
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
