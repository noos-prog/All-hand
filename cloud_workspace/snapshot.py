"""Content-addressed snapshots for a workspace tree.

Each snapshot is a gzipped tar archive of the workspace ``tree/`` folder
plus a SHA-256 checksum. Snapshots are immutable and stored beside the
workspace, so recovery works even after a process restart.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tarfile
import tempfile
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from .runtime import Workspace, WorkspaceRuntime


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class Snapshot:
    snapshot_id: str
    workspace_id: str
    archive_path: Path
    checksum: str
    size_bytes: int
    created_at: str = field(default_factory=_utcnow_iso)
    note: str = ""

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["archive_path"] = str(self.archive_path)
        return data


class SnapshotStore:
    def __init__(self, runtime: WorkspaceRuntime) -> None:
        self._runtime = runtime
        self._lock = threading.RLock()

    # --------------------------------------------------------------- helpers
    def _dir(self, ws: Workspace) -> Path:
        d = ws.root / "snapshots"
        d.mkdir(exist_ok=True)
        return d

    def _index_path(self, ws: Workspace) -> Path:
        return self._dir(ws) / "index.json"

    def _load_index(self, ws: Workspace) -> List[Snapshot]:
        idx = self._index_path(ws)
        if not idx.exists():
            return []
        raw = json.loads(idx.read_text())
        return [
            Snapshot(
                snapshot_id=r["snapshot_id"],
                workspace_id=r["workspace_id"],
                archive_path=Path(r["archive_path"]),
                checksum=r["checksum"],
                size_bytes=int(r["size_bytes"]),
                created_at=r.get("created_at", _utcnow_iso()),
                note=r.get("note", ""),
            )
            for r in raw
        ]

    def _save_index(self, ws: Workspace, snaps: List[Snapshot]) -> None:
        self._index_path(ws).write_text(
            json.dumps([s.to_dict() for s in snaps], indent=2)
        )

    # ---------------------------------------------------------------- public
    def create(self, workspace_id: str, *, note: str = "") -> Snapshot:
        with self._lock:
            ws = self._runtime.get(workspace_id)
            tree = ws.root / "tree"
            if not tree.exists():
                raise FileNotFoundError(f"workspace {workspace_id} has no tree")

            snapshot_id = f"snap_{uuid.uuid4().hex[:12]}"
            archive = self._dir(ws) / f"{snapshot_id}.tar.gz"
            digest = hashlib.sha256()

            with tarfile.open(archive, "w:gz") as tar:
                tar.add(tree, arcname="tree")

            with archive.open("rb") as fh:
                for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                    digest.update(chunk)

            snap = Snapshot(
                snapshot_id=snapshot_id,
                workspace_id=workspace_id,
                archive_path=archive,
                checksum=digest.hexdigest(),
                size_bytes=archive.stat().st_size,
                note=note,
            )
            snaps = self._load_index(ws)
            snaps.append(snap)
            self._save_index(ws, snaps)
            return snap

    def list(self, workspace_id: str) -> List[Snapshot]:
        with self._lock:
            return self._load_index(self._runtime.get(workspace_id))

    def get(self, workspace_id: str, snapshot_id: str) -> Snapshot:
        for s in self.list(workspace_id):
            if s.snapshot_id == snapshot_id:
                return s
        raise KeyError(f"no snapshot {snapshot_id} for {workspace_id}")

    def verify(self, workspace_id: str, snapshot_id: str) -> bool:
        snap = self.get(workspace_id, snapshot_id)
        digest = hashlib.sha256()
        with snap.archive_path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest() == snap.checksum

    def restore(self, workspace_id: str, snapshot_id: str) -> None:
        with self._lock:
            ws = self._runtime.get(workspace_id)
            snap = self.get(workspace_id, snapshot_id)
            if not self.verify(workspace_id, snapshot_id):
                raise IOError(f"snapshot {snapshot_id} failed checksum")

            tree = ws.root / "tree"
            with tempfile.TemporaryDirectory(prefix="ws-restore-") as tmp:
                with tarfile.open(snap.archive_path, "r:gz") as tar:
                    tar.extractall(tmp, filter="data")
                staged = Path(tmp) / "tree"
                if tree.exists():
                    shutil.rmtree(tree)
                shutil.move(str(staged), str(tree))

    def prune(self, workspace_id: str, *, keep: int = 10) -> int:
        with self._lock:
            ws = self._runtime.get(workspace_id)
            snaps = sorted(self._load_index(ws), key=lambda s: s.created_at)
            to_drop = snaps[: max(0, len(snaps) - keep)]
            for s in to_drop:
                s.archive_path.unlink(missing_ok=True)
            remaining = snaps[len(to_drop):]
            self._save_index(ws, remaining)
            return len(to_drop)
