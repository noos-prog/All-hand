"""
AGOS Enterprise Model (AEM)
==========================

Enterprise-scale AI agent orchestration system.
Implements the 4-layer hierarchy: Skill → Capability → Service → Department.

Not 1000 Agents. A 1000-Capability Enterprise.

Core Brain (CEO) orchestrates.
Providers execute.
"""

from .hierarchy import (
    Skill, Capability, Service, Department,
    HierarchyLevel, SkillType
)
from .core_brain import CoreBrain, BrainDecision, BrainStrategy
from .provider import Provider, ProviderType, ProviderStatus
from .marketplace import Marketplace, ProviderListing
from .capability_pack import CapabilityPack, PackType
from .orchestrator import EnterpriseOrchestrator
from .benchmark import BenchmarkRunner, BenchmarkResult

__all__ = [
    # Hierarchy
    "Skill",
    "Capability", 
    "Service",
    "Department",
    "HierarchyLevel",
    "SkillType",
    # Core Brain
    "CoreBrain",
    "BrainDecision",
    "BrainStrategy",
    # Provider
    "Provider",
    "ProviderType",
    "ProviderStatus",
    # Marketplace
    "Marketplace",
    "ProviderListing",
    # Capability Packs
    "CapabilityPack",
    "PackType",
    # Orchestrator
    "EnterpriseOrchestrator",
    # Benchmark
    "BenchmarkRunner",
    "BenchmarkResult",
]

__version__ = "1.0.0"
