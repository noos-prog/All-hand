"""ACL and role-based permission checks for workspaces."""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Set


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    SNAPSHOT = "snapshot"
    RESTORE = "restore"
    SHARE = "share"
    ADMIN = "admin"


class Role(str, Enum):
    VIEWER = "viewer"
    CONTRIBUTOR = "contributor"
    OPERATOR = "operator"
    OWNER = "owner"


_ROLE_MATRIX: Dict[Role, Set[Permission]] = {
    Role.VIEWER: {Permission.READ},
    Role.CONTRIBUTOR: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
    Role.OPERATOR: {
        Permission.READ, Permission.WRITE, Permission.EXECUTE,
        Permission.SNAPSHOT, Permission.RESTORE,
    },
    Role.OWNER: set(Permission),
}


class PermissionDenied(PermissionError):
    """Raised when a principal lacks the requested permission."""


@dataclass
class ACL:
    workspace_id: str
    owner: str
    grants: Dict[str, Role] = field(default_factory=dict)

    def role_for(self, principal: str) -> Role:
        if principal == self.owner:
            return Role.OWNER
        return self.grants.get(principal, Role.VIEWER) if principal in self.grants else Role.VIEWER

    def grant(self, principal: str, role: Role) -> None:
        if principal == self.owner:
            return
        self.grants[principal] = role

    def revoke(self, principal: str) -> None:
        self.grants.pop(principal, None)

    def can(self, principal: str, permission: Permission) -> bool:
        if principal not in self.grants and principal != self.owner:
            return permission is Permission.READ and False
        return permission in _ROLE_MATRIX[self.role_for(principal)]

    def require(self, principal: str, permission: Permission) -> None:
        if not self.can(principal, permission):
            raise PermissionDenied(
                f"{principal!r} lacks {permission.value} on workspace {self.workspace_id}"
            )

    # -------------------------------------------------------------- persistence
    def to_dict(self) -> Dict[str, object]:
        return {
            "workspace_id": self.workspace_id,
            "owner": self.owner,
            "grants": {p: r.value for p, r in self.grants.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "ACL":
        return cls(
            workspace_id=str(data["workspace_id"]),
            owner=str(data["owner"]),
            grants={p: Role(r) for p, r in dict(data.get("grants", {})).items()},
        )


class ACLStore:
    """Per-workspace ACL persistence on disk."""

    FILE = "acl.json"

    def __init__(self, root: Path) -> None:
        self._root = Path(root)
        self._lock = threading.RLock()

    def _path(self, workspace_id: str) -> Path:
        return self._root / workspace_id / self.FILE

    def load(self, workspace_id: str, *, owner: str) -> ACL:
        with self._lock:
            path = self._path(workspace_id)
            if path.exists():
                return ACL.from_dict(json.loads(path.read_text()))
            return ACL(workspace_id=workspace_id, owner=owner)

    def save(self, acl: ACL) -> None:
        with self._lock:
            path = self._path(acl.workspace_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(acl.to_dict(), indent=2))
