"""Contracts - Interfaces and contracts for providers."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class RepositoryMetadata:
    """Repository metadata."""
    url: str = ""
    name: str = ""
    owner: str = ""
    branch: str = "main"
    commit: Optional[str] = None


@dataclass
class FileNode:
    """A file or directory in the repository."""
    path: str
    is_dir: bool
    size: int = 0
    content: Optional[str] = None


@dataclass
class RepositorySnapshot:
    """A snapshot of a repository."""
    metadata: RepositoryMetadata
    files: List[FileNode] = field(default_factory=list)
    root_path: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def get_file(self, path: str) -> Optional[FileNode]:
        """Get a file by path."""
        for f in self.files:
            if f.path == path:
                return f
        return None
    
    def list_files(self, pattern: str = "*") -> List[FileNode]:
        """List files matching pattern."""
        import fnmatch
        return [f for f in self.files if not f.is_dir and fnmatch.fnmatch(f.path, pattern)]
    
    def list_dirs(self) -> List[FileNode]:
        """List directories."""
        return [f for f in self.files if f.is_dir]


@dataclass
class RepositoryDNA:
    """
    Repository DNA - the identity of a repository.
    """
    # Identity
    name: str = ""
    url: str = ""
    owner: str = ""
    
    # Languages
    primary_language: str = ""
    languages: List[str] = field(default_factory=list)
    
    # Frameworks
    frameworks: List[str] = field(default_factory=list)
    
    # Dependencies
    package_managers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    # Configuration
    config_files: List[str] = field(default_factory=list)
    
    # Structure
    entry_points: List[str] = field(default_factory=list)
    directory_tree: List[str] = field(default_factory=list)
    
    # Documentation
    readme_summary: str = ""
    license: str = ""
    
    # Metadata
    generated_at: datetime = field(default_factory=datetime.utcnow)
    snapshot_path: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "url": self.url,
            "owner": self.owner,
            "primary_language": self.primary_language,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "package_managers": self.package_managers,
            "dependencies": self.dependencies,
            "config_files": self.config_files,
            "entry_points": self.entry_points,
            "directory_tree": self.directory_tree,
            "readme_summary": self.readme_summary,
            "license": self.license,
            "generated_at": self.generated_at.isoformat(),
            "snapshot_path": self.snapshot_path
        }
