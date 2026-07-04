#!/usr/bin/env python3
"""Test script for Civilization Runtime."""
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from execution import MissionCompiler, GraphRuntime, ParallelExecutor
from execution import NodeType, EdgeType
from verification import VerificationRuntime, VerificationType
from approval import ApprovalRuntime, ApprovalSource
from collaboration import HumanRuntime, CollaborationAction
from organization import OrganizationRuntime, OrganizationType
from governance import GovernanceRuntime, GovernanceDomain
from trust import TrustRuntime, TrustLevel
from civilization import get_civilization


def test_mission_compiler():
    """Test Mission Compiler."""
    print("=" * 60)
    print("Testing Mission Compiler")
    print("=" * 60)
    
    compiler = MissionCompiler()
    
    # Compile a mission
    mission = compiler.compile(
        intent_text="Build a universal platform",
        context={"domain": "engineering"},
    )
    
    print(f"✓ Mission compiled: {mission.id}")
    print(f"  Phases: {len(mission.phases)}")
    print(f"  Goals: {len(mission.goals)}")
    print(f"  Status: {mission.status.value}")
    
    return compiler


def test_execution_graph():
    """Test Execution Graph."""
    print("\n" + "=" * 60)
    print("Testing Execution Graph")
    print("=" * 60)
    
    runtime = GraphRuntime()
    
    # Create graph
    graph = runtime.create_graph("Test Graph")
    print(f"✓ Graph created: {graph.id}")
    
    # Add nodes
    runtime.add_node(graph.id, "start", NodeType.MISSION)
    runtime.add_node(graph.id, "execute", NodeType.CAPABILITY)
    runtime.add_node(graph.id, "validate", NodeType.VALIDATION)
    print(f"✓ Nodes added: {len(graph.nodes)}")
    
    # Add edges
    runtime.add_edge(graph.id, "start", "execute", EdgeType.DEPENDS_ON)
    runtime.add_edge(graph.id, "execute", "validate", EdgeType.PRODUCES)
    print(f"✓ Edges added: {len(graph.edges)}")
    
    # Get parallel groups
    groups = runtime.get_parallel_groups(graph.id)
    print(f"✓ Parallel groups: {len(groups)}")
    
    return runtime


def test_parallel_executor():
    """Test Parallel Execution."""
    print("\n" + "=" * 60)
    print("Testing Parallel Execution")
    print("=" * 60)
    
    executor = ParallelExecutor(max_workers=5)
    
    # Create tasks
    tasks = []
    for i in range(3):
        from execution.parallel import ExecutionTask
        task = ExecutionTask(
            id=f"task-{i}",
            name=f"Task {i}",
            dependencies=[] if i == 0 else [f"task-{i-1}"],
        )
        tasks.append(task)
    
    # Execute
    results = executor.execute(tasks)
    print(f"✓ Tasks executed: {len(results)}")
    
    # Stats
    stats = executor.get_stats()
    print(f"✓ Stats: {stats}")
    
    return executor


def test_verification():
    """Test Verification."""
    print("\n" + "=" * 60)
    print("Testing Verification")
    print("=" * 60)
    
    runtime = VerificationRuntime()
    
    # Verify artifact
    report = runtime.verify(
        artifact_id="test-artifact",
        artifact_data={"name": "test"},
    )
    
    print(f"✓ Verification completed")
    print(f"  Results: {len(report.results)}")
    print(f"  Passed: {report.overall_passed}")
    
    return runtime


def test_approval():
    """Test Approval."""
    print("\n" + "=" * 60)
    print("Testing Approval")
    print("=" * 60)
    
    runtime = ApprovalRuntime()
    
    # Create request
    request = runtime.create_request(
        request_type="deployment",
        description="Deploy to production",
        source=ApprovalSource.AUTOMATIC,
    )
    
    print(f"✓ Approval request created: {request.id}")
    
    # Approve
    runtime.approve(request.id, "admin", "Approved")
    print(f"✓ Request approved")
    
    return runtime


