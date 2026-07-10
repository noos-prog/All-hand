#!/usr/bin/env python3
"""
ARI - Repository Module
=====================

Repository discovery, analysis, and metrics.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json


class Language(Enum):
    """Programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    OTHER = "other"


class RepositoryStatus(Enum):
    """Repository status."""
    DISCOVERED = "discovered"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


@dataclass
class RepositoryMetrics:
    """Metrics for a repository."""
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    issues: int = 0
    pull_requests: int = 0
    commits: int = 0
    contributors: int = 0
    branches: int = 0
    releases: int = 0
    packages: int = 0
    
    # Code metrics
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    files: int = 0
    
    # Activity
    last_commit: Optional[str] = None
    last_release: Optional[str] = None
    open_issues: int = 0
    closed_issues: int = 0
    
    # Health
    license_type: Optional[str] = None
    has_readme: bool = False
    has_contributing: bool = False
    has_license: bool = False
    
    def get_health_score(self) -> float:
        """Calculate repository health score."""
        score = 0.0
        if self.has_license:
            score += 0.1
        if self.has_readme:
            score += 0.1
        if self.has_contributing:
            score += 0.1
        if self.stars > 100:
            score += 0.2
        if self.contributors > 5:
            score += 0.2
        if self.open_issues < 50:
            score += 0.15
        if self.commits > 100:
            score += 0.15
        return min(1.0, score)


@dataclass
class Repository:
    """
    A repository in the data lake.
    """
    repo_id: str
    name: str
    full_name: str                      # owner/repo
    url: str
    description: Optional[str] = None
    
    # Classification
    primary_language: Optional[Language] = None
    languages: Tuple[str, ...] = ()
    topics: Tuple[str, ...] = ()
    
    # Metrics
    metrics: RepositoryMetrics = field(default_factory=RepositoryMetrics)
    
    # Analysis
    capabilities: Tuple[str, ...] = ()   # What this repo can do
    dependencies: Tuple[str, ...] = ()  # Dependencies
    technologies: Tuple[str, ...] = ()  # Tech stack
    patterns: Tuple[str, ...] = ()     # Architecture patterns
    
    # Metadata
    status: RepositoryStatus = RepositoryStatus.DISCOVERED
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_analyzed: Optional[str] = None
    
    # Source
    source: str = "github"             # github, gitlab, etc.
    source_id: Optional[str] = None
    
    # Quality
    quality_score: float = 0.0
    security_score: float = 0.0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get repository summary."""
        return {
            "name": self.full_name,
            "language": self.primary_language.value if self.primary_language else None,
            "stars": self.metrics.stars,
            "health": f"{self.metrics.get_health_score():.0%}",
            "capabilities": len(self.capabilities),
        }


class RepositoryDiscovery:
    """
    Discovers repositories from various sources.
    """
    
    def __init__(self):
        self._sources: Dict[str, Callable] = {}
        self._filters: List[Callable] = []
        self._discovered: Dict[str, Repository] = {}
    
    def add_source(self, name: str, discover_func: Callable) -> None:
        """Add a discovery source."""
        self._sources[name] = discover_func
    
    def add_filter(self, filter_func: Callable[[Repository], bool]) -> None:
        """Add a repository filter."""
        self._filters.append(filter_func)
    
    def discover(self, source: str, query: str = "", limit: int = 100) -> List[Repository]:
        """Discover repositories from a source."""
        if source not in self._sources:
            raise ValueError(f"Unknown source: {source}")
        
        repos = self._sources[source](query, limit)
        
        # Apply filters
        for repo in repos:
            if all(f(repo) for f in self._filters):
                self._discovered[repo.repo_id] = repo
        
        return list(self._discovered.values())
    
    def discover_from_github(self, topic: str, min_stars: int = 100) -> List[Repository]:
        """Discover repositories from GitHub by topic."""
        # Simulated - in real implementation would use GitHub API
        repo = Repository(
            repo_id=f"github_{topic}_1",
            name=f"{topic}-project",
            full_name=f"user/{topic}-project",
            url=f"https://github.com/user/{topic}-project",
            description=f"A {topic} project",
            primary_language=Language.PYTHON,
            topics=(topic,),
        )
        repo.metrics.stars = min_stars
        repo.metrics.has_readme = True
        repo.metrics.has_license = True
        repo.status = RepositoryStatus.ANALYZED
        
        self._discovered[repo.repo_id] = repo
        return [repo]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get discovery statistics."""
        by_status = {}
        by_language = {}
        
        for repo in self._discovered.values():
            status = repo.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            lang = repo.primary_language.value if repo.primary_language else "unknown"
            by_language[lang] = by_language.get(lang, 0) + 1
        
        return {
            "total_discovered": len(self._discovered),
            "by_status": by_status,
            "by_language": by_language,
            "sources": list(self._sources.keys()),
        }


