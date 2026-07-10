"""
AGOS Canon & Constitution Module
================================

The supreme law for AGOS (Autonomous General Orchestration System).
Every code, contract, and component must comply with these rules.

Canon is truth.
Constitution is law.
Specification is eternal.
"""

from .vocabulary import Vocabulary, get_vocabulary
from .rules import CanonRules, CanonType
from .constitution import Constitution, ArticleType
from .validator import CanonValidator, ComplianceLevel
from .registry import CanonRegistry

__all__ = [
    "Vocabulary",
    "get_vocabulary",
    "CanonRules",
    "CanonType",
    "Constitution",
    "ArticleType",
    "CanonValidator",
    "ComplianceLevel",
    "CanonRegistry",
]

__version__ = "1.0.0"
