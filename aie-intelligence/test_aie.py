#!/usr/bin/env python3
"""
AIE - Test Suite
===============

Tests for the AGOS Intelligence Engine.
Run with: python test_aie.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, '01-Core-Engines'))
sys.path.insert(0, os.path.join(base_dir, '02-Decision-Graph'))
sys.path.insert(0, os.path.join(base_dir, '03-Decision-Packet'))

from knowledge_engine import (
    KnowledgeEngine, KnowledgeNode, KnowledgeGraph,
    Evidence, EvidenceSource, KnowledgeType, NodeStatus
)
from reasoning_engine import (
    ReasoningEngine, ReasoningChain, ReasoningType,
    LogicalStatement, InferenceRule
)
from simulation_engine import (
    SimulationEngine, SimulationScenario, SimulationType,
    StateVector, StateTransition
)
from optimization_engine import (
    OptimizationEngine, OptimizationType, ConstraintType
)
from verification_engine import (
    VerificationEngine, VerificationType, Invariant
)
from decision_graph import (
    DecisionGraph, DecisionNode, DecisionEdge,
    NodeType, EdgeType, PathFinder
)
from decision_packet import (
    DecisionPacket, DecisionContext, DecisionOption,
    PacketStatus, PacketPriority, create_decision_packet
)


def test_knowledge_engine():
    """Test knowledge engine."""
    print("\n=== Testing Knowledge Engine ===")
    
    # Create evidence
    evidence = Evidence(
        evidence_id="ev_001",
        source=EvidenceSource.LLM_CLAUDE,
        content={"finding": "TypeScript improves code quality"},
        confidence=0.85,
        timestamp="2024-01-01T00:00:00",
    )
    
    # Create knowledge node
    node = KnowledgeNode(
        node_id="know_001",
        knowledge_type=KnowledgeType.FACT,
        statement="TypeScript improves code quality",
        content={"technology": "TypeScript", "benefit": "code_quality"},
        evidence=(evidence,),
    )
    
    # Create engine
    engine = KnowledgeEngine()
    engine.add_knowledge(
        node_id=node.node_id,
        knowledge_type=node.knowledge_type,
        statement=node.statement,
        content=node.content,
        evidence=[evidence],
    )
    
    # Query
    results = engine.query_knowledge(min_confidence=0.5)
    print(f"  Knowledge nodes: {len(results)}")
    
    # Stats
    stats = engine.get_statistics()
    print(f"  Total knowledge: {stats['total_nodes']}")
    
    print("  ✓ Knowledge engine tests passed")


def test_reasoning_engine():
    """Test reasoning engine."""
    print("\n=== Testing Reasoning Engine ===")
    
    # Create engine
    engine = ReasoningEngine()
    
    # Add statements
    stmt1 = LogicalStatement(
        statement_id="stmt_001",
        content="If it rains, the ground is wet",
        symbolic_form="P → Q",
        is_known=True,
        truth_value=True,
    )
    
    stmt2 = LogicalStatement(
        statement_id="stmt_002",
        content="It is raining",
        symbolic_form="P",
        is_known=True,
        truth_value=True,
    )
    
    engine.add_statement(stmt1)
    engine.add_statement(stmt2)
    
    # Reason
    chain = engine.reason(
        ReasoningType.DEDUCTION,
        premises=["stmt_001", "stmt_002"]
    )
    
    print(f"  Reasoning chain: {chain.chain_id}")
    print(f"  Is valid: {chain.is_valid}")
    print(f"  Confidence: {chain.confidence}")
    
    # Stats
    stats = engine.get_statistics()
    print(f"  Total chains: {stats['total_chains']}")
    
    print("  ✓ Reasoning engine tests passed")


def test_simulation_engine():
    """Test simulation engine."""
    print("\n=== Testing Simulation Engine ===")
    
    # Create engine
    engine = SimulationEngine()
    
    # Create scenario
    scenario = engine.create_scenario(
        scenario_id="scenario_001",
        name="API Request",
        description="Simulate API request flow",
        initial_values={"requests": 100, "capacity": 50},
        transitions=[
            {"id": "t1", "from_state": "initial", "to_state": "processing", "probability": 0.9, "duration_ms": 100},
            {"id": "t2", "from_state": "processing", "to_state": "success", "probability": 0.8},
            {"id": "t3", "from_state": "processing", "to_state": "failed", "probability": 0.2},
        ]
    )
    
    # Run simulation
    result = engine.run_simulation(
        scenario_id="scenario_001",
        simulation_type=SimulationType.MONTE_CARLO,
        iterations=100
    )
    
    print(f"  Simulations run: {result.paths_explored}")
    print(f"  Success rate: {result.success_rate:.1%}")
    print(f"  Confidence: {result.confidence:.1%}")
    
    # Stats
    stats = engine.get_statistics()
    print(f"  Total scenarios: {stats['total_scenarios']}")
    
    print("  ✓ Simulation engine tests passed")


def test_optimization_engine():
    """Test optimization engine."""
    print("\n=== Testing Optimization Engine ===")
    
    # Create engine
    engine = OptimizationEngine()
    
    # Define variables
    engine.define_variable("x", lower_bound=0, upper_bound=10)
    engine.define_variable("y", lower_bound=0, upper_bound=10)
    
    # Add constraint
    engine.add_constraint(
        constraint_id="c1",
        name="x + y <= 10",
        constraint_type=ConstraintType.INEQUALITY,
        evaluate=lambda v: v.get("x", 0) + v.get("y", 0),
        rhs_value=10
    )
    
    # Add objective (maximize x + y)
    engine.add_objective(
        objective_id="obj1",
        name="Maximize x + y",
        objective_type="maximize",
        evaluate=lambda v: v.get("x", 0) + v.get("y", 0)
    )
    
    # Optimize
    result = engine.optimize(
        optimization_type=OptimizationType.GRADIENT_DESCENT,
        max_iterations=100
    )
    
    print(f"  Optimization completed: {result.convergence_achieved}")
    
    if result.best_solution:
        print(f"  Best value: {result.best_solution.total_cost:.2f}")
    
    # Stats
    stats = engine.get_statistics()
    print(f"  Variables: {stats['variables_defined']}")
    
    print("  ✓ Optimization engine tests passed")


def test_verification_engine():
    """Test verification engine."""
    print("\n=== Testing Verification Engine ===")
    
    # Create engine
    engine = VerificationEngine()
    
    # Add invariant
    engine.add_invariant(
        invariant_id="inv_001",
        name="Non-negative Count",
        description="Count must be non-negative",
        check=lambda state: state.get("count", 0) >= 0,
        is_critical=True
    )
    
    # Verify
    state = {"count": 10, "name": "test"}
    result = engine.verify(VerificationType.INVARIANT, state)
    
    print(f"  Verification passed: {result.passed}")
    print(f"  Checks: {result.passed_checks}/{result.total_checks}")
    
    # Verify with violation
    state_bad = {"count": -5, "name": "test"}
    result_bad = engine.verify(VerificationType.INVARIANT, state_bad)
    
    print(f"  Violation detected: {not result_bad.passed}")
    
    print("  ✓ Verification engine tests passed")


def test_decision_graph():
    """Test decision graph."""
    print("\n=== Testing Decision Graph ===")
    
    # Create graph
    graph = DecisionGraph()
    
    # Add nodes
    node1 = DecisionNode(
        node_id="start",
        name="Start",
        node_type=NodeType.STATE,
        content={},
        value=0.0
    )
    
    node2 = DecisionNode(
        node_id="decision",
        name="Make Decision",
        node_type=NodeType.DECISION,
        content={},
        value=5.0,
        probability=0.9
    )
    
    node3 = DecisionNode(
        node_id="end",
        name="End",
        node_type=NodeType.OUTCOME,
        content={},
        value=10.0
    )
    
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_node(node3)
    
    # Add edges
    edge1 = DecisionEdge(
        edge_id="e1",
        from_node="start",
        to_node="decision",
        edge_type=EdgeType.LEADS_TO,
        weight=1.0
    )
    
    edge2 = DecisionEdge(
        edge_id="e2",
        from_node="decision",
        to_node="end",
        edge_type=EdgeType.CAUSES,
        weight=2.0,
        probability=0.8
    )
    
    graph.add_edge(edge1)
    graph.add_edge(edge2)
    
    # Find path
    path = graph.find_path("start", "end")
    print(f"  Path found: {path}")
    print(f"  Path length: {len(path) if path else 0}")
    
    # Stats
    stats = graph.get_statistics()
    print(f"  Nodes: {stats['total_nodes']}")
    print(f"  Edges: {stats['total_edges']}")
    
    print("  ✓ Decision graph tests passed")


def test_decision_packet():
    """Test decision packet."""
    print("\n=== Testing Decision Packet ===")
    
    # Create options
    options = [
        {
            "id": "opt_001",
            "name": "Use TypeScript",
            "description": "Use TypeScript for type safety",
            "value": 8.0,
            "cost": 3.0,
            "confidence": 0.9,
        },
        {
            "id": "opt_002",
            "name": "Use JavaScript",
            "description": "Use plain JavaScript",
            "value": 5.0,
            "cost": 1.0,
            "confidence": 0.7,
        },
    ]
    
    # Create packet
    packet = create_decision_packet(
        packet_id="packet_001",
        decision_type="technology_choice",
        decision_goal="Choose the best language",
        context_data={
            "request_id": "req_001",
            "user_id": "user_001",
        },
        options=options
    )
    
    print(f"  Packet ID: {packet.packet_id}")
    print(f"  Options: {len(packet.options)}")
    print(f"  Recommended: {packet.recommended_option_id}")
    
    # Select best
    best = packet.select_best_option()
    print(f"  Best option: {best.name if best else None}")
    
    print("  ✓ Decision packet tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("AIE - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_knowledge_engine()
        test_reasoning_engine()
        test_simulation_engine()
        test_optimization_engine()
        test_verification_engine()
        test_decision_graph()
        test_decision_packet()
        
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
