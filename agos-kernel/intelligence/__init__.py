"""
Universal Engineering Intelligence Platform.

Integrates Repository Intelligence, Code Intelligence, Architecture Intelligence,
Knowledge Extraction, Capability Discovery, Provider Discovery, and Project DNA
Generation into one comprehensive engineering intelligence platform.

EXECUTION-000041 to EXECUTION-000050: Engineering Intelligence Foundation
"""

# Repository Intelligence
from .repository.models import (
    Language,
    Framework,
    BuildSystem,
    ContainerTech,
    CloudProvider,
    Database,
    Queue,
    DirectoryNode,
    Module,
    FileMetrics,
    RepositoryMetrics,
    RepositoryGenome,
)
from .repository.analyzer import RepositoryAnalyzer

# Code Intelligence
from .code.models import (
    SymbolType,
    ComplexityLevel,
    PatternType,
    Location,
    Symbol,
    Import,
    CallGraph,
    ImportGraph,
    InheritanceRelationship,
    Duplication,
    DeadCode,
    CodePattern,
    CodeHealth,
    FileAnalysis,
    CodeGenome,
)
from .code.analyzer import CodeIntelligenceEngine, PythonCodeAnalyzer

# Architecture Intelligence
from .architecture.models import (
    LayerType,
    ComponentType,
    BoundaryType,
    ArchitectureStyle,
    Layer,
    Boundary,
    Component,
    Interface,
    Contract,
    Event,
    Policy,
    ArchitectureGraph,
    ArchitectureScore,
    ArchitectureViolation,
    ArchitectureRisk,
    ArchitectureGenome,
)
from .architecture.analyzer import ArchitectureAnalyzer

# Knowledge Extraction
from .knowledge import (
    BestPractice,
    CodePattern as KnowledgeCodePattern,
    AntiPattern,
    ArchitectureDecision,
    TechnologyChoice,
    CodingStandard,
    PerformanceOptimization,
    SecurityPractice,
    TestingStrategy,
    DeploymentStrategy,
    KnowledgeObject,
    KnowledgeExtraction,
    KnowledgeExtractor,
)

# Capability Discovery
from .capability import (
    Capability,
    CapabilityDNA,
    CapabilityMetadata,
    CandidateCapability,
    CapabilityDiscoveryEngine,
)

# Provider Discovery
from .provider import (
    ProviderProfile,
    ProviderContract,
    ProviderHealth,
    ProviderBenchmark,
    ProviderDiscoveryEngine,
)

# Project DNA
from .dna import ProjectDNA, ProjectDNAGenerator

# Platform
from .engine import (
    AnalysisReport,
    QueryResult,
    EngineeringIntelligencePlatform,
    analyze_repository,
)

__version__ = "2.0.0"

__all__ = [
    # Repository Intelligence
    "Language",
    "Framework",
    "BuildSystem",
    "ContainerTech",
    "CloudProvider",
    "Database",
    "Queue",
    "DirectoryNode",
    "Module",
    "FileMetrics",
    "RepositoryMetrics",
    "RepositoryGenome",
    "RepositoryAnalyzer",
    # Code Intelligence
    "SymbolType",
    "ComplexityLevel",
    "PatternType",
    "Location",
    "Symbol",
    "Import",
    "CallGraph",
    "ImportGraph",
    "InheritanceRelationship",
    "Duplication",
    "DeadCode",
    "CodeHealth",
    "FileAnalysis",
    "CodeGenome",
    "CodeIntelligenceEngine",
    "PythonCodeAnalyzer",
    # Architecture Intelligence
    "LayerType",
    "ComponentType",
    "BoundaryType",
    "ArchitectureStyle",
    "Layer",
    "Boundary",
    "Component",
    "Interface",
    "Contract",
    "Event",
    "Policy",
    "ArchitectureGraph",
    "ArchitectureScore",
    "ArchitectureViolation",
    "ArchitectureRisk",
    "ArchitectureGenome",
    "ArchitectureAnalyzer",
    # Knowledge
    "BestPractice",
    "AntiPattern",
    "ArchitectureDecision",
    "TechnologyChoice",
    "CodingStandard",
    "PerformanceOptimization",
    "SecurityPractice",
    "TestingStrategy",
    "DeploymentStrategy",
    "KnowledgeObject",
    "KnowledgeExtraction",
    "KnowledgeExtractor",
    # Capability
    "Capability",
    "CapabilityDNA",
    "CapabilityMetadata",
    "CandidateCapability",
    "CapabilityDiscoveryEngine",
    # Provider
    "ProviderProfile",
    "ProviderContract",
    "ProviderHealth",
    "ProviderBenchmark",
    "ProviderDiscoveryEngine",
    # Project DNA
    "ProjectDNA",
    "ProjectDNAGenerator",
    # Platform
    "AnalysisReport",
    "QueryResult",
    "EngineeringIntelligencePlatform",
    "analyze_repository",
]
