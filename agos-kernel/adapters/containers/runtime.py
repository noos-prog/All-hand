"""Container Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000019: Docker Adapter
class DockerAdapter(Adapter):
    """Docker container adapter."""
    
    def __init__(self):
        super().__init__("Docker", "docker", "Docker Container Runtime")
        self.metadata.auth_types = ["socket", "tcp"]
        self.metadata.capabilities = ["build", "run", "push", "pull", "compose"]


# ADAPTER-000020: Podman Adapter
class PodmanAdapter(Adapter):
    """Podman container adapter."""
    
    def __init__(self):
        super().__init__("Podman", "podman", "Podman Container Engine")
        self.metadata.auth_types = ["socket"]
        self.metadata.capabilities = ["build", "run", "push", "pull"]


# ADAPTER-000021: containerd Adapter
class ContainerdAdapter(Adapter):
    """containerd container adapter."""
    
    def __init__(self):
        super().__init__("containerd", "containerd", "containerd Container Runtime")


# Registry
CONTAINER_ADAPTERS = {
    "docker": DockerAdapter,
    "podman": PodmanAdapter,
    "containerd": ContainerdAdapter,
}


def get_adapter(name: str):
    """Get a container adapter."""
    adapter_class = CONTAINER_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()