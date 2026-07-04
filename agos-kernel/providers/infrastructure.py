"""Infrastructure Providers (26-40)."""
import os
from typing import Any, Dict, List, Optional
from .base import Provider


# ============ PROVIDER-000027: Azure DevOps Provider ============
class AzureDevOpsProvider(Provider):
    """Azure DevOps provider."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("AzureDevOps", "Azure DevOps API")
        self.token = token or os.environ.get("AZURE_DEVOPS_TOKEN", "")
        self.metadata.auth_types = ["token"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": bool(self.token), "authenticated": bool(self.token)}


# ============ PROVIDER-000028: Jenkins Provider ============
class JenkinsProvider(Provider):
    """Jenkins CI provider."""
    
    def __init__(self, url: str = "http://localhost:8080"):
        super().__init__("Jenkins", "Jenkins CI")
        self.url = url
        self.metadata.auth_types = ["basic"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True, "url": self.url}


# ============ PROVIDER-000029: GitHub Actions Provider ============
class GitHubActionsProvider(Provider):
    """GitHub Actions provider."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("GitHubActions", "GitHub Actions")
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.metadata.auth_types = ["token"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True, "authenticated": bool(self.token)}


# ============ PROVIDER-000030: GitLab CI Provider ============
class GitLabCIProvider(Provider):
    """GitLab CI provider."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("GitLabCI", "GitLab CI")
        self.token = token or os.environ.get("GITLAB_TOKEN", "")
        self.metadata.auth_types = ["token"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True, "authenticated": bool(self.token)}


# ============ PROVIDER-000031: CircleCI Provider ============
class CircleCIProvider(Provider):
    """CircleCI provider."""
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("CircleCI", "CircleCI")
        self.token = token or os.environ.get("CIRCLECI_TOKEN", "")
        self.metadata.auth_types = ["token"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": bool(self.token)}


# ============ PROVIDER-000032: ArgoCD Provider ============
class ArgoCDProvider(Provider):
    """ArgoCD provider."""
    
    def __init__(self, url: str = "http://localhost:8080"):
        super().__init__("ArgoCD", "ArgoCD GitOps")
        self.url = url
        self.metadata.auth_types = ["token"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True, "url": self.url}


# ============ PROVIDER-000033: Helm Provider ============
class HelmProvider(Provider):
    """Helm provider."""
    
    def __init__(self):
        super().__init__("Helm", "Helm package manager")
        self.metadata.auth_types = ["none"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000034: Kubernetes Provider ============
class KubernetesProvider(Provider):
    """Kubernetes provider."""
    
    def __init__(self, kubeconfig: Optional[str] = None):
        super().__init__("Kubernetes", "Kubernetes cluster")
        self.kubeconfig = kubeconfig or os.environ.get("KUBECONFIG", "")
        self.metadata.auth_types = ["kubeconfig", "service_account"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000035: Terraform Provider ============
class TerraformProvider(Provider):
    """Terraform provider."""
    
    def __init__(self):
        super().__init__("Terraform", "Terraform IaC")
        self.metadata.auth_types = ["none"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000036: Ansible Provider ============
class AnsibleProvider(Provider):
    """Ansible provider."""
    
    def __init__(self):
        super().__init__("Ansible", "Ansible automation")
        self.metadata.auth_types = ["ssh_key"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000037: PostgreSQL Provider ============
class PostgreSQLProvider(Provider):
    """PostgreSQL provider."""
    
    def __init__(self, connection_string: Optional[str] = None):
        super().__init__("PostgreSQL", "PostgreSQL database")
        self.connection_string = connection_string or os.environ.get("DATABASE_URL", "")
        self.metadata.auth_types = ["password", "certificate"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000038: MySQL Provider ============
class MySQLProvider(Provider):
    """MySQL provider."""
    
    def __init__(self, connection_string: Optional[str] = None):
        super().__init__("MySQL", "MySQL database")
        self.connection_string = connection_string or ""
        self.metadata.auth_types = ["password", "certificate"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000039: MongoDB Provider ============
class MongoDBProvider(Provider):
    """MongoDB provider."""
    
    def __init__(self, connection_string: Optional[str] = None):
        super().__init__("MongoDB", "MongoDB database")
        self.connection_string = connection_string or os.environ.get("MONGODB_URI", "")
        self.metadata.auth_types = ["password", "certificate"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# ============ PROVIDER-000040: Redis Provider ============
class RedisProvider(Provider):
    """Redis provider."""
    
    def __init__(self, connection_string: Optional[str] = None):
        super().__init__("Redis", "Redis cache")
        self.connection_string = connection_string or os.environ.get("REDIS_URL", "")
        self.metadata.auth_types = ["password"]
    
    def health_check(self) -> Dict[str, Any]:
        return {"healthy": True}


# Registry
INFRA_PROVIDERS = {
    "azure_devops": AzureDevOpsProvider,
    "jenkins": JenkinsProvider,
    "github_actions": GitHubActionsProvider,
    "gitlab_ci": GitLabCIProvider,
    "circleci": CircleCIProvider,
    "argocd": ArgoCDProvider,
    "helm": HelmProvider,
    "kubernetes": KubernetesProvider,
    "terraform": TerraformProvider,
    "ansible": AnsibleProvider,
    "postgresql": PostgreSQLProvider,
    "mysql": MySQLProvider,
    "mongodb": MongoDBProvider,
    "redis": RedisProvider,
}


def get_infra_provider(name: str) -> Provider:
    """Get an infrastructure provider."""
    provider_class = INFRA_PROVIDERS.get(name)
    if not provider_class:
        raise ValueError(f"Unknown infrastructure provider: {name}")
    return provider_class()