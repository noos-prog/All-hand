"""Infrastructure Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000025: Terraform Adapter
class TerraformAdapter(Adapter):
    """Terraform IaC adapter."""
    
    def __init__(self):
        super().__init__("Terraform", "terraform", "HashiCorp Terraform")
        self.metadata.capabilities = ["plan", "apply", "destroy", "validate"]


# ADAPTER-000026: OpenTofu Adapter
class OpenTofuAdapter(Adapter):
    """OpenTofu IaC adapter."""
    
    def __init__(self):
        super().__init__("OpenTofu", "opentofu", "OpenTofu IaC")
        self.metadata.capabilities = ["plan", "apply", "destroy"]


# ADAPTER-000027: Ansible Adapter
class AnsibleAdapter(Adapter):
    """Ansible automation adapter."""
    
    def __init__(self):
        super().__init__("Ansible", "ansible", "Ansible Automation Platform")
        self.metadata.auth_types = ["ssh_key", "password"]
        self.metadata.capabilities = ["playbook", "ad-hoc", "inventory"]


# ADAPTER-000028: Pulumi Adapter
class PulumiAdapter(Adapter):
    """Pulumi IaC adapter."""
    
    def __init__(self):
        super().__init__("Pulumi", "pulumi", "Pulumi Infrastructure as Code")
        self.metadata.capabilities = ["up", "preview", "destroy"]


# Registry
INFRASTRUCTURE_ADAPTERS = {
    "terraform": TerraformAdapter,
    "opentofu": OpenTofuAdapter,
    "ansible": AnsibleAdapter,
    "pulumi": PulumiAdapter,
}


def get_adapter(name: str):
    """Get an infrastructure adapter."""
    adapter_class = INFRASTRUCTURE_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()