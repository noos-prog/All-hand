"""
AGOS Cognition
==============

The pure-cognition layer. Contains no I/O and no side effects: it turns
inputs into decisions, plans and hypotheses using pluggable reasoners.

Consumers (kernel, agents, civilization) inject a ``Reasoner`` — anything
implementing the ``Reasoner`` protocol, including LLM-backed reasoners,
rule engines, or deterministic stubs used in tests.
"""

from .memory import BeliefStore, WorkingMemory
from .model import (
    Alternative,
    Belief,
    CognitiveError,
    Decision,
    Evidence,
    Goal,
    Hypothesis,
    Intent,
    Observation,
    Plan,
    PlanStep,
    Reasoner,
)
from .reasoners import DeterministicReasoner, WeightedReasoner
from .pipeline import CognitivePipeline, PipelineTrace, UniversalCognitiveCore

__all__ = [
    "Alternative",
    "Belief",
    "BeliefStore",
    "CognitiveError",
    "CognitivePipeline",
    "Decision",
    "DeterministicReasoner",
    "Evidence",
    "Goal",
    "Hypothesis",
    "Intent",
    "Observation",
    "PipelineTrace",
    "Plan",
    "PlanStep",
    "Reasoner",
    "UniversalCognitiveCore",
    "WeightedReasoner",
    "WorkingMemory",
]

__version__ = "10.0.0"
