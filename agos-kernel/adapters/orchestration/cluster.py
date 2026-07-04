"""Orchestration Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000022: Kubernetes Adapter
class KubernetesAdapter(Adapter):
    """Kubernetes orchestration adapter."""
    
    def __init__(self):
        super().__init__("Kubernetes", "kubernetes", "Kubernetes Container Orchestration")
        self.metadata.auth_types = ["kubeconfig", "service_account", "token"]
        self.metadata.capabilities = ["deploy", "scale", "rollback", "logs", "exec"]


# ADAPTER-000023: Helm Adapter
class HelmAdapter(Adapter):
    """Helm package manager adapter."""
    
    def __init__(self):
        super().__init__("Helm", "helm", "Helm Kubernetes Package Manager")
        self.metadata.capabilities = ["install", "upgrade", "rollback", "template"]


# ADAPTER-000024: Nomad Adapter
class NomadAdapter(Adapter):
    """Nomad orchestration adapter."""
    
    def __init__(self):
        super().__init__("Nomad", "nomad", "HashiCorp Nomad Orchestration")
        self.metadata.auth_types = ["token"]
        self.metadata.capabilities = ["run", "status", "allocations"]


# Registry
ORCHESTRATION_ADAPTERS = {
    "kubernetes": KubernetesAdapter,
    "helm": HelmAdapter,
    "nomad": NomadAdapter,
}


def get_adapter(name: str):
    """Get an orchestration adapter."""
    adapter_class = ORCHESTRATION_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()