"""
AGOS Foundation Capabilities (CAPABILITY-000001 to CAPABILITY-000020)

This module implements the first twenty production-grade capabilities.
Each capability is independently installable, versioned, benchmarked, observable, and certifiable.

CAPABILITY-000001: Repository Discovery
CAPABILITY-000002: Repository Clone
CAPABILITY-000003: Repository Synchronization
CAPABILITY-000004: Repository Fingerprinting
CAPABILITY-000005: Repository Structure Analysis
CAPABILITY-000006: Technology Detection
CAPABILITY-000007: Dependency Analysis
CAPABILITY-000008: Code Indexing
CAPABILITY-000009: Architecture Extraction
CAPABILITY-000010: Architecture Validation
CAPABILITY-000011: Pattern Detection
CAPABILITY-000012: Anti-Pattern Detection
CAPABILITY-000013: Dead Code Detection
CAPABILITY-000014: Security Scan
CAPABILITY-000015: License Analysis
CAPABILITY-000016: Documentation Analysis
CAPABILITY-000017: Configuration Analysis
CAPABILITY-000018: Infrastructure Analysis
CAPABILITY-000019: Repository DNA Generation
CAPABILITY-000020: Engineering Knowledge Extraction
"""

from .capability_001_discovery import RepositoryDiscoveryCapability
from .capability_002_clone import RepositoryCloneCapability
from .capability_003_sync import RepositorySyncCapability
from .capability_004_fingerprint import RepositoryFingerprintCapability
from .capability_005_structure import StructureAnalysisCapability
from .capability_006_technology import TechnologyDetectionCapability
from .capability_007_dependency import DependencyAnalysisCapability
from .capability_008_indexing import CodeIndexingCapability
from .capability_009_arch_extraction import ArchitectureExtractionCapability
from .capability_010_arch_validation import ArchitectureValidationCapability
from .capability_011_pattern import PatternDetectionCapability
from .capability_012_antipattern import AntiPatternDetectionCapability
from .capability_013_deadcode import DeadCodeDetectionCapability
from .capability_014_security import SecurityScanCapability
from .capability_015_license import LicenseAnalysisCapability
from .capability_016_docs import DocumentationAnalysisCapability
from .capability_017_config import ConfigurationAnalysisCapability
from .capability_018_infra import InfrastructureAnalysisCapability
from .capability_019_dna import RepositoryDNACapability
from .capability_020_knowledge import KnowledgeExtractionCapability

__all__ = [
    "RepositoryDiscoveryCapability",
    "RepositoryCloneCapability",
    "RepositorySyncCapability",
    "RepositoryFingerprintCapability",
    "StructureAnalysisCapability",
    "TechnologyDetectionCapability",
    "DependencyAnalysisCapability",
    "CodeIndexingCapability",
    "ArchitectureExtractionCapability",
    "ArchitectureValidationCapability",
    "PatternDetectionCapability",
    "AntiPatternDetectionCapability",
    "DeadCodeDetectionCapability",
    "SecurityScanCapability",
    "LicenseAnalysisCapability",
    "DocumentationAnalysisCapability",
    "ConfigurationAnalysisCapability",
    "InfrastructureAnalysisCapability",
    "RepositoryDNACapability",
    "KnowledgeExtractionCapability",
]
