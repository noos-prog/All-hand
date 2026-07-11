"""Quality Scores for repositories."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class QualityScores:
    """Quality scores for a repository."""
    architecture: float = 0.0
    quality: float = 0.0
    maintainability: float = 0.0
    documentation: float = 0.0
    plugin_readiness: float = 0.0
    ai_maturity: float = 0.0
    capability_coverage: float = 0.0
    
    def get_overall(self) -> float:
        scores = [
            self.architecture,
            self.quality,
            self.maintainability,
            self.documentation,
            self.plugin_readiness,
            self.ai_maturity,
            self.capability_coverage,
        ]
        return sum(scores) / len(scores)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "architecture": self.architecture,
            "quality": self.quality,
            "maintainability": self.maintainability,
            "documentation": self.documentation,
            "plugin_readiness": self.plugin_readiness,
            "ai_maturity": self.ai_maturity,
            "capability_coverage": self.capability_coverage,
            "overall": self.get_overall(),
        }


@dataclass
class ProductionReadiness:
    """Production readiness assessment."""
    has_cicd: bool = False
    has_testing: bool = False
    has_documentation: bool = False
    has_monitoring: bool = False
    has_security: bool = False
    has_error_handling: bool = False
    has_logging: bool = False
    has_containerization: bool = False
    
    def get_score(self) -> float:
        factors = [
            self.has_cicd,
            self.has_testing,
            self.has_documentation,
            self.has_monitoring,
            self.has_security,
            self.has_error_handling,
            self.has_logging,
            self.has_containerization,
        ]
        return sum(factors) / len(factors) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "has_cicd": self.has_cicd,
            "has_testing": self.has_testing,
            "has_documentation": self.has_documentation,
            "has_monitoring": self.has_monitoring,
            "has_security": self.has_security,
            "has_error_handling": self.has_error_handling,
            "has_logging": self.has_logging,
            "has_containerization": self.has_containerization,
            "score": self.get_score(),
        }
