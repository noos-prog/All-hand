"""
CGP: Capability Genome Project
==========================

From Repository DNA to Capability DNA.

Hierarchy:
  MISSION → DEPARTMENT → SERVICE → CAPABILITY → SKILL → PRIMITIVE

This module provides:
- Skills: Primitive building blocks
- Capabilities: Composed skills
- Services: Aggregated capabilities
- Departments: Organized services
- Missions: Full projects
- Genome: Complete analysis
"""

from .skills.primitive import (
    Skill, SkillCategory, SkillDifficulty,
    SkillRegistry, SkillExtractor
)
from .capabilities.composer import (
    Capability, CapabilityComposer,
    CapabilityRegistry, CapabilityAnalyzer
)
from .services.aggregator import (
    Service, ServiceAggregator,
    ServiceRegistry
)
from .departments.organizer import (
    Department, DepartmentOrganizer,
    DepartmentRegistry
)
from .missions.builder import (
    Mission, MissionBuilder,
    MissionRegistry, MissionExecutor
)
from .genome.analyzer import (
    CapabilityGenome, GenomeAnalyzer,
    GenomeGenerator, GenomeComparison
)
from .graph.capability_graph import (
    CapabilityGraph, GraphNode, GraphEdge,
    DependencyAnalyzer, GapFinder
)
from .reuse.engine import (
    ReuseEngine, ReuseAnalyzer,
    ReuseScore
)
from .overlap.analyzer import (
    OverlapAnalyzer, OverlapMatrix,
    SimilarityCalculator
)
from .evolution.tracker import (
    EvolutionTracker, EvolutionAnalyzer,
    TrendPredictor
)

__all__ = [
    # Skills
    "Skill",
    "SkillCategory",
    "SkillRegistry",
    "SkillExtractor",
    # Capabilities
    "Capability",
    "CapabilityComposer",
    "CapabilityRegistry",
    "CapabilityAnalyzer",
    # Services
    "Service",
    "ServiceAggregator",
    "ServiceRegistry",
    # Departments
    "Department",
    "DepartmentOrganizer",
    "DepartmentRegistry",
    # Missions
    "Mission",
    "MissionBuilder",
    "MissionRegistry",
    "MissionExecutor",
    # Genome
    "CapabilityGenome",
    "GenomeAnalyzer",
    "GenomeGenerator",
    "GenomeComparison",
    # Graph
    "CapabilityGraph",
    "GraphNode",
    "GraphEdge",
    "DependencyAnalyzer",
    "GapFinder",
    # Reuse
    "ReuseEngine",
    "ReuseAnalyzer",
    "ReuseScore",
    # Overlap
    "OverlapAnalyzer",
    "OverlapMatrix",
    "SimilarityCalculator",
    # Evolution
    "EvolutionTracker",
    "EvolutionAnalyzer",
    "TrendPredictor",
]

__version__ = "1.0.0"
