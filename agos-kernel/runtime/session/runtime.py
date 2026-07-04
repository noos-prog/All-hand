"""Universal Session Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Session, SessionStatus, SessionType, SessionEvent,
    SessionTimeline, SessionMetrics
)


class SessionRuntime:
    """Universal Session Runtime."""
    
    def __init__(self):
        """Initialize session runtime."""
        self.sessions: Dict[str, Session] = {}
        self.active_sessions: Dict[str, str] = {}  # session_id -> workspace_id
    
    def create_session(
        self,
        name: str,
        session_type: SessionType,
        mission_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        provider_id: Optional[str] = None,
        replay_enabled: bool = True,
    ) -> Session:
        """Create a new session."""
        session_id = self._generate_id(name)
        
        session = Session(
            id=session_id,
            name=name,
            session_type=session_type,
            mission_id=mission_id,
            workspace_id=workspace_id,
            agent_id=agent_id,
            user_id=user_id,
            provider_id=provider_id,
            status=SessionStatus.INITIALIZING,
            timeline=SessionTimeline(started_at=datetime.now()),
            replay_enabled=replay_enabled,
        )
        
        # Initialize session
        session.status = SessionStatus.ACTIVE
        session.created_at = datetime.now()
        session.updated_at = datetime.now()
        session.last_activity = datetime.now()
        
        # Add creation event
        session.add_event("session_created", {"session_type": session_type.value})
        
        # Store session
        self.sessions[session_id] = session
        
        if workspace_id:
            self.active_sessions[session_id] = workspace_id
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        return self.sessions.get(session_id)
    
    def list_sessions(
        self,
        status: Optional[SessionStatus] = None,
        session_type: Optional[SessionType] = None,
        workspace_id: Optional[str] = None,
    ) -> List[Session]:
        """List sessions with optional filtering."""
        sessions = list(self.sessions.values())
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        if session_type:
            sessions = [s for s in sessions if s.session_type == session_type]
        
        if workspace_id:
            sessions = [s for s in sessions if s.workspace_id == workspace_id]
        
        return sessions
    
    def update_session(self, session_id: str, **kwargs) -> Optional[Session]:
        """Update session attributes."""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        session.updated_at = datetime.now()
        return session
    
    def end_session(self, session_id: str, reason: str = "completed") -> bool:
        """End a session."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.status = SessionStatus.ENDING
        session.updated_at = datetime.now()
        
        # Add end event
        session.add_event("session_ended", {"reason": reason})
        
        # Update timeline
        session.timeline.ended_at = datetime.now()
        
        session.status = SessionStatus.ENDED
        
        # Remove from active
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        
        return True
    
    def pause_session(self, session_id: str) -> bool:
        """Pause a session."""
        session = self.sessions.get(session_id)
        if not session or session.status != SessionStatus.ACTIVE:
            return False
        
        session.status = SessionStatus.PAUSED
        session.updated_at = datetime.now()
        session.add_event("session_paused")
        return True
    
    def resume_session(self, session_id: str) -> bool:
        """Resume a paused session."""
        session = self.sessions.get(session_id)
        if not session or session.status != SessionStatus.PAUSED:
            return False
        
        session.status = SessionStatus.ACTIVE
        session.updated_at = datetime.now()
        session.add_event("session_resumed")
        return True
    
    def add_interaction(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Add an interaction to the session."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.metrics.interactions += 1
        session.last_activity = datetime.now()
        session.add_event("interaction", data)
        
        # Store for replay
        if session.replay_enabled:
            session.replay_data.append({
                "timestamp": datetime.now().isoformat(),
                "type": "interaction",
                "data": data,
            })
        
        return True
    
    def replay_session(self, session_id: str, from_index: int = 0) -> List[Dict[str, Any]]:
        """Replay session events."""
        session = self.sessions.get(session_id)
        if not session or not session.replay_enabled:
            return []
        
        return session.replay_data[from_index:]
    
    def recover_session(self, session_id: str) -> bool:
        """Recover a crashed session."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.status = SessionStatus.RECOVERING
        session.updated_at = datetime.now()
        
        # Add recovery event
        session.add_event("session_recovering")
        
        # Restore to previous state
        session.status = SessionStatus.ACTIVE
        
        session.add_event("session_recovered")
        return True
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get session analytics."""
        session = self.sessions.get(session_id)
        if not session:
            return {}
        
        return {
            "session_id": session.id,
            "duration_seconds": session.timeline.duration_seconds,
            "metrics": {
                "interactions": session.metrics.interactions,
                "messages_sent": session.metrics.messages_sent,
                "messages_received": session.metrics.messages_received,
                "tokens_used": session.metrics.tokens_used,
                "tokens_generated": session.metrics.tokens_generated,
                "api_calls": session.metrics.api_calls,
                "errors": session.metrics.errors,
                "avg_latency_ms": session.metrics.latency_ms_avg,
                "cost": session.metrics.cost,
            },
            "events_count": len(session.timeline.events),
            "event_types": list(set(e.event_type for e in session.timeline.events)),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
