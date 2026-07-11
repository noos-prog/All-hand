"""Repository Domain Model."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RepositoryType(Enum):
    """Types of repositories."""
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"


class RepositoryLanguage(Enum):
    """Programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    GO = "go"
    RUST = "rust"
    C_SHARP = "c_sharp"
    CPP = "cpp"
    C = "c"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SCALA = "scala"
    PHP = "php"
    UNKNOWN = "unknown"


@dataclass
class FileInfo:
    """Information about a file."""
    path: str
    name: str
    extension: str
    size_bytes: int
    is_binary: bool = False
    language: Optional[RepositoryLanguage] = None


@dataclass
class DirectoryInfo:
    """Information about a directory."""
    path: str
    name: str
    file_count: int
    subdirectories: List[str] = field(default_factory=list)


@dataclass
class Dependency:
    """A dependency."""
    name: str
    version: str
    package_manager: str
    is_dev: bool = False


@dataclass
class Repository:
    """A repository."""
    repo_id: str
    name: str
    url: str
    owner: str
    repo_type: RepositoryType = RepositoryType.PUBLIC
    description: str = ""
    default_branch: str = "main"
    languages: List[RepositoryLanguage] = field(default_factory=list)
    files: List[FileInfo] = field(default_factory=list)
    directories: List[DirectoryInfo] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)
    has_readme: bool = False
    has_license: bool = False
    has_tests: bool = False
    has_ci: bool = False
    has_docker: bool = False
    stars: int = 0
    forks: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
