"""
AGOS Session Manager
==================

Manages user and agent sessions.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    IDLE = "idle"
    EXPIRED = "expired"
    CLOSED = "closed"


class SessionType(Enum):
    """Session type."""
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    API = "api"


@dataclass
class SessionConfig:
    """Session configuration."""
    timeout_minutes: int = 30
    max_idle_minutes: int = 10
    enable_refresh: bool = True
    store_history: bool = True


@dataclass
class Session:
    """A session."""
    id: str
    session_type: SessionType
    owner_id: str
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if session is expired."""
        if self.expires_at and datetime.now() > self.expires_at:
            return True
        return False
    
    def touch(self) -> None:
        """Update last activity."""
        self.last_activity = datetime.now()


class SessionManager:
    """
    Session Manager.
    
    Manages user and agent sessions with timeout handling.
    
    Usage:
        manager = SessionManager()
        
        session = manager.create_session(
            session_type=SessionType.USER,
            owner_id="user-123",
        )
        
        manager.update_activity(session.id)
        manager.close_session(session.id)
    """
    
    def __init__(self, config: Optional[SessionConfig] = None):
        """Initialize session manager."""
        self.config = config or SessionConfig()
        self._sessions: Dict[str, Session] = {}
        self._owner_sessions: Dict[str, List[str]] = {}  # owner_id -> session_ids
    
    def create_session(
        self,
        session_type: SessionType,
        owner_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        expires_in_minutes: Optional[int] = None,
    ) -> Session:
        """Create a new session."""
        session_id = f"sess-{uuid.uuid4().hex[:8]}"
        
        expires_at = None
        if expires_in_minutes:
            expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        elif self.config.timeout_minutes:
            expires_at = datetime.now() + timedelta(minutes=self.config.timeout_minutes)
        
        session = Session(
            id=session_id,
            session_type=session_type,
            owner_id=owner_id,
            expires_at=expires_at,
            metadata=metadata or {},
            context=context or {},
        )
        
        self._sessions[session_id] = session
        
        if owner_id not in self._owner_sessions:
            self._owner_sessions[owner_id] = []
        self._owner_sessions[owner_id].append(session_id)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID."""
        return self._sessions.get(session_id)
    
    def list_sessions(
        self,
        status: Optional[SessionStatus] = None,
        session_type: Optional[SessionType] = None,
    ) -> List[Session]:
        """List sessions with optional filtering."""
        sessions = list(self._sessions.values())
        
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        if session_type:
            sessions = [s for s in sessions if s.session_type == session_type]
        
        return sessions
    
    def update_activity(self, session_id: str) -> bool:
        """Update session activity."""
        session = self._sessions.get(session_id)
        if not session:
            return False
        
        session.touch()
        
        if session.status == SessionStatus.IDLE:
            session.status = SessionStatus.ACTIVE
        
        return True
    
    def close_session(self, session_id: str) -> bool:
        """Close a session."""
        session = self._sessions.get(session_id)
        if not session:
            return False
        
        session.status = SessionStatus.CLOSED
        return True
    
    def expire_session(self, session_id: str) -> bool:
        """Mark a session as expired."""
        session = self._sessions.get(session_id)
        if not session:
            return False
        
        session.status = SessionStatus.EXPIRED
        return True
    
    def cleanup_expired(self) -> int:
        """Clean up expired sessions."""
        count = 0
        for session in self._sessions.values():
            if session.is_expired() and session.status == SessionStatus.ACTIVE:
                session.status = SessionStatus.EXPIRED
                count += 1
        return count
    
    def get_sessions_for(self, owner_id: str) -> List[Session]:
        """Get all sessions for an owner."""
        session_ids = self._owner_sessions.get(owner_id, [])
        return [self._sessions[sid] for sid in session_ids if sid in self._sessions]
    
    def get_active_count(self) -> int:
        """Get count of active sessions."""
        return sum(1 for s in self._sessions.values() if s.status == SessionStatus.ACTIVE)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "total_sessions": len(self._sessions),
            "active_sessions": sum(1 for s in self._sessions.values() if s.status == SessionStatus.ACTIVE),
            "idle_sessions": sum(1 for s in self._sessions.values() if s.status == SessionStatus.IDLE),
            "expired_sessions": sum(1 for s in self._sessions.values() if s.status == SessionStatus.EXPIRED),
            "closed_sessions": sum(1 for s in self._sessions.values() if s.status == SessionStatus.CLOSED),
            "by_type": {
                stype.value: sum(1 for s in self._sessions.values() if s.session_type == stype)
                for stype in SessionType
            },
        }


# Global instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the global session manager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
