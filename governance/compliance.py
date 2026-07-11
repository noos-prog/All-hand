"""
Compliance Module
================

Compliance management and policy enforcement.
Provides compliance checking and audit trail management.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ComplianceStatus(Enum):
    """Compliance status values."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING = "pending"
    EXEMPT = "exempt"
    UNKNOWN = "unknown"


class ComplianceLevel(Enum):
    """Compliance levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ADVISORY = "advisory"


@dataclass
class CompliancePolicy:
    """A compliance policy definition."""
    policy_id: str
    name: str
    description: str
    level: ComplianceLevel
    requirements: List[str] = field(default_factory=list)
    controls: List[str] = field(default_factory=list)
    is_mandatory: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceCheck:
    """A single compliance check result."""
    check_id: str
    policy_id: str
    resource_id: str
    status: ComplianceStatus
    findings: List[str] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.utcnow)
    next_check_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceReport:
    """Comprehensive compliance report."""
    report_id: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    overall_status: ComplianceStatus
    checks: List[ComplianceCheck]
    policy_count: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    pending_count: int = 0
    findings_summary: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at.isoformat(),
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "overall_status": self.overall_status.value,
            "policy_count": self.policy_count,
            "compliant_count": self.compliant_count,
            "non_compliant_count": self.non_compliant_count,
            "pending_count": self.pending_count,
            "checks": [
                {
                    "check_id": c.check_id,
                    "policy_id": c.policy_id,
                    "status": c.status.value,
                    "findings": c.findings,
                }
                for c in self.checks
            ],
        }


@dataclass
class AuditTrail:
    """Audit trail entry."""
    entry_id: str
    action: str
    actor: str
    resource: str
    result: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ComplianceManager:
    """
    Universal Compliance Management System.
    
    Manages compliance policies, checks, and reporting
    for the entire AGOS platform.
    """
    
    def __init__(self):
        self.policies: Dict[str, CompliancePolicy] = {}
        self.checks: Dict[str, ComplianceCheck] = {}
        self.audit_trail: List[AuditTrail] = []
        self._setup_default_policies()
    
    def _setup_default_policies(self) -> None:
        """Set up default compliance policies."""
        self.add_policy(CompliancePolicy(
            policy_id="POL-001",
            name="Data Privacy",
            description="Ensure data privacy compliance",
            level=ComplianceLevel.CRITICAL,
            requirements=["encryption_at_rest", "encryption_in_transit"],
        ))
        self.add_policy(CompliancePolicy(
            policy_id="POL-002",
            name="Access Control",
            description="Enforce access control policies",
            level=ComplianceLevel.HIGH,
            requirements=["rbac", "least_privilege"],
        ))
        self.add_policy(CompliancePolicy(
            policy_id="POL-003",
            name="Audit Logging",
            description="Require comprehensive audit logging",
            level=ComplianceLevel.MEDIUM,
            requirements=["log_all_actions", "retain_logs"],
        ))
    
    def add_policy(self, policy: CompliancePolicy) -> None:
        """Add a compliance policy."""
        self.policies[policy.policy_id] = policy
    
    def get_policy(self, policy_id: str) -> Optional[CompliancePolicy]:
        """Get a compliance policy."""
        return self.policies.get(policy_id)
    
    def run_check(
        self,
        policy_id: str,
        resource_id: str,
        validator: callable,
    ) -> ComplianceCheck:
        """Run a compliance check."""
        policy = self.policies.get(policy_id)
        if not policy:
            return ComplianceCheck(
                check_id=str(uuid.uuid4()),
                policy_id=policy_id,
                resource_id=resource_id,
                status=ComplianceStatus.UNKNOWN,
                findings=["Policy not found"],
            )
        
        findings = validator(policy)
        
        check = ComplianceCheck(
            check_id=str(uuid.uuid4()),
            policy_id=policy_id,
            resource_id=resource_id,
            status=ComplianceStatus.COMPLIANT if not findings else ComplianceStatus.NON_COMPLIANT,
            findings=findings,
        )
        
        self.checks[check.check_id] = check
        return check
    
    def generate_report(
        self,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
    ) -> ComplianceReport:
        """Generate a compliance report."""
        start = period_start or datetime.utcnow()
        end = period_end or datetime.utcnow()
        
        recent_checks = [
            c for c in self.checks.values()
            if start <= c.checked_at <= end
        ]
        
        compliant = sum(1 for c in recent_checks if c.status == ComplianceStatus.COMPLIANT)
        non_compliant = sum(1 for c in recent_checks if c.status == ComplianceStatus.NON_COMPLIANT)
        pending = sum(1 for c in recent_checks if c.status == ComplianceStatus.PENDING)
        
        findings_summary: Dict[str, int] = {}
        for check in recent_checks:
            for finding in check.findings:
                findings_summary[finding] = findings_summary.get(finding, 0) + 1
        
        overall = ComplianceStatus.COMPLIANT
        if non_compliant > 0:
            overall = ComplianceStatus.NON_COMPLIANT
        elif pending > len(recent_checks) * 0.5:
            overall = ComplianceStatus.PENDING
        
        return ComplianceReport(
            report_id=f"RPT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            generated_at=datetime.utcnow(),
            period_start=start,
            period_end=end,
            overall_status=overall,
            checks=recent_checks,
            policy_count=len(self.policies),
            compliant_count=compliant,
            non_compliant_count=non_compliant,
            pending_count=pending,
            findings_summary=findings_summary,
        )
    
    def log_action(
        self,
        action: str,
        actor: str,
        resource: str,
        result: str,
        **metadata,
    ) -> AuditTrail:
        """Log an action to the audit trail."""
        entry = AuditTrail(
            entry_id=str(uuid.uuid4()),
            action=action,
            actor=actor,
            resource=resource,
            result=result,
            metadata=metadata,
        )
        self.audit_trail.append(entry)
        return entry
    
    def query_audit_trail(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        since: Optional[datetime] = None,
    ) -> List[AuditTrail]:
        """Query the audit trail."""
        results = self.audit_trail
        
        if actor:
            results = [e for e in results if e.actor == actor]
        if action:
            results = [e for e in results if e.action == action]
        if since:
            results = [e for e in results if e.timestamp >= since]
        
        return results
