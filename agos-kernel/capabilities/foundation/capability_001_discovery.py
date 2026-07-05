"""
CAPABILITY-000001: Repository Discovery

PURPOSE: Discover repositories from local, remote, or connected sources.

INPUT: Repository Source (URL, path, or connection string)
OUTPUT: Repository Descriptor

CONTRACTS:
- Input validation
- Source type detection
- Error handling

VERSION: 1.0.0
"""
import hashlib
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class SourceType(Enum):
    """Repository source type."""
    LOCAL = "local"
    GIT_URL = "git_url"
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"


class DiscoveryStatus(Enum):
    """Discovery status."""
    DISCOVERED = "discovered"
    NOT_FOUND = "not_found"
    ACCESS_DENIED = "access_denied"
    INVALID = "invalid"


@dataclass
class RepositoryDescriptor:
    """
    Repository Descriptor - Output of discovery.
    """
    source_type: SourceType
    source: str
    url: str = ""
    path: str = ""
    name: str = ""
    owner: str = ""
    branch: str = "main"
    discovered_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type.value,
            "source": self.source,
            "url": self.url,
            "path": self.path,
            "name": self.name,
            "owner": self.owner,
            "branch": self.branch,
            "discovered_at": self.discovered_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class DiscoveryEvidence:
    """Evidence for discovery operation."""
    source: str
    source_type: SourceType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    verified: bool = False
    checksum: str = ""


