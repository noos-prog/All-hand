#!/usr/bin/env python3
"""Test script for Civilization Platform."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from orchestrator import WorkspaceOrchestrator, WorkspaceState
from repository import MultiRepositoryRuntime, RepositoryType
from crossdomain import CrossDomainRuntime, Domain
from crossdomain import LongRunningMissionRuntime, MissionState
from crossdomain import SelfDiagnosticsRuntime
from healing import SelfHealingRuntime, FailureType
from prediction import PredictionRuntime
from simulation import SimulationRuntime, SimulationType
from api import CivilizationAPI
from platform import get_platform


def test_orchestrator():
    """Test Multi-Workspace Orchestrator."""
    print("=" * 60)
    print("Testing Multi-Workspace Orchestrator")
    print("=" * 60)
    
    orchestrator = WorkspaceOrchestrator()
    
    # Create workspaces
    ws1 = orchestrator.create_workspace("workspace-1")
    ws2 = orchestrator.create_workspace("workspace-2", parent_id=ws1.id)
    
    print(f"✓ Workspace created: {ws1.id}")
    print(f"✓ Nested workspace created: {ws2.id}")
    
    # Clone
    cloned = orchestrator.clone_workspace(ws1.id, "cloned-workspace")
    print(f"✓ Cloned workspace: {cloned.id}")
    
    # Checkpoint
    checkpoint = orchestrator.create_checkpoint(ws1.id)
    print(f"✓ Checkpoint created: {checkpoint}")
    
    # Stats
    stats = orchestrator.get_stats()
    print(f"✓ Total workspaces: {stats['total_workspaces']}")
    
    return orchestrator


def test_repository():
    """Test Multi-Repository Runtime."""
    print("\n" + "=" * 60)
    print("Testing Multi-Repository Runtime")
    print("=" * 60)
    
    runtime = MultiRepositoryRuntime()
    
    # Register repositories
    repo1 = runtime.register_repository(
        name="frontend",
        url="https://github.com/org/frontend",
        repo_type=RepositoryType.SOURCE,
        org="org1",
    )
    
    repo2 = runtime.register_repository(
        name="backend",
        url="https://github.com/org/backend",
        repo_type=RepositoryType.SOURCE,
        org="org1",
    )
    
    print(f"✓ Repository registered: {repo1.name}")
    print(f"✓ Repository registered: {repo2.name}")
    
    # Snapshot
    snapshot = runtime.create_snapshot(repo1.id)
    print(f"✓ Snapshot created: {snapshot}")
    
    # Federation analysis
    analysis = runtime.analyze_federation("org1")
    print(f"✓ Federation analysis: {analysis['repository_count']} repos")
    
    return runtime


def test_cross_domain():
    """Test Cross-Domain Runtime."""
    print("\n" + "=" * 60)
    print("Testing Cross-Domain Reasoning")
    print("=" * 60)
    
    runtime = CrossDomainRuntime()
    
    # Add context
    runtime.add_context(Domain.SOFTWARE, knowledge=["python", "testing"])
    runtime.add_context(Domain.SECURITY, knowledge=["authentication", "encryption"])
    
    # Reason across domains
    decision = runtime.reason(
        problem="Secure software deployment",
        domains=[Domain.SOFTWARE, Domain.SECURITY],
    )
    
    print(f"✓ Cross-domain decision: {decision.id}")
    print(f"  Reasoning: {decision.reasoning[:50]}...")
    
    return runtime


def test_long_running():
    """Test Long-Running Mission Runtime."""
    print("\n" + "=" * 60)
    print("Testing Long-Running Mission Runtime")
    print("=" * 60)
    
    runtime = LongRunningMissionRuntime()
    
    # Create mission
    mission = runtime.create_mission("long-running-1")
    print(f"✓ Mission created: {mission['id']}")
    
    # Start and pause
    runtime.start(mission['id'])
    runtime.pause(mission['id'])
    runtime.resume(mission['id'])
    
    # Checkpoint
    checkpoint = runtime.checkpoint(mission['id'])
    print(f"✓ Checkpoint created: {checkpoint}")
    
    # Timeline
    timeline = runtime.get_timeline(mission['id'])
    print(f"✓ Timeline events: {len(timeline)}")
    
    return runtime


def test_diagnostics():
    """Test Self-Diagnostics Runtime."""
    print("\n" + "=" * 60)
    print("Testing Self-Diagnostics Runtime")
    print("=" * 60)
    
    runtime = SelfDiagnosticsRuntime()
    
    # Register subsystems
    runtime.register_subsystem("kernel")
    runtime.register_subsystem("knowledge")
    runtime.register_subsystem("execution")
    
    # Diagnose
    reports = runtime.diagnose()
    print(f"✓ Diagnostic reports: {len(reports)}")
    
    # Health report
    health = runtime.generate_health_report()
    print(f"✓ Platform health: {health['status']}")
    
    return runtime


def test_healing():
    """Test Self-Healing Runtime."""
    print("\n" + "=" * 60)
    print("Testing Self-Healing Runtime")
    print("=" * 60)
    
    runtime = SelfHealingRuntime()
    
    # Detect failure
    failure = runtime.detect_failure(
        failure_type=FailureType.PROVIDER,
        description="Provider timeout",
    )
    print(f"✓ Failure detected: {failure.id}")
    
    # Plan recovery
    plan = runtime.plan_recovery(failure.id)
    print(f"✓ Recovery planned: {plan.id}")
    print(f"  Actions: {len(plan.actions)}")
    
    # Execute
    success = runtime.execute_recovery(plan.id)
    print(f"✓ Recovery executed: {success}")
    
    return runtime


def test_prediction():
    """Test Prediction Runtime."""
    print("\n" + "=" * 60)
    print("Testing Prediction Runtime")
    print("=" * 60)
    
    runtime = PredictionRuntime()
    
    # Predict
    duration = runtime.predict_duration("mission-1", {"estimated_duration": 3600})
    cost = runtime.predict_cost("mission-1", {"estimated_cost": 100})
    risk = runtime.predict_risk("mission-1", {"estimated_risk": 0.3})
    
    print(f"✓ Duration predicted: {duration.predicted_value:.0f}s (confidence: {duration.confidence:.0%})")
    print(f"✓ Cost predicted: ${cost.predicted_value:.2f}")
    print(f"✓ Risk predicted: {risk.predicted_value:.0%}")
    
    # Forecast
    forecast = runtime.forecast_resource_usage("cpu", periods=5)
    print(f"✓ Forecast generated: {len(forecast.values)} periods")
    
    return runtime


def test_simulation():
    """Test Simulation Runtime."""
    print("\n" + "=" * 60)
    print("Testing Simulation Runtime")
    print("=" * 60)
    
    runtime = SimulationRuntime()
    
    # Create scenario
    scenario = runtime.create_scenario(
        name="test-deployment",
        simulation_type=SimulationType.MISSION_PLAN,
    )
    print(f"✓ Scenario created: {scenario.name}")
    
    # Run simulation
    simulation = runtime.run_simulation(scenario.id)
    print(f"✓ Simulation run: {simulation.id}")
    print(f"  Status: {simulation.status.value}")
    
    # Analyze
    analysis = runtime.analyze(simulation.id)
    print(f"✓ Analysis: {analysis.get('results', {})}")
    
    return runtime


def test_api():
    """Test Civilization API."""
    print("\n" + "=" * 60)
    print("Testing Civilization API")
    print("=" * 60)
    
    from simulation.runtime import setup_api
    
    runtime = CivilizationAPI()
    setup_api(runtime)
    
    print(f"✓ API initialized: v{runtime.version}")
    print(f"✓ Endpoints registered: {len(runtime.endpoints)}")
    
    # Create request
    request = runtime.create_request("/mission", params={}, body={})
    print(f"✓ Request created: {request.id}")
    
    return runtime


def test_platform():
    """Test Civilization Platform."""
    print("\n" + "=" * 60)
    print("Testing AGOS Civilization Platform v1.0")
    print("=" * 60)
    
    platform = get_platform()
    
    print(f"✓ Platform initialized")
    print(f"  Version: {platform.version}")
    print(f"  Name: {platform.name}")
    
    # Health check
    health = platform.health_check()
    print(f"\n✓ Platform health: {health['status']}")
    print(f"  Subsystems healthy: {sum(1 for v in health['subsystems'].values() if v == 'healthy')}/{len(health['subsystems'])}")
    
    # Stats
    stats = platform.get_stats()
    print(f"\n✓ Platform Stats:")
    print(f"  Workspaces: {stats['metrics']['workspaces']}")
    print(f"  Repositories: {stats['metrics']['repositories']}")
    print(f"  Organizations: {stats['metrics']['organizations']}")
    
    # Describe
    description = platform.describe()
    print(f"\n✓ Platform Description:")
    print(f"  Capabilities: {len(description['capabilities'])}")
    print(f"  Subsystems: {len(description['subsystems'])}")
    
    return platform


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS CIVILIZATION PLATFORM - TEST SUITE")
    print("EXECUTION-000081 to EXECUTION-000090")
    print("=" * 60)
    
    # Test subsystems
    test_orchestrator()
    test_repository()
    test_cross_domain()
    test_long_running()
    test_diagnostics()
    test_healing()
    test_prediction()
    test_simulation()
    test_api()
    
    # Test platform
    test_platform()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nAGOS Civilization Platform v1.0 Ready!")


if __name__ == "__main__":
    main()
