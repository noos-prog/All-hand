#!/usr/bin/env python3
"""
AGOS Intelligence - Test Suite
==============================

Tests for the intelligence system.
Run with: python test_intelligence.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from intelligence_modes import (
    IntelligenceEngine, ModeType, ModeStatus,
    InstantMode, EngineerMode, ResearchMode, ModeResult
)
from decision_engine import (
    DecisionEngine, DecisionType, DecisionConfidence,
    DecisionRule, Evidence
)
from knowledge_base import (
    KnowledgeBase, IntelligenceKnowledge,
    KnowledgeSource, Evidence, EvidenceType
)
from time_machine import (
    TimeMachine, MissionSnapshot, MissionStatus, TimelineEvent
)
from academy import (
    AGOSAcademy, LearningPath, LearningLevel
)


def test_intelligence_modes():
    """Test intelligence modes."""
    print("\n=== Testing Intelligence Modes ===")
    
    engine = IntelligenceEngine()
    
    # Test instant mode selection
    instant_request = {
        "intent": "fix this bug",
        "request_id": "test_001"
    }
    mode = engine.select_mode(instant_request)
    assert mode == ModeType.INSTANT
    print(f"  Instant request → {mode.value}")
    
    # Test engineer mode selection
    engineer_request = {
        "intent": "build production API",
        "request_id": "test_002"
    }
    mode = engine.select_mode(engineer_request)
    assert mode == ModeType.ENGINEER
    print(f"  Production request → {mode.value}")
    
    # Test research mode selection
    research_request = {
        "intent": "how should I build real-time collaboration",
        "request_id": "test_003"
    }
    mode = engine.select_mode(research_request)
    assert mode == ModeType.RESEARCH
    print(f"  Research request → {mode.value}")
    
    # Test instant mode execution
    instant_mode = InstantMode()
    result = instant_mode.execute(instant_request)
    print(f"  Instant execution: {result.status.value}")
    assert result.is_success()
    
    # Test engineer mode execution
    engineer_mode = EngineerMode()
    result = engineer_mode.execute(engineer_request)
    print(f"  Engineer execution: {result.status.value}")
    assert result.status == ModeStatus.AWAITING_APPROVAL
    
    # Test research mode execution
    research_mode = ResearchMode()
    result = research_mode.execute(research_request)
    print(f"  Research execution: {result.status.value}")
    assert result.is_success()
    
    print("  ✓ Intelligence modes tests passed")


def test_decision_engine():
    """Test decision engine."""
    print("\n=== Testing Decision Engine ===")
    
    engine = DecisionEngine()
    
    # Add a rule
    rule = DecisionRule(
        rule_id="test_rule",
        name="Test Rule",
        description="A test rule",
        decision_type=DecisionType.ROUTING,
        condition="priority >= 5",
        priority=100,
    )
    engine.add_rule(rule)
    
    # Test rule was added
    retrieved_rule = engine.get_rule("test_rule")
    assert retrieved_rule is not None
    print(f"  Rule added: {retrieved_rule.name}")
    
    # Test making a decision
    decision = engine.decide(
        decision_type=DecisionType.ROUTING,
        input_data=("test input",),
        context={"priority": 8, "intent": "test"},
    )
    print(f"  Decision made: {decision.decision_id}")
    print(f"  Decision type: {decision.decision_type.value}")
    print(f"  Confidence: {decision.confidence.value}")
    
    # Test decision history
    history = engine.get_decision_history()
    assert len(history) == 1
    print(f"  Decision history: {len(history)} decisions")
    
    # Test explain decision
    explanation = engine.explain_decision(decision.decision_id)
    assert "what_was_decided" in explanation
    print(f"  Decision explained successfully")
    
    # Test statistics
    stats = engine.get_statistics()
    print(f"  Statistics: {stats['total_decisions']} decisions, {stats['total_rules']} rules")
    
    print("  ✓ Decision engine tests passed")


def test_knowledge_base():
    """Test knowledge base."""
    print("\n=== Testing Knowledge Base ===")
    
    kb = KnowledgeBase()
    
    # Create evidence
    evidence = Evidence(
        evidence_id="ev_001",
        evidence_type=EvidenceType.STATISTICAL,
        source=KnowledgeSource.REPOSITORY_ANALYSIS,
        content={"finding": "70% of successful projects use this approach"},
        confidence=0.85,
        timestamp="2024-01-01T00:00:00",
    )
    
    # Create knowledge
    knowledge = IntelligenceKnowledge(
        knowledge_id="know_001",
        topic="api_design",
        statement="REST APIs with clear versioning are more maintainable",
        category="best_practices",
        evidence=(evidence,),
        confidence=0.85,
        tags=("api", "rest", "design"),
    )
    
    # Add knowledge
    kb.add_knowledge(knowledge)
    print(f"  Knowledge added: {knowledge.statement[:50]}...")
    
    # Search knowledge
    results = kb.search(query="api")
    assert len(results) >= 1
    print(f"  Search found: {len(results)} results")
    
    # Get statistics
    stats = kb.get_statistics()
    print(f"  Knowledge base stats: {stats['total_knowledge']} items")
    
    print("  ✓ Knowledge base tests passed")


def test_time_machine():
    """Test time machine."""
    print("\n=== Testing Time Machine ===")
    
    tm = TimeMachine()
    
    # Record mission start
    mission_id = tm.record_mission_start(
        mission_id="mission_001",
        goal="Build authentication system",
        mode="engineer",
        context={"priority": 8},
    )
    print(f"  Mission started: {mission_id}")
    
    # Record events
    event_id = tm.record_event(
        mission_id=mission_id,
        event_type="task_started",
        data={"task": "auth_service"},
        actor="engineer_mode",
    )
    print(f"  Event recorded: {event_id}")
    
    # Record decision
    tm.record_decision(
        mission_id=mission_id,
        decision={
            "decision_id": "dec_001",
            "output": "claude",
            "reasoning": "Best for auth code",
        }
    )
    print("  Decision recorded")
    
    # Complete mission
    tm.complete_mission(
        mission_id=mission_id,
        outcome={"status": "success"},
        lessons=["JWT worked well", "Rate limiting needed"],
        duration_seconds=16200,
        cost_usd=8.50,
    )
    print("  Mission completed")
    
    # Get mission
    mission = tm.get_mission(mission_id)
    assert mission is not None
    assert mission.status == MissionStatus.COMPLETED
    print(f"  Mission retrieved: {mission.goal}")
    
    # Find similar missions
    similar = tm.find_similar_missions("Build authentication")
    print(f"  Similar missions: {len(similar)}")
    
    # Get statistics
    stats = tm.get_statistics()
    print(f"  Time machine stats: {stats['total_missions']} missions")
    
    print("  ✓ Time machine tests passed")


def test_academy():
    """Test AGOS Academy."""
    print("\n=== Testing AGOS Academy ===")
    
    academy = AGOSAcademy()
    
    # Get best practices
    practices = academy.get_best_practices()
    assert len(practices) > 0
    print(f"  Best practices: {len(practices)}")
    
    # Get architectures
    architectures = academy.get_architectures()
    assert len(architectures) > 0
    print(f"  Architectures: {len(architectures)}")
    
    # Get providers
    providers = academy.get_provider_recommendations(category="llm")
    assert len(providers) > 0
    print(f"  LLM providers: {len(providers)}")
    
    # Get common mistakes
    mistakes = academy.get_common_mistakes()
    assert len(mistakes) > 0
    print(f"  Common mistakes: {len(mistakes)}")
    
    # Get topic overview
    overview = academy.get_topic_overview("architecture")
    assert "best_practices" in overview
    print(f"  Topic overview generated: {overview['summary'][:50]}...")
    
    # Get learning paths
    paths = academy.get_learning_paths()
    assert len(paths) > 0
    print(f"  Learning paths: {len(paths)}")
    
    # Generate learning plan
    plan = academy.generate_learning_plan("Build a SaaS application")
    assert "recommended_paths" in plan
    print(f"  Learning plan generated with {len(plan['next_steps'])} steps")
    
    # Get statistics
    stats = academy.get_statistics()
    print(f"  Academy stats: {stats['total_content_items']} content items")
    
    print("  ✓ Academy tests passed")


def test_integration():
    """Test integration between modules."""
    print("\n=== Testing Integration ===")
    
    # Create knowledge base with evidence
    kb = KnowledgeBase()
    evidence = Evidence(
        evidence_id="ev_integration",
        evidence_type=EvidenceType.STATISTICAL,
        source=KnowledgeSource.REPOSITORY_ANALYSIS,
        content={"finding": "Microservices have 85% success rate"},
        confidence=0.90,
        timestamp="2024-01-01T00:00:00",
    )
    knowledge = IntelligenceKnowledge(
        knowledge_id="know_integration",
        topic="microservices",
        statement="Microservices architecture",
        category="architecture",
        evidence=(evidence,),
        confidence=0.90,
    )
    kb.add_knowledge(knowledge)
    
    # Create decision engine with knowledge base
    engine = DecisionEngine(knowledge_base=kb)
    decision = engine.decide(
        decision_type=DecisionType.ROUTING,
        input_data=("architecture",),
        context={"topic": "microservices"},
    )
    print(f"  Decision with knowledge: {decision.decision_id}")
    assert len(decision.evidence_ids) > 0
    
    # Create time machine with knowledge base
    tm = TimeMachine(knowledge_base=kb)
    mission_id = tm.record_mission_start(
        mission_id="mission_integration",
        goal="Build microservices app",
        mode="research",
        context={},
    )
    
    # Create academy
    academy = AGOSAcademy(knowledge_base=kb)
    overview = academy.get_topic_overview("microservices")
    print(f"  Academy overview with KB: {overview['summary'][:50]}...")
    
    print("  ✓ Integration tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("AGOS INTELLIGENCE - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_intelligence_modes()
        test_decision_engine()
        test_knowledge_base()
        test_time_machine()
        test_academy()
        test_integration()
        
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
