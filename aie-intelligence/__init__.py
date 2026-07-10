"""
AGOS Intelligence Engine (AIE)
===========================

The Mathematical Brain, Not the Linguistic Brain.

AIE transforms LLM from "the brain" to "one sensor" among many.
The real brain is mathematical: reasoning, simulation, optimization.

Core Engines:
- Knowledge Engine: Facts, Evidence, Patterns
- Reasoning Engine: Logic, Deduction, Induction
- Decision Engine: Options, Risks, Costs, Benefits
- Simulation Engine: What-if, Scenarios, Predictions
- Optimization Engine: Maximize, Minimize, Balance
- Verification Engine: Validate, Check, Compare
"""

from .core.knowledge_engine import (
    KnowledgeEngine, KnowledgeNode, KnowledgeGraph,
    Evidence, EvidenceSource, KnowledgeType
)
from .core.reasoning_engine import (
    ReasoningEngine, ReasoningChain, ReasoningType,
    LogicalProof, InferenceRule
)
from .core.simulation_engine import (
    SimulationEngine, SimulationScenario, SimulationResult,
    StateVector, StateTransition
)
from .core.optimization_engine import (
    OptimizationEngine, OptimizationObjective,
    Constraint, Solution, OptimizationType
)
from .core.verification_engine import (
    VerificationEngine, VerificationResult,
    VerificationType, Invariant
)
from .graph.decision_graph import (
    DecisionGraph, DecisionNode, DecisionEdge,
    GraphTraversal, PathFinder
)
from .graph.decision_packet import (
    DecisionPacket, DecisionContext, DecisionMetadata,
    PacketStatus, PacketPriority
)

__all__ = [
    # Core Engines
    "KnowledgeEngine",
    "KnowledgeNode",
    "KnowledgeGraph",
    "Evidence",
    "EvidenceSource",
    "KnowledgeType",
    # Reasoning
    "ReasoningEngine",
    "ReasoningChain",
    "ReasoningType",
    "LogicalProof",
    "InferenceRule",
    # Simulation
    "SimulationEngine",
    "SimulationScenario",
    "SimulationResult",
    "StateVector",
    "StateTransition",
    # Optimization
    "OptimizationEngine",
    "OptimizationObjective",
    "Constraint",
    "Solution",
    "OptimizationType",
    # Verification
    "VerificationEngine",
    "VerificationResult",
    "VerificationType",
    "Invariant",
    # Graph
    "DecisionGraph",
    "DecisionNode",
    "DecisionEdge",
    "GraphTraversal",
    "PathFinder",
    # Packet
    "DecisionPacket",
    "DecisionContext",
    "DecisionMetadata",
    "PacketStatus",
    "PacketPriority",
]

__version__ = "1.0.0"
