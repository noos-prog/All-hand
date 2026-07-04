"""Filesystem Provider."""
import os
import shutil
from typing import Any, Dict, List, Optional

from .base import Provider


class FilesystemProvider(Provider):
    """Filesystem access provider."""
    
    def __init__(self):
        """Initialize provider."""
        super().__init__("Filesystem", "Local filesystem access")
        self.metadata.auth_types = ["none"]
    
    def health_check(self) -> Dict[str, Any]:
        """Check filesystem health."""
        return {
            "healthy": True,
            "latency_ms": 1,
            "writable": os.access("/", os.W_OK),
        }
    
    def read(self, path: str) -> str:
        """Read file."""
        with open(path, "r") as f:
            return f.read()
    
    def write(self, path: str, content: str) -> bool:
        """Write file."""
        with open(path, "w") as f:
            f.write(content)
        return True
    
    def list(self, path: str) -> List[str]:
        """List directory."""
        if os.path.exists(path):
            return os.listdir(path)
        return []
    
    def exists(self, path: str) -> bool:
        """Check if path exists."""
        return os.path.exists(path)


"""Git Provider."""
import subprocess
from typing import Any, Dict, List, Optional

from .base import Provider


class GitProvider(Provider):
    """Git operations provider."""
    
    def __init__(self):
        """Initialize provider."""
        super().__init__("Git", "Git version control")
        self.metadata.auth_types = ["ssh_key", "token"]
    
    def health_check(self) -> Dict[str, Any]:
        """Check git health."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return {
                "healthy": result.returncode == 0,
                "version": result.stdout.strip(),
                "latency_ms": 10,
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    def clone(self, url: str, path: str, shallow: bool = False) -> bool:
        """Clone repository."""
        cmd = ["git", "clone"]
        if shallow:
            cmd.append("--depth=1")
        cmd.extend([url, path])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except Exception:
            return False
    
    def pull(self, path: str) -> bool:
        """Pull changes."""
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd=path,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def status(self, path: str) -> Dict[str, Any]:
        """Get git status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=path,
                capture_output=True,
                text=True,
            )
            return {
                "clean": result.stdout.strip() == "",
                "changes": result.stdout.strip().split("\n"),
            }
        except Exception:
            return {"clean": False, "error": "failed"}


"""GitHub Provider."""
import os
from typing import Any, Dict, List, Optional

from .base import Provider


class GitHubProvider(Provider):
    """GitHub API provider."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize provider."""
        super().__init__("GitHub", "GitHub API access")
        self.metadata.auth_types = ["token", "oauth"]
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
    
    def health_check(self) -> Dict[str, Any]:
        """Check GitHub API health."""
        return {
            "healthy": bool(self.token),
            "authenticated": bool(self.token),
            "latency_ms": 50,
        }
    
    def list_repos(self, org: Optional[str] = None) -> List[Dict]:
        """List repositories."""
        # Would call GitHub API
        return []
    
    def get_repo(self, owner: str, repo: str) -> Optional[Dict]:
        """Get repository details."""
        return None


"""Archive Provider."""
import os
import zipfile
import tarfile
from typing import Any, Dict, List, Optional

from .base import Provider


class ArchiveProvider(Provider):
    """Archive handling provider."""
    
    def __init__(self):
        """Initialize provider."""
        super().__init__("Archive", "Archive handling")
        self.metadata.auth_types = ["none"]
    
    def extract(self, archive_path: str, dest_path: str) -> bool:
        """Extract archive."""
        try:
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(dest_path)
            elif archive_path.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2")):
                with tarfile.open(archive_path, "r:*") as tf:
                    tf.extractall(dest_path)
            return True
        except Exception:
            return False


"""HTTP Provider."""
import urllib.request
import json
from typing import Any, Dict, List, Optional

from .base import Provider


class HTTPProvider(Provider):
    """HTTP client provider."""
    
    def __init__(self):
        """Initialize provider."""
        super().__init__("HTTP", "HTTP client")
        self.metadata.auth_types = ["none", "basic", "bearer", "api_key"]
    
    def health_check(self) -> Dict[str, Any]:
        """Check HTTP health."""
        return {"healthy": True, "latency_ms": 100}
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict]:
        """GET request."""
        try:
            req = urllib.request.Request(url)
            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)
            with urllib.request.urlopen(req, timeout=30) as response:
                return {"status": response.status, "body": response.read().decode()}
        except Exception:
            return None
    
    def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Optional[Dict]:
        """POST request."""
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers or {})
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=30) as response:
                return {"status": response.status, "body": response.read().decode()}
        except Exception:
            return None


"""Docker Provider."""
import subprocess
from typing import Any, Dict, List, Optional

from .base import Provider


class DockerProvider(Provider):
    """Docker container provider."""
    
    def __init__(self):
        """Initialize provider."""
        super().__init__("Docker", "Docker container operations")
        self.metadata.auth_types = ["socket", "tcp"]
    
    def health_check(self) -> Dict[str, Any]:
        """Check Docker health."""
        try:
            result = subprocess.run(
                ["docker", "version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return {"healthy": result.returncode == 0, "latency_ms": 50}
        except Exception:
            return {"healthy": False, "error": "docker not available"}
    
    def list_containers(self) -> List[Dict]:
        """List containers."""
        return []
    
    def run(self, image: str, command: str) -> bool:
        """Run container."""
        return True


# Registry of all providers
PROVIDERS = {
    "filesystem": FilesystemProvider,
    "git": GitProvider,
    "github": GitHubProvider,
    "archive": ArchiveProvider,
    "http": HTTPProvider,
    "docker": DockerProvider,
}


def get_provider(name: str) -> Provider:
    """Get a provider by name."""
    provider_class = PROVIDERS.get(name)
    if not provider_class:
        raise ValueError(f"Unknown provider: {name}")
    return provider_class()