class RepositoryAnalyzer:
    """
    Analyzes repositories to extract capabilities and patterns.
    """
    
    def __init__(self):
        self._analyzers: Dict[str, Callable] = {}
    
    def register_analyzer(self, name: str, analyzer: Callable[[Repository], Dict]) -> None:
        """Register an analyzer."""
        self._analyzers[name] = analyzer
    
    def analyze(self, repo: Repository) -> Repository:
        """Analyze a repository."""
        repo.status = RepositoryStatus.ANALYZING
        repo.last_analyzed = datetime.utcnow().isoformat()
        
        # Run all analyzers
        for name, analyzer in self._analyzers.items():
            try:
                result = analyzer(repo)
                if result:
                    self._apply_analysis(repo, result)
            except Exception as e:
                print(f"Analyzer {name} failed: {e}")
        
        repo.status = RepositoryStatus.ANALYZED
        return repo
    
    def _apply_analysis(self, repo: Repository, result: Dict[str, Any]) -> None:
        """Apply analysis results to repository."""
        if "capabilities" in result:
            repo.capabilities = tuple(result["capabilities"])
        if "dependencies" in result:
            repo.dependencies = tuple(result["dependencies"])
        if "technologies" in result:
            repo.technologies = tuple(result["technologies"])
        if "patterns" in result:
            repo.patterns = tuple(result["patterns"])
        if "quality_score" in result:
            repo.quality_score = result["quality_score"]
        if "security_score" in result:
            repo.security_score = result["security_score"]
    
    def analyze_file_structure(self, repo: Repository) -> Dict[str, Any]:
        """Analyze file structure."""
        return {
            "technologies": ["python", "pytest", "docker"],
            "patterns": ["api", "rest", "crud"],
        }
    
    def analyze_code_quality(self, repo: Repository) -> Dict[str, Any]:
        """Analyze code quality."""
        return {
            "quality_score": 0.85,
            "security_score": 0.90,
        }
    
    def analyze_dependencies(self, repo: Repository) -> Dict[str, Any]:
        """Analyze dependencies."""
        return {
            "dependencies": ["requests", "flask", "sqlalchemy"],
        }


class RepositoryDataLake:
    """
    Main data lake for repositories.
    """
    
    def __init__(self):
        self._repositories: Dict[str, Repository] = {}
        self._discovery = RepositoryDiscovery()
        self._analyzer = RepositoryAnalyzer()
        
        # Register default analyzers
        self._analyzer.register_analyzer("structure", self._analyzer.analyze_file_structure)
        self._analyzer.register_analyzer("quality", self._analyzer.analyze_code_quality)
        self._analyzer.register_analyzer("deps", self._analyzer.analyze_dependencies)
    
    def add_repository(self, repo: Repository) -> str:
        """Add a repository to the lake."""
        self._repositories[repo.repo_id] = repo
        return repo.repo_id
    
    def get_repository(self, repo_id: str) -> Optional[Repository]:
        """Get a repository by ID."""
        return self._repositories.get(repo_id)
    
    def search(
        self,
        language: Optional[Language] = None,
        min_stars: int = 0,
        topics: List[str] = None,
        capabilities: List[str] = None,
        limit: int = 100
    ) -> List[Repository]:
        """Search repositories."""
        results = list(self._repositories.values())
        
        if language:
            results = [r for r in results if r.primary_language == language]
        
        if min_stars > 0:
            results = [r for r in results if r.metrics.stars >= min_stars]
        
        if topics:
            results = [
                r for r in results
                if any(t in r.topics for t in topics)
            ]
        
        if capabilities:
            results = [
                r for r in results
                if any(c in r.capabilities for c in capabilities)
            ]
        
        # Sort by stars
        results.sort(key=lambda r: r.metrics.stars, reverse=True)
        
        return results[:limit]
    
    def discover_and_analyze(
        self,
        source: str,
        query: str,
        min_stars: int = 100
    ) -> List[Repository]:
        """Discover and analyze repositories."""
        repos = self._discovery.discover_from_github(query, min_stars)
        
        analyzed = []
        for repo in repos:
            repo = self._analyzer.analyze(repo)
            self.add_repository(repo)
            analyzed.append(repo)
        
        return analyzed
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get data lake statistics."""
        by_language = {}
        total_stars = 0
        total_capabilities = 0
        
        for repo in self._repositories.values():
            lang = repo.primary_language.value if repo.primary_language else "unknown"
            by_language[lang] = by_language.get(lang, 0) + 1
            total_stars += repo.metrics.stars
            total_capabilities += len(repo.capabilities)
        
        return {
            "total_repositories": len(self._repositories),
            "by_language": by_language,
            "total_stars": total_stars,
            "total_capabilities": total_capabilities,
            "avg_stars": total_stars / len(self._repositories) if self._repositories else 0,
        }