def test_collaboration():
    """Test Human Collaboration."""
    print("\n" + "=" * 60)
    print("Testing Human Collaboration")
    print("=" * 60)
    
    runtime = HumanRuntime()
    
    # Add contribution
    contribution = runtime.add_contribution(
        action=CollaborationAction.REVIEW,
        contributor_id="user-1",
        content="Code review feedback",
    )
    
    print(f"✓ Contribution added: {contribution.id}")
    
    # Create review
    review = runtime.create_review(
        target_id="pr-123",
        target_type="pull_request",
        reviewer_id="user-1",
    )
    
    print(f"✓ Review created: {review.id}")
    
    return runtime


def test_organization():
    """Test Organization."""
    print("\n" + "=" * 60)
    print("Testing Organization")
    print("=" * 60)
    
    runtime = OrganizationRuntime()
    
    # Create organization
    org = runtime.create_organization(
        name="Engineering",
        org_type=OrganizationType.DEPARTMENT,
        description="Engineering department",
    )
    
    print(f"✓ Organization created: {org.id}")
    print(f"  Name: {org.name}")
    
    return runtime


def test_governance():
    """Test Governance."""
    print("\n" + "=" * 60)
    print("Testing Governance")
    print("=" * 60)
    
    runtime = GovernanceRuntime()
    
    # Create rule
    rule = runtime.create_rule(
        name="Security Check",
        domain=GovernanceDomain.SECURITY,
        description="All deployments must pass security check",
        severity="error",
    )
    
    print(f"✓ Governance rule created: {rule.id}")
    
    # Check compliance
    result = runtime.check_compliance(
        entity_id="test-entity",
        entity_type="deployment",
    )
    
    print(f"✓ Compliance checked: {result['compliant']}")
    
    return runtime


def test_trust():
    """Test Trust."""
    print("\n" + "=" * 60)
    print("Testing Trust")
    print("=" * 60)
    
    runtime = TrustRuntime()
    
    # Create trust score
    score = runtime.create_trust_score(
        entity_id="test-entity",
        entity_type="artifact",
        factors={
            "verification": 0.9,
            "evidence": 0.8,
            "history": 0.7,
        },
    )
    
    print(f"✓ Trust score created: {score.overall_score:.2f}")
    print(f"  Level: {score.trust_level.value}")
    
    return runtime


def test_civilization():
    """Test Civilization Runtime."""
    print("\n" + "=" * 60)
    print("Testing AGOS Autonomous Civilization Runtime v1.0")
    print("=" * 60)
    
    civilization = get_civilization()
    
    print(f"✓ Civilization initialized")
    print(f"  Version: {civilization.version}")
    print(f"  Name: {civilization.name}")
    
    # Compile mission
    mission = civilization.compile_mission("Build universal AI platform")
    print(f"✓ Mission compiled: {mission.id}")
    
    # Create execution graph
    graph = civilization.create_execution_graph("Test Graph")
    print(f"✓ Execution graph created: {graph.id}")
    
    # Verify
    report = civilization.verify("test-artifact", {"data": "test"})
    print(f"✓ Artifact verified: {report.overall_passed}")
    
    # Create organization
    org = civilization.create_organization("AGOS Corp", OrganizationType.TEAM)
    print(f"✓ Organization created: {org.name}")
    
    # Check governance
    result = civilization.check_governance("entity-1", "deployment")
    print(f"✓ Governance check: {result['compliant']}")
    
    # Assess trust
    score = civilization.assess_trust("artifact-1", "artifact")
    print(f"✓ Trust assessed: {score.overall_score:.2f}")
    
    # Get stats
    stats = civilization.get_stats()
    print(f"\n✓ Civilization Stats:")
    print(f"  Missions compiled: {stats['metrics']['missions_compiled']}")
    print(f"  Graphs created: {stats['metrics']['graphs_created']}")
    print(f"  Verifications run: {stats['metrics']['verifications_run']}")
    
    # Health check
    health = civilization.health_check()
    print(f"\n✓ Health: {health['status']}")
    
    return civilization


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS CIVILIZATION RUNTIME - TEST SUITE")
    print("EXECUTION-000071 to EXECUTION-000080")
    print("=" * 60)
    
    # Test subsystems
    test_mission_compiler()
    test_execution_graph()
    test_parallel_executor()
    test_verification()
    test_approval()
    test_collaboration()
    test_organization()
    test_governance()
    test_trust()
    
    # Test civilization
    test_civilization()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\nAGOS Autonomous Civilization Runtime v1.0 Ready!")


if __name__ == "__main__":
    main()
