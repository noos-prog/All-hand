"""
AGOS CONSTITUTION v1.0
======================

THIS DOCUMENT HAS HIGHER PRIORITY THAN ANY IMPLEMENTATION.
IF ANY IMPLEMENTATION CONFLICTS WITH THIS CONSTITUTION,
THE IMPLEMENTATION MUST CHANGE.
THE CONSTITUTION NEVER CHANGES DURING NORMAL DEVELOPMENT.

THIS CONSTITUTION IS THE HIGHEST AUTHORITY OF AGOS.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from enum import Enum

class ViolationSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ConstitutionalRule:
    article: int
    title: str
    description: str
    mandatory: bool = True

# =============================================================================
# ARTICLE 1: AGOS IDENTITY
# =============================================================================
IDENTITY_STATEMENT = """
AGOS IS NOT AN AI AGENT.
AGOS IS NOT A CHATBOT.
AGOS IS NOT AN IDE.
AGOS IS NOT A FRAMEWORK.
AGOS IS NOT AN ORCHESTRATION TOOL.
AGOS IS NOT AN MCP CLIENT.
AGOS IS AN OPERATING SYSTEM FOR AUTONOMOUS EXECUTION.
"""

# =============================================================================
# ARTICLE 2: KERNEL PROPERTIES
# =============================================================================
KERNEL_PROPERTIES = ["Small", "Deterministic", "Observable", "Portable", "Replaceable", "Vendor Independent", "Domain Independent", "AI Independent"]

# =============================================================================
# ARTICLE 3: KERNEL MAY NEVER KNOW
# =============================================================================
KERNEL_BLACKLIST = ["Models", "Agents", "Providers", "Capabilities", "Domains", "Languages", "Cloud Vendors", "Tools", "Storage Engines"]

# =============================================================================
# ARTICLE 4: CONTRACTS
# =============================================================================
CONTRACT_RULES = ["No Direct Dependencies", "No Hidden Dependencies", "No Runtime Shortcuts"]

# =============================================================================
# ARTICLE 5: VERSIONING
# =============================================================================
VERSIONED_ENTITIES = ["Contracts", "Schemas", "Events", "Capabilities", "Providers", "Skills", "Artifacts", "Knowledge", "Policies", "Missions", "Workflows"]

# =============================================================================
# ARTICLE 6: OBSERVABILITY
# =============================================================================
OBSERVABILITY_RULES = ["No Silent Execution", "Every Action Produces Events", "Every Decision Produces Evidence", "Every Failure Produces Diagnostics"]

# =============================================================================
# ARTICLE 7: REPLACEABILITY
# =============================================================================
REPLACEABILITY_RULE = "No Implementation Is Permanent"

# =============================================================================
# ARTICLE 8: COMPONENT HIERARCHY
# =============================================================================
COMPONENT_HIERARCHY = "No Component Owns The System. Every Component Is A Servant Of The Kernel."

# =============================================================================
# ARTICLE 9: EXTERNAL AI RESTRICTIONS
# =============================================================================
EXTERNAL_AI_RESTRICTED = ["Plan", "Reason", "Govern", "Remember", "Own Context", "Own Knowledge", "Own Missions"]

# =============================================================================
# ARTICLE 10: EXTERNAL AI ALLOWED
# =============================================================================
EXTERNAL_AI_ALLOWED = ["Execute", "Generate", "Transform", "Analyze", "Summarize", "Translate", "Review", "Evaluate"]

# =============================================================================
# ARTICLE 11: KERNEL OWNS
# =============================================================================
KERNEL_OWNERSHIP = ["Intent", "Goals", "Context", "Planning", "Reasoning", "Policies", "Knowledge", "Execution Graph", "Mission State"]

# =============================================================================
# ARTICLE 12: DECISION REQUIREMENTS
# =============================================================================
DECISION_REQUIREMENTS = ["Traceable", "Explainable", "Repeatable", "Auditable"]

# =============================================================================
# ARTICLE 13: KNOWLEDGE OBJECT REQUIREMENTS
# =============================================================================
KNOWLEDGE_OBJECT_REQUIREMENTS = ["Source", "Evidence", "Confidence", "Version", "Timestamp", "Lineage"]

# =============================================================================
# ARTICLE 14: EXECUTION REQUIREMENTS
# =============================================================================
EXECUTION_REQUIREMENTS = ["Idempotent", "Recoverable", "Cancelable", "Replayable", "Observable"]

# =============================================================================
# ARTICLE 15: EXECUTION BOUNDARY
# =============================================================================
EXECUTION_BOUNDARY = "Nothing Executes Outside The Mission Runtime."

# =============================================================================
# ARTICLE 16: KERNEL PROTECTION
# =============================================================================
KERNEL_PROTECTION = "Nothing Modifies The Kernel. Ever."

class ConstitutionalValidator:
    """Validates that implementations follow the AGOS Constitution."""
    
    def __init__(self):
        self.version = "1.0.0"
        self.violations: List[Dict[str, Any]] = []
    
    def validate_kernel_properties(self, kernel: Dict[str, Any]) -> bool:
        """Article 2: Validate kernel properties."""
        for prop in KERNEL_PROPERTIES:
            if prop.lower() not in str(kernel).lower():
                self.violations.append({
                    "article": 2,
                    "rule": prop,
                    "severity": ViolationSeverity.CRITICAL,
                    "message": f"Kernel must be {prop}"
                })
        return len(self.violations) == 0
    
    def validate_kernel_blacklist(self, kernel: Dict[str, Any]) -> bool:
        """Article 3: Validate kernel doesn't know blacklisted entities."""
        kernel_str = str(kernel).lower()
        for item in KERNEL_BLACKLIST:
            if item.lower() in kernel_str:
                self.violations.append({
                    "article": 3,
                    "rule": item,
                    "severity": ViolationSeverity.CRITICAL,
                    "message": f"Kernel may never know {item}"
                })
        return len(self.violations) == 0
    
    def validate_contracts(self, components: List[Dict[str, Any]]) -> bool:
        """Article 4: Validate no direct dependencies."""
        # Implementation would check for direct dependencies
        return True
    
    def validate_versioning(self, entity: Dict[str, Any]) -> bool:
        """Article 5: Validate versioning."""
        if "version" not in entity:
            self.violations.append({
                "article": 5,
                "rule": "version_required",
                "severity": ViolationSeverity.HIGH,
                "message": "Every entity must be versioned"
            })
            return False
        return True
    
    def validate_observability(self, component: Dict[str, Any]) -> bool:
        """Article 6: Validate observability."""
        if "events" not in component and "telemetry" not in component:
            self.violations.append({
                "article": 6,
                "rule": "observability_required",
                "severity": ViolationSeverity.HIGH,
                "message": "Component must produce events"
            })
            return False
        return True
    
    def validate_kernel_ownership(self, component: str) -> bool:
        """Article 11: Validate kernel owns critical responsibilities."""
        if component in KERNEL_OWNERSHIP:
            # External components should not own these
            return False
        return True
    
    def get_violations(self) -> List[Dict[str, Any]]:
        return self.violations
    
    def clear_violations(self) -> None:
        self.violations = []

