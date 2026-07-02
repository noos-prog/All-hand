"""Universal Integration Layer - Any platform without kernel modifications."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict

ADAPTERS = [
    # Version Control
    "GitHub", "GitLab", "Bitbucket", "Azure DevOps",
    # Project Management
    "Jira", "Linear", "Notion",
    # Communication
    "Slack", "Discord", "Microsoft Teams",
    # Storage
    "Google Drive", "Figma",
    # Infrastructure
    "Docker Hub", "Kubernetes", "AWS", "Azure", "GCP", "Cloudflare",
    # Deployment
    "Vercel", "Netlify", "Railway",
    # Databases
    "Supabase", "Firebase", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    # Vector DBs
    "Qdrant", "Milvus", "Pinecone", "Weaviate",
    # AI
    "MCP Servers"
]

@dataclass
class IntegrationConfig:
    adapter_name: str
    endpoint: str
    credentials: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True

class IIntegrationAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def connect(self, config: IntegrationConfig) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        pass

class BaseIntegrationAdapter(IIntegrationAdapter):
    def __init__(self, name: str):
        self._name = name
        self._connected = False
    
    @property
    def name(self) -> str:
        return self._name
    
    def connect(self, config: IntegrationConfig) -> bool:
        self._connected = True
        return True
    
    def disconnect(self) -> bool:
        self._connected = False
        return True
    
    def health_check(self) -> bool:
        return self._connected

class IntegrationRegistry:
    """
    Integration Registry.
    Rules:
    ✅ Every integration is an Adapter
    ✅ Every adapter is isolated
    ✅ Adapters cannot access Kernel internals
    ✅ Adapters communicate through contracts only
    """
    def __init__(self):
        self._adapters: Dict[str, IIntegrationAdapter] = {}
    
    def register(self, adapter: IIntegrationAdapter) -> None:
        self._adapters[adapter.name] = adapter
    
    def get(self, name: str) -> IIntegrationAdapter:
        return self._adapters.get(name)
    
    def list_all(self) -> list:
        return list(self._adapters.keys())
    
    def health_check_all(self) -> Dict[str, bool]:
        return {name: a.health_check() for name, a in self._adapters.items()}
