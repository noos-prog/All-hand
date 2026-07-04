"""
Provider Contract
PHASE-02: EXECUTION-000007 - Universal Provider Runtime

Every Provider shall expose:
- Provider ID
- Provider Type
- Provider Version
- Supported Capabilities
- Supported Skills
- Supported Protocols
- Authentication Methods
- Authorization Requirements
- Configuration Schema
- Health Endpoints
- Performance Characteristics
- Compatibility Matrix
- Certification Status
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class ProviderType(Enum):
    """Provider types."""
    FILESYSTEM = "filesystem"
    GIT = "git"
    GITHUB = "github"
    GITLAB = "gitlab"
    JENKINS = "jenkins"
    DOCKER = "docker"
    KUBERNETES = "kubernetes"
    DATABASE = "database"
    HTTP = "http"
    GRAPHQL = "graphql"
    REST = "rest"
    WEBSOCKET = "websocket"


class Protocol(Enum):
    """Supported protocols."""
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    GIT = "git"
    FILE = "file"
    TCP = "tcp"
    UDP = "udp"
    WEBSOCKET = "websocket"
    GRAPHQL = "graphql"
    GRPC = "grpc"


class AuthenticationMethod(Enum):
    """Authentication methods."""
    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    SSH_KEY = "ssh_key"
    TOKEN = "token"


class CertificationStatus(Enum):
    """Certification status."""
    UNCERTIFIED = "uncertified"
    CERTIFIED = "certified"
    DEPRECATED = "deprecated"
    BETA = "beta"


@dataclass
class ConfigurationSchema:
    """Configuration schema."""
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    defaults: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthEndpoint:
    """Health endpoint."""
    name: str = ""
    url: str = ""
    method: str = "GET"
    expected_status: int = 200


@dataclass
class PerformanceCharacteristics:
    """Performance characteristics."""
    avg_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    throughput_rps: float = 0.0  # requests per second
    max_concurrent: int = 10


@dataclass
class CompatibilityEntry:
    """Compatibility entry."""
    provider: str = ""
    version: str = ""
    compatible: bool = True
    notes: str = ""


@dataclass
class ProviderContract:
    """
    Provider Contract.
    
    Standardized contract for every Provider.
    """
    
    # Identity
    provider_id: str = ""
    provider_type: ProviderType = ProviderType.HTTP
    name: str = ""
    version: str = "1.0.0"
    
    # Metadata
    description: str = ""
    owner: str = ""
    
    # Capabilities
    supported_capabilities: List[str] = field(default_factory=list)
    supported_skills: List[str] = field(default_factory=list)
    supported_protocols: List[Protocol] = field(default_factory=list)
    
    # Security
    authentication_methods: List[AuthenticationMethod] = field(default_factory=list)
    authorization_requirements: List[str] = field(default_factory=list)
    
    # Configuration
    configuration_schema: ConfigurationSchema = field(default_factory=ConfigurationSchema)
    
    # Health
    health_endpoints: List[HealthEndpoint] = field(default_factory=list)
    
    # Performance
    performance: PerformanceCharacteristics = field(default_factory=PerformanceCharacteristics)
    
    # Compatibility
    compatibility_matrix: List[CompatibilityEntry] = field(default_factory=list)
    
    # Status
    certification_status: CertificationStatus = CertificationStatus.UNCERTIFIED
    certification_date: str = ""
    
    # Lifecycle
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'provider_id': self.provider_id,
            'provider_type': self.provider_type.value if isinstance(self.provider_type, ProviderType) else self.provider_type,
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'owner': self.owner,
            'supported_capabilities': self.supported_capabilities,
            'supported_skills': self.supported_skills,
            'supported_protocols': [p.value if isinstance(p, Protocol) else p for p in self.supported_protocols],
            'authentication_methods': [a.value if isinstance(a, AuthenticationMethod) else a for a in self.authentication_methods],
            'authorization_requirements': self.authorization_requirements,
            'configuration_schema': self.configuration_schema.__dict__,
            'health_endpoints': [h.__dict__ for h in self.health_endpoints],
            'performance': self.performance.__dict__,
            'compatibility_matrix': [c.__dict__ for c in self.compatibility_matrix],
            'certification_status': self.certification_status.value if isinstance(self.certification_status, CertificationStatus) else self.certification_status,
            'certification_date': self.certification_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


@dataclass
class ProviderRegistryEntry:
    """Provider registry entry."""
    contract: ProviderContract
    status: str = "active"  # active, inactive, deprecated
    registered_at: str = ""
    last_used: str = ""
    use_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'contract': self.contract.to_dict(),
            'status': self.status,
            'registered_at': self.registered_at,
            'last_used': self.last_used,
            'use_count': self.use_count,
        }
