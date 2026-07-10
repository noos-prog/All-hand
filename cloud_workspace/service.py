"""High-level facade combining runtime, snapshots, ACLs and telemetry."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional

from .permissions import ACL, ACLStore, Permission, Role
from .runtime import Workspace, WorkspaceRuntime, WorkspaceType
from .snapshot import Snapshot, SnapshotStore
from .telemetry import WorkspaceTelemetry


class UniversalCloudWorkspace:
    """One-stop facade for building agent-driven workspaces."""

    def __init__(self, root: str | os.PathLike[str] = "./.agos/workspaces") -> None:
        self._root = Path(root)
        self.runtime = WorkspaceRuntime(self._root)
        self.snapshots = SnapshotStore(self.runtime)
        self.acls = ACLStore(self._root)
        self.telemetry = WorkspaceTelemetry()

    # ---------------------------------------------------------------- create
    def create_workspace(
        self,
        name: str,
        ws_type: WorkspaceType = WorkspaceType.BLANK,
        *,
        owner: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> Workspace:
        ws = self.runtime.create(name, ws_type, owner, labels=labels)
        self.acls.save(ACL(workspace_id=ws.workspace_id, owner=owner))
        self.telemetry.incr(ws.workspace_id, "created")
        return ws

    # ------------------------------------------------------------ operations
    def snapshot(self, workspace_id: str, principal: str, *, note: str = "") -> Snapshot:
        self._require(workspace_id, principal, Permission.SNAPSHOT)
        snap = self.snapshots.create(workspace_id, note=note)
        self.telemetry.incr(workspace_id, "snapshots")
        return snap

    def restore(self, workspace_id: str, snapshot_id: str, principal: str) -> None:
        self._require(workspace_id, principal, Permission.RESTORE)
        self.snapshots.restore(workspace_id, snapshot_id)
        self.telemetry.incr(workspace_id, "restores")

    def share(self, workspace_id: str, principal: str, target: str, role: Role) -> None:
        self._require(workspace_id, principal, Permission.SHARE)
        acl = self.acls.load(workspace_id, owner=self.runtime.get(workspace_id).owner)
        acl.grant(target, role)
        self.acls.save(acl)
        self.telemetry.incr(workspace_id, "shares")

    def clone(self, workspace_id: str, new_name: str, principal: str) -> Workspace:
        self._require(workspace_id, principal, Permission.READ)
        new = self.runtime.clone(workspace_id, new_name, owner=principal)
        self.acls.save(ACL(workspace_id=new.workspace_id, owner=principal))
        self.telemetry.incr(workspace_id, "clones")
        return new

    def destroy(self, workspace_id: str, principal: str) -> None:
        self._require(workspace_id, principal, Permission.ADMIN)
        self.runtime.destroy(workspace_id)

    def list_workspaces(self, *, owner: Optional[str] = None) -> List[Workspace]:
        return self.runtime.list(owner=owner)

    # ----------------------------------------------------------------- meta
    def statistics(self) -> Dict[str, object]:
        workspaces = self.runtime.list()
        return {
            "version": "3.0.0",
            "root": str(self._root),
            "total": len(workspaces),
            "by_status": _bucket(workspaces, lambda w: w.status.value),
            "by_type": _bucket(workspaces, lambda w: w.type.value),
            "telemetry": self.telemetry.all(),
        }

    # ---------------------------------------------------------------- guards
    def _require(self, workspace_id: str, principal: str, permission: Permission) -> None:
        ws = self.runtime.get(workspace_id)
        acl = self.acls.load(workspace_id, owner=ws.owner)
        acl.require(principal, permission)


def _bucket(items, key) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for it in items:
        k = key(it)
        out[k] = out.get(k, 0) + 1
    return out
