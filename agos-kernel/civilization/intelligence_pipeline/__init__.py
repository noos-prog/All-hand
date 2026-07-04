"""
Engineering Intelligence Pipeline
PHASE-02: EXECUTION-000003 - Engineering Intelligence Pipeline

Converts raw repositories into structured Engineering Intelligence Packages.
"""

__version__ = "1.0"

from agos_kernel.civilization.intelligence_pipeline.intelligence_package import (
    EngineeringIntelligencePackage,
    RepositoryIdentity,
    RepositoryDNA,
    TechnologyStack,
    ArchitectureSummary,
    DependencyInfo,
    QualityProfile,
    SecurityProfile,
    PerformanceProfile,
    TestingProfile,
    DocumentationProfile,
    EvidencePackage,
    Recommendation,
    TrustLevel,
    RiskLevel,
)
from agos_kernel.civilization.intelligence_pipeline.pipeline import (
    EngineeringIntelligencePipeline,
    PipelineResult,
)
from agos_kernel.civilization.intelligence_pipeline.stages import (
    PipelineStage,
    RepositoryFingerprintStage,
    TechnologyDetectionStage,
    LanguageDetectionStage,
    DependencyResolutionStage,
    ArchitectureAnalysisStage,
    CodeGraphConstructionStage,
    EvidenceGenerationStage,
)

__all__ = [
    'EngineeringIntelligencePackage',
    'RepositoryIdentity',
    'RepositoryDNA',
    'TechnologyStack',
    'ArchitectureSummary',
    'DependencyInfo',
    'QualityProfile',
    'SecurityProfile',
    'PerformanceProfile',
    'TestingProfile',
    'DocumentationProfile',
    'EvidencePackage',
    'Recommendation',
    'TrustLevel',
    'RiskLevel',
    'EngineeringIntelligencePipeline',
    'PipelineResult',
    'PipelineStage',
    'RepositoryFingerprintStage',
    'TechnologyDetectionStage',
    'LanguageDetectionStage',
    'DependencyResolutionStage',
    'ArchitectureAnalysisStage',
    'CodeGraphConstructionStage',
    'EvidenceGenerationStage',
]
