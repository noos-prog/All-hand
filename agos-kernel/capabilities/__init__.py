"""
AGOS Capabilities Module
=====================

Capability management for AGOS.
"""

from .base import Capability, CapabilityMetadata, CapabilityStatus
from .registry import CapabilityRegistry, CapabilityType, get_capability_registry

# Import RepositoryAnalysisCapability for backward compatibility
from ._repository_analysis import RepositoryAnalysisCapability, RepositoryAnalysisInput

__all__ = [
    "Capability",
    "CapabilityMetadata",
    "CapabilityStatus",
    "CapabilityRegistry",
    "CapabilityType",
    "get_capability_registry",
    "RepositoryAnalysisCapability",
    "RepositoryAnalysisInput",
]
