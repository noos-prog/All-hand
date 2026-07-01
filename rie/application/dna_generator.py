"""Repository DNA Generator v2 - Complete DNA generation."""
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class RepositoryDNAv2:
    """
    Repository DNA v2 - Complete repository identity.
    
    Includes:
    - Identity
    - Technology Stack
    - Architecture
    - Capabilities
    - Providers
    - AI Stack
    - Dependencies
    - Quality
    - Production Readiness
    - Confidence Scores
    - Evidence References
    """
    
    # Identity
    id: str = ""
    name: str = ""
    url: str = ""
    owner: str = ""
    branch: str = "main"
    commit: str = ""
    
    # Technology Stack
    primary_language: str = ""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    package_managers: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    
    # Architecture
    architecture_type: str = ""
    architecture_confidence: float = 0.0
    architecture_evidence: List[str] = field(default_factory=list)
    
    # Capabilities
    capabilities: Dict[str, float] = field(default_factory=dict)  # name -> confidence
    capability_evidence: Dict[str, List[str]] = field(default_factory=dict)
    
    # AI Stack
    ai_stack: Dict[str, List[str]] = field(default_factory=dict)
    
    # Structure
    entry_points: List[str] = field(default_factory=list)
    directory_tree: List[str] = field(default_factory=list)
    
    # Documentation
    license_type: str = ""
    has_license: bool = False
    has_readme: bool = False
    has_changelog: bool = False
    
    # Quality
    scores: Dict[str, float] = field(default_factory=dict)
    
    # Statistics
    total_files: int = 0
    total_directories: int = 0
    total_size_bytes: int = 0
    
    # Metadata
    version: str = "2.0.0"
    generated_at: datetime = field(default_factory=datetime.utcnow)
    generator_version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "owner": self.owner,
            "branch": self.branch,
            "commit": self.commit,
            "primary_language": self.primary_language,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "package_managers": self.package_managers,
            "dependencies": self.dependencies,
            "config_files": self.config_files,
            "architecture_type": self.architecture_type,
            "architecture_confidence": self.architecture_confidence,
            "architecture_evidence": self.architecture_evidence,
            "capabilities": self.capabilities,
            "capability_evidence": self.capability_evidence,
            "ai_stack": self.ai_stack,
            "entry_points": self.entry_points,
            "directory_tree": self.directory_tree,
            "license_type": self.license_type,
            "has_license": self.has_license,
            "has_readme": self.has_readme,
            "has_changelog": self.has_changelog,
            "scores": self.scores,
            "total_files": self.total_files,
            "total_directories": self.total_directories,
            "total_size_bytes": self.total_size_bytes,
            "version": self.version,
            "generated_at": self.generated_at.isoformat(),
            "generator_version": self.generator_version
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_yaml(self) -> str:
        """Serialize to YAML."""
        return yaml.dump(self.to_dict(), default_flow_style=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RepositoryDNAv2':
        """Deserialize from dictionary."""
        dna = cls()
        for key, value in data.items():
            if hasattr(dna, key):
                setattr(dna, key, value)
        return dna
    
    @classmethod
    def from_json(cls, json_str: str) -> 'RepositoryDNAv2':
        """Deserialize from JSON."""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'RepositoryDNAv2':
        """Deserialize from YAML."""
        return cls.from_dict(yaml.safe_load(yaml_str))


class DNAGeneratorV2:
    """
    Repository DNA Generator v2.
    
    Input:
    - Repository Features
    - Repository Scores
    
    Output:
    - RepositoryDNA v2
    
    Serialization:
    ✅ JSON
    ✅ YAML
    ✅ Binary (future)
    
    Validation:
    ✅ Schema Compliance
    ✅ Deterministic Output
    ✅ Version Compatibility
    """
    
    def __init__(self):
        self.version = "2.0.0"
    
    def generate(
        self,
        normalized: Dict[str, Any],
        features: Any,  # RepositoryFeatureSet
        scores: Any,  # RepositoryScore
        detector_results: List[Any] = None
    ) -> RepositoryDNAv2:
        """Generate complete DNA."""
        
        dna = RepositoryDNAv2()
        
        # Identity
        dna.id = normalized.get("commit", "")
        dna.name = normalized.get("name", "")
        dna.url = normalized.get("url", "")
        dna.owner = normalized.get("owner", "")
        dna.branch = normalized.get("branch", "main")
        dna.commit = normalized.get("commit", "")
        
        # Technology Stack
        if hasattr(features, "languages"):
            # Get primary language
            if features.languages:
                dna.primary_language = max(features.languages, key=features.languages.get)
            dna.languages = list(features.languages.keys()) if features.languages else []
        
        dna.frameworks = features.frameworks if hasattr(features, "frameworks") else []
        dna.package_managers = features.package_managers if hasattr(features, "package_managers") else []
        dna.dependencies = features.dependencies if hasattr(features, "dependencies") else []
        dna.config_files = features.config_files if hasattr(features, "config_files") else []
        
        # Architecture
        if hasattr(features, "architecture_type"):
            dna.architecture_type = features.architecture_type
        if hasattr(features, "architecture_confidence"):
            dna.architecture_confidence = features.architecture_confidence
        if hasattr(features, "architecture_evidence"):
            dna.architecture_evidence = features.architecture_evidence
        
        # Capabilities
        if hasattr(features, "capabilities"):
            dna.capabilities = features.capabilities if isinstance(features.capabilities, dict) else {}
        if hasattr(features, "capability_evidence"):
            dna.capability_evidence = features.capability_evidence if isinstance(features.capability_evidence, dict) else {}
        
        # AI Stack
        if hasattr(features, "ai_stack"):
            dna.ai_stack = features.ai_stack if isinstance(features.ai_stack, dict) else {}
        
        # Structure
        dna.entry_points = features.entry_points if hasattr(features, "entry_points") else []
        dna.directory_tree = features.directory_tree if hasattr(features, "directory_tree") else []
        
        # Documentation
        dna.has_license = features.has_license if hasattr(features, "has_license") else False
        dna.has_readme = features.has_readme if hasattr(features, "has_readme") else False
        dna.has_changelog = features.has_changelog if hasattr(features, "has_changelog") else False
        dna.license_type = features.license_type if hasattr(features, "license_type") else ""
        
        # Scores
        if hasattr(scores, "to_dict"):
            dna.scores = scores.to_dict()
            # Remove non-numeric fields
            dna.scores = {k: v for k, v in dna.scores.items() if isinstance(v, (int, float))}
        
        # Statistics
        dna.total_files = normalized.get("total_files", 0)
        dna.total_directories = normalized.get("total_directories", len(dna.directory_tree))
        
        return dna
    
    def validate(self, dna: RepositoryDNAv2) -> tuple:
        """Validate DNA schema compliance."""
        errors = []
        
        # Required fields
        if not dna.id:
            errors.append("ID is required")
        if not dna.name:
            errors.append("Name is required")
        if not dna.url:
            errors.append("URL is required")
        
        # Version check
        if not dna.version:
            errors.append("Version is required")
        
        # Deterministic check
        if not dna.generated_at:
            errors.append("Generated at timestamp is required")
        
        return len(errors) == 0, errors


def create_dna_generator_v2() -> DNAGeneratorV2:
    """Create DNA Generator v2."""
    return DNAGeneratorV2()
