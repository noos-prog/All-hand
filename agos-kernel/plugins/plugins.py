"""AGOS Plugin System."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class PluginStatus(Enum):
    """Plugin status."""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    ACTIVE = "active"
    DISABLED = "disabled"


@dataclass
class Plugin:
    """A plugin."""
    id: str
    name: str
    version: str
    handler: Callable
    status: PluginStatus = PluginStatus.UNLOADED
    metadata: Dict[str, Any] = field(default_factory=dict)


class PluginManager:
    """
    Plugin Manager.
    
    Manages plugins for AGOS.
    
    Usage:
        manager = PluginManager()
        plugin = manager.register("my_plugin", my_handler)
    """
    
    def __init__(self):
        """Initialize plugin manager."""
        self._plugins: Dict[str, Plugin] = {}
    
    def register(self, name: str, handler: Callable, version: str = "1.0.0") -> Plugin:
        """Register a plugin."""
        plugin = Plugin(
            id=f"plugin-{uuid.uuid4().hex[:8]}",
            name=name,
            handler=handler,
            version=version,
            status=PluginStatus.LOADED,
        )
        self._plugins[name] = plugin
        return plugin
    
    def get(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def list_all(self) -> List[Plugin]:
        """List all plugins."""
        return list(self._plugins.values())
    
    def unregister(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self._plugins:
            del self._plugins[name]
            return True
        return False


# Global instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
