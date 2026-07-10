"""
AIE Core Engines Module
====================

The 6 mathematical engines of AIE:
1. Knowledge Engine
2. Reasoning Engine
3. Decision Engine
4. Simulation Engine
5. Optimization Engine
6. Verification Engine
"""

from .knowledge_engine import (
    KnowledgeEngine, KnowledgeNode, KnowledgeGraph,
    Evidence, EvidenceSource, KnowledgeType
)
from .reasoning_engine import (
    ReasoningEngine, ReasoningChain, ReasoningType,
    LogicalProof, InferenceRule
)
from .simulation_engine import (
    SimulationEngine, SimulationScenario, SimulationResult,
    StateVector, StateTransition
)
from .optimization_engine import (
    OptimizationEngine, OptimizationObjective,
    Constraint, Solution, OptimizationType
)
from .verification_engine import (
    VerificationEngine, VerificationResult,
    VerificationType, Invariant
)

__all__ = [
    "KnowledgeEngine",
    "KnowledgeNode",
    "KnowledgeGraph",
    "Evidence",
    "EvidenceSource",
    "KnowledgeType",
    "ReasoningEngine",
    "ReasoningChain",
    "ReasoningType",
    "LogicalProof",
    "InferenceRule",
    "SimulationEngine",
    "SimulationScenario",
    "SimulationResult",
    "StateVector",
    "StateTransition",
    "OptimizationEngine",
    "OptimizationObjective",
    "Constraint",
    "Solution",
    "OptimizationType",
    "VerificationEngine",
    "VerificationResult",
    "VerificationType",
    "Invariant",
]
