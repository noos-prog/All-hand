#!/usr/bin/env python3
"""
CGP - Capability Genome Analyzer
==============================

Complete capability genome analysis.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class GenomeScore(Enum):
    """Genome quality scores."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"
    POOR = "poor"


@dataclass
class SimilarProject:
    """A similar project."""
    project_id: str
    name: str
    similarity_score: float
    shared_capabilities: int


@dataclass
class CapabilityGenome:
    """
    Complete genome for a project.
    
    From Repository DNA to Capability DNA.
    """
    genome_id: str
    project_id: str
    project_name: str
    
    # Counts
    skill_count: int = 0
    capability_count: int = 0
    service_count: int = 0
    department_count: int = 0
    
    # Coverage
    coverage_percentage: float = 0.0
    unique_capabilities: Tuple[str, ...] = ()
    shared_capabilities: Tuple[str, ...] = ()
    missing_capabilities: Tuple[str, ...] = ()
    
    # Quality Metrics
    avg_accuracy: float = 0.0
    avg_cost: float = 0.0
    avg_duration_seconds: int = 0
    avg_success_rate: float = 0.0
    
    # Comparison
    similar_projects: Tuple[SimilarProject, ...] = ()
    gaps: Tuple[str, ...] = ()  # Missing capabilities
    
    # Evolution
    evolution_trend: str = "stable"  # growing, declining, stable
    growth_rate: float = 0.0
    
    # Score
    genome_score: GenomeScore = GenomeScore.AVERAGE
    
    # Metadata
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: str = "1.0"
    
    def get_total_component_count(self) -> int:
        """Get total count of all components."""
        return self.skill_count + self.capability_count + self.service_count + self.department_count


@dataclass
class GenomeComparison:
    """Comparison between two genomes."""
    genome_a_id: str
    genome_b_id: str
    
    shared_skills: Tuple[str, ...] = ()
    unique_skills_a: Tuple[str, ...] = ()
    unique_skills_b: Tuple[str, ...] = ()
    
    shared_capabilities: Tuple[str, ...] = ()
    unique_capabilities_a: Tuple[str, ...] = ()
    unique_capabilities_b: Tuple[str, ...] = ()
    
    skill_similarity: float = 0.0
    capability_similarity: float = 0.0
    
    jaccard_index: float = 0.0


class GenomeAnalyzer:
    """
    Analyzes capability genomes.
    """
    
    def __init__(self, capability_registry=None):
        self.capability_registry = capability_registry
    
    def analyze_quality(self, genome: CapabilityGenome) -> Dict[str, Any]:
        """Analyze genome quality."""
        scores = []
        
        # Check coverage
        if genome.coverage_percentage >= 0.8:
            scores.append("excellent_coverage")
        elif genome.coverage_percentage >= 0.6:
            scores.append("good_coverage")
        else:
            scores.append("needs_improvement")
        
        # Check gaps
        if len(genome.gaps) == 0:
            scores.append("no_gaps")
        elif len(genome.gaps) < 5:
            scores.append("few_gaps")
        else:
            scores.append("many_gaps")
        
        # Check success rate
        if genome.avg_success_rate >= 0.9:
            scores.append("high_success")
        elif genome.avg_success_rate >= 0.7:
            scores.append("moderate_success")
        else:
            scores.append("low_success")
        
        return {
            "scores": scores,
            "quality_rating": "good" if len(scores) >= 4 else "needs_work",
        }
    
    def find_gaps(
        self,
        genome: CapabilityGenome,
        required_capabilities: List[str]
    ) -> List[str]:
        """Find gaps in capabilities."""
        genome_caps = set(genome.unique_capabilities) | set(genome.shared_capabilities)
        required = set(required_capabilities)
        
        return list(required - genome_caps)
    
    def suggest_improvements(self, genome: CapabilityGenome) -> List[str]:
        """Suggest improvements based on genome analysis."""
        suggestions = []
        
        # Coverage
        if genome.coverage_percentage < 0.8:
            suggestions.append("Increase capability coverage")
        
        # Cost
        if genome.avg_cost > 1.0:
            suggestions.append("Optimize cost efficiency")
        
        # Duration
        if genome.avg_duration_seconds > 300:
            suggestions.append("Reduce execution time")
        
        # Success rate
        if genome.avg_success_rate < 0.8:
            suggestions.append("Improve success rate")
        
        # Gaps
        if genome.gaps:
            suggestions.append(f"Address {len(genome.gaps)} capability gaps")
        
        return suggestions


class GenomeGenerator:
    """
    Generates capability genomes from projects.
    """
    
    def __init__(self, skill_registry=None, capability_registry=None):
        self.skill_registry = skill_registry
        self.capability_registry = capability_registry
    
    def generate(
        self,
        project_id: str,
        project_name: str,
        skill_ids: List[str],
        capability_ids: List[str],
        service_ids: List[str] = None,
        department_ids: List[str] = None
    ) -> CapabilityGenome:
        """Generate a genome for a project."""
        genome = CapabilityGenome(
            genome_id=f"genome_{project_id}",
            project_id=project_id,
            project_name=project_name,
            skill_count=len(skill_ids),
            capability_count=len(capability_ids),
            service_count=len(service_ids or []),
            department_count=len(department_ids or []),
            unique_capabilities=tuple(capability_ids),
        )
        
        # Calculate coverage
        if self.capability_registry:
            total_caps = len(self.capability_registry._capabilities)
            if total_caps > 0:
                genome.coverage_percentage = len(capability_ids) / total_caps
        
        return genome


class GenomeComparisonEngine:
    """
    Compare capability genomes.
    """
    
    def compare(self, genome_a: CapabilityGenome, genome_b: CapabilityGenome) -> GenomeComparison:
        """Compare two genomes."""
        # Skills
        skills_a = set([f"skill_{i}" for i in range(genome_a.skill_count)])
        skills_b = set([f"skill_{i}" for i in range(genome_b.skill_count)])
        
        shared_skills = skills_a & skills_b
        unique_skills_a = skills_a - skills_b
        unique_skills_b = skills_b - skills_a
        
        # Capabilities
        caps_a = set(genome_a.unique_capabilities) | set(genome_a.shared_capabilities)
        caps_b = set(genome_b.unique_capabilities) | set(genome_b.shared_capabilities)
        
        shared_caps = caps_a & caps_b
        unique_caps_a = caps_a - caps_b
        unique_caps_b = caps_b - caps_a
        
        # Jaccard
        all_items = caps_a | caps_b
        jaccard = len(shared_caps) / len(all_items) if all_items else 0
        
        return GenomeComparison(
            genome_a_id=genome_a.genome_id,
            genome_b_id=genome_b.genome_id,
            shared_skills=tuple(shared_skills),
            unique_skills_a=tuple(unique_skills_a),
            unique_skills_b=tuple(unique_skills_b),
            shared_capabilities=tuple(shared_caps),
            unique_capabilities_a=tuple(unique_caps_a),
            unique_capabilities_b=tuple(unique_caps_b),
            skill_similarity=len(shared_skills) / max(len(skills_a | skills_b), 1),
            capability_similarity=len(shared_caps) / max(len(caps_a | caps_b), 1),
            jaccard_index=jaccard,
        )
