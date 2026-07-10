"""
AGOS Intelligence System
=====================

Three Levels of Intelligence. One Decision Engine.

Modes:
- Instant Mode: ChatGPT speed
- Engineer Mode: Thoughtful planning
- Research Mode: Evidence-based decisions

Every decision is:
- Explainable
- Traceable
- Learnable
"""

from .intelligence_modes import (
    IntelligenceMode, IntelligenceEngine,
    InstantMode, EngineerMode, ResearchMode,
    ModeResult, ModeStatus
)
from .decision_engine import (
    DecisionEngine, Decision, DecisionType,
    DecisionConfidence, DecisionRule
)
from .knowledge_base import (
    IntelligenceKnowledge, KnowledgeSource,
    Evidence, EvidenceType
)
from .time_machine import (
    TimeMachine, MissionSnapshot,
    TimelineEvent, MissionReplay
)
from .academy import (
    AGOSAcademy, LearningPath,
    BestPractice, ArchitectureRecommendation,
    ProviderRecommendation
)

__all__ = [
    # Intelligence Modes
    "IntelligenceMode",
    "IntelligenceEngine",
    "InstantMode",
    "EngineerMode",
    "ResearchMode",
    "ModeResult",
    "ModeStatus",
    # Decision Engine
    "DecisionEngine",
    "Decision",
    "DecisionType",
    "DecisionConfidence",
    "DecisionRule",
    # Knowledge Base
    "IntelligenceKnowledge",
    "KnowledgeSource",
    "Evidence",
    "EvidenceType",
    # Time Machine
    "TimeMachine",
    "MissionSnapshot",
    "TimelineEvent",
    "MissionReplay",
    # Academy
    "AGOSAcademy",
    "LearningPath",
    "BestPractice",
    "ArchitectureRecommendation",
    "ProviderRecommendation",
]

__version__ = "1.0.0"
