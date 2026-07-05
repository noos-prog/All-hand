"""AGOS Sandbox."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class SandboxStatus(Enum):
    """Sandbox status."""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class Sandbox:
    """A sandbox environment."""
    id: str
    name: str
    status: SandboxStatus = SandboxStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SandboxManager:
    """
    Sandbox Manager.
    
    Manages sandbox environments for secure execution.
    
    Usage:
        manager = SandboxManager()
        sandbox = manager.create("test_sandbox")
        result = manager.execute(sandbox.id, code="print('hello')")
    """
    
    def __init__(self):
        """Initialize sandbox manager."""
        self._sandboxes: Dict[str, Sandbox] = {}
    
    def create(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> Sandbox:
        """Create a sandbox."""
        sandbox = Sandbox(
            id=f"sandbox-{uuid.uuid4().hex[:8]}",
            name=name,
            metadata=metadata or {},
        )
        self._sandboxes[sandbox.id] = sandbox
        return sandbox
    
    def get(self, sandbox_id: str) -> Optional[Sandbox]:
        """Get a sandbox by ID."""
        return self._sandboxes.get(sandbox_id)
    
    def execute(self, sandbox_id: str, code: str, timeout: int = 30) -> bool:
        """Execute code in a sandbox."""
        sandbox = self._sandboxes.get(sandbox_id)
        if not sandbox:
            return False
        
        sandbox.status = SandboxStatus.RUNNING
        
        try:
            # Simple execution (in real implementation, use proper isolation)
            import io
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            exec(code, {"__name__": "__sandbox__"})
            
            sandbox.output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            sandbox.status = SandboxStatus.COMPLETED
            return True
        
        except Exception as e:
            sandbox.error = str(e)
            sandbox.status = SandboxStatus.FAILED
            return False
    
    def delete(self, sandbox_id: str) -> bool:
        """Delete a sandbox."""
        if sandbox_id in self._sandboxes:
            del self._sandboxes[sandbox_id]
            return True
        return False


# Global instance
_sandbox_manager: Optional[SandboxManager] = None


def get_sandbox_manager() -> SandboxManager:
    """Get the global sandbox manager."""
    global _sandbox_manager
    if _sandbox_manager is None:
        _sandbox_manager = SandboxManager()
    return _sandbox_manager
