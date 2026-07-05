"""
AGOS Registry Module
==================

Unified Registry System for all AGOS components:
- Component Registry
- Capability Registry
- Provider Registry
- Workflow Registry
- Knowledge Registry

All components must be registered to be used by the Kernel.
"""

from .component import ComponentRegistry, Component, ComponentStatus
from .cap_registry import CapabilityRegistry, Capability, CapabilityType
from .provider_registry import ProviderRegistry, Provider, ProviderStatus
from .workflow_registry import WorkflowRegistry, Workflow, WorkflowStep
from .knowledge_registry import KnowledgeRegistry, KnowledgeEntry, KnowledgeType

__all__ = [
    # Component
    "ComponentRegistry",
    "Component",
    "ComponentStatus",
    # Capability
    "CapabilityRegistry",
    "Capability",
    "CapabilityType",
    # Provider
    "ProviderRegistry",
    "Provider",
    "ProviderStatus",
    # Workflow
    "WorkflowRegistry",
    "Workflow",
    "WorkflowStep",
    # Knowledge
    "KnowledgeRegistry",
    "KnowledgeEntry",
    "KnowledgeType",
]