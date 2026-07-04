"""Universal Governance Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class GovernanceDomain(Enum):
    """Governance domain."""
    ARCHITECTURE = "architecture"
    KNOWLEDGE = "knowledge"
    EXECUTION = "execution"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    RESOURCES = "resources"
    COSTS = "costs"
    POLICIES = "policies"
    ORGANIZATIONS = "organizations"
    DOMAINS = "domains"


class GovernanceStatus(Enum):
    """Governance status."""
    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


@dataclass
class GovernanceRule:
    """A governance rule."""
    id: str
    name: str
    domain: GovernanceDomain
    description: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    actions: Dict[str, Any] = field(default_factory=dict)
    severity: str = "warning"
    status: GovernanceStatus = GovernanceStatus.ACTIVE


@dataclass
class GovernanceViolation:
    """A governance violation."""
    id: str
    rule_id: str
    entity_id: str
    entity_type: str
    severity: str
    description: str
    detected_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution: str = ""


@dataclass
class GovernanceAudit:
    """Governance audit record."""
    id: str
    action: str
    actor: str
    entity_id: str
    entity_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    result: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class GovernanceRuntime:
    """Universal Governance Runtime."""
    
    def __init__(self):
        """Initialize governance runtime."""
        self.rules: Dict[str, GovernanceRule] = {}
        self.violations: List[GovernanceViolation] = []
        self.audits: List[GovernanceAudit] = []
    
    def add_rule(self, rule: GovernanceRule) -> None:
        """Add a governance rule."""
        self.rules[rule.id] = rule
    
    def create_rule(
        self,
        name: str,
        domain: GovernanceDomain,
        description: str,
        conditions: Optional[Dict[str, Any]] = None,
        severity: str = "warning",
    ) -> GovernanceRule:
        """Create a governance rule."""
        rule = GovernanceRule(
            id=self._generate_id(name),
            name=name,
            domain=domain,
            description=description,
            conditions=conditions or {},
            severity=severity,
        )
        
        self.rules[rule.id] = rule
        return rule
    
    def check_compliance(
        self,
        entity_id: str,
        entity_type: str,
        domain: Optional[GovernanceDomain] = None,
    ) -> Dict[str, Any]:
        """Check compliance for an entity."""
        violations = []
        
        rules_to_check = self.rules.values()
        if domain:
            rules_to_check = [r for r in rules_to_check if r.domain == domain]
        
        for rule in rules_to_check:
            if rule.status != GovernanceStatus.ACTIVE:
                continue
            
            # Simple compliance check
            if rule.severity == "error":
                violations.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "description": f"Compliance check: {rule.description}",
                })
        
        return {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "compliant": len(violations) == 0,
            "violations": violations,
        }
    
    def report_violation(
        self,
        rule_id: str,
        entity_id: str,
        entity_type: str,
        description: str,
    ) -> GovernanceViolation:
        """Report a governance violation."""
        rule = self.rules.get(rule_id)
        severity = rule.severity if rule else "warning"
        
        violation = GovernanceViolation(
            id=self._generate_id("violation"),
            rule_id=rule_id,
            entity_id=entity_id,
            entity_type=entity_type,
            severity=severity,
            description=description,
        )
        
        self.violations.append(violation)
        
        # Audit
        self.audit(
            action="violation_reported",
            actor="system",
            entity_id=entity_id,
            entity_type=entity_type,
            result="violation_logged",
        )
        
        return violation
    
    def resolve_violation(self, violation_id: str, resolution: str) -> bool:
        """Resolve a violation."""
        for violation in self.violations:
            if violation.id == violation_id:
                violation.resolved = True
                violation.resolution = resolution
                return True
        return False
    
    def audit(
        self,
        action: str,
        actor: str,
        entity_id: str,
        entity_type: str,
        result: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> GovernanceAudit:
        """Record an audit entry."""
        audit = GovernanceAudit(
            id=self._generate_id("audit"),
            action=action,
            actor=actor,
            entity_id=entity_id,
            entity_type=entity_type,
            result=result,
            metadata=metadata or {},
        )
        
        self.audits.append(audit)
        return audit
    
    def get_violations(
        self,
        resolved: Optional[bool] = None,
        severity: Optional[str] = None,
    ) -> List[GovernanceViolation]:
        """Get violations."""
        violations = self.violations
        
        if resolved is not None:
            violations = [v for v in violations if v.resolved == resolved]
        
        if severity:
            violations = [v for v in violations if v.severity == severity]
        
        return violations
    
    def get_audits(
        self,
        entity_id: Optional[str] = None,
        actor: Optional[str] = None,
    ) -> List[GovernanceAudit]:
        """Get audit records."""
        audits = self.audits
        
        if entity_id:
            audits = [a for a in audits if a.entity_id == entity_id]
        
        if actor:
            audits = [a for a in audits if a.actor == actor]
        
        return audits
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate governance report."""
        total_violations = len(self.violations)
        resolved_violations = sum(1 for v in self.violations if v.resolved)
        active_rules = sum(1 for r in self.rules.values() if r.status == GovernanceStatus.ACTIVE)
        
        by_domain = {}
        for rule in self.rules.values():
            domain_name = rule.domain.value
            by_domain[domain_name] = by_domain.get(domain_name, 0) + 1
        
        return {
            "total_rules": len(self.rules),
            "active_rules": active_rules,
            "total_violations": total_violations,
            "resolved_violations": resolved_violations,
            "violation_resolution_rate": resolved_violations / total_violations if total_violations > 0 else 0,
            "total_audits": len(self.audits),
            "rules_by_domain": by_domain,
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
