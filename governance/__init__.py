"""
AGOS Governance Platform
====================

Universal governance platform for AI agent civilization.
Architectural enforcement, audit, and compliance for millions of agents.

Author: AGOS Team
Version: 1.0.0
"""

from .audit import (
    ArchitectureAuditor, AuditReport, Violation, ViolationSeverity,
    ArchitecturalRule, LayerBoundary, DependencyGraph
)
from .normalization import (
    ArchitectureNormalizer, ArchitectureDecision, ADRGenerator,
    CodingStandard, NamingConvention, StandardValidator
)
from .enforcement import (
    ArchitectureEnforcer, PolicyValidator, LayerValidator,
    ContractValidator, EnforcementResult, BuildGate
)
from .compliance import (
    ComplianceManager, CompliancePolicy, ComplianceReport,
    AuditTrail, ComplianceStatus
)
from .policy_engine import (
    PolicyEngine, PolicyRule, PolicyContext, PolicyResult
)

__all__ = [
    # Audit
    "ArchitectureAuditor", "AuditReport", "Violation", "ViolationSeverity",
    "ArchitecturalRule", "LayerBoundary", "DependencyGraph",
    # Normalization
    "ArchitectureNormalizer", "ArchitectureDecision", "ADRGenerator",
    "CodingStandard", "NamingConvention", "StandardValidator",
    # Enforcement
    "ArchitectureEnforcer", "PolicyValidator", "LayerValidator",
    "ContractValidator", "EnforcementResult", "BuildGate",
    # Compliance
    "ComplianceManager", "CompliancePolicy", "ComplianceReport",
    "AuditTrail", "ComplianceStatus",
    # Policy
    "PolicyEngine", "PolicyRule", "PolicyContext", "PolicyResult",
]

__version__ = "1.0.0"
