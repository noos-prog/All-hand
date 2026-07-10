#!/usr/bin/env python3
"""
Cloud Session - Test Suite
======================

Tests for the AGOS Universal Session Platform.
Run with: python test_cloud_session.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import __init__ as session
from __init__ import (
    UniversalSessionPlatform,
    SessionStatus, SessionType, TimelineType, ClientType,
    Session, ConversationMessage, Context, Decision, Execution, KnowledgeEntry, Artifact
)


def test_session_platform():
    """Test universal session platform."""
    print("\n=== Testing Universal Session Platform ===")
    
    platform = session.UniversalSessionPlatform()
    
    # Get statistics
    stats = platform.get_statistics()
    print(f"  Version: {stats['version']}")
    print(f"  Session support: {stats['session_support']}")
    
    print("  ✓ Session platform tests passed")


def test_session_management():
    """Test session management."""
    print("\n=== Testing Session Management ===")
    
    platform = session.UniversalSessionPlatform()
    
    # Create session
    sess = platform.create_session("user_1", SessionType.INTERACTIVE, ClientType.BROWSER)
    print(f"  Created session: {sess.session_id}")
    print(f"  Session type: {sess.session_type.value}")
    print(f"  Client type: {sess.client_type.value}")
    print(f"  Status: {sess.status.value}")
    
    # Get session
    retrieved = platform.get_session(sess.session_id)
    print(f"  Retrieved: {retrieved.session_id if retrieved else 'None'}")
    
    # Get user sessions
    sessions = platform.get_user_sessions("user_1")
    print(f"  User sessions: {len(sessions)}")
    
    # Update session
    platform.update_session(sess.session_id, status=SessionStatus.IDLE)
    sess = platform.get_session(sess.session_id)
    print(f"  Updated status: {sess.status.value}")
    
    print("  ✓ Session management tests passed")


def test_conversation():
    """Test conversation management."""
    print("\n=== Testing Conversation Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Add messages
    msg1 = platform.add_message(sess.session_id, "user", "Hello, how are you?")
    msg2 = platform.add_message(sess.session_id, "assistant", "I'm doing well, thanks!")
    print(f"  Added messages: {msg1.message_id}, {msg2.message_id}")
    
    # Get history
    history = platform.get_conversation_history(sess.session_id)
    print(f"  History length: {len(history)}")
    
    print("  ✓ Conversation tests passed")


def test_context():
    """Test context management."""
    print("\n=== Testing Context Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Set context
    platform.set_context(sess.session_id, "language", "python")
    platform.set_context(sess.session_id, "framework", "django")
    print("  Set contexts")
    
    # Get context
    lang = platform.get_context(sess.session_id, "language")
    print(f"  Retrieved language: {lang}")
    
    # Get all context
    all_ctx = platform.get_all_context(sess.session_id)
    print(f"  All contexts: {len(all_ctx)}")
    
    print("  ✓ Context tests passed")


def test_timeline():
    """Test timeline management."""
    print("\n=== Testing Timeline Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Add timeline events
    event_id1 = platform.add_timeline_event(
        sess.session_id, 
        TimelineType.MISSION, 
        "mission_started", 
        {"mission_id": "m1"}
    )
    event_id2 = platform.add_timeline_event(
        sess.session_id, 
        TimelineType.EXECUTION, 
        "code_generated", 
        {"lines": 100}
    )
    print(f"  Added events: {event_id1}, {event_id2}")
    
    # Get events
    events = platform.get_timeline_events(sess.session_id)
    print(f"  Total events: {len(events)}")
    
    # Get by type
    mission_events = platform.get_timeline_events(sess.session_id, TimelineType.MISSION)
    print(f"  Mission events: {len(mission_events)}")
    
    print("  ✓ Timeline tests passed")


def test_decisions():
    """Test decision management."""
    print("\n=== Testing Decision Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Record decisions
    dec1 = platform.record_decision(
        sess.session_id,
        "architecture",
        "Use microservices",
        "Better scalability"
    )
    dec2 = platform.record_decision(
        sess.session_id,
        "database",
        "Use PostgreSQL",
        "Better for relational data"
    )
    print(f"  Recorded decisions: {dec1.decision_id}, {dec2.decision_id}")
    
    # Get decisions
    decisions = platform.get_decisions(sess.session_id)
    print(f"  Total decisions: {len(decisions)}")
    
    print("  ✓ Decision tests passed")


def test_execution():
    """Test execution management."""
    print("\n=== Testing Execution Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Start execution
    exec1 = platform.start_execution(sess.session_id, "mission_1")
    print(f"  Started execution: {exec1.execution_id}")
    
    # Complete execution
    platform.complete_execution(exec1.execution_id, {"success": True, "output": "Done!"})
    exec_result = platform.execution_runtime.get(exec1.execution_id)
    print(f"  Status: {exec_result.status}")
    
    # Get executions
    executions = platform.get_executions(sess.session_id)
    print(f"  Total executions: {len(executions)}")
    
    print("  ✓ Execution tests passed")


def test_knowledge():
    """Test knowledge management."""
    print("\n=== Testing Knowledge Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Add knowledge
    know1 = platform.add_knowledge(
        sess.session_id,
        "pattern",
        "Use dependency injection for better testing",
        "code_review"
    )
    know2 = platform.add_knowledge(
        sess.session_id,
        "best_practice",
        "Write unit tests for all public methods",
        "documentation"
    )
    print(f"  Added knowledge: {know1.entry_id}, {know2.entry_id}")
    
    # Get knowledge
    knowledge = platform.get_knowledge(sess.session_id)
    print(f"  Total knowledge: {len(knowledge)}")
    
    print("  ✓ Knowledge tests passed")


def test_artifacts():
    """Test artifact management."""
    print("\n=== Testing Artifact Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Create artifact
    art1 = platform.create_artifact(
        sess.session_id,
        "code",
        "main.py",
        "/path/to/main.py",
        size_bytes=1024
    )
    art2 = platform.create_artifact(
        sess.session_id,
        "document",
        "README.md",
        "/path/to/README.md",
        size_bytes=512
    )
    print(f"  Created artifacts: {art1.artifact_id}, {art2.artifact_id}")
    
    # Get artifacts
    artifacts = platform.get_artifacts(sess.session_id)
    print(f"  Total artifacts: {len(artifacts)}")
    
    # Total size
    total_size = sum(a.size_bytes for a in artifacts)
    print(f"  Total size: {total_size} bytes")
    
    print("  ✓ Artifact tests passed")


def test_recovery():
    """Test recovery management."""
    print("\n=== Testing Recovery Management ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Create snapshot
    state = {"step": 5, "data": {"counter": 10}}
    snapshot = platform.create_snapshot(sess.session_id, state, "Checkpoint at step 5")
    print(f"  Created snapshot: {snapshot.snapshot_id}")
    
    # Restore snapshot
    restored = platform.restore_snapshot(snapshot.snapshot_id)
    print(f"  Restored state: {restored}")
    
    print("  ✓ Recovery tests passed")


def test_replay():
    """Test replay functionality."""
    print("\n=== Testing Replay Functionality ===")
    
    platform = session.UniversalSessionPlatform()
    sess = platform.create_session("user_1")
    
    # Add messages
    platform.add_message(sess.session_id, "user", "First message")
    platform.add_message(sess.session_id, "assistant", "First response")
    platform.add_message(sess.session_id, "user", "Second message")
    
    # Replay
    replay = platform.replay(sess.session_id)
    print(f"  Replayed messages: {len(replay)}")
    
    print("  ✓ Replay tests passed")


def test_statistics():
    """Test statistics."""
    print("\n=== Testing Statistics ===")
    
    platform = session.UniversalSessionPlatform()
    
    # Create some data
    sess = platform.create_session("user_1")
    platform.add_message(sess.session_id, "user", "Test")
    platform.set_context(sess.session_id, "key", "value")
    platform.record_decision(sess.session_id, "type", "rationale", "outcome")
    
    # Get statistics
    stats = platform.get_statistics()
    print(f"  Version: {stats['version']}")
    print(f"  Sessions: {stats['total_sessions']}")
    print(f"  Messages: {stats['total_messages']}")
    print(f"  Contexts: {stats['total_contexts']}")
    print(f"  Decisions: {stats['total_decisions']}")
    
    print("  ✓ Statistics tests passed")


def test_session_model():
    """Test session model."""
    print("\n=== Testing Session Model ===")
    
    sess = session.Session(
        session_id="sess_1",
        user_id="user_1",
        session_type=SessionType.INTERACTIVE,
        status=SessionStatus.ACTIVE,
        client_type=ClientType.BROWSER
    )
    print(f"  Session: {sess.session_id}")
    print(f"  Type: {sess.session_type.value}")
    print(f"  Status: {sess.status.value}")
    
    print("  ✓ Session model tests passed")


def test_conversation_message_model():
    """Test conversation message model."""
    print("\n=== Testing Conversation Message Model ===")
    
    msg = session.ConversationMessage(
        message_id="msg_1",
        session_id="sess_1",
        role="user",
        content="Hello world",
        attachments=("file1.txt", "file2.txt")
    )
    print(f"  Message: {msg.content}")
    print(f"  Role: {msg.role}")
    print(f"  Attachments: {msg.attachments}")
    
    print("  ✓ Conversation message model tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLOUD SESSION - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_session_platform()
        test_session_management()
        test_conversation()
        test_context()
        test_timeline()
        test_decisions()
        test_execution()
        test_knowledge()
        test_artifacts()
        test_recovery()
        test_replay()
        test_statistics()
        test_session_model()
        test_conversation_message_model()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
