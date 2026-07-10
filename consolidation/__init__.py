"""
AGOS Consolidation
==================

Turns raw episodic memory (agent traces, tool calls, observations) into
compact, deduplicated, decayed semantic memory suitable for long-term
storage and retrieval.

Pipeline:  episodes -> dedup -> summarize -> decay -> store
"""

from .decay import DecayPolicy, ExponentialDecay, LinearDecay
from .dedup import Deduplicator, ShingleFingerprint
from .episode import Episode, EpisodicStream, SemanticRecord
from .consolidator import Consolidator, ConsolidationReport

__all__ = [
    "ConsolidationReport",
    "Consolidator",
    "DecayPolicy",
    "Deduplicator",
    "Episode",
    "EpisodicStream",
    "ExponentialDecay",
    "LinearDecay",
    "SemanticRecord",
    "ShingleFingerprint",
]
