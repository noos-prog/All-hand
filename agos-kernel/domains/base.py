"""AGOS Domain Base."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DomainStatus(Enum):
    """Domain status."""
    DRAFT = "draft"
    DEVELOPMENT = "development"
    TESTING = "testing"
    CERTIFIED = "certified"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"


@dataclass
class DomainMetadata:
    """Domain metadata."""
    id: str
    name: str
    version: str = "1.0.0"
    author: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class DomainCapability:
    """A capability contributed by domain."""
    name: str
    version: str
    description: str


@dataclass
class DomainKnowledgePack:
    """A knowledge pack contributed by domain."""
    name: str
    version: str
    content: Dict[str, Any]


@dataclass
class DomainPolicy:
    """A policy contributed by domain."""
    name: str
    version: str
    rules: List[Dict]


@dataclass
class DomainWorkflow:
    """A workflow contributed by domain."""
    name: str
    version: str
    steps: List[Dict]


class Domain:
    """Base domain class."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize domain."""
        self.metadata = DomainMetadata(
            id=f"domain-{uuid.uuid4().hex[:8]}",
            name=name,
            description=description,
        )
        self.status = DomainStatus.DRAFT
        self.capabilities: List[DomainCapability] = []
        self.knowledge_packs: List[DomainKnowledgePack] = []
        self.policies: List[DomainPolicy] = []
        self.workflows: List[DomainWorkflow] = []
    
    def contribute_capability(self, name: str, version: str, description: str) -> None:
        """Contribute a capability."""
        self.capabilities.append(DomainCapability(name, version, description))
    
    def contribute_knowledge(self, name: str, version: str, content: Dict) -> None:
        """Contribute knowledge."""
        self.knowledge_packs.append(DomainKnowledgePack(name, version, content))
    
    def contribute_policy(self, name: str, version: str, rules: List[Dict]) -> None:
        """Contribute a policy."""
        self.policies.append(DomainPolicy(name, version, rules))
    
    def contribute_workflow(self, name: str, version: str, steps: List[Dict]) -> None:
        """Contribute a workflow."""
        self.workflows.append(DomainWorkflow(name, version, steps))


class DomainRegistry:
    """Registry for all domains."""
    
    def __init__(self):
        """Initialize registry."""
        self.domains: Dict[str, Domain] = {}
    
    def register(self, domain: Domain) -> None:
        """Register a domain."""
        self.domains[domain.metadata.id] = domain
    
    def get(self, domain_id: str) -> Optional[Domain]:
        """Get a domain."""
        return self.domains.get(domain_id)
    
    def list_all(self) -> List[Domain]:
        """List all domains."""
        return list(self.domains.values())


# Global registry
_registry = DomainRegistry()


def get_registry() -> DomainRegistry:
    """Get the global domain registry."""
    return _registry