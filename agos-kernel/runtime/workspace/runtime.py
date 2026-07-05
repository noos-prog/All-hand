"""Universal Workspace Runtime."""
import hashlib
import os
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    Workspace, WorkspaceStatus, WorkspaceType, WorkspaceResources,
    WorkspaceContext, WorkspaceSnapshot, WorkspaceTemplate
)


@dataclass
class WorkspaceConfig:
    """Workspace manager configuration."""
    base_path: str = "/tmp/agos-workspaces"
    default_resources: WorkspaceResources = field(default_factory=WorkspaceResources)
    auto_cleanup: bool = True
    max_workspaces: int = 100


class WorkspaceManager:
    """
    Workspace Manager - High-level interface for workspace management.
    """
    
    def __init__(self, config: Optional[WorkspaceConfig] = None):
        """Initialize workspace manager."""
        self.config = config or WorkspaceConfig()
        self._runtime = WorkspaceRuntime(base_path=self.config.base_path)
        self._pools: Dict[str, List[str]] = {}
    
    def allocate(self, name: str, workspace_type: WorkspaceType = WorkspaceType.MISSION,
                 mission_id: Optional[str] = None) -> Workspace:
        """Allocate a new workspace."""
        return self._runtime.create_workspace(
            name=name, workspace_type=workspace_type, mission_id=mission_id,
            resources=self.config.default_resources,
        )
    
    def release(self, workspace_id: str) -> bool:
        """Release a workspace."""
        return self._runtime.delete_workspace(workspace_id, force=True)
    
    def get(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID."""
        return self._runtime.get_workspace(workspace_id)
    
    def list_active(self) -> List[Workspace]:
        """List active workspaces."""
        return self._runtime.list_workspaces(status=WorkspaceStatus.RUNNING)
    
    def snapshot(self, workspace_id: str) -> Optional[WorkspaceSnapshot]:
        """Create workspace snapshot."""
        return self._runtime.snapshot_workspace(workspace_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        all_workspaces = self._runtime.list_workspaces()
        return {
            "total_workspaces": len(all_workspaces),
            "active_workspaces": len([w for w in all_workspaces if w.status == WorkspaceStatus.RUNNING]),
        }


class WorkspaceRuntime:
    """Universal Workspace Runtime."""
    
    def __init__(self, base_path: str = "/tmp/agos-workspaces"):
        """Initialize workspace runtime."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.workspaces: Dict[str, Workspace] = {}
        self.templates: Dict[str, WorkspaceTemplate] = {}
    
    def create_workspace(self, name: str, workspace_type: WorkspaceType = WorkspaceType.MISSION,
                        mission_id: Optional[str] = None,
                        resources: Optional[WorkspaceResources] = None,
                        template: Optional[WorkspaceTemplate] = None) -> Workspace:
        """Create a new workspace."""
        workspace_id = self._generate_id(name)
        ws_resources = resources or template.resources if template else WorkspaceResources()
        
        workspace = Workspace(
            id=workspace_id, name=name, mission_id=mission_id,
            workspace_type=workspace_type, status=WorkspaceStatus.CREATING,
            resources=ws_resources,
            context=WorkspaceContext(
                filesystem_root=str(self.base_path / workspace_id),
                working_directory=str(self.base_path / workspace_id),
            ),
        )
        
        if template:
            workspace.context.default_repositories = template.default_repositories
            workspace.context.policies = template.default_policies
            workspace.context.environment_vars = template.default_environment
        
        self._create_filesystem(workspace)
        workspace.status = WorkspaceStatus.READY
        workspace.created_at = datetime.now()
        workspace.updated_at = datetime.now()
        self.workspaces[workspace_id] = workspace
        return workspace
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID."""
        return self.workspaces.get(workspace_id)
    
    def list_workspaces(self, status: Optional[WorkspaceStatus] = None,
                        workspace_type: Optional[WorkspaceType] = None) -> List[Workspace]:
        """List workspaces."""
        workspaces = list(self.workspaces.values())
        if status:
            workspaces = [w for w in workspaces if w.status == status]
        if workspace_type:
            workspaces = [w for w in workspaces if w.workspace_type == workspace_type]
        return workspaces
    
    def delete_workspace(self, workspace_id: str, force: bool = False) -> bool:
        """Delete a workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return False
        if workspace.status == WorkspaceStatus.RUNNING and not force:
            return False
        
        workspace.status = WorkspaceStatus.TERMINATING
        self._delete_filesystem(workspace)
        workspace.status = WorkspaceStatus.TERMINATED
        del self.workspaces[workspace_id]
        return True
    
    def snapshot_workspace(self, workspace_id: str) -> Optional[WorkspaceSnapshot]:
        """Create a snapshot."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return None
        
        root = Path(workspace.context.filesystem_root)
        files = []
        if root.exists():
            for f in root.rglob("*"):
                if f.is_file():
                    files.append(str(f.relative_to(root)))
        
        return WorkspaceSnapshot(
            id=self._generate_id(f"snapshot-{workspace_id}"),
            workspace_id=workspace_id, created_at=datetime.now(),
            files=files, artifacts=[], state={"status": workspace.status.value},
            metadata={"workspace_name": workspace.name},
        )
    
    def pause_workspace(self, workspace_id: str) -> bool:
        """Pause a workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace or workspace.status != WorkspaceStatus.RUNNING:
            return False
        workspace.status = WorkspaceStatus.PAUSED
        workspace.updated_at = datetime.now()
        return True
    
    def resume_workspace(self, workspace_id: str) -> bool:
        """Resume a workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace or workspace.status != WorkspaceStatus.PAUSED:
            return False
        workspace.status = WorkspaceStatus.RUNNING
        workspace.updated_at = datetime.now()
        return True
    
    def create_template(self, name: str, description: str = "",
                       workspace_type: WorkspaceType = WorkspaceType.MISSION,
                       resources: Optional[WorkspaceResources] = None) -> WorkspaceTemplate:
        """Create a workspace template."""
        template = WorkspaceTemplate(
            id=self._generate_id(name), name=name, description=description,
            workspace_type=workspace_type, resources=resources or WorkspaceResources(),
        )
        self.templates[template.id] = template
        return template
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        return hashlib.md5(f"{name}-{uuid.uuid4().hex[:8]}".encode()).hexdigest()[:16]
    
    def _create_filesystem(self, workspace: Workspace) -> None:
        """Create workspace filesystem."""
        root = Path(workspace.context.filesystem_root)
        root.mkdir(parents=True, exist_ok=True)
        for d in ["workspace", "artifacts", "tmp", "cache"]:
            (root / d).mkdir(exist_ok=True)
    
    def _delete_filesystem(self, workspace: Workspace) -> None:
        """Delete workspace filesystem."""
        root = Path(workspace.context.filesystem_root)
        if root.exists() and root.parent == self.base_path:
            shutil.rmtree(root, ignore_errors=True)


# Global workspace manager instance
_workspace_manager: Optional[WorkspaceManager] = None


def get_workspace_manager() -> WorkspaceManager:
    """Get the global workspace manager instance."""
    global _workspace_manager
    if _workspace_manager is None:
        _workspace_manager = WorkspaceManager()
    return _workspace_manager
