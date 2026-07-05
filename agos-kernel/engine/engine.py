"""
AGOS Engine
===========

Core execution engine for AGOS.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class EngineStatus(Enum):
    """Engine status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class ExecutionResult:
    """Execution result."""
    success: bool
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AGOSEngine:
    """
    AGOS Core Execution Engine.
    
    Provides the core execution loop for missions and tasks.
    
    Usage:
        engine = AGOSEngine()
        result = engine.execute(handler=my_task, args=(data,))
    """
    
    def __init__(self):
        """Initialize engine."""
        self.status = EngineStatus.IDLE
        self._handlers: Dict[str, Callable] = {}
        self._metrics: Dict[str, Any] = {}
    
    def execute(
        self,
        handler: Callable,
        args: tuple = None,
        kwargs: Dict[str, Any] = None,
    ) -> ExecutionResult:
        """Execute a handler."""
        start_time = time.time()
        self.status = EngineStatus.RUNNING
        
        try:
            result = handler(*(args or ()), **(kwargs or {}))
            duration = (time.time() - start_time) * 1000
            
            self.status = EngineStatus.IDLE
            return ExecutionResult(
                success=True,
                output=result,
                duration_ms=duration,
            )
        
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.status = EngineStatus.IDLE
            return ExecutionResult(
                success=False,
                error=str(e),
                duration_ms=duration,
            )
    
    def register_handler(self, name: str, handler: Callable) -> None:
        """Register a handler."""
        self._handlers[name] = handler
    
    def get_handler(self, name: str) -> Optional[Callable]:
        """Get a handler by name."""
        return self._handlers.get(name)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "status": self.status.value,
            "registered_handlers": len(self._handlers),
            "metrics": self._metrics,
        }


# Global instance
_engine: Optional[AGOSEngine] = None


def get_engine() -> AGOSEngine:
    """Get the global engine instance."""
    global _engine
    if _engine is None:
        _engine = AGOSEngine()
    return _engine
