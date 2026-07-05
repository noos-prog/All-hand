"""
AGOS Resource Module
===================

Resource management and allocation.
"""

from .resource import (
    ResourceManager,
    Resource,
    ResourceType,
    ResourceAllocation,
    get_resource_manager,
)

__all__ = [
    "ResourceManager",
    "Resource",
    "ResourceType",
    "ResourceAllocation",
    "get_resource_manager",
]