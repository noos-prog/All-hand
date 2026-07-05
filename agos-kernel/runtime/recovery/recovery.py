"""
AGOS Recovery Manager
====================

Manages recovery points and fault tolerance.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class RecoveryStrategy(Enum):
    """Recovery strategy."""
    RETRY = "retry"
    FAILOVER = "failover"
    RESTORE = "restore"
    SKIP = "skip"
    MANUAL = "manual"


class RecoveryStatus(Enum):
    """Recovery status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class RecoveryPoint:
    """A recovery point."""
    id: str
    name: str
    state_data: Dict[str, Any]
    checkpoint: Callable = field(default=None)
    restore_handler: Callable = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryAction:
    """A recovery action."""
    id: str
    strategy: RecoveryStrategy
    status: RecoveryStatus = RecoveryStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RecoveryManager:
    """
    Recovery Manager.
    
    Manages recovery points and fault tolerance strategies.
    
    Usage:
        manager = RecoveryManager()
        
        # Create a recovery point
        point = manager.create_recovery_point(
            name="before_migration",
            state_data={"step": 1},
        )
        
        # Execute with recovery
        result = manager.execute_with_recovery(
            handler=risky_operation,
            recovery_strategies=[RecoveryStrategy.RETRY],
        )
    """
    
    def __init__(self):
        """Initialize recovery manager."""
        self._recovery_points: Dict[str, RecoveryPoint] = {}
        self._recovery_actions: Dict[str, RecoveryAction] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def create_recovery_point(
        self,
        name: str,
        state_data: Dict[str, Any],
        checkpoint: Optional[Callable] = None,
        restore_handler: Optional[Callable] = None,
        expires_in_minutes: Optional[int] = None,
    ) -> RecoveryPoint:
        """Create a recovery point."""
        from datetime import timedelta
        
        expires_at = None
        if expires_in_minutes:
            expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        
        point = RecoveryPoint(
            id=f"rp-{uuid.uuid4().hex[:8]}",
            name=name,
            state_data=state_data,
            checkpoint=checkpoint,
            restore_handler=restore_handler,
            expires_at=expires_at,
        )
        
        self._recovery_points[point.id] = point
        return point
    
    def get_recovery_point(self, point_id: str) -> Optional[RecoveryPoint]:
        """Get a recovery point by ID."""
        return self._recovery_points.get(point_id)
    
    def list_recovery_points(self) -> List[RecoveryPoint]:
        """List all recovery points."""
        return list(self._recovery_points.values())
    
    def delete_recovery_point(self, point_id: str) -> bool:
        """Delete a recovery point."""
        if point_id in self._recovery_points:
            del self._recovery_points[point_id]
            return True
        return False
    
    def execute_with_recovery(
        self,
        handler: Callable,
        recovery_strategies: List[RecoveryStrategy] = None,
        max_attempts: int = 3,
        *args,
        **kwargs,
    ) -> Any:
        """Execute a handler with recovery strategies."""
        recovery_strategies = recovery_strategies or [RecoveryStrategy.RETRY]
        
        action = RecoveryAction(
            id=f"action-{uuid.uuid4().hex[:8]}",
            strategy=recovery_strategies[0],
            max_attempts=max_attempts,
        )
        self._recovery_actions[action.id] = action
        
        last_error = None
        
        for attempt in range(max_attempts):
            action.attempts = attempt + 1
            action.status = RecoveryStatus.IN_PROGRESS
            
            try:
                result = handler(*args, **kwargs)
                action.status = RecoveryStatus.SUCCESS
                return result
            
            except Exception as e:
                last_error = str(e)
                action.error = last_error
                
                # Try next strategy
                if attempt < len(recovery_strategies) - 1:
                    continue
                else:
                    break
        
        action.status = RecoveryStatus.FAILED
        raise RuntimeError(f"Recovery failed after {max_attempts} attempts: {last_error}")
    
    def restore(self, point_id: str) -> bool:
        """Restore from a recovery point."""
        point = self._recovery_points.get(point_id)
        if not point:
            return False
        
        if point.restore_handler:
            try:
                point.restore_handler(point.state_data)
                return True
            except:
                return False
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "total_recovery_points": len(self._recovery_points),
            "total_recovery_actions": len(self._recovery_actions),
            "successful_actions": sum(
                1 for a in self._recovery_actions.values()
                if a.status == RecoveryStatus.SUCCESS
            ),
            "failed_actions": sum(
                1 for a in self._recovery_actions.values()
                if a.status == RecoveryStatus.FAILED
            ),
        }


# Global instance
_recovery_manager: Optional[RecoveryManager] = None


def get_recovery_manager() -> RecoveryManager:
    """Get the global recovery manager."""
    global _recovery_manager
    if _recovery_manager is None:
        _recovery_manager = RecoveryManager()
    return _recovery_manager
