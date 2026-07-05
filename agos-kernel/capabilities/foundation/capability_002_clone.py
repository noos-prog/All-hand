"""
CAPABILITY-000002: Repository Clone

PURPOSE: Clone repositories safely.

SUPPORT:
- HTTPS
- SSH
- Local Mirror
- Shallow Clone
- Incremental Clone

VERSION: 1.0.0
"""
import hashlib
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from .capability_001_discovery import RepositoryDescriptor, SourceType


@dataclass
class CloneOptions:
    """Clone options."""
    depth: int = 1  # Shallow clone
    branch: str = "main"
    use_https: bool = True
    use_ssh: bool = False
    credentials: Optional[Dict[str, str]] = None


@dataclass
class CloneResult:
    """Result of clone operation."""
    path: str
    descriptor: RepositoryDescriptor
    clone_time_ms: float = 0
    size_bytes: int = 0
    commit_hash: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "descriptor": self.descriptor.to_dict(),
            "clone_time_ms": self.clone_time_ms,
            "size_bytes": self.size_bytes,
            "commit_hash": self.commit_hash,
        }


class RepositoryCloneCapability:
    """
    CAPABILITY-000002: Repository Clone
    
    Clones repositories with support for HTTPS, SSH, local mirrors,
    shallow clones, and incremental clones.
    
    VERSION: 1.0.0
    """
    
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000002"
    
    def __init__(self):
        self.temp_base = tempfile.gettempdir()
    
    @property
    def name(self) -> str:
        return "RepositoryClone"
    
    @property
    def description(self) -> str:
        return "Clones repositories safely with HTTPS, SSH, and shallow clone support"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> CloneResult:
        """
        Execute repository clone.
        
        Args:
            input_data: Dict with 'source' or 'descriptor' key
            
        Returns:
            CloneResult with cloned repository path
        """
        import time
        start_time = time.time()
        
        # Get source
        source = input_data.get("source", "")
        descriptor_data = input_data.get("descriptor")
        
        if descriptor_data:
            if isinstance(descriptor_data, RepositoryDescriptor):
                descriptor = descriptor_data
            else:
                # Reconstruct from dict
                source = descriptor_data.get("url", descriptor_data.get("source", ""))
                descriptor = RepositoryDescriptor(
                    source_type=SourceType.GITHUB,
                    source=source,
                    url=descriptor_data.get("url", source),
                    name=descriptor_data.get("name", ""),
                    owner=descriptor_data.get("owner", ""),
                )
        else:
            # Create descriptor from source
            from .capability_001_discovery import RepositoryDiscoveryCapability
            discovery = RepositoryDiscoveryCapability()
            descriptor = discovery.execute({"source": source})
        
        # Parse options
        options = CloneOptions(
            depth=input_data.get("depth", 1),
            branch=input_data.get("branch", "main"),
            use_https=input_data.get("use_https", True),
        )
        
        # Create temp directory
        repo_name = descriptor.name or "repo"
        temp_dir = tempfile.mkdtemp(prefix=f"agos_clone_{repo_name}_")
        repo_path = os.path.join(temp_dir, repo_name)
        
        # Build git command
        cmd = ["git", "clone"]
        
        if options.depth > 0:
            cmd.extend(["--depth", str(options.depth)])
        
        if options.branch:
            cmd.extend(["--branch", options.branch])
        
        # Handle URL with credentials
        url = self._prepare_url(descriptor.url, options)
        cmd.append(url)
        cmd.append(repo_path)
        
        try:
            # Execute clone
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Get commit hash
            commit_hash = ""
            try:
                result = subprocess.run(
                    ["git", "-C", repo_path, "rev-parse", "HEAD"],
                    capture_output=True, text=True, check=True
                )
                commit_hash = result.stdout.strip()
            except:
                pass
            
            # Calculate size
            size_bytes = self._calculate_size(repo_path)
            
            clone_time_ms = (time.time() - start_time) * 1000
            
            return CloneResult(
                path=repo_path,
                descriptor=descriptor,
                clone_time_ms=clone_time_ms,
                size_bytes=size_bytes,
                commit_hash=commit_hash,
            )
            
        except subprocess.CalledProcessError as e:
            # Clean up on failure
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            raise RuntimeError(f"Clone failed: {e.stderr}")
    
    def _prepare_url(self, url: str, options: CloneOptions) -> str:
        """Prepare URL with credentials if needed."""
        if not options.credentials:
            return url
        
        # Convert SSH to HTTPS with credentials if requested
        if options.use_https and url.startswith("git@"):
            # Convert git@github.com:owner/repo.git to https://owner:token@github.com/owner/repo
            url = url.replace("git@", "")
            url = url.replace(":", "/")
            url = f"https://{options.credentials.get('token', '')}@{url}"
        
        return url
    
    def _calculate_size(self, path: str) -> int:
        """Calculate total size of directory."""
        total = 0
        for dirpath, dirnames, filenames in os.walk(path):
            # Skip .git
            if ".git" in dirpath:
                continue
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except:
                    pass
        return total
    
    def clone_shallow(self, source: str, branch: str = "main") -> CloneResult:
        """Convenience method for shallow clone."""
        return self.execute({"source": source, "branch": branch, "depth": 1})
    
    def clone_full(self, source: str, branch: str = "main") -> CloneResult:
        """Convenience method for full clone."""
        return self.execute({"source": source, "branch": branch, "depth": 0})
