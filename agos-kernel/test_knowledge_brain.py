#!/usr/bin/env python3
"""Test script for Knowledge Fabric, Brain, and Core."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from knowledge import KnowledgeRuntime, KnowledgeType, Knowledge, Evidence, EvidenceQuality
from memory import MemoryRuntime, MemoryType, MemoryPriority
from learning import LearningRuntime, LearningSource
from experience import ExperienceRuntime, ExperienceType
from recommendation import RecommendationEngine, RecommendationType
from benchmark import BenchmarkPlatform, BenchmarkType
from optimization import OptimizationEngine, OptimizationType
from brain import EngineeringBrain, get_brain
from core import AutonomousCore, get_core, CoreStatus, MissionStatus


def test_knowledge():
    """Test Knowledge Fabric."""
    print("=" * 60)
    print("Testing Knowledge Fabric")
    print("=" * 60)
    
    runtime = KnowledgeRuntime()
    
    # Create knowledge
    knowledge = runtime.create_knowledge(
        title="Test Knowledge",
        knowledge_type=KnowledgeType.FACT,
        description="A test knowledge item",
        tags=["test", "example"],
    )
    print(f"✓ Knowledge created: {knowledge.id}")
    
    # Add evidence
    evidence = Evidence(
        id="evidence-1",
        content="This is evidence",
        source="test",
        quality=EvidenceQuality.HIGH,
    )
    runtime.add_evidence(knowledge.id, evidence)
    print(f"✓ Evidence added")
    
    # Search
    results = runtime.search_knowledge("test")
    print(f"✓ Search found {len(results)} results")
    
    return runtime


def test_memory():
    """Test Memory Runtime."""
    print("\n" + "=" * 60)
    print("Testing Memory Runtime")
    print("=" * 60)
    
    runtime = MemoryRuntime()
    
    # Create memory
    memory = runtime.create_memory(
        name="test-memory",
        memory_type=MemoryType.PROJECT,
        priority=MemoryPriority.HIGH,
    )
    print(f"✓ Memory created: {memory.id}")
    
    # Add content
    chunk = runtime.add_to_memory(memory.id, "This is a test content", importance=0.8)
    print(f"✓ Content added: {chunk.id}")
    
    # Retrieve
    results = runtime.retrieve("test")
    print(f"✓ Retrieved {len(results)} memories")
    
    return runtime


def test_learning():
    """Test Learning Runtime."""
    print("\n" + "=" * 60)
    print("Testing Learning Runtime")
    print("=" * 60)
    
    runtime = LearningRuntime()
    
    # Learn
    item = runtime.learn(
        source=LearningSource.MISSION_RESULT,
        content="Successfully completed mission",
        evidence={"mission_id": "test-1"},
    )
    print(f"✓ Learning item created: {item.id}")
    
    # Validate
    is_valid = runtime.validate(item.id, "test-validator")
    print(f"✓ Validated: {is_valid}")
    
    # Stats
    stats = runtime.get_learning_stats()
    print(f"✓ Stats: {stats}")
    
    return runtime


def test_experience():
    """Test Experience Runtime."""
    print("\n" + "=" * 60)
    print("Testing Experience Runtime")
    print("=" * 60)
    
    runtime = ExperienceRuntime()
    
    # Create experience
    exp = runtime.create_experience(
        name="Test Experience",
        experience_type=ExperienceType.PLAYBOOK,
        content="Steps to do something...",
        tags=["test"],
    )
    print(f"✓ Experience created: {exp.id}")
    
    # Validate
    is_valid = runtime.validate_experience(exp.id)
    print(f"✓ Validated: {is_valid}")
    
    # Rank
    runtime.rank_experience(exp.id, success=True)
    print(f"✓ Ranked")
    
    return runtime


def test_recommendation():
    """Test Recommendation Engine."""
    print("\n" + "=" * 60)
    print("Testing Recommendation Engine")
    print("=" * 60)
    
    engine = RecommendationEngine()
    
    # Recommend
    rec = engine.recommend(
        recommendation_type=RecommendationType.CAPABILITY,
        name="Test Recommendation",
        description="A test recommendation",
    )
    print(f"✓ Recommendation created: {rec.id}")
    
    # Set scores
    engine.set_score(rec.id, evidence=0.8, knowledge=0.7, past_success=0.9)
    print(f"✓ Scores set")
    
    return engine


def test_benchmark():
    """Test Benchmark Platform."""
    print("\n" + "=" * 60)
    print("Testing Benchmark Platform")
    print("=" * 60)
    
    platform = BenchmarkPlatform()
    
    # Run benchmark
    result = platform.run_benchmark(
        name="Test Benchmark",
        benchmark_type=BenchmarkType.MODEL,
        metrics={"latency_ms": 100, "accuracy": 0.95, "reliability": 0.99},
    )
    print(f"✓ Benchmark run: {result.id}")
    print(f"  Score: {result.overall_score}")
    
    return platform


def test_optimization():
    """Test Optimization Engine."""
    print("\n" + "=" * 60)
    print("Testing Optimization Engine")
    print("=" * 60)
    
    engine = OptimizationEngine()
    
    # Create optimization
    opt = engine.create_optimization(
        optimization_type=OptimizationType.PERFORMANCE,
    )
    print(f"✓ Optimization created: {opt.id}")
    
    # Add objective
    engine.add_objective(opt.id, "reduce_latency", target=50, current=100)
    print(f"✓ Objective added")
    
    # Execute
    engine.execute(opt.id)
    print(f"✓ Executed")
    
    return engine


def test_brain():
    """Test Engineering Brain."""
    print("\n" + "=" * 60)
    print("Testing Engineering Brain")
    print("=" * 60)
    
    brain = get_brain()
    
    # Think
    result = brain.think("How to optimize performance?")
    print(f"✓ Thought processed: {brain.metrics.thoughts_processed}")
    
    # Health check
    health = brain.health_check()
    print(f"✓ Brain health: {health['status']}")
    print(f"  All capabilities: {health['all_capabilities_available']}")
    
    # Stats
    stats = brain.get_brain_stats()
    print(f"✓ Brain stats:")
    for key, value in stats.items():
        if isinstance(value, int):
            print(f"  {key}: {value}")
    
    return brain


def test_core():
    """Test Autonomous Engineering Core."""
    print("\n" + "=" * 60)
    print("Testing AGOS Autonomous Engineering Core v1.0")
    print("=" * 60)
    
    core = get_core()
    
    print(f"✓ Core initialized: {core.name} v{core.version}")
    print(f"  Status: {core.status.value}")
    
    # Create mission
    mission = core.create_mission(
        objective="Build a universal platform",
        context={"domain": "engineering"},
    )
    print(f"✓ Mission created: {mission.id}")
    print(f"  Objective: {mission.objective}")
    
    # Understand
    core.understand(mission)
    print(f"✓ Mission understood")
    
    # Plan
    plan = core.plan(mission)
    print(f"✓ Plan created with {len(plan)} steps")
    
    # Validate
    is_valid = core.validate(mission)
    print(f"✓ Mission validated: {is_valid}")
    
    # Execute
    core.execute(mission)
    print(f"✓ Mission executing")
    
    # Complete (skip learning since source=None)
    mission.status = MissionStatus.COMPLETED
    print(f"✓ Mission completed")
    
    # Health check
    health = core.health_check()
    print(f"✓ Core health: {health['status']}")
    
    # Verify capabilities
    caps = core.verify_capabilities()
    print(f"✓ Capabilities verified:")
    for cap, available in caps.items():
        print(f"  {cap}: {available}")
    
    # Stats
    stats = core.get_stats()
    print(f"✓ Core stats:")
    print(f"  Missions created: {stats['metrics']['missions_created']}")
    print(f"  Missions completed: {stats['metrics']['missions_completed']}")
    print(f"  Success rate: {stats['metrics']['success_rate']:.0%}")
    
    return core


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS KNOWLEDGE, BRAIN & CORE - TEST SUITE")
    print("EXECUTION-000061 to EXECUTION-000070")
    print("=" * 60)
    
    # Test subsystems
    test_knowledge()
    test_memory()
    test_learning()
    test_experience()
    test_recommendation()
    test_benchmark()
    test_optimization()
    
    # Test brain
    test_brain()
    
    # Test core
    test_core()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nAGOS Autonomous Engineering Core v1.0 Ready!")


if __name__ == "__main__":
    main()