class AGOSConstitution:
    """
    AGOS Constitution v1.0
    
    This document has higher priority than any implementation.
    If any implementation conflicts with this constitution, the implementation must change.
    The constitution never changes during normal development.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.validator = ConstitutionalValidator()
    
    def get_identity(self) -> str:
        return IDENTITY_STATEMENT
    
    def get_kernel_properties(self) -> List[str]:
        return KERNEL_PROPERTIES
    
    def get_kernel_blacklist(self) -> List[str]:
        return KERNEL_BLACKLIST
    
    def get_kernel_ownership(self) -> List[str]:
        return KERNEL_OWNERSHIP
    
    def get_versioned_entities(self) -> List[str]:
        return VERSIONED_ENTITIES
    
    def get_observability_rules(self) -> List[str]:
        return OBSERVABILITY_RULES
    
    def get_decision_requirements(self) -> List[str]:
        return DECISION_REQUIREMENTS
    
    def get_execution_requirements(self) -> List[str]:
        return EXECUTION_REQUIREMENTS
    
    def get_external_ai_rules(self) -> Dict[str, List[str]]:
        return {
            "restricted": EXTERNAL_AI_RESTRICTED,
            "allowed": EXTERNAL_AI_ALLOWED
        }
    
    def validate(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        self.validator.clear_violations()
        self.validator.validate_kernel_properties(entity)
        self.validator.validate_kernel_blacklist(entity)
        self.validator.validate_versioning(entity)
        self.validator.validate_observability(entity)
        
        return {
            "valid": len(self.validator.get_violations()) == 0,
            "violations": self.validator.get_violations(),
            "constitution_version": self.VERSION
        }
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "articles": 16,
            "kernel_properties": len(KERNEL_PROPERTIES),
            "kernel_blacklist": len(KERNEL_BLACKLIST),
            "kernel_ownership": len(KERNEL_OWNERSHIP),
            "versioned_entities": len(VERSIONED_ENTITIES),
            "decision_requirements": len(DECISION_REQUIREMENTS),
            "execution_requirements": len(EXECUTION_REQUIREMENTS),
            "external_ai_allowed": len(EXTERNAL_AI_ALLOWED),
            "external_ai_restricted": len(EXTERNAL_AI_RESTRICTED)
        }
