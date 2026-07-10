"""
AGOS Canons Module
==================

The 10 immutable rules of AGOS.
These cannot be overridden, ignored, or extended.
Compliance is MANDATORY for all AGOS components.

CANON-001: Vocabulary     - One definition per word
CANON-002: Forbidden Words - No ambiguous terms
CANON-003: Canonical Flow  - One official flow
CANON-004: Object Ownership - Strict ownership rules
CANON-005: Decision Rules  - Decision-making rules
CANON-006: Principles       - 10 absolute principles
CANON-007: Diagrams         - Official diagram formats
CANON-008: Naming           - Naming conventions
CANON-009: Contracts        - Contract versioning
CANON-010: Testing          - Mandatory testing
"""

from .rules import CanonRules, CanonType, ViolationSeverity, CanonRule

__all__ = [
    "CanonRules",
    "CanonType",
    "ViolationSeverity",
    "CanonRule",
]
