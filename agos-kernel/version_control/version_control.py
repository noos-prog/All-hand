"""AGOS Version Control."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class VCStatus(Enum):
    """Version control status."""
    CLEAN = "clean"
    MODIFIED = "modified"
    CONFLICT = "conflict"
    UNTRACKED = "untracked"


@dataclass
class Repository:
    """A repository."""
    id: str
    name: str
    url: str
    branch: str = "main"
    status: VCStatus = VCStatus.CLEAN
    last_commit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Commit:
    """A commit."""
    id: str
    message: str
    author: str
    timestamp: datetime = field(default_factory=datetime.now)
    files: List[str] = field(default_factory=list)


class VersionControl:
    """
    Version Control.
    
    Manages version control operations.
    
    Usage:
        vc = VersionControl()
        repo = vc.clone("https://github.com/org/repo")
        vc.commit(repo.id, "Update files")
    """
    
    def __init__(self):
        """Initialize version control."""
        self._repositories: Dict[str, Repository] = {}
        self._commits: Dict[str, List[Commit]] = {}
    
    def create_repository(self, name: str, url: str) -> Repository:
        """Create a repository."""
        repo = Repository(
            id=f"repo-{uuid.uuid4().hex[:8]}",
            name=name,
            url=url,
        )
        self._repositories[repo.id] = repo
        self._commits[repo.id] = []
        return repo
    
    def get_repository(self, repo_id: str) -> Optional[Repository]:
        """Get a repository by ID."""
        return self._repositories.get(repo_id)
    
    def commit(self, repo_id: str, message: str, author: str = "AGOS", files: Optional[List[str]] = None) -> Commit:
        """Create a commit."""
        commit = Commit(
            id=f"commit-{uuid.uuid4().hex[:8]}",
            message=message,
            author=author,
            files=files or [],
        )
        
        if repo_id not in self._commits:
            self._commits[repo_id] = []
        self._commits[repo_id].append(commit)
        
        repo = self._repositories.get(repo_id)
        if repo:
            repo.last_commit = commit.id
        
        return commit
    
    def get_commits(self, repo_id: str) -> List[Commit]:
        """Get commits for a repository."""
        return self._commits.get(repo_id, [])
    
    def list_repositories(self) -> List[Repository]:
        """List all repositories."""
        return list(self._repositories.values())


# Global instance
_version_control: Optional[VersionControl] = None


def get_version_control() -> VersionControl:
    """Get the global version control."""
    global _version_control
    if _version_control is None:
        _version_control = VersionControl()
    return _version_control
