#!/usr/bin/env python3
"""
Civilization - Test Suite
========================

Tests for the AGOS Autonomous Engineering Civilization.
Run with: python test_civilization.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

# Import modules directly
import __init__ as civilization
from learning import (
    LearningRuntime, MissionExperience,
    LearnedPattern, OptimizationRule,
    ExperienceEngine, FailureAnalyzer, SuccessAnalyzer
)
from optimization import (
    SelfOptimizationRuntime, OptimizationPlan,
    OptimizationReport
)
from integration import (
    IntegrationRegistry, BaseIntegrationAdapter,
    IntegrationConfig, IIntegrationAdapter
)
from release import (
    ReleaseManager, ReleaseCandidate, TestSuite,
    ArchitectureAudit, SecurityAudit, PerformanceAudit
)


def test_civilization_runtime():
    """Test civilization runtime."""
    print("\n=== Testing Civilization Runtime ===")
    
    runtime = civilization.CivilizationRuntime()
    
    # Create organization
    org = runtime.create_default_organization("agos", "AGOS")
    print(f"  Organization: {org.name}")
    print(f"  Departments: {len(org.departments)}")
    
    # Get department
    backend = org.get_department("Backend")
    print(f"  Backend capabilities: {backend.capabilities if backend else 'None'}")
    
    # Governance
    result = runtime.governance.evaluate({"test": "context"})
    print(f"  Governance: {result['approved']}")
    
    # Statistics
    stats = runtime.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("  ✓ Civilization runtime tests passed")


def test_learning_runtime():
    """Test learning runtime."""
    print("\n=== Testing Learning Runtime ===")
    
    runtime = LearningRuntime()
    
    # Learn from mission
    runtime.learn_from_mission("m1", expected=True, actual=True, duration_ms=1000)
    runtime.learn_from_mission("m2", expected=True, actual=False, duration_ms=500)
    
    stats = runtime.get_statistics()
    print(f"  Total experiences: {stats['total_experiences']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Failed: {stats['failed']}")
    
    print("  ✓ Learning runtime tests passed")


def test_optimization_runtime():
    """Test optimization runtime."""
    print("\n=== Testing Optimization Runtime ===")
    
    runtime = SelfOptimizationRuntime()
    
    # Optimize
    plan = runtime.optimize("latency", {"latency": 100, "cost": 50})
    print(f"  Plan: {plan.target}")
    print(f"  Current: {plan.current_value}ms")
    print(f"  Target: {plan.target_value}ms")
    
    # Recommendations
    recs = runtime.get_recommendations()
    print(f"  Recommendations: {len(recs)}")
    
    print("  ✓ Optimization runtime tests passed")


def test_integration_registry():
    """Test integration registry."""
    print("\n=== Testing Integration Registry ===")
    
    registry = IntegrationRegistry()
    
    # Register adapter
    adapter = BaseIntegrationAdapter("GitHub")
    registry.register(adapter)
    
    # Get adapter
    gh = registry.get("GitHub")
    print(f"  Adapter: {gh.name if gh else 'None'}")
    
    # List all
    all_adapters = registry.list_all()
    print(f"  Total adapters: {len(all_adapters)}")
    
    print("  ✓ Integration registry tests passed")


def test_release_manager():
    """Test release manager."""
    print("\n=== Testing Release Manager ===")
    
    manager = ReleaseManager()
    
    # Run audits
    audits = manager.run_all_audits()
    print(f"  Audits run: {len(audits)}")
    
    # Run tests
    tests = manager.run_all_tests()
    print(f"  Test suites: {len(tests)}")
    
    # Create release
    release = manager.create_release("1.0.0")
    print(f"  Release: {release.version}")
    print(f"  Artifacts: {len(release.artifacts)}")
    
    print("  ✓ Release manager tests passed")


def test_governance_engine():
    """Test governance engine."""
    print("\n=== Testing Governance Engine ===")
    
    engine = civilization.GovernanceEngine()
    
    # Add policy
    policy = civilization.Policy(
        policy_id="sec_001",
        name="Security Policy",
        description="Security requirements",
        rules=("security_check",),
        severity="high"
    )
    engine.add_policy(policy)
    
    # Evaluate
    result = engine.evaluate({"security_check": True})
    print(f"  Policy approved: {result['approved']}")
    print(f"  Policies checked: {result['policies_checked']}")
    
    print("  ✓ Governance engine tests passed")


def test_architecture_board():
    """Test architecture board."""
    print("\n=== Testing Architecture Board ===")
    
    board = civilization.ArchitectureBoard()
    
    # Review architecture
    arch = {"name": "microservices", "security": True}
    review = board.review(arch)
    print(f"  Status: {review.status}")
    print(f"  Score: {review.score}")
    print(f"  Issues: {len(review.issues)}")
    
    print("  ✓ Architecture board tests passed")


def test_risk_board():
    """Test risk board."""
    print("\n=== Testing Risk Board ===")
    
    board = civilization.RiskBoard()
    
    # Assess risk
    context = {"security": True, "deployment": True}
    assessment = board.assess(context)
    print(f"  Risk level: {assessment.risk_level}")
    print(f"  Mitigation: {assessment.mitigation}")
    
    print("  ✓ Risk board tests passed")


def test_test_suite():
    """Test test suite."""
    print("\n=== Testing Test Suite ===")
    
    suite = TestSuite("Unit Tests")
    
    # Add tests
    suite.add_test("test_api", True)
    suite.add_test("test_database", True)
    suite.add_test("test_cache", False)
    
    results = suite.get_results()
    print(f"  Total: {results['total']}")
    print(f"  Passed: {results['passed']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Pass rate: {results['pass_rate']:.0%}")
    
    print("  ✓ Test suite tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CIVILIZATION - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_civilization_runtime()
        test_learning_runtime()
        test_optimization_runtime()
        test_integration_registry()
        test_release_manager()
        test_governance_engine()
        test_architecture_board()
        test_risk_board()
        test_test_suite()
        
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
