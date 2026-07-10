"""
CGP Capabilities Module
======================

Capabilities composed of skills.
"""

from .composer import (
    Capability, CapabilityComposer,
    CapabilityRegistry, CapabilityAnalyzer
)

__all__ = [
    "Capability",
    "CapabilityComposer",
    "CapabilityRegistry",
    "CapabilityAnalyzer",
]
