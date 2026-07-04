"""Data models for Repository Intelligence."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class Language(Enum):
    """Programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    GO = "go"
    RUST = "rust"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    SCALA = "scala"
    HASKELL = "haskell"
    SHELL = "shell"
    DOCKERFILE = "dockerfile"
    UNKNOWN = "unknown"


class Framework(Enum):
    """Frameworks."""
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    NEXTJS = "nextjs"
    NESTJS = "nestjs"
    SPRING = "spring"
    FLUTTER = "flutter"
    EXPRESS = "express"
    FASTIFY = "fastify"
    GIN = "gin"
    AXUM = "axum"
    UNKNOWN = "unknown"


class BuildSystem(Enum):
    """Build systems."""
    CMAKE = "cmake"
    GRADLE = "gradle"
    MAVEN = "maven"
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"
    POETRY = "poetry"
    PIP = "pip"
    CARGO = "cargo"
    UNKNOWN = "unknown"


class ContainerTech(Enum):
    """Container technologies."""
    DOCKER = "docker"
    PODMAN = "podman"
    CONTAINERD = "containerd"
    KUBERNETES = "kubernetes"
    HELM = "helm"
    UNKNOWN = "unknown"


class CloudProvider(Enum):
    """Cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    DIGITALOCEAN = "digitalocean"
    HEROKU = "heroku"
    VERCEL = "vercel"
    UNKNOWN = "unknown"


class Database(Enum):
    """Databases."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"
    CASSANDRA = "cassandra"
    NEO4J = "neo4j"
    UNKNOWN = "unknown"


class Queue(Enum):
    """Message queues."""
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"
    SQS = "sqs"
    NATS = "nats"
    REDIS_QUEUE = "redis_queue"
    UNKNOWN = "unknown"


@dataclass
class DirectoryNode:
    """A node in the directory tree."""
    path: str
    name: str
    is_dir: bool
    size: int = 0
    children: List['DirectoryNode'] = field(default_factory=list)
    depth: int = 0


@dataclass
class Module:
    """A module/package in the repository."""
    path: str
    name: str
    type: str  # module, package, library, application
    files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)


@dataclass
class FileMetrics:
    """Metrics for a file."""
    path: str
    lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    complexity: int = 0


@dataclass
class RepositoryMetrics:
    """Repository metrics."""
    total_files: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    languages: Dict[str, int] = field(default_factory=dict)  # language -> lines
    largest_files: List[tuple] = field(default_factory=list)  # (path, size)
    depth: int = 0


@dataclass
class RepositoryGenome:
    """Complete DNA of a repository."""
    # Identity
    name: str = ""
    path: str = ""
    root_path: str = ""
    
    # Structure
    directories: List[DirectoryNode] = field(default_factory=list)
    modules: List[Module] = field(default_factory=list)
    
    # Detected Technologies
    languages: Set[Language] = field(default_factory=set)
    frameworks: Set[Framework] = field(default_factory=set)
    build_systems: Set[BuildSystem] = field(default_factory=set)
    package_managers: Set[str] = field(default_factory=set)
    test_frameworks: Set[str] = field(default_factory=set)
    ci_cd_systems: Set[str] = field(default_factory=set)
    container_tech: Set[ContainerTech] = field(default_factory=set)
    cloud_providers: Set[CloudProvider] = field(default_factory=set)
    databases: Set[Database] = field(default_factory=set)
    queues: Set[Queue] = field(default_factory=set)
    
    # Metrics
    metrics: RepositoryMetrics = field(default_factory=RepositoryMetrics)
    file_metrics: List[FileMetrics] = field(default_factory=list)
    
    # Analysis
    config_files: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    test_files: List[str] = field(default_factory=list)
    docs: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    assets: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    analyzed_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "languages": [l.value for l in self.languages],
            "frameworks": [f.value for f in self.frameworks],
            "build_systems": [b.value for b in self.build_systems],
            "metrics": {
                "total_files": self.metrics.total_files,
                "total_lines": self.metrics.total_lines,
                "languages": self.metrics.languages,
            },
            "modules_count": len(self.modules),
            "config_files_count": len(self.config_files),
            "test_files_count": len(self.test_files),
        }
