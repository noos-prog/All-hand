"""
AGOS Cloud Workspace
====================

Persistent, isolated cloud workspaces that hold the working state of
agent civilizations: source trees, artifacts, execution snapshots and
per-workspace ACLs.

The public surface is intentionally small so higher layers (kernel,
orchestration, civilization) never depend on storage internals.
"""

from .runtime import Workspace, WorkspaceRuntime, WorkspaceStatus, WorkspaceType
from .snapshot import Snapshot, SnapshotStore
from .permissions import ACL, Permission, PermissionDenied, Role
from .telemetry import TelemetryCounter, WorkspaceTelemetry
from .service import UniversalCloudWorkspace

__all__ = [
    "Workspace",
    "WorkspaceRuntime",
    "WorkspaceStatus",
    "WorkspaceType",
    "Snapshot",
    "SnapshotStore",
    "ACL",
    "Permission",
    "PermissionDenied",
    "Role",
    "TelemetryCounter",
    "WorkspaceTelemetry",
    "UniversalCloudWorkspace",
]

__version__ = "3.0.0"
