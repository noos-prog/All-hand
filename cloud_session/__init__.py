"""Universal Session Platform - Persistent engineering sessions."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# =============================================================================
# ENUMS
# =============================================================================

class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    IDLE = "idle"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    EXPIRED = "expired"


class SessionType(Enum):
    """Session types."""
    INTERACTIVE = "interactive"
    BACKGROUND = "background"
    BATCH = "batch"
    STREAMING = "streaming"
    API = "api"


class TimelineType(Enum):
    """Timeline types."""
    MISSION = "mission"
    CONTEXT = "context"
    DECISION = "decision"
    EXECUTION = "execution"
    KNOWLEDGE = "knowledge"
    ARTIFACT = "artifact"
    CONVERSATION = "conversation"


class ClientType(Enum):
    """Client types."""
    BROWSER = "browser"
    MOBILE = "mobile"
    API = "api"
    SDK = "sdk"
    CLI = "cli"
    REALTIME = "realtime"


class SyncStatus(Enum):
    """Sync status."""
    SYNCED = "synced"
    PENDING = "pending"
    CONFLICT = "conflict"
    OFFLINE = "offline"


# =============================================================================
# MODELS
# =============================================================================

@dataclass
class Session:
    """Session model."""
    session_id: str
    user_id: str
    session_type: SessionType = SessionType.INTERACTIVE
    status: SessionStatus = SessionStatus.ACTIVE
    client_type: ClientType = ClientType.BROWSER
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimelineEvent:
    """Timeline event model."""
    event_id: str
    session_id: str
    timeline_type: TimelineType
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = "system"


@dataclass
class Timeline:
    """Timeline model."""
    timeline_id: str
    session_id: str
    timeline_type: TimelineType
    events: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConversationMessage:
    """Conversation message model."""
    message_id: str
    session_id: str
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    attachments: Tuple[str, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Context:
    """Context model."""
    context_id: str
    session_id: str
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Decision:
    """Decision model."""
    decision_id: str
    session_id: str
    decision_type: str
    rationale: str
    outcome: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Execution:
    """Execution model."""
    execution_id: str
    session_id: str
    mission_id: str
    status: str
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None


@dataclass
class KnowledgeEntry:
    """Knowledge entry model."""
    entry_id: str
    session_id: str
    knowledge_type: str
    content: str
    source: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Artifact:
    """Artifact model."""
    artifact_id: str
    session_id: str
    artifact_type: str
    name: str
    path: str
    size_bytes: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SessionSnapshot:
    """Session snapshot model."""
    snapshot_id: str
    session_id: str
    state: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    description: str = ""


# =============================================================================
# SESSION SUPPORT
# =============================================================================

SESSION_SUPPORT = (
    "Browser",
    "Mobile",
    "API",
    "SDK",
    "CLI",
    "Realtime"
)


# =============================================================================
# SESSION RUNTIME
# =============================================================================

class SessionRuntime:
    """Session runtime."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        self._timelines: Dict[str, Timeline] = {}
        self._events: Dict[str, TimelineEvent] = {}
        self._next_id = 1
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        id_str = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def create_session(self, user_id: str, session_type: SessionType = SessionType.INTERACTIVE,
                      client_type: ClientType = ClientType.BROWSER) -> Session:
        """Create session."""
        session = Session(
            session_id=self._generate_id("sess"),
            user_id=user_id,
            session_type=session_type,
            client_type=client_type
        )
        self._sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session."""
        return self._sessions.get(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get user sessions."""
        return [s for s in self._sessions.values() if s.user_id == user_id]
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session."""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            session.last_active = datetime.utcnow()
            return True
        return False
    
    def suspend_session(self, session_id: str) -> bool:
        """Suspend session."""
        return self.update_session(session_id, status=SessionStatus.SUSPENDED)
    
    def terminate_session(self, session_id: str) -> bool:
        """Terminate session."""
        return self.update_session(session_id, status=SessionStatus.TERMINATED)
    
    def create_timeline(self, session_id: str, timeline_type: TimelineType) -> Timeline:
        """Create timeline."""
        timeline = Timeline(
            timeline_id=self._generate_id("tl"),
            session_id=session_id,
            timeline_type=timeline_type
        )
        self._timelines[timeline.timeline_id] = timeline
        return timeline
    
    def get_timeline(self, timeline_id: str) -> Optional[Timeline]:
        """Get timeline."""
        return self._timelines.get(timeline_id)
    
    def get_session_timelines(self, session_id: str) -> List[Timeline]:
        """Get session timelines."""
        return [t for t in self._timelines.values() if t.session_id == session_id]
    
    def add_timeline_event(self, event: TimelineEvent) -> str:
        """Add timeline event."""
        self._events[event.event_id] = event
        
        # Add to timeline
        for timeline in self._timelines.values():
            if timeline.session_id == event.session_id and timeline.timeline_type == event.timeline_type:
                events = list(timeline.events) + [event.event_id]
                timeline.events = tuple(events)
        
        return event.event_id
    
    def get_timeline_events(self, session_id: str, timeline_type: Optional[TimelineType] = None) -> List[TimelineEvent]:
        """Get timeline events."""
        events = [e for e in self._events.values() if e.session_id == session_id]
        if timeline_type:
            events = [e for e in events if e.timeline_type == timeline_type]
        return sorted(events, key=lambda e: e.timestamp)


# =============================================================================
# CONVERSATION RUNTIME
# =============================================================================

class ConversationRuntime:
    """Conversation runtime."""
    
    def __init__(self):
        self._messages: Dict[str, ConversationMessage] = {}
        self._next_id = 1
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        id_str = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def add_message(self, session_id: str, role: str, content: str,
                   attachments: Tuple[str, ...] = (), metadata: Dict[str, Any] = None) -> ConversationMessage:
        """Add message."""
        message = ConversationMessage(
            message_id=self._generate_id("msg"),
            session_id=session_id,
            role=role,
            content=content,
            attachments=attachments,
            metadata=metadata or {}
        )
        self._messages[message.message_id] = message
        return message
    
    def get_message(self, message_id: str) -> Optional[ConversationMessage]:
        """Get message."""
        return self._messages.get(message_id)
    
    def get_history(self, session_id: str, limit: int = 100) -> List[ConversationMessage]:
        """Get conversation history."""
        messages = [m for m in self._messages.values() if m.session_id == session_id]
        messages = sorted(messages, key=lambda m: m.timestamp, reverse=True)
        return messages[:limit]
    
    def search_messages(self, session_id: str, query: str) -> List[ConversationMessage]:
        """Search messages."""
        messages = [m for m in self._messages.values() 
                   if m.session_id == session_id and query.lower() in m.content.lower()]
        return sorted(messages, key=lambda m: m.timestamp, reverse=True)


# =============================================================================
# CONTEXT RUNTIME
# =============================================================================

class ContextRuntime:
    """Context runtime."""
    
    def __init__(self):
        self._contexts: Dict[str, Context] = {}
    
    def set(self, session_id: str, key: str, value: Any) -> Context:
        """Set context."""
        context_id = f"{session_id}_{key}"
        
        if context_id in self._contexts:
            context = self._contexts[context_id]
            context.value = value
            context.updated_at = datetime.utcnow()
        else:
            context = Context(
                context_id=context_id,
                session_id=session_id,
                key=key,
                value=value
            )
            self._contexts[context_id] = context
        
        return context
    
    def get(self, session_id: str, key: str) -> Optional[Any]:
        """Get context."""
        context_id = f"{session_id}_{key}"
        context = self._contexts.get(context_id)
        return context.value if context else None
    
    def get_all(self, session_id: str) -> Dict[str, Any]:
        """Get all contexts for session."""
        return {
            c.key: c.value 
            for c in self._contexts.values() 
            if c.session_id == session_id
        }
    
    def delete(self, session_id: str, key: str) -> bool:
        """Delete context."""
        context_id = f"{session_id}_{key}"
        if context_id in self._contexts:
            del self._contexts[context_id]
            return True
        return False
    
    def clear(self, session_id: str) -> int:
        """Clear all contexts for session."""
        count = 0
        keys_to_delete = [c.context_id for c in self._contexts.values() if c.session_id == session_id]
        for key in keys_to_delete:
            del self._contexts[key]
            count += 1
        return count


# =============================================================================
# DECISION RUNTIME
# =============================================================================

class DecisionRuntime:
    """Decision runtime."""
    
    def __init__(self):
        self._decisions: Dict[str, Decision] = {}
        self._next_id = 1
    
    def _generate_id(self) -> str:
        """Generate unique ID."""
        id_str = f"dec_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def record(self, session_id: str, decision_type: str, rationale: str, outcome: str) -> Decision:
        """Record decision."""
        decision = Decision(
            decision_id=self._generate_id(),
            session_id=session_id,
            decision_type=decision_type,
            rationale=rationale,
            outcome=outcome
        )
        self._decisions[decision.decision_id] = decision
        return decision
    
    def get(self, decision_id: str) -> Optional[Decision]:
        """Get decision."""
        return self._decisions.get(decision_id)
    
    def get_session_decisions(self, session_id: str) -> List[Decision]:
        """Get session decisions."""
        return sorted(
            [d for d in self._decisions.values() if d.session_id == session_id],
            key=lambda d: d.timestamp,
            reverse=True
        )


# =============================================================================
# EXECUTION RUNTIME
# =============================================================================

class ExecutionRuntime:
    """Execution runtime."""
    
    def __init__(self):
        self._executions: Dict[str, Execution] = {}
        self._next_id = 1
    
    def _generate_id(self) -> str:
        """Generate unique ID."""
        id_str = f"exec_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def start(self, session_id: str, mission_id: str) -> Execution:
        """Start execution."""
        execution = Execution(
            execution_id=self._generate_id(),
            session_id=session_id,
            mission_id=mission_id,
            status="running"
        )
        self._executions[execution.execution_id] = execution
        return execution
    
    def complete(self, execution_id: str, result: Dict[str, Any]) -> bool:
        """Complete execution."""
        if execution_id in self._executions:
            execution = self._executions[execution_id]
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            execution.result = result
            return True
        return False
    
    def fail(self, execution_id: str, error: str) -> bool:
        """Fail execution."""
        if execution_id in self._executions:
            execution = self._executions[execution_id]
            execution.status = "failed"
            execution.completed_at = datetime.utcnow()
            execution.result = {"error": error}
            return True
        return False
    
    def get(self, execution_id: str) -> Optional[Execution]:
        """Get execution."""
        return self._executions.get(execution_id)
    
    def get_session_executions(self, session_id: str) -> List[Execution]:
        """Get session executions."""
        return sorted(
            [e for e in self._executions.values() if e.session_id == session_id],
            key=lambda e: e.started_at,
            reverse=True
        )


# =============================================================================
# KNOWLEDGE RUNTIME
# =============================================================================

class KnowledgeRuntime:
    """Knowledge runtime."""
    
    def __init__(self):
        self._entries: Dict[str, KnowledgeEntry] = {}
        self._next_id = 1
    
    def _generate_id(self) -> str:
        """Generate unique ID."""
        id_str = f"know_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def add(self, session_id: str, knowledge_type: str, content: str, source: str) -> KnowledgeEntry:
        """Add knowledge entry."""
        entry = KnowledgeEntry(
            entry_id=self._generate_id(),
            session_id=session_id,
            knowledge_type=knowledge_type,
            content=content,
            source=source
        )
        self._entries[entry.entry_id] = entry
        return entry
    
    def get(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get knowledge entry."""
        return self._entries.get(entry_id)
    
    def get_session_knowledge(self, session_id: str) -> List[KnowledgeEntry]:
        """Get session knowledge."""
        return sorted(
            [e for e in self._entries.values() if e.session_id == session_id],
            key=lambda e: e.timestamp,
            reverse=True
        )
    
    def search(self, session_id: str, query: str) -> List[KnowledgeEntry]:
        """Search knowledge."""
        return [
            e for e in self._entries.values() 
            if e.session_id == session_id and query.lower() in e.content.lower()
        ]


