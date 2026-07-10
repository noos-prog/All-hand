"""
AGOS Constitution
=================

Canonical, immutable rules for the AGOS civilization. Anything that
violates a constitutional article fails validation — implementations
must change, never the constitution.

This module also ships a :class:`ConstitutionValidator` that scans a
project tree and reports violations mechanically, so CI can enforce the
rules instead of relying on convention.
"""

from .articles import (
    ARTICLES,
    Article,
    ViolationSeverity,
    IDENTITY_STATEMENT,
    KERNEL_BLACKLIST,
    KERNEL_PROPERTIES,
    CONTRACT_RULES,
)
from .validator import ConstitutionValidator, Violation

__all__ = [
    "ARTICLES",
    "Article",
    "CONTRACT_RULES",
    "ConstitutionValidator",
    "IDENTITY_STATEMENT",
    "KERNEL_BLACKLIST",
    "KERNEL_PROPERTIES",
    "Violation",
    "ViolationSeverity",
]

__version__ = "1.0.0"
