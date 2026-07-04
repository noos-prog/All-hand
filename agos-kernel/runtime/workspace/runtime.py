"""Universal Workspace Runtime."""
import hashlib
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    Workspace, WorkspaceStatus, WorkspaceType, WorkspaceResources,
    WorkspaceContext, WorkspaceSnapshot, WorkspaceTemplate
)


class WorkspaceRuntime:
    """Universal Workspace Runtime."""
    
    def __init__(self, base_path: str = "/tmp/agos-workspaces"):
        """Initialize workspace runtime."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.workspaces: Dict[str, Workspace] = {}
        self.templates: Dict[str, WorkspaceTemplate] = {}
    
    def create_workspace(
        self,
        name: str,
        workspace_type: WorkspaceType = WorkspaceType.MISSION,
        mission_id: Optional[str] = None,
        resources: Optional[WorkspaceResources] = None,
        template: Optional[WorkspaceTemplate] = None,
    ) -> Workspace:
        """Create a new workspace."""
        workspace_id = self._generate_id(name)
        
        # Determine resources
        if resources:
            ws_resources = resources
        elif template:
            ws_resources = template.resources
        else:
            ws_resources = WorkspaceResources()
        
        # Create workspace object
        workspace = Workspace(
            id=workspace_id,
            name=name,
            mission_id=mission_id,
            workspace_type=workspace_type,
            status=WorkspaceStatus.CREATING,
            resources=ws_resources,
            context=WorkspaceContext(
                filesystem_root=str(self.base_path / workspace_id),
                working_directory=str(self.base_path / workspace_id),
            ),
        )
        
        # Apply template context if provided
        if template:
            workspace.context.default_repositories = template.default_repositories
            workspace.context.policies = template.default_policies
            workspace.context.environment_vars = template.default_environment
        
        # Create filesystem
        self._create_filesystem(workspace)
        
        # Update status
        workspace.status = WorkspaceStatus.READY
        workspace.created_at = datetime.now()
        workspace.updated_at = datetime.now()
        
        # Store workspace
        self.workspaces[workspace_id] = workspace
        
        return workspace
    
    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace by ID."""
        return self.workspaces.get(workspace_id)
    
    def list_workspaces(
        self,
        status: Optional[WorkspaceStatus] = None,
        workspace_type: Optional[WorkspaceType] = None,
    ) -> List[Workspace]:
        """List workspaces with optional filtering."""
        workspaces = list(self.workspaces.values())
        
        if status:
            workspaces = [w for w in workspaces if w.status == status]
        
        if workspace_type:
            workspaces = [w for w in workspaces if w.workspace_type == workspace_type]
        
        return workspaces
    
    def update_workspace(self, workspace_id: str, **kwargs) -> Optional[Workspace]:
        """Update workspace attributes."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return None
        
        for key, value in kwargs.items():
            if hasattr(workspace, key):
                setattr(workspace, key, value)
        
        workspace.updated_at = datetime.now()
        return workspace
    
    def delete_workspace(self, workspace_id: str, force: bool = False) -> bool:
        """Delete a workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return False
        
        if workspace.status == WorkspaceStatus.RUNNING and not force:
            return False
        
        # Update status
        workspace.status = WorkspaceStatus.TERMINATING
        
        # Delete filesystem
        self._delete_filesystem(workspace)
        
        # Update status
        workspace.status = WorkspaceStatus.TERMINATED
        
        # Remove from registry
        del self.workspaces[workspace_id]
        
        return True
    
    def snapshot_workspace(self, workspace_id: str) -> Optional[WorkspaceSnapshot]:
        """Create a snapshot of workspace state."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return None
        
        workspace.status = WorkspaceStatus.SNAPSHOTTING
        workspace.updated_at = datetime.now()
        
        # Collect files
        root = Path(workspace.context.filesystem_root)
        files = []
        if root.exists():
            for f in root.rglob("*"):
                if f.is_file():
                    files.append(str(f.relative_to(root)))
        
        # Create snapshot
        snapshot = WorkspaceSnapshot(
            id=self._generate_id(f"snapshot-{workspace_id}"),
            workspace_id=workspace_id,
            created_at=datetime.now(),
            files=files,
            artifacts=[],  # Would collect artifacts
            state={
                "status": workspace.status.value,
                "context": {
                    "environment_vars": workspace.context.environment_vars,
                    "repositories": workspace.context.repositories,
                },
            },
            metadata={
                "workspace_name": workspace.name,
                "workspace_type": workspace.workspace_type.value,
            },
        )
        
        workspace.status = WorkspaceStatus.READY
        return snapshot
    
    def restore_workspace(self, workspace_id: str, snapshot: WorkspaceSnapshot) -> bool:
        """Restore workspace from snapshot."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace:
            return False
        
        workspace.status = WorkspaceStatus.RESTORING
        workspace.updated_at = datetime.now()
        
        # Restore state
        if "status" in snapshot.state:
            workspace.status = WorkspaceStatus(snapshot.state["status"])
        
        if "context" in snapshot.state:
            ctx = snapshot.state["context"]
            if "environment_vars" in ctx:
                workspace.context.environment_vars = ctx["environment_vars"]
            if "repositories" in ctx:
                workspace.context.repositories = ctx["repositories"]
        
        workspace.status = WorkspaceStatus.READY
        return True
    
    def clone_workspace(
        self,
        source_workspace_id: str,
        new_name: str,
        clone_state: bool = True,
    ) -> Optional[Workspace]:
        """Clone an existing workspace."""
        source = self.workspaces.get(source_workspace_id)
        if not source:
            return None
        
        # Create new workspace
        clone = self.create_workspace(
            name=new_name,
            workspace_type=source.workspace_type,
            mission_id=source.mission_id,
            resources=source.resources,
        )
        
        clone.parent_id = source_workspace_id
        
        # Clone filesystem if requested
        if clone_state and Path(source.context.filesystem_root).exists():
            src = Path(source.context.filesystem_root)
            dst = Path(clone.context.filesystem_root)
            for item in src.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(src)
                    dst_file = dst / rel_path
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dst_file)
        
        return clone
    
    def pause_workspace(self, workspace_id: str) -> bool:
        """Pause a running workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace or workspace.status != WorkspaceStatus.RUNNING:
            return False
        
        workspace.status = WorkspaceStatus.PAUSED
        workspace.updated_at = datetime.now()
        return True
    
    def resume_workspace(self, workspace_id: str) -> bool:
        """Resume a paused workspace."""
        workspace = self.workspaces.get(workspace_id)
        if not workspace or workspace.status != WorkspaceStatus.PAUSED:
            return False
        
        workspace.status = WorkspaceStatus.RUNNING
        workspace.updated_at = datetime.now()
        return True
    
    def update_telemetry(self, workspace_id: str, metrics: Dict[str, Any]) -> None:
        """Update workspace telemetry."""
        workspace = self.workspaces.get(workspace_id)
        if workspace:
            workspace.telemetry.update(metrics)
            workspace.updated_at = datetime.now()
    
    # Template management
    def create_template(
        self,
        name: str,
        description: str = "",
        workspace_type: WorkspaceType = WorkspaceType.MISSION,
        resources: Optional[WorkspaceResources] = None,
    ) -> WorkspaceTemplate:
        """Create a workspace template."""
        template_id = self._generate_id(name)
        
        template = WorkspaceTemplate(
            id=template_id,
            name=name,
            description=description,
            workspace_type=workspace_type,
            resources=resources or WorkspaceResources(),
        )
        
        self.templates[template_id] = template
        return template
    
    def get_template(self, template_id: str) -> Optional[WorkspaceTemplate]:
        """Get template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[WorkspaceTemplate]:
        """List all templates."""
        return list(self.templates.values())
    
    # Internal methods
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
    
    def _create_filesystem(self, workspace: Workspace) -> None:
        """Create workspace filesystem."""
        root = Path(workspace.context.filesystem_root)
        root.mkdir(parents=True, exist_ok=True)
        
        # Create standard directories
        (root / "workspace").mkdir(exist_ok=True)
        (root / "artifacts").mkdir(exist_ok=True)
        (root / "tmp").mkdir(exist_ok=True)
        (root / "cache").mkdir(exist_ok=True)
    
    def _delete_filesystem(self, workspace: Workspace) -> None:
        """Delete workspace filesystem."""
        root = Path(workspace.context.filesystem_root)
        if root.exists() and root.parent == self.base_path:
            shutil.rmtree(root, ignore_errors=True)
