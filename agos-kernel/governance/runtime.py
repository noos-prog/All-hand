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


# ============================================================
# GOVERNANCE-000001: Decision Records
# ============================================================

class DecisionType(Enum):
    ADR = "adr"
    TDR = "tdr"
    PDR = "pdr"
    SDR = "sdr"
    ODR = "odr"


class DecisionStatus(Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


@dataclass
class Decision:
    id: str
    decision_type: DecisionType
    title: str
    status: DecisionStatus
    context: str
    problem_statement: str
    decision: str
    alternatives: List[str] = field(default_factory=list)
    trade_offs: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    approved_by: str = ""
    version: str = "1.0"
    superseded_by: Optional[str] = None


class DecisionRegistry:
    def __init__(self):
        self.decisions: Dict[str, Decision] = {}
        self._init_core_decisions()
    
    def _init_core_decisions(self):
        self.record(Decision(
            id="ADR-000001", decision_type=DecisionType.ADR,
            title="Kernel Architecture v2.0", status=DecisionStatus.APPROVED,
            context="Establishing AGOS Kernel",
            problem_statement="Need stable kernel without business logic",
            decision="Implement kernel with Capabilities, Providers, Adapters",
            alternatives=["Monolithic design"],
            consequences=["Kernel is immutable", "Extensions are isolated"],
            approved_by="Architecture Board"
        ))
        self.record(Decision(
            id="ADR-000002", decision_type=DecisionType.ADR,
            title="Async Execution Model", status=DecisionStatus.APPROVED,
            context="Execution requirements",
            problem_statement="Need concurrent execution",
            decision="Use asyncio",
            approved_by="Architecture Board"
        ))
        self.record(Decision(
            id="TDR-000001", decision_type=DecisionType.TDR,
            title="Python Implementation", status=DecisionStatus.APPROVED,
            context="Implementation language",
            problem_statement="Need broad ecosystem",
            decision="Use Python 3.10+",
            approved_by="Technical Board"
        ))
    
    def record(self, decision: Decision):
        self.decisions[decision.id] = decision
    
    def get(self, decision_id: str) -> Optional[Decision]:
        return self.decisions.get(decision_id)
    
    def list_by_type(self, dtype: DecisionType) -> List[Decision]:
        return [d for d in self.decisions.values() if d.decision_type == dtype]
    
    def approve(self, decision_id: str, approved_by: str) -> bool:
        decision = self.decisions.get(decision_id)
        if not decision:
            return False
        decision.status = DecisionStatus.APPROVED
        decision.approved_by = approved_by
        return True


# ============================================================
# GOVERNANCE-000002: Technical Debt
# ============================================================

class DebtType(Enum):
    ARCHITECTURE = "architecture"
    CODE = "code"
    KNOWLEDGE = "knowledge"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    PERFORMANCE = "performance"
    INFRASTRUCTURE = "infrastructure"
    TESTING = "testing"


class DebtStatus(Enum):
    IDENTIFIED = "identified"
    ACKNOWLEDGED = "acknowledged"
    REMEDIATION = "rememdy"
    RESOLVED = "resolved"


@dataclass
class TechnicalDebt:
    id: str
    title: str
    debt_type: DebtType
    description: str
    owner: str
    priority: int
    status: DebtStatus
    evidence: List[str] = field(default_factory=list)
    cost_estimate_hours: float = 0.0
    interest_per_release: float = 0.0
    resolution_strategy: str = ""
    target_release: str = ""


class TechnicalDebtRegistry:
    def __init__(self):
        self.debts: Dict[str, TechnicalDebt] = {}
        self._init_debt()
    
    def _init_debt(self):
        self.record(TechnicalDebt(
            id="DEBT-000001", title="Test Coverage Gap",
            debt_type=DebtType.TESTING, description="Coverage below target",
            owner="Engineering Team", priority=3, status=DebtStatus.ACKNOWLEDGED,
            evidence=["Coverage report"], cost_estimate_hours=40.0,
            interest_per_release=0.5, resolution_strategy="Incremental coverage",
            target_release="v2.1"
        ))
    
    def record(self, debt: TechnicalDebt):
        self.debts[debt.id] = debt
    
    def get(self, debt_id: str) -> Optional[TechnicalDebt]:
        return self.debts.get(debt_id)
    
    def list_by_priority(self) -> List[TechnicalDebt]:
        return sorted(self.debts.values(), key=lambda d: d.priority)
    
    def total_cost(self) -> float:
        return sum(d.cost_estimate_hours for d in self.debts.values())


# ============================================================
# GOVERNANCE-000003: Release Governance
# ============================================================

class ReleaseType(Enum):
    DEVELOPMENT = "development"
    ALPHA = "alpha"
    BETA = "beta"
    RC = "release_candidate"
    PRODUCTION = "production"
    HOTFIX = "hotfix"
    LTS = "long_term_support"


class ReleaseStatus(Enum):
    PLANNED = "planned"
    BUILDING = "building"
    TESTING = "testing"
    CERTIFIED = "certified"
    PUBLISHED = "published"
    SIGNED = "signed"


@dataclass
class ReleaseManifest:
    version: str
    release_type: ReleaseType
    status: ReleaseStatus
    change_log: List[str] = field(default_factory=list)
    migration_guide: str = ""
    security_report: Dict[str, Any] = field(default_factory=dict)
    benchmark_results: Dict[str, float] = field(default_factory=dict)
    certification_results: Dict[str, bool] = field(default_factory=dict)
    evidence_package: List[str] = field(default_factory=list)
    known_issues: List[str] = field(default_factory=list)
    digital_signature: str = ""
    published_at: Optional[datetime] = None


class ReleaseGovernance:
    def __init__(self):
        self.releases: Dict[str, ReleaseManifest] = {}
        self._init_release()
    
    def _init_release(self):
        self.create_release("2.0.0", ReleaseType.PRODUCTION)
    
    def create_release(self, version: str, release_type: ReleaseType) -> ReleaseManifest:
        manifest = ReleaseManifest(
            version=version, release_type=release_type,
            status=ReleaseStatus.PLANNED
        )
        self.releases[version] = manifest
        return manifest
    
    def get_release(self, version: str) -> Optional[ReleaseManifest]:
        return self.releases.get(version)
    
    def sign_release(self, version: str) -> bool:
        release = self.releases.get(version)
        if not release or release.status != ReleaseStatus.CERTIFIED:
            return False
        release.digital_signature = hashlib.sha256(version.encode()).hexdigest()
        release.status = ReleaseStatus.SIGNED
        return True


# Global instances
_decision_registry = DecisionRegistry()
_debt_registry = TechnicalDebtRegistry()
_release_governance = ReleaseGovernance()


def get_decision_registry() -> DecisionRegistry:
    return _decision_registry


def get_debt_registry() -> TechnicalDebtRegistry:
    return _debt_registry


def get_release_governance() -> ReleaseGovernance:
    return _release_governance


def test_governance():
    """Test governance."""
    print("=" * 60)
    print("AGOS Engineering Governance")
    print("=" * 60)
    
    decisions = get_decision_registry()
    print(f"\nDecisions: {len(decisions.decisions)}")
    for d in list(decisions.decisions.values())[:3]:
        print(f"  - {d.id}: {d.title}")
    
    debt = get_debt_registry()
    print(f"\nTechnical Debt: {len(debt.debts)} items")
    print(f"  Total Cost: {debt.total_cost()} hours")
    
    releases = get_release_governance()
    print(f"\nReleases: {len(releases.releases)}")
    for v, r in releases.releases.items():
        print(f"  - v{v} ({r.release_type.value})")
    
    print("\n" + "=" * 60)
    print("Governance Systems Ready!")
    print("=" * 60)


if __name__ == "__main__":
    test_governance()
