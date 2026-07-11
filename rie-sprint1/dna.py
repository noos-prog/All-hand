"""DNA Generation - Generate Repository DNA."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class RepositoryDNAv1:
    """Repository DNA v1."""
    dna_id: str
    version: str = "v1"
    generated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Identity
    repo_name: str = ""
    repo_url: str = ""
    repo_owner: str = ""
    
    # Technology
    primary_language: str = ""
    languages: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    
    # AI Stack
    has_ai_stack: bool = False
    ai_providers: List[str] = field(default_factory=list)
    
    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    
    # Quality
    has_readme: bool = False
    has_license: bool = False
    has_tests: bool = False
    has_ci: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dna_id": self.dna_id,
            "version": self.version,
            "generated_at": self.generated_at.isoformat(),
            "repo_name": self.repo_name,
            "repo_url": self.repo_url,
            "repo_owner": self.repo_owner,
            "primary_language": self.primary_language,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "has_ai_stack": self.has_ai_stack,
            "ai_providers": self.ai_providers,
            "capabilities": self.capabilities,
            "has_readme": self.has_readme,
            "has_license": self.has_license,
            "has_tests": self.has_tests,
            "has_ci": self.has_ci,
        }
    
    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), indent=2)


class DNAGenerator:
    """
    DNA Generator v1.
    
    Generates Repository DNA v1 with:
    ✅ Identity
    ✅ Technology Stack
    ✅ AI Stack
    ✅ Capabilities
    ✅ Quality Indicators
    """
    
    def __init__(self):
        self.version = "1.0.0"
    
    def generate(
        self,
        repo_name: str,
        repo_url: str,
        repo_owner: str,
        languages: Dict[str, int],
        frameworks: List[str],
        ai_stack: Dict[str, List[str]],
        capabilities: List[str],
        quality_flags: Dict[str, bool],
    ) -> RepositoryDNAv1:
        """Generate Repository DNA."""
        # Determine primary language
        primary = max(languages, key=languages.get) if languages else ""
        
        # Check AI stack
        has_ai = bool(ai_stack.get("llm_providers") or ai_stack.get("ml_frameworks"))
        
        dna = RepositoryDNAv1(
            dna_id=str(uuid.uuid4()),
            repo_name=repo_name,
            repo_url=repo_url,
            repo_owner=repo_owner,
            primary_language=primary,
            languages=list(languages.keys()),
            frameworks=frameworks,
            has_ai_stack=has_ai,
            ai_providers=ai_stack.get("llm_providers", []),
            capabilities=capabilities,
            has_readme=quality_flags.get("has_readme", False),
            has_license=quality_flags.get("has_license", False),
            has_tests=quality_flags.get("has_tests", False),
            has_ci=quality_flags.get("has_ci", False),
        )
        
        return dna
