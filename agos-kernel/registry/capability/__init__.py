"""Capability Registry."""
from typing import Dict, List, Optional, Type

from interfaces import ICapability


class CapabilityRegistry:
    """
    Registry for capabilities.
    No singleton - inject as dependency.
    """
    
    def __init__(self):
        self._capabilities: Dict[str, ICapability] = {}
    
    def register(self, capability: ICapability) -> None:
        """Register a capability."""
        self._capabilities[capability.name] = capability
    
    def get(self, name: str) -> Optional[ICapability]:
        """Get a capability by name."""
        return self._capabilities.get(name)
    
    def list_all(self) -> List[ICapability]:
        """List all registered capabilities."""
        return list(self._capabilities.values())
    
    def exists(self, name: str) -> bool:
        """Check if capability exists."""
        return name in self._capabilities
    
    def unregister(self, name: str) -> None:
        """Unregister a capability."""
        if name in self._capabilities:
            del self._capabilities[name]
