"""AGOS Tools."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class ToolStatus(Enum):
    """Tool status."""
    AVAILABLE = "available"
    BUSY = "busy"
    DISABLED = "disabled"


@dataclass
class Tool:
    """A tool."""
    id: str
    name: str
    handler: Callable
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: ToolStatus = ToolStatus.AVAILABLE
    usage_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """
    Tool Registry.
    
    Manages tools available for missions.
    
    Usage:
        registry = ToolRegistry()
        tool = registry.register("web_search", search_handler, description="Search the web")
        result = registry.execute("web_search", query="python")
    """
    
    def __init__(self):
        """Initialize tool registry."""
        self._tools: Dict[str, Tool] = {}
    
    def register(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Tool:
        """Register a tool."""
        tool = Tool(
            id=f"tool-{uuid.uuid4().hex[:8]}",
            name=name,
            handler=handler,
            description=description,
            parameters=parameters or {},
        )
        self._tools[name] = tool
        return tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def execute(self, name: str, **kwargs) -> Any:
        """Execute a tool."""
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        tool.status = ToolStatus.BUSY
        tool.usage_count += 1
        
        try:
            result = tool.handler(**kwargs)
            return result
        finally:
            tool.status = ToolStatus.AVAILABLE
    
    def list_all(self) -> List[Tool]:
        """List all tools."""
        return list(self._tools.values())
    
    def unregister(self, name: str) -> bool:
        """Unregister a tool."""
        if name in self._tools:
            del self._tools[name]
            return True
        return False


# Global instance
_tool_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry."""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = ToolRegistry()
    return _tool_registry
