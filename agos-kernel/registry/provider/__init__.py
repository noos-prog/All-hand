"""Provider Registry."""
from typing import Dict, List, Optional

from interfaces import IProvider


class ProviderRegistry:
    """
    Registry for providers.
    No singleton - inject as dependency.
    """
    
    def __init__(self):
        self._providers: Dict[str, IProvider] = {}
    
    def register(self, provider: IProvider) -> None:
        """Register a provider."""
        self._providers[provider.name] = provider
    
    def get(self, name: str) -> Optional[IProvider]:
        """Get a provider by name."""
        return self._providers.get(name)
    
    def list_all(self) -> List[IProvider]:
        """List all registered providers."""
        return list(self._providers.values())
    
    def exists(self, name: str) -> bool:
        """Check if provider exists."""
        return name in self._providers
    
    def find_for_skill(self, skill_name: str) -> Optional[IProvider]:
        """Find a provider that supports a skill."""
        for provider in self._providers.values():
            if provider.supports_skill(skill_name):
                return provider
        return None
    
    def unregister(self, name: str) -> None:
        """Unregister a provider."""
        if name in self._providers:
            del self._providers[name]