class RepositoryDiscoveryCapability:
    """
    CAPABILITY-000001: Repository Discovery
    
    Discovers repositories from various sources:
    - Local filesystem
    - Git URLs
    - GitHub
    - GitLab
    - Bitbucket
    
    VERSION: 1.0.0
    """
    
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000001"
    
    def __init__(self):
        self.supported_sources = {
            SourceType.LOCAL,
            SourceType.GIT_URL,
            SourceType.GITHUB,
            SourceType.GITLAB,
            SourceType.BITBUCKET,
        }
    
    @property
    def name(self) -> str:
        return "RepositoryDiscovery"
    
    @property
    def description(self) -> str:
        return "Discovers repositories from local, remote, or connected sources"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> RepositoryDescriptor:
        """
        Execute repository discovery.
        
        Args:
            input_data: Dict with 'source' key containing repository source
            
        Returns:
            RepositoryDescriptor with discovery results
        """
        source = input_data.get("source", "")
        if not source:
            raise ValueError("Source is required")
        
        # Detect source type
        source_type = self._detect_source_type(source)
        
        # Discover based on type
        if source_type == SourceType.LOCAL:
            return self._discover_local(source)
        elif source_type == SourceType.GIT_URL:
            return self._discover_git_url(source)
        elif source_type == SourceType.GITHUB:
            return self._discover_github(source)
        elif source_type == SourceType.GITLAB:
            return self._discover_gitlab(source)
        elif source_type == SourceType.BITBUCKET:
            return self._discover_bitbucket(source)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    def _detect_source_type(self, source: str) -> SourceType:
        """Detect the type of repository source."""
        if os.path.isdir(source):
            # Check if it's a git repository
            if os.path.isdir(os.path.join(source, ".git")):
                return SourceType.LOCAL
            return SourceType.LOCAL
        
        if source.startswith("git@"):
            if "github.com" in source:
                return SourceType.GITHUB
            elif "gitlab.com" in source:
                return SourceType.GITLAB
            elif "bitbucket.org" in source:
                return SourceType.BITBUCKET
            return SourceType.GIT_URL
        
        if source.startswith("https://"):
            if "github.com" in source:
                return SourceType.GITHUB
            elif "gitlab.com" in source:
                return SourceType.GITLAB
            elif "bitbucket.org" in source:
                return SourceType.BITBUCKET
            return SourceType.GIT_URL
        
        # Try to detect as path
        if os.path.exists(source):
            return SourceType.LOCAL
        
        # Default to GitHub URL format
        return SourceType.GITHUB
    
    def _discover_local(self, path: str) -> RepositoryDescriptor:
        """Discover local repository."""
        if not os.path.isdir(path):
            raise ValueError(f"Not a directory: {path}")
        
        git_dir = os.path.join(path, ".git")
        if not os.path.isdir(git_dir):
            raise ValueError(f"Not a git repository: {path}")
        
        # Get git remote
        url = ""
        try:
            result = subprocess.run(
                ["git", "-C", path, "remote", "get-url", "origin"],
                capture_output=True, text=True, check=True
            )
            url = result.stdout.strip()
        except:
            pass
        
        # Get current branch
        branch = "main"
        try:
            result = subprocess.run(
                ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, check=True
            )
            branch = result.stdout.strip()
        except:
            pass
        
        # Extract name and owner from URL
        name = os.path.basename(path)
        owner = ""
        if url:
            parts = url.replace(".git", "").split("/")
            if len(parts) >= 2:
                owner = parts[-2]
                name = parts[-1]
        
        return RepositoryDescriptor(
            source_type=SourceType.LOCAL,
            source=path,
            path=os.path.abspath(path),
            url=url,
            name=name,
            owner=owner,
            branch=branch,
            metadata={"local_path": os.path.abspath(path)}
        )
    
    def _discover_git_url(self, url: str) -> RepositoryDescriptor:
        """Discover from git URL."""
        parts = url.replace(".git", "").split("/")
        name = parts[-1] if parts else ""
        owner = parts[-2] if len(parts) >= 2 else ""
        
        return RepositoryDescriptor(
            source_type=SourceType.GIT_URL,
            source=url,
            url=url,
            name=name,
            owner=owner,
            metadata={"raw_url": url}
        )
    
    def _discover_github(self, source: str) -> RepositoryDescriptor:
        """Discover GitHub repository."""
        # Parse GitHub URL or owner/repo format
        if "/" in source:
            parts = source.split("/")
            owner = parts[-2] if len(parts) >= 2 else ""
            repo = parts[-1].replace(".git", "") if parts else ""
        else:
            owner, repo = "", source.replace(".git", "")
        
        url = f"https://github.com/{owner}/{repo}.git"
        
        return RepositoryDescriptor(
            source_type=SourceType.GITHUB,
            source=source,
            url=url,
            name=repo,
            owner=owner,
            metadata={
                "platform": "github",
                "raw_source": source
            }
        )
    
    def _discover_gitlab(self, source: str) -> RepositoryDescriptor:
        """Discover GitLab repository."""
        parts = source.split("/")
        name = parts[-1].replace(".git", "") if parts else ""
        owner = parts[-2] if len(parts) >= 2 else ""
        
        url = f"https://gitlab.com/{owner}/{name}.git"
        
        return RepositoryDescriptor(
            source_type=SourceType.GITLAB,
            source=source,
            url=url,
            name=name,
            owner=owner,
            metadata={"platform": "gitlab"}
        )
    
    def _discover_bitbucket(self, source: str) -> RepositoryDescriptor:
        """Discover Bitbucket repository."""
        parts = source.split("/")
        name = parts[-1].replace(".git", "") if parts else ""
        owner = parts[-2] if len(parts) >= 2 else ""
        
        url = f"https://bitbucket.org/{owner}/{name}.git"
        
        return RepositoryDescriptor(
            source_type=SourceType.BITBUCKET,
            source=source,
            url=url,
            name=name,
            owner=owner,
            metadata={"platform": "bitbucket"}
        )
    
    def discover_multiple(self, sources: List[str]) -> List[RepositoryDescriptor]:
        """Discover multiple repositories."""
        results = []
        for source in sources:
            try:
                descriptor = self.execute({"source": source})
                results.append(descriptor)
            except Exception as e:
                # Log error but continue
                print(f"Warning: Failed to discover {source}: {e}")
        return results
    
    def validate_source(self, source: str) -> bool:
        """Validate if source is accessible."""
        try:
            source_type = self._detect_source_type(source)
            
            if source_type == SourceType.LOCAL:
                return os.path.isdir(source) and os.path.isdir(os.path.join(source, ".git"))
            else:
                # For remote sources, return True if format is valid
                return bool(source)
        except:
            return False
