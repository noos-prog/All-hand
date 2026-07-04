"""
Engineering Intelligence Package Schema
PHASE-02: EXECUTION-000003 - Engineering Intelligence Pipeline

Defines the structure of the Engineering Intelligence Package.
Every capability consumes this package.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class TrustLevel(Enum):
    """Trust levels for repositories."""
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    TRUSTED = "trusted"


class RiskLevel(Enum):
    """Risk levels for repositories."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class RepositoryIdentity:
    """Repository identity information."""
    name: str = ""
    full_name: str = ""
    description: str = ""
    url: str = ""
    default_branch: str = "main"
    language: str = ""
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    size_bytes: int = 0
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    watchers: int = 0
    license: str = ""
    topics: List[str] = field(default_factory=list)


@dataclass
class RepositoryDNA:
    """Repository DNA - unique fingerprint."""
    version: str = "1.0"
    structure_hash: str = ""
    code_hash: str = ""
    config_hash: str = ""
    dependency_hash: str = ""
    combined_hash: str = ""
    signature: str = ""


@dataclass
class TechnologyStack:
    """Technology stack information."""
    languages: Dict[str, int] = field(default_factory=dict)  # language -> bytes
    frameworks: List[str] = field(default_factory=list)
    build_systems: List[str] = field(default_factory=list)
    runtimes: List[str] = field(default_factory=list)
    databases: List[str] = field(default_factory=list)
    message_queues: List[str] = field(default_factory=list)
    cloud_providers: List[str] = field(default_factory=list)


@dataclass
class ArchitectureSummary:
    """Architecture summary."""
    pattern: str = ""  # monolith, microservices, serverless, etc.
    layers: List[str] = field(default_factory=list)
    modules: int = 0
    packages: int = 0
    services: int = 0
    components: int = 0
    entry_points: List[str] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Dependency information."""
    total_count: int = 0
    direct_dependencies: List[Dict] = field(default_factory=list)
    dev_dependencies: List[Dict] = field(default_factory=list)
    internal_dependencies: List[str] = field(default_factory=list)
    external_dependencies: List[Dict] = field(default_factory=list)


@dataclass
class QualityProfile:
    """Quality profile."""
    overall_score: float = 0.0
    documentation_score: float = 0.0
    complexity_score: float = 0.0
    test_coverage: float = 0.0
    grade: str = "N/A"
    issues_count: int = 0
    code_smells: int = 0
    duplicated_lines: int = 0


@dataclass
class SecurityProfile:
    """Security profile."""
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = 100.0
    vulnerabilities_critical: int = 0
    vulnerabilities_high: int = 0
    vulnerabilities_medium: int = 0
    vulnerabilities_low: int = 0
    hardcoded_secrets: List[Dict] = field(default_factory=list)
    insecure_patterns: List[Dict] = field(default_factory=list)


@dataclass
class PerformanceProfile:
    """Performance profile."""
    startup_time_ms: float = 0.0
    memory_usage_mb: float = 0.0
    complexity_avg: float = 0.0
    complexity_max: int = 0
    long_functions: int = 0


@dataclass
class TestingProfile:
    """Testing profile."""
    test_files: int = 0
    test_functions: int = 0
    coverage_percent: float = 0.0
    has_ci: bool = False
    ci_systems: List[str] = field(default_factory=list)


@dataclass
class DocumentationProfile:
    """Documentation profile."""
    has_readme: bool = False
    has_contributing: bool = False
    has_license: bool = False
    has_changelog: bool = False
    has_api_docs: bool = False
    documentation_score: float = 0.0


@dataclass
class EvidencePackage:
    """Immutable evidence package."""
    version: str = "1.0"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    evidence_id: str = ""
    artifacts: List[Dict] = field(default_factory=list)
    verifications: List[Dict] = field(default_factory=list)
    signatures: List[str] = field(default_factory=list)


@dataclass
class Recommendation:
    """Improvement recommendation."""
    priority: str = "low"  # critical, high, medium, low
    category: str = ""
    title: str = ""
    description: str = ""
    effort_hours: float = 0.0
    impact: str = ""


@dataclass
class EngineeringIntelligencePackage:
    """
    Engineering Intelligence Package.
    
    The universal engineering language of AGOS.
    Every capability consumes this package.
    """
    
    # Metadata
    version: str = "1.0"
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    pipeline_version: str = "1.0"
    
    # Core Identity
    identity: RepositoryIdentity = field(default_factory=RepositoryIdentity)
    dna: RepositoryDNA = field(default_factory=RepositoryDNA)
    
    # Analysis Results
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    architecture_summary: ArchitectureSummary = field(default_factory=ArchitectureSummary)
    dependency_info: DependencyInfo = field(default_factory=DependencyInfo)
    
    # Profiles
    quality_profile: QualityProfile = field(default_factory=QualityProfile)
    security_profile: SecurityProfile = field(default_factory=SecurityProfile)
    performance_profile: PerformanceProfile = field(default_factory=PerformanceProfile)
    testing_profile: TestingProfile = field(default_factory=TestingProfile)
    documentation_profile: DocumentationProfile = field(default_factory=DocumentationProfile)
    
    # Knowledge
    knowledge_objects: List[Dict] = field(default_factory=list)
    
    # Evidence
    evidence: EvidencePackage = field(default_factory=EvidencePackage)
    
    # Assessment
    trust_level: TrustLevel = TrustLevel.MEDIUM
    risk_level: RiskLevel = RiskLevel.MEDIUM
    trust_score: float = 50.0
    
    # Recommendations
    recommendations: List[Recommendation] = field(default_factory=list)
    
    # Status
    stages_completed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'version': self.version,
            'generated_at': self.generated_at,
            'pipeline_version': self.pipeline_version,
            'identity': self.identity.__dict__,
            'dna': self.dna.__dict__,
            'technology_stack': self.technology_stack.__dict__,
            'architecture_summary': self.architecture_summary.__dict__,
            'dependency_info': self.dependency_info.__dict__,
            'quality_profile': self.quality_profile.__dict__,
            'security_profile': {
                **self.security_profile.__dict__,
                'risk_level': self.security_profile.risk_level.value,
            },
            'performance_profile': self.performance_profile.__dict__,
            'testing_profile': self.testing_profile.__dict__,
            'documentation_profile': self.documentation_profile.__dict__,
            'knowledge_objects': self.knowledge_objects,
            'evidence': self.evidence.__dict__,
            'trust_level': self.trust_level.value,
            'risk_level': self.risk_level.value,
            'trust_score': self.trust_score,
            'recommendations': [r.__dict__ for r in self.recommendations],
            'stages_completed': self.stages_completed,
            'errors': self.errors,
            'warnings': self.warnings,
        }
    
    def add_evidence(self, artifact_type: str, artifact: Dict) -> None:
        """Add immutable evidence."""
        self.evidence.artifacts.append({
            'type': artifact_type,
            'data': artifact,
            'timestamp': datetime.utcnow().isoformat(),
        })
    
    def add_recommendation(self, rec: Recommendation) -> None:
        """Add recommendation."""
        self.recommendations.append(rec)
    
    def mark_stage_complete(self, stage: str) -> None:
        """Mark pipeline stage as complete."""
        if stage not in self.stages_completed:
            self.stages_completed.append(stage)
