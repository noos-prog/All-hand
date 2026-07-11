"""Repository DNA - Complete repository fingerprint."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json


class DNAVersion(Enum):
    """DNA version."""
    V1 = "v1"
    V2 = "v2"


@dataclass
class Evidence:
    """Evidence for a detection."""
    file_path: str
    line_number: Optional[int] = None
    content: str = ""
    confidence: float = 1.0


@dataclass
class TechnologyStack:
    """Technology stack detected."""
    languages: Dict[str, float] = field(default_factory=dict)  # language -> percentage
    frameworks: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)


@dataclass
class ArchitecturePattern:
    """Architecture pattern detected."""
    pattern_name: str
    confidence: float
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class Capability:
    """A capability detected."""
    capability_name: str
    confidence: float
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class AIStack:
    """AI/ML stack detected."""
    llm_providers: List[str] = field(default_factory=list)
    ml_frameworks: List[str] = field(default_factory=list)
    embedding_models: List[str] = field(default_factory=list)
    vector_databases: List[str] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Dependency information."""
    package_manager: str
    dependencies: List[Dict[str, str]] = field(default_factory=list)
    dev_dependencies: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class DNASection:
    """A section of the DNA."""
    section_name: str
    data: Dict[str, Any]
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class RepositoryDNA:
    """Complete Repository DNA v2."""
    dna_id: str
    version: DNAVersion = DNAVersion.V2
    generated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Identity
    repo_name: str = ""
    repo_url: str = ""
    repo_owner: str = ""
    
    # Technology
    technology_stack: Optional[TechnologyStack] = None
    architecture_patterns: List[ArchitecturePattern] = field(default_factory=list)
    
    # Capabilities
    capabilities: List[Capability] = field(default_factory=list)
    
    # AI Stack
    ai_stack: Optional[AIStack] = None
    
    # Quality Scores
    architecture_score: float = 0.0
    quality_score: float = 0.0
    maintainability_score: float = 0.0
    documentation_score: float = 0.0
    ai_maturity_score: float = 0.0
    production_readiness_score: float = 0.0
    
    # Confidence
    overall_confidence: float = 0.0
    
    # Dependencies
    dependencies: List[DependencyInfo] = field(default_factory=list)
    
    # Evidence
    evidence: List[Evidence] = field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dna_id": self.dna_id,
            "version": self.version.value,
            "generated_at": self.generated_at.isoformat(),
            "identity": {
                "repo_name": self.repo_name,
                "repo_url": self.repo_url,
                "repo_owner": self.repo_owner,
            },
            "technology_stack": {
                "languages": self.technology_stack.languages if self.technology_stack else {},
                "frameworks": self.technology_stack.frameworks if self.technology_stack else [],
                "tools": self.technology_stack.tools if self.technology_stack else [],
            } if self.technology_stack else {},
            "capabilities": [
                {"name": c.capability_name, "confidence": c.confidence}
                for c in self.capabilities
            ],
            "scores": {
                "architecture": self.architecture_score,
                "quality": self.quality_score,
                "maintainability": self.maintainability_score,
                "documentation": self.documentation_score,
                "ai_maturity": self.ai_maturity_score,
                "production_readiness": self.production_readiness_score,
            },
            "overall_confidence": self.overall_confidence,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    def to_yaml(self) -> str:
        import yaml
        return yaml.dump(self.to_dict())
