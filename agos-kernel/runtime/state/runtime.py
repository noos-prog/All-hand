"""Universal State Runtime."""
import hashlib
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    State, StateType, StateStatus, StateTransition, StateSnapshot
)


class StateRuntime:
    """Universal State Runtime."""
    
    def __init__(self):
        """Initialize state runtime."""
        self.states: Dict[str, State] = {}
    
    def create_state(
        self,
        name: str,
        state_type: StateType,
        mission_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        initial_data: Optional[Dict[str, Any]] = None,
        schema: Optional[Dict[str, Any]] = None,
    ) -> State:
        """Create a new state."""
        state_id = self._generate_id(name)
        
        state = State(
            id=state_id,
            name=name,
            state_type=state_type,
            data=initial_data or {},
            mission_id=mission_id,
            execution_id=execution_id,
            workspace_id=workspace_id,
            schema=schema,
        )
        
        state.status = StateStatus.ACTIVE
        state.created_at = datetime.now()
        state.updated_at = datetime.now()
        
        self.states[state_id] = state
        return state
    
    def get_state(self, state_id: str) -> Optional[State]:
        """Get state by ID."""
        return self.states.get(state_id)
    
    def list_states(
        self,
        state_type: Optional[StateType] = None,
        status: Optional[StateStatus] = None,
    ) -> List[State]:
        """List states with optional filtering."""
        states = list(self.states.values())
        
        if state_type:
            states = [s for s in states if s.state_type == state_type]
        
        if status:
            states = [s for s in states if s.status == status]
        
        return states
    
    def update_state(self, state_id: str, data: Dict[str, Any]) -> Optional[State]:
        """Update state data."""
        state = self.states.get(state_id)
        if not state:
            return None
        
        # Store previous version
        if state.diff_enabled:
            state.previous_versions.append(state.data.copy())
            if len(state.previous_versions) > 10:
                state.previous_versions.pop(0)
        
        # Update data
        state.data = data
        state.version += 1
        state.updated_at = datetime.now()
        
        # Validate if schema exists
        if state.schema:
            state.validate()
        
        return state
    
    def patch_state(self, state_id: str, patch: Dict[str, Any]) -> Optional[State]:
        """Patch state data (partial update)."""
        state = self.states.get(state_id)
        if not state:
            return None
        
        # Store previous version
        if state.diff_enabled:
            state.previous_versions.append(state.data.copy())
            if len(state.previous_versions) > 10:
                state.previous_versions.pop(0)
        
        # Apply patch
        state.data.update(patch)
        state.version += 1
        state.updated_at = datetime.now()
        
        return state
    
    def transition(self, state_id: str, new_state: str, reason: str = "", metadata: Dict[str, Any] = None) -> Optional[State]:
        """Transition state to a new status."""
        state = self.states.get(state_id)
        if not state:
            return None
        
        state.transition_to(new_state, reason, metadata)
        return state
    
    def snapshot(self, state_id: str) -> Optional[StateSnapshot]:
        """Create a snapshot of state."""
        state = self.states.get(state_id)
        if not state:
            return None
        
        snapshot = state.create_snapshot(state.data)
        return snapshot
    
    def restore_snapshot(self, state_id: str, snapshot_id: str) -> bool:
        """Restore state from a snapshot."""
        state = self.states.get(state_id)
        if not state:
            return False
        
        for snapshot in state.snapshots:
            if snapshot.id == snapshot_id:
                state.data = snapshot.data.copy()
                state.updated_at = datetime.now()
                return True
        
        return False
    
    def replay_state(self, state_id: str, to_version: int) -> Optional[Dict[str, Any]]:
        """Replay state to a specific version."""
        state = self.states.get(state_id)
        if not state:
            return None
        
        if to_version >= state.version:
            return state.data
        
        # Find the version
        if to_version <= 0 or to_version > len(state.previous_versions):
            return None
        
        return state.previous_versions[to_version - 1].copy()
    
    def diff(self, state_id: str) -> Optional[Dict[str, Any]]:
        """Get diff from previous version."""
        state = self.states.get(state_id)
        if not state or not state.previous_versions:
            return None
        
        previous = state.previous_versions[-1]
        current = state.data
        
        return self._calculate_diff(previous, current)
    
    def validate_state(self, state_id: str) -> bool:
        """Validate state against schema."""
        state = self.states.get(state_id)
        if not state:
            return False
        
        return state.validate()
    
    def archive_state(self, state_id: str) -> bool:
        """Archive a state."""
        state = self.states.get(state_id)
        if not state:
            return False
        
        state.status = StateStatus.ARCHIVED
        state.updated_at = datetime.now()
        return True
    
    def delete_state(self, state_id: str) -> bool:
        """Delete a state."""
        if state_id in self.states:
            del self.states[state_id]
            return True
        return False
    
    def _calculate_diff(self, old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate diff between two states."""
        added = {k: v for k, v in new.items() if k not in old}
        removed = {k: v for k, v in old.items() if k not in new}
        modified = {k: {"old": old[k], "new": new[k]} for k in old if k in new and old[k] != new[k]}
        
        return {
            "added": added,
            "removed": removed,
            "modified": modified,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
