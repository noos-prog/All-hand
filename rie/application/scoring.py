"""Repository Scoring Engine - Calculates repository scores."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from rie.contracts import RepositoryFeatureSet


@dataclass
class RepositoryScore:
    """Repository score with breakdown."""
    repository_url: str
    
    # Overall scores (0-100)
    overall_score: float = 0.0
    
    # Component scores
    architecture_score: float = 0.0
    quality_score: float = 0.0
    maintainability_score: float = 0.0
    documentation_score: float = 0.0
    plugin_readiness: float = 0.0
    production_readiness: float = 0.0
    ai_maturity: float = 0.0
    capability_coverage: float = 0.0
    
    # Metadata
    calculated_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    
    # Formula details
    formula: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository_url": self.repository_url,
            "overall_score": round(self.overall_score, 2),
            "architecture_score": round(self.architecture_score, 2),
            "quality_score": round(self.quality_score, 2),
            "maintainability_score": round(self.maintainability_score, 2),
            "documentation_score": round(self.documentation_score, 2),
            "plugin_readiness": round(self.plugin_readiness, 2),
            "production_readiness": round(self.production_readiness, 2),
            "ai_maturity": round(self.ai_maturity, 2),
            "capability_coverage": round(self.capability_coverage, 2),
            "calculated_at": self.calculated_at.isoformat(),
            "version": self.version,
            "formula": self.formula
        }


class ScoringEngine:
    """
    Repository Scoring Engine.
    
    Rules:
    ✅ Transparent Formula
    ✅ Deterministic
    ✅ Explainable
    ✅ Versioned
    """
    
    def __init__(self):
        self.version = "1.0.0"
    
    def calculate(self, repository_url: str, features: RepositoryFeatureSet) -> RepositoryScore:
        """Calculate all scores."""
        score = RepositoryScore(repository_url=repository_url)
        
        # Architecture Score
        score.architecture_score = self._calculate_architecture_score(features)
        score.formula["architecture"] = score.architecture_score
        
        # Quality Score
        score.quality_score = self._calculate_quality_score(features)
        score.formula["quality"] = score.quality_score
        
        # Maintainability Score
        score.maintainability_score = self._calculate_maintainability_score(features)
        score.formula["maintainability"] = score.maintainability_score
        
        # Documentation Score
        score.documentation_score = self._calculate_documentation_score(features)
        score.formula["documentation"] = score.documentation_score
        
        # Plugin Readiness
        score.plugin_readiness = self._calculate_plugin_readiness(features)
        score.formula["plugin_readiness"] = score.plugin_readiness
        
        # Production Readiness
        score.production_readiness = self._calculate_production_readiness(features)
        score.formula["production_readiness"] = score.production_readiness
        
        # AI Maturity
        score.ai_maturity = self._calculate_ai_maturity(features)
        score.formula["ai_maturity"] = score.ai_maturity
        
        # Capability Coverage
        score.capability_coverage = self._calculate_capability_coverage(features)
        score.formula["capability_coverage"] = score.capability_coverage
        
        # Overall Score (weighted average)
        score.overall_score = (
            score.architecture_score * 0.15 +
            score.quality_score * 0.15 +
            score.maintainability_score * 0.10 +
            score.documentation_score * 0.10 +
            score.plugin_readiness * 0.15 +
            score.production_readiness * 0.15 +
            score.ai_maturity * 0.10 +
            score.capability_coverage * 0.10
        )
        
        return score
    
    def _calculate_architecture_score(self, features: RepositoryFeatureSet) -> float:
        """Calculate architecture score."""
        score = 50.0  # Base score
        
        # Entry points indicate good architecture
        if features.entry_points:
            score += min(len(features.entry_points) * 5, 20)
        
        # Directory structure indicates organization
        if features.directory_tree:
            score += min(len(features.directory_tree) * 0.5, 15)
        
        # Framework diversity
        if features.frameworks:
            score += min(len(features.frameworks) * 5, 15)
        
        return min(score, 100)
    
    def _calculate_quality_score(self, features: RepositoryFeatureSet) -> float:
        """Calculate quality score."""
        score = 50.0
        
        # Configuration files indicate quality
        if features.config_files:
            score += min(len(features.config_files) * 3, 25)
        
        # Multiple package managers indicate maturity
        if len(features.package_managers) > 1:
            score += 10
        
        # Dependencies count (more = more complex)
        if features.dependencies:
            score += min(len(features.dependencies) * 0.5, 15)
        
        return min(score, 100)
    
    def _calculate_maintainability_score(self, features: RepositoryFeatureSet) -> float:
        """Calculate maintainability score."""
        score = 50.0
        
        # Multiple languages (some penalty for complexity)
        lang_count = len(features.languages)
        if lang_count == 1:
            score += 20
        elif lang_count <= 3:
            score += 10
        else:
            score += 5
        
        # License presence
        if features.has_license:
            score += 15
        
        # Documentation
        if features.has_readme:
            score += 10
        if features.has_changelog:
            score += 5
        
        return min(score, 100)
    
    def _calculate_documentation_score(self, features: RepositoryFeatureSet) -> float:
        """Calculate documentation score."""
        score = 0.0
        
        # README
        if features.has_readme:
            score += 35
        
        # License
        if features.has_license:
            score += 25
        
        # Changelog
        if features.has_changelog:
            score += 20
        
        # Contributing guide (check directory tree)
        if any("contributing" in d.lower() for d in features.directory_tree):
            score += 10
        
        # Docs directory
        if any("docs" in d.lower() for d in features.directory_tree):
            score += 10
        
        return min(score, 100)
    
    def _calculate_plugin_readiness(self, features: RepositoryFeatureSet) -> float:
        """Calculate plugin readiness score."""
        score = 30.0
        
        # Config files indicate extensibility
        if features.config_files:
            score += min(len(features.config_files) * 3, 20)
        
        # Entry points
        if features.entry_points:
            score += min(len(features.entry_points) * 10, 25)
        
        # Plugin-related directories
        plugin_dirs = ["plugins", "extensions", "addons"]
        for d in features.directory_tree:
            if any(pd in d.lower() for pd in plugin_dirs):
                score += 10
        
        # Multiple package managers (more modular)
        if len(features.package_managers) > 1:
            score += 15
        
        return min(score, 100)
    
    def _calculate_production_readiness(self, features: RepositoryFeatureSet) -> float:
        """Calculate production readiness score."""
        score = 30.0
        
        # CI/CD indicators
        ci_indicators = ["ci", "github/workflows", ".github", ".gitlab-ci", "Jenkinsfile"]
        for d in features.directory_tree:
            if any(ind in d.lower() for ind in ci_indicators):
                score += 15
                break
        
        # Docker
        if any("docker" in d.lower() or "dockerfile" in d.lower() for d in features.directory_tree + list(features.config_files)):
            score += 15
        
        # License
        if features.has_license:
            score += 15
        
        # Documentation
        if features.has_readme and features.has_changelog:
            score += 10
        
        # Testing indicators
        test_dirs = ["test", "tests", "__tests__", "spec"]
        for d in features.directory_tree:
            if any(td in d.lower() for td in test_dirs):
                score += 10
                break
        
        return min(score, 100)
    
    def _calculate_ai_maturity(self, features: RepositoryFeatureSet) -> float:
        """Calculate AI maturity score."""
        score = 20.0
        
        # AI frameworks
        ai_frameworks = ["langchain", "llamaindex", "haystack", "crewai", "autogen"]
        if features.frameworks:
            for fw in features.frameworks:
                if any(aif in fw.lower() for aif in ai_frameworks):
                    score += 15
        
        # Vector databases
        if features.package_managers:
            # Check if any vector db is detected
            score += 10
        
        # Multiple languages support (AI tools often polyglot)
        if len(features.languages) > 2:
            score += 10
        
        # Entry points indicate tool-like behavior
        if features.entry_points:
            score += min(len(features.entry_points) * 5, 20)
        
        return min(score, 100)
    
    def _calculate_capability_coverage(self, features: RepositoryFeatureSet) -> float:
        """Calculate capability coverage score."""
        score = 50.0
        
        # Package managers indicate capabilities
        if features.package_managers:
            score += min(len(features.package_managers) * 5, 25)
        
        # Config files indicate capabilities
        if features.config_files:
            score += min(len(features.config_files) * 2, 15)
        
        # Entry points
        if features.entry_points:
            score += min(len(features.entry_points) * 10, 10)
        
        return min(score, 100)


def create_scoring_engine() -> ScoringEngine:
    """Create scoring engine."""
    return ScoringEngine()