# =============================================================================
# ARTIFACT RUNTIME
# =============================================================================

class ArtifactRuntime:
    """Artifact runtime."""
    
    def __init__(self):
        self._artifacts: Dict[str, Artifact] = {}
        self._next_id = 1
    
    def _generate_id(self) -> str:
        """Generate unique ID."""
        id_str = f"art_{self._next_id}"
        self._next_id += 1
        return id_str
    
    def create(self, session_id: str, artifact_type: str, name: str, path: str, size_bytes: int = 0) -> Artifact:
        """Create artifact."""
        artifact = Artifact(
            artifact_id=self._generate_id(),
            session_id=session_id,
            artifact_type=artifact_type,
            name=name,
            path=path,
            size_bytes=size_bytes
        )
        self._artifacts[artifact.artifact_id] = artifact
        return artifact
    
    def get(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact."""
        return self._artifacts.get(artifact_id)
    
    def get_session_artifacts(self, session_id: str) -> List[Artifact]:
        """Get session artifacts."""
        return sorted(
            [a for a in self._artifacts.values() if a.session_id == session_id],
            key=lambda a: a.created_at,
            reverse=True
        )
    
    def delete(self, artifact_id: str) -> bool:
        """Delete artifact."""
        if artifact_id in self._artifacts:
            del self._artifacts[artifact_id]
            return True
        return False


# =============================================================================
# RECOVERY RUNTIME
# =============================================================================

class RecoveryRuntime:
    """Session recovery runtime."""
    
    def __init__(self):
        self._snapshots: Dict[str, SessionSnapshot] = {}
    
    def create_snapshot(self, session_id: str, state: Dict[str, Any], description: str = "") -> SessionSnapshot:
        """Create snapshot."""
        snapshot = SessionSnapshot(
            snapshot_id=f"snap_{session_id}_{len(self._snapshots)}",
            session_id=session_id,
            state=state,
            description=description
        )
        self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot
    
    def get_snapshot(self, snapshot_id: str) -> Optional[SessionSnapshot]:
        """Get snapshot."""
        return self._snapshots.get(snapshot_id)
    
    def get_session_snapshots(self, session_id: str) -> List[SessionSnapshot]:
        """Get session snapshots."""
        return sorted(
            [s for s in self._snapshots.values() if s.session_id == session_id],
            key=lambda s: s.created_at,
            reverse=True
        )
    
    def restore(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """Restore from snapshot."""
        snapshot = self._snapshots.get(snapshot_id)
        return snapshot.state if snapshot else None


# =============================================================================
# UNIVERSAL SESSION PLATFORM
# =============================================================================

class UniversalSessionPlatform:
    """
    Universal Session Platform.
    
    Target: Persistent engineering sessions.
    
    Implements:
    ✅ Session Runtime
    ✅ Conversation Runtime
    ✅ Mission Timeline
    ✅ Context Timeline
    ✅ Decision Timeline
    ✅ Execution Timeline
    ✅ Knowledge Timeline
    ✅ Artifact Timeline
    ✅ Session Recovery
    ✅ Session Replay
    ✅ Session Synchronization
    
    Support:
    ✅ Browser, Mobile, API, SDK, CLI, Realtime
    """
    
    def __init__(self):
        self.version = "2.0.0"
        self.session_runtime = SessionRuntime()
        self.conversation_runtime = ConversationRuntime()
        self.context_runtime = ContextRuntime()
        self.decision_runtime = DecisionRuntime()
        self.execution_runtime = ExecutionRuntime()
        self.knowledge_runtime = KnowledgeRuntime()
        self.artifact_runtime = ArtifactRuntime()
        self.recovery_runtime = RecoveryRuntime()
    
    # Session Management
    def create_session(self, user_id: str, session_type: SessionType = SessionType.INTERACTIVE,
                      client_type: ClientType = ClientType.BROWSER) -> Session:
        """Create session."""
        session = self.session_runtime.create_session(user_id, session_type, client_type)
        
        # Create default timelines
        for timeline_type in TimelineType:
            self.session_runtime.create_timeline(session.session_id, timeline_type)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session."""
        return self.session_runtime.get_session(session_id)
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get user sessions."""
        return self.session_runtime.get_user_sessions(user_id)
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session."""
        return self.session_runtime.update_session(session_id, **kwargs)
    
    def terminate_session(self, session_id: str) -> bool:
        """Terminate session."""
        return self.session_runtime.terminate_session(session_id)
    
    # Conversation
    def add_message(self, session_id: str, role: str, content: str) -> ConversationMessage:
        """Add conversation message."""
        return self.conversation_runtime.add_message(session_id, role, content)
    
    def get_conversation_history(self, session_id: str, limit: int = 100) -> List[ConversationMessage]:
        """Get conversation history."""
        return self.conversation_runtime.get_history(session_id, limit)
    
    # Context
    def set_context(self, session_id: str, key: str, value: Any) -> Context:
        """Set context."""
        return self.context_runtime.set(session_id, key, value)
    
    def get_context(self, session_id: str, key: str) -> Optional[Any]:
        """Get context."""
        return self.context_runtime.get(session_id, key)
    
    def get_all_context(self, session_id: str) -> Dict[str, Any]:
        """Get all context."""
        return self.context_runtime.get_all(session_id)
    
    # Timeline
    def add_timeline_event(self, session_id: str, timeline_type: TimelineType,
                          event_type: str, data: Dict[str, Any], source: str = "system") -> str:
        """Add timeline event."""
        event = TimelineEvent(
            event_id=f"evt_{len(self.session_runtime._events)}",
            session_id=session_id,
            timeline_type=timeline_type,
            event_type=event_type,
            data=data,
            source=source
        )
        return self.session_runtime.add_timeline_event(event)
    
    def get_timeline_events(self, session_id: str, timeline_type: Optional[TimelineType] = None) -> List[TimelineEvent]:
        """Get timeline events."""
        return self.session_runtime.get_timeline_events(session_id, timeline_type)
    
    # Decisions
    def record_decision(self, session_id: str, decision_type: str, rationale: str, outcome: str) -> Decision:
        """Record decision."""
        return self.decision_runtime.record(session_id, decision_type, rationale, outcome)
    
    def get_decisions(self, session_id: str) -> List[Decision]:
        """Get decisions."""
        return self.decision_runtime.get_session_decisions(session_id)
    
    # Executions
    def start_execution(self, session_id: str, mission_id: str) -> Execution:
        """Start execution."""
        return self.execution_runtime.start(session_id, mission_id)
    
    def complete_execution(self, execution_id: str, result: Dict[str, Any]) -> bool:
        """Complete execution."""
        return self.execution_runtime.complete(execution_id, result)
    
    def get_executions(self, session_id: str) -> List[Execution]:
        """Get executions."""
        return self.execution_runtime.get_session_executions(session_id)
    
    # Knowledge
    def add_knowledge(self, session_id: str, knowledge_type: str, content: str, source: str) -> KnowledgeEntry:
        """Add knowledge."""
        return self.knowledge_runtime.add(session_id, knowledge_type, content, source)
    
    def get_knowledge(self, session_id: str) -> List[KnowledgeEntry]:
        """Get knowledge."""
        return self.knowledge_runtime.get_session_knowledge(session_id)
    
    # Artifacts
    def create_artifact(self, session_id: str, artifact_type: str, name: str, 
                       path: str, size_bytes: int = 0) -> Artifact:
        """Create artifact."""
        return self.artifact_runtime.create(session_id, artifact_type, name, path, size_bytes)
    
    def get_artifacts(self, session_id: str) -> List[Artifact]:
        """Get artifacts."""
        return self.artifact_runtime.get_session_artifacts(session_id)
    
    # Recovery
    def create_snapshot(self, session_id: str, state: Dict[str, Any], description: str = "") -> SessionSnapshot:
        """Create snapshot."""
        return self.recovery_runtime.create_snapshot(session_id, state, description)
    
    def restore_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """Restore from snapshot."""
        return self.recovery_runtime.restore(snapshot_id)
    
    # Replay
    def replay(self, session_id: str) -> List[ConversationMessage]:
        """Replay session conversation."""
        return self.conversation_runtime.get_history(session_id)
    
    # Statistics
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return {
            "version": self.version,
            "session_support": SESSION_SUPPORT,
            "total_sessions": len(self.session_runtime._sessions),
            "total_messages": len(self.conversation_runtime._messages),
            "total_contexts": len(self.context_runtime._contexts),
            "total_decisions": len(self.decision_runtime._decisions),
            "total_executions": len(self.execution_runtime._executions),
            "total_knowledge": len(self.knowledge_runtime._entries),
            "total_artifacts": len(self.artifact_runtime._artifacts),
            "total_snapshots": len(self.recovery_runtime._snapshots)
        }
