"""
AGOS State Manager
=================

Manages state snapshots and persistence for runtime execution.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class StateStatus(Enum):
    """State status."""
    ACTIVE = "active"
    SAVED = "saved"
    RESTORED = "restored"
    FAILED = "failed"


@dataclass
class State:
    """Runtime state."""
    id: str
    name: str
    data: Dict[str, Any]
    status: StateStatus = StateStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateSnapshot:
    """State snapshot for persistence."""
    id: str
    state_id: str
    data: str  # JSON serialized
    created_at: datetime = field(default_factory=datetime.now)
    checksum: str = ""


class StateManager:
    """
    State Manager.
    
    Manages runtime state and snapshots.
    
    Usage:
        manager = StateManager()
        
        manager.set_state("mission-123", {"status": "running"})
        state = manager.get_state("mission-123")
        
        snapshot = manager.snapshot("mission-123")
        manager.restore(snapshot.id)
    """
    
    def __init__(self):
        """Initialize state manager."""
        self._states: Dict[str, State] = {}
        self._snapshots: Dict[str, StateSnapshot] = {}
        self._history: Dict[str, List[str]] = {}  # state_id -> snapshot_ids
    
    def set_state(self, state_id: str, data: Dict[str, Any], name: str = "") -> State:
        """Set or update a state."""
        if state_id in self._states:
            state = self._states[state_id]
            state.data = data
            state.updated_at = datetime.now()
        else:
            state = State(
                id=state_id,
                name=name or state_id,
                data=data,
            )
            self._states[state_id] = state
        
        return state
    
    def get_state(self, state_id: str) -> Optional[State]:
        """Get a state by ID."""
        return self._states.get(state_id)
    
    def delete_state(self, state_id: str) -> bool:
        """Delete a state."""
        if state_id in self._states:
            del self._states[state_id]
            return True
        return False
    
    def list_states(self) -> List[State]:
        """List all states."""
        return list(self._states.values())
    
    def snapshot(self, state_id: str) -> Optional[StateSnapshot]:
        """Create a snapshot of a state."""
        state = self._states.get(state_id)
        if not state:
            return None
        
        # Serialize state data
        data_json = json.dumps(state.data, default=str)
        
        # Create checksum
        import hashlib
        checksum = hashlib.md5(data_json.encode()).hexdigest()
        
        snapshot = StateSnapshot(
            id=f"snap-{uuid.uuid4().hex[:8]}",
            state_id=state_id,
            data=data_json,
            checksum=checksum,
        )
        
        self._snapshots[snapshot.id] = snapshot
        
        # Track history
        if state_id not in self._history:
            self._history[state_id] = []
        self._history[state_id].append(snapshot.id)
        
        # Keep only last 10 snapshots per state
        if len(self._history[state_id]) > 10:
            old_snap_id = self._history[state_id].pop(0)
            if old_snap_id in self._snapshots:
                del self._snapshots[old_snap_id]
        
        return snapshot
    
    def restore(self, snapshot_id: str) -> bool:
        """Restore a state from snapshot."""
        snapshot = self._snapshots.get(snapshot_id)
        if not snapshot:
            return False
        
        # Verify checksum
        import hashlib
        if hashlib.md5(snapshot.data.encode()).hexdigest() != snapshot.checksum:
            return False
        
        # Restore state
        data = json.loads(snapshot.data)
        state = self.set_state(snapshot.state_id, data)
        state.status = StateStatus.RESTORED
        
        return True
    
    def get_snapshot(self, snapshot_id: str) -> Optional[StateSnapshot]:
        """Get a snapshot by ID."""
        return self._snapshots.get(snapshot_id)
    
    def get_history(self, state_id: str) -> List[StateSnapshot]:
        """Get snapshot history for a state."""
        snapshot_ids = self._history.get(state_id, [])
        return [self._snapshots[sid] for sid in snapshot_ids if sid in self._snapshots]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "total_states": len(self._states),
            "total_snapshots": len(self._snapshots),
            "states_with_history": len(self._history),
        }


# Global instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the global state manager."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager
