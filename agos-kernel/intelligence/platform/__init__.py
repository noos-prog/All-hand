"""
AGOS Intelligence - Platform Module
=================================

Platform intelligence for understanding deployment and infrastructure.
"""

from .analyzer import (
    PlatformAnalyzer,
    PlatformType,
    DeploymentConfig,
    get_platform_analyzer,
)

__all__ = [
    "PlatformAnalyzer",
    "PlatformType",
    "DeploymentConfig",
    "get_platform_analyzer",
]