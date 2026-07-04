"""
Capability Contract
PHASE-02: EXECUTION-000006 - Universal Capability Runtime

Every Capability shall expose:
- Identity
- Version
- Semantic Version
- Owner
- Domain
- Required Skills
- Required Providers
- Required Policies
- Supported Inputs
- Supported Outputs
- Configuration Schema
- Execution Constraints
- Security Requirements
- Performance Targets
- Compatibility Matrix
- Certification Status
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class CapabilityDomain(Enum):
    """Capability domains."""
    SOFTWARE_ENGINEERING = "software_engineering"
    BACKEND_ENGINEERING = "backend_engineering"
    FRONTEND_ENGINEERING = "frontend_engineering"
    DEVOPS_ENGINEERING = "devops_engineering"
    QUALITY_ENGINEERING = "quality_engineering"
    DATA_ENGINEERING = "data_engineering"
    SECURITY_ENGINEERING = "security_engineering"
    KNOWLEDGE_ENGINEERING = "knowledge_engineering"
    ML_ENGINEERING = "ml_engineering"


class ExecutionMode(Enum):
    """Execution modes."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"
    LONG_RUNNING = "long_running"
    INTERRUPTIBLE = "interruptible"
    DISTRIBUTED = "distributed"
    RETRYABLE = "retryable"
    RECOVERABLE = "recoverable"


class CertificationStatus(Enum):
    """Certification status."""
    UNCERTIFIED = "uncertified"
    CERTIFIED = "certified"
    DEPRECATED = "deprecated"
    BETA = "beta"


@dataclass
class InputSpec:
    """Input specification."""
    name: str = ""
    type: str = ""  # string, number, object, array, file
    required: bool = True
    description: str = ""


@dataclass
class OutputSpec:
    """Output specification."""
    name: str = ""
    type: str = ""
    description: str = ""


@dataclass
class ConfigurationSchema:
    """Configuration schema."""
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    defaults: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionConstraint:
    """Execution constraint."""
    type: str = ""  # timeout, memory, cpu, network
    value: Any = None
    unit: str = ""


@dataclass
class SecurityRequirement:
    """Security requirement."""
    type: str = ""  # authentication, authorization, encryption
    level: str = "low"  # low, medium, high
    description: str = ""


@dataclass
class PerformanceTarget:
    """Performance target."""
    metric: str = ""  # latency, throughput, memory
    target: float = 0.0
    unit: str = ""


@dataclass
class CompatibilityEntry:
    """Compatibility entry."""
    capability: str = ""
    version: str = ""
    compatible: bool = True
    notes: str = ""


@dataclass
class CapabilityContract:
    """
    Capability Contract.
    
    Standardized contract for every Capability.
    """
    
    # Identity
    identity: str = ""
    name: str = ""
    version: str = "1.0.0"
    semantic_version: str = "1.0.0"  # MAJOR.MINOR.PATCH
    
    # Metadata
    owner: str = ""
    domain: CapabilityDomain = CapabilityDomain.SOFTWARE_ENGINEERING
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    # Requirements
    required_skills: List[str] = field(default_factory=list)
    required_providers: List[str] = field(default_factory=list)
    required_policies: List[str] = field(default_factory=list)
    
    # I/O
    supported_inputs: List[InputSpec] = field(default_factory=list)
    supported_outputs: List[OutputSpec] = field(default_factory=list)
    
    # Configuration
    configuration_schema: ConfigurationSchema = field(default_factory=ConfigurationSchema)
    
    # Constraints
    execution_constraints: List[ExecutionConstraint] = field(default_factory=list)
    security_requirements: List[SecurityRequirement] = field(default_factory=list)
    
    # Performance
    performance_targets: List[PerformanceTarget] = field(default_factory=list)
    
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
            'identity': self.identity,
            'name': self.name,
            'version': self.version,
            'semantic_version': self.semantic_version,
            'owner': self.owner,
            'domain': self.domain.value if isinstance(self.domain, CapabilityDomain) else self.domain,
            'description': self.description,
            'tags': self.tags,
            'required_skills': self.required_skills,
            'required_providers': self.required_providers,
            'required_policies': self.required_policies,
            'supported_inputs': [i.__dict__ for i in self.supported_inputs],
            'supported_outputs': [o.__dict__ for o in self.supported_outputs],
            'configuration_schema': self.configuration_schema.__dict__,
            'execution_constraints': [c.__dict__ for c in self.execution_constraints],
            'security_requirements': [s.__dict__ for s in self.security_requirements],
            'performance_targets': [p.__dict__ for p in self.performance_targets],
            'compatibility_matrix': [c.__dict__ for c in self.compatibility_matrix],
            'certification_status': self.certification_status.value if isinstance(self.certification_status, CertificationStatus) else self.certification_status,
            'certification_date': self.certification_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


@dataclass
class CapabilityRegistryEntry:
    """Capability registry entry."""
    contract: CapabilityContract = field(default_factory=CapabilityContract)
    status: str = "active"  # active, inactive, deprecated
    loaded_at: str = ""
    execution_count: int = 0
    last_executed: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'contract': self.contract.to_dict(),
            'status': self.status,
            'loaded_at': self.loaded_at,
            'execution_count': self.execution_count,
            'last_executed': self.last_executed,
        }