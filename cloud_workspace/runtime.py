"""Workspace runtime: create, isolate, list, destroy on-disk workspaces.

Every workspace maps to a directory tree under ``root``. Metadata is
persisted as ``workspace.json`` next to the working tree so recovery is
possible from disk alone.
"""

from __future__ import annotations

import json
import os
import shutil
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional


class WorkspaceType(str, Enum):
    GIT_REPOSITORY = "git_repository"
    REMOTE_REPOSITORY = "remote_repository"
    BLANK = "blank"
    TEMPLATE = "template"
    IMPORTED_ARCHIVE = "imported_archive"
    GENERATED_PROJECT = "generated_project"


class WorkspaceStatus(str, Enum):
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"
    DESTROYED = "destroyed"


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Workspace:
    workspace_id: str
    name: str
    type: WorkspaceType
    owner: str
    root: Path
    status: WorkspaceStatus = WorkspaceStatus.PROVISIONING
    created_at: str = field(default_factory=_utcnow_iso)
    updated_at: str = field(default_factory=_utcnow_iso)
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        data["status"] = self.status.value
        data["root"] = str(self.root)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workspace":
        return cls(
            workspace_id=data["workspace_id"],
            name=data["name"],
            type=WorkspaceType(data["type"]),
            owner=data["owner"],
            root=Path(data["root"]),
            status=WorkspaceStatus(data["status"]),
            created_at=data.get("created_at", _utcnow_iso()),
            updated_at=data.get("updated_at", _utcnow_iso()),
            labels=data.get("labels", {}),
        )


class WorkspaceRuntime:
    """Filesystem-backed workspace store with in-memory index and a lock."""

    METADATA_FILE = "workspace.json"

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self._root = Path(root).expanduser().resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._workspaces: Dict[str, Workspace] = {}
        self._reload()

    # ------------------------------------------------------------------ index
    def _reload(self) -> None:
        with self._lock:
            self._workspaces.clear()
            for entry in self._root.iterdir():
                meta = entry / self.METADATA_FILE
                if entry.is_dir() and meta.is_file():
                    try:
                        ws = Workspace.from_dict(json.loads(meta.read_text()))
                        self._workspaces[ws.workspace_id] = ws
                    except (ValueError, KeyError, OSError):
                        # corrupt or partial workspace — leave it on disk
                        continue

    def _persist(self, ws: Workspace) -> None:
        ws.updated_at = _utcnow_iso()
        (ws.root / self.METADATA_FILE).write_text(json.dumps(ws.to_dict(), indent=2))

    # ---------------------------------------------------------------- lifecycle
    def create(
        self,
        name: str,
        ws_type: WorkspaceType,
        owner: str,
        *,
        labels: Optional[Dict[str, str]] = None,
    ) -> Workspace:
        if not name or "/" in name or ".." in name:
            raise ValueError(f"invalid workspace name: {name!r}")
        with self._lock:
            workspace_id = f"ws_{uuid.uuid4().hex[:12]}"
            root = self._root / workspace_id
            root.mkdir(parents=True, exist_ok=False)
            (root / "tree").mkdir()
            ws = Workspace(
                workspace_id=workspace_id,
                name=name,
                type=ws_type,
                owner=owner,
                root=root,
                status=WorkspaceStatus.ACTIVE,
                labels=dict(labels or {}),
            )
            self._persist(ws)
            self._workspaces[workspace_id] = ws
            return ws

    def get(self, workspace_id: str) -> Workspace:
        with self._lock:
            try:
                return self._workspaces[workspace_id]
            except KeyError as exc:
                raise KeyError(f"unknown workspace: {workspace_id}") from exc

    def list(self, *, owner: Optional[str] = None) -> List[Workspace]:
        with self._lock:
            values = list(self._workspaces.values())
        if owner is not None:
            values = [w for w in values if w.owner == owner]
        return sorted(values, key=lambda w: w.created_at)

    def suspend(self, workspace_id: str) -> Workspace:
        return self._set_status(workspace_id, WorkspaceStatus.SUSPENDED)

    def resume(self, workspace_id: str) -> Workspace:
        return self._set_status(workspace_id, WorkspaceStatus.ACTIVE)

    def archive(self, workspace_id: str) -> Workspace:
        return self._set_status(workspace_id, WorkspaceStatus.ARCHIVED)

    def destroy(self, workspace_id: str) -> None:
        with self._lock:
            ws = self.get(workspace_id)
            shutil.rmtree(ws.root, ignore_errors=True)
            ws.status = WorkspaceStatus.DESTROYED
            self._workspaces.pop(workspace_id, None)

    def clone(self, workspace_id: str, new_name: str, *, owner: Optional[str] = None) -> Workspace:
        with self._lock:
            src = self.get(workspace_id)
            new = self.create(new_name, src.type, owner or src.owner, labels=dict(src.labels))
            src_tree = src.root / "tree"
            dst_tree = new.root / "tree"
            if src_tree.exists():
                shutil.rmtree(dst_tree)
                shutil.copytree(src_tree, dst_tree, symlinks=False)
            return new

    def _set_status(self, workspace_id: str, status: WorkspaceStatus) -> Workspace:
        with self._lock:
            ws = self.get(workspace_id)
            ws.status = status
            self._persist(ws)
            return ws

    # ------------------------------------------------------------------ iter
    def __iter__(self) -> Iterator[Workspace]:
        return iter(self.list())

    def __len__(self) -> int:
        with self._lock:
            return len(self._workspaces)
