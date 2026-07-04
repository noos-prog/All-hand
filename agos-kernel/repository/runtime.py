"""Universal Multi-Repository Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class RepositoryType(Enum):
    """Repository type."""
    SOURCE = "source"
    DATA = "data"
    MODEL = "model"
    CONFIG = "config"
    DOCUMENTATION = "documentation"
    ARCHIVE = "archive"


class RepositoryHealth(Enum):
    """Repository health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class Repository:
    """Universal Repository."""
    id: str
    name: str
    url: str
    repo_type: RepositoryType
    health: RepositoryHealth = RepositoryHealth.UNKNOWN
    
    # Lineage
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    
    # Analysis
    dependencies: List[str] = field(default_factory=list)
    shared_components: List[str] = field(default_factory=list)
    
    # Diff
    last_diff: Optional[str] = None
    last_merge: Optional[str] = None
    
    # Snapshot
    snapshots: List[str] = field(default_factory=list)
    last_snapshot: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class RepositoryRegistry:
    """Registry of repositories."""
    
    def __init__(self):
        """Initialize registry."""
        self.repositories: Dict[str, Repository] = {}
        self.federation: Dict[str, Set[str]] = {}  # org -> repo IDs
    
    def register(self, repo: Repository) -> None:
        """Register a repository."""
        self.repositories[repo.id] = repo
    
    def unregister(self, repo_id: str) -> bool:
        """Unregister a repository."""
        if repo_id in self.repositories:
            del self.repositories[repo_id]
            return True
        return False
    
    def get(self, repo_id: str) -> Optional[Repository]:
        """Get repository by ID."""
        return self.repositories.get(repo_id)
    
    def list_by_org(self, org: str) -> List[Repository]:
        """List repositories by organization."""
        repo_ids = self.federation.get(org, set())
        return [self.repositories[rid] for rid in repo_ids if rid in self.repositories]


class RepositoryAnalyzer:
    """Analyze repositories."""
    
    def __init__(self):
        """Initialize analyzer."""
        self.dependencies: Dict[str, Set[str]] = {}
    
    def analyze_dependencies(self, repo: Repository) -> List[str]:
        """Analyze repository dependencies."""
        # Simplified dependency analysis
        return repo.dependencies
    
    def find_cross_repo_deps(self, repos: List[Repository]) -> Dict[str, List[str]]:
        """Find cross-repository dependencies."""
        cross_deps = {}
        
        for repo in repos:
            deps = set()
            for other in repos:
                if repo.id != other.id:
                    if any(d in other.metadata.get("provides", []) for d in repo.dependencies):
                        deps.add(other.id)
            if deps:
                cross_deps[repo.id] = list(deps)
        
        return cross_deps
    
    def detect_architecture_drift(
        self,
        repo: Repository,
        baseline: Dict[str, Any],
    ) -> List[str]:
        """Detect architecture drift."""
        drift = []
        
        for key, expected in baseline.items():
            actual = repo.metadata.get(key)
            if actual != expected:
                drift.append(f"{key}: expected {expected}, got {actual}")
        
        return drift


class MultiRepositoryRuntime:
    """Universal Multi-Repository Runtime."""
    
    def __init__(self):
        """Initialize runtime."""
        self.registry = RepositoryRegistry()
        self.analyzer = RepositoryAnalyzer()
        self.synchronizer = RepositorySynchronizer()
        self.diff_engine = RepositoryDiffEngine()
        self.merge_engine = RepositoryMergeEngine()
    
    def register_repository(
        self,
        name: str,
        url: str,
        repo_type: RepositoryType,
        org: Optional[str] = None,
    ) -> Repository:
        """Register a new repository."""
        repo_id = self._generate_id(name)
        
        repo = Repository(
            id=repo_id,
            name=name,
            url=url,
            repo_type=repo_type,
        )
        
        self.registry.register(repo)
        
        # Add to federation
        if org:
            if org not in self.registry.federation:
                self.registry.federation[org] = set()
            self.registry.federation[org].add(repo_id)
        
        return repo
    
    def create_snapshot(self, repo_id: str) -> str:
        """Create repository snapshot."""
        repo = self.registry.get(repo_id)
        if not repo:
            return ""
        
        snapshot_id = self._generate_id(f"snapshot-{repo_id}")
        repo.snapshots.append(snapshot_id)
        repo.last_snapshot = datetime.now()
        
        return snapshot_id
    
    def diff(self, repo_id1: str, repo_id2: str) -> Dict[str, Any]:
        """Diff two repositories."""
        return self.diff_engine.diff(repo_id1, repo_id2)
    
    def merge(self, repo_id1: str, repo_id2: str) -> bool:
        """Merge two repositories."""
        return self.merge_engine.merge(repo_id1, repo_id2)
    
    def analyze(self, repo_id: str) -> Dict[str, Any]:
        """Analyze repository."""
        repo = self.registry.get(repo_id)
        if not repo:
            return {}
        
        return {
            "id": repo.id,
            "name": repo.name,
            "dependencies": self.analyzer.analyze_dependencies(repo),
            "health": repo.health.value,
        }
    
    def analyze_federation(self, org: str) -> Dict[str, Any]:
        """Analyze organization federation."""
        repos = self.registry.list_by_org(org)
        
        return {
            "organization": org,
            "repository_count": len(repos),
            "repositories": [r.name for r in repos],
            "cross_dependencies": self.analyzer.find_cross_repo_deps(repos),
        }
    
    def sync(self, repo_ids: List[str]) -> bool:
        """Synchronize repositories."""
        return self.synchronizer.sync(repo_ids)
    
    def get_health(self, repo_id: str) -> RepositoryHealth:
        """Get repository health."""
        repo = self.registry.get(repo_id)
        if not repo:
            return RepositoryHealth.UNKNOWN
        return repo.health
    
    def get_lineage(self, repo_id: str) -> List[Repository]:
        """Get repository lineage."""
        repo = self.registry.get(repo_id)
        if not repo:
            return []
        
        lineage = [repo]
        
        # Get ancestors
        current = repo
        while current.parent_id:
            parent = self.registry.get(current.parent_id)
            if parent:
                lineage.insert(0, parent)
                current = parent
            else:
                break
        
        # Get descendants
        def get_descendants(r: Repository) -> List[Repository]:
            descendants = []
            for child_id in r.children:
                child = self.registry.get(child_id)
                if child:
                    descendants.append(child)
                    descendants.extend(get_descendants(child))
            return descendants
        
        lineage.extend(get_descendants(repo))
        return lineage
    
    def get_stats(self) -> Dict[str, Any]:
        """Get runtime statistics."""
        return {
            "total_repositories": len(self.registry.repositories),
            "by_type": {
                t.value: sum(1 for r in self.registry.repositories.values() if r.repo_type == t)
                for t in RepositoryType
            },
            "by_health": {
                h.value: sum(1 for r in self.registry.repositories.values() if r.health == h)
                for h in RepositoryHealth
            },
            "federations": len(self.registry.federation),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]


class RepositorySynchronizer:
    """Synchronize repositories."""
    
    def sync(self, repo_ids: List[str]) -> bool:
        """Sync repositories."""
        return True


class RepositoryDiffEngine:
    """Diff repositories."""
    
    def diff(self, repo_id1: str, repo_id2: str) -> Dict[str, Any]:
        """Diff two repositories."""
        return {
            "repo1": repo_id1,
            "repo2": repo_id2,
            "differences": [],
            "similarities": [],
        }


class RepositoryMergeEngine:
    """Merge repositories."""
    
    def merge(self, repo_id1: str, repo_id2: str) -> bool:
        """Merge repositories."""
        return True
