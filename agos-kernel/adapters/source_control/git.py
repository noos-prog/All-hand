"""Source Control Adapters."""
from typing import Any, Dict, List, Optional
from ..base import Adapter


# ADAPTER-000001: Git Adapter
class GitAdapter(Adapter):
    """Git source control adapter."""
    
    def __init__(self):
        super().__init__("Git", "git", "Git version control")
        self.metadata.auth_types = ["ssh_key", "token", "none"]
        self.metadata.capabilities = ["clone", "pull", "push", "branch", "merge", "log", "diff"]
    
    def discover(self) -> List[Dict]:
        """Discover git repositories."""
        return [{"type": "git", "operations": self.metadata.capabilities}]
    
    def health_check(self) -> Dict[str, Any]:
        """Check git health."""
        return {"healthy": True, "version": "2.x", "latency_ms": 5}


# ADAPTER-000002: GitHub Adapter
class GitHubAdapter(Adapter):
    """GitHub source control adapter."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("GitHub", "github", "GitHub API")
        self.token = token
        self.metadata.auth_types = ["token", "oauth", "github_app"]
        self.metadata.capabilities = ["repos", "issues", "prs", "actions", "packages"]
    
    def discover(self) -> List[Dict]:
        """Discover GitHub resources."""
        return [{"type": "github", "capabilities": self.metadata.capabilities}]
    
    def health_check(self) -> Dict[str, Any]:
        """Check GitHub API health."""
        return {"healthy": bool(self.token), "authenticated": bool(self.token)}


# ADAPTER-000003: GitLab Adapter
class GitLabAdapter(Adapter):
    """GitLab source control adapter."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("GitLab", "gitlab", "GitLab API")
        self.token = token
        self.metadata.auth_types = ["token", "oauth"]
        self.metadata.capabilities = ["repos", "issues", "mrs", "ci", "packages"]


# ADAPTER-000004: Bitbucket Adapter
class BitbucketAdapter(Adapter):
    """Bitbucket source control adapter."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("Bitbucket", "bitbucket", "Bitbucket API")
        self.token = token
        self.metadata.auth_types = ["token", "oauth"]


# ADAPTER-000005: Azure DevOps Adapter
class AzureDevOpsAdapter(Adapter):
    """Azure DevOps source control adapter."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("AzureDevOps", "azure_devops", "Azure DevOps API")
        self.token = token
        self.metadata.auth_types = ["token", "pat"]


# ADAPTER-000006: Subversion Adapter
class SubversionAdapter(Adapter):
    """Subversion source control adapter."""
    
    def __init__(self):
        super().__init__("Subversion", "svn", "Subversion version control")
        self.metadata.auth_types = ["username", "password"]


# ADAPTER-000007: Mercurial Adapter
class MercurialAdapter(Adapter):
    """Mercurial source control adapter."""
    
    def __init__(self):
        super().__init__("Mercurial", "hg", "Mercurial version control")


# Registry
SOURCE_CONTROL_ADAPTERS = {
    "git": GitAdapter,
    "github": GitHubAdapter,
    "gitlab": GitLabAdapter,
    "bitbucket": BitbucketAdapter,
    "azure_devops": AzureDevOpsAdapter,
    "subversion": SubversionAdapter,
    "mercurial": MercurialAdapter,
}


def get_adapter(name: str):
    """Get a source control adapter."""
    adapter_class = SOURCE_CONTROL_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()