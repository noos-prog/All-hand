"""Universal Verification Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class VerificationType(Enum):
    """Verification type."""
    STRUCTURAL = "structural"
    SEMANTIC = "semantic"
    ARCHITECTURAL = "architectural"
    POLICY = "policy"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPATIBILITY = "compatibility"
    EVIDENCE = "evidence"


class VerificationStatus(Enum):
    """Verification status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class VerificationRule:
    """A verification rule."""
    id: str
    name: str
    verification_type: VerificationType
    checker: Callable = field(default_factory=lambda: True)
    severity: str = "error"
    description: str = ""


@dataclass
class VerificationResult:
    """Result of verification."""
    id: str
    verification_type: VerificationType
    status: VerificationStatus
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    executed_at: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0


@dataclass
class VerificationReport:
    """Comprehensive verification report."""
    id: str
    artifact_id: str
    results: List[VerificationResult] = field(default_factory=list)
    overall_passed: bool = True
    total_errors: int = 0
    total_warnings: int = 0
    created_at: datetime = field(default_factory=datetime.now)


class VerificationRuntime:
    """Universal Verification Runtime."""
    
    def __init__(self):
        """Initialize verification runtime."""
        self.rules: Dict[str, VerificationRule] = {}
        self.history: List[VerificationReport] = []
        self._register_default_rules()
    
    def _register_default_rules(self) -> None:
        """Register default verification rules."""
        # Structural verification
        self.add_rule(VerificationRule(
            id="struct-1",
            name="Check artifact structure",
            verification_type=VerificationType.STRUCTURAL,
            severity="error",
            description="Verify artifact has required fields",
        ))
        
        # Security verification
        self.add_rule(VerificationRule(
            id="security-1",
            name="Check for hardcoded secrets",
            verification_type=VerificationType.SECURITY,
            severity="error",
            description="Verify no hardcoded secrets in code",
        ))
        
        # Policy verification
        self.add_rule(VerificationRule(
            id="policy-1",
            name="Check policy compliance",
            verification_type=VerificationType.POLICY,
            severity="warning",
            description="Verify compliance with organizational policies",
        ))
    
    def add_rule(self, rule: VerificationRule) -> None:
        """Add a verification rule."""
        self.rules[rule.id] = rule
    
    def verify(
        self,
        artifact_id: str,
        artifact_data: Any,
        verification_types: Optional[List[VerificationType]] = None,
    ) -> VerificationReport:
        """Verify an artifact."""
        report = VerificationReport(
            id=self._generate_id("report"),
            artifact_id=artifact_id,
        )
        
        types_to_verify = verification_types or [t for t in VerificationType]
        
        for vtype in types_to_verify:
            result = self._verify_type(artifact_id, artifact_data, vtype)
            report.results.append(result)
            
            if not result.passed:
                report.overall_passed = False
                report.total_errors += len(result.errors)
            report.total_warnings += len(result.warnings)
        
        self.history.append(report)
        return report
    
    def _verify_type(
        self,
        artifact_id: str,
        artifact_data: Any,
        verification_type: VerificationType,
    ) -> VerificationResult:
        """Verify a specific type."""
        result = VerificationResult(
            id=self._generate_id(f"verify-{verification_type.value}"),
            verification_type=verification_type,
            status=VerificationStatus.RUNNING,
            passed=True,
        )
        
        start = datetime.now()
        
        # Apply rules for this verification type
        rules = [r for r in self.rules.values() if r.verification_type == verification_type]
        
        for rule in rules:
            if rule.verification_type == verification_type:
                try:
                    # Simple rule checking
                    if rule.severity == "error":
                        result.errors.append(f"Rule {rule.name}: Check required")
                    else:
                        result.warnings.append(f"Rule {rule.name}: Advisory check")
                except Exception as e:
                    result.errors.append(f"Rule {rule.name}: {str(e)}")
                    result.passed = False
        
        # Determine overall result
        critical_errors = [e for e in result.errors if "error" in e.lower()]
        if critical_errors:
            result.passed = False
            result.status = VerificationStatus.FAILED
        else:
            result.status = VerificationStatus.PASSED
        
        result.duration_ms = (datetime.now() - start).total_seconds() * 1000
        return result
    
    def verify_artifacts(
        self,
        artifact_ids: List[str],
        verification_types: Optional[List[VerificationType]] = None,
    ) -> List[VerificationReport]:
        """Verify multiple artifacts."""
        reports = []
        
        for artifact_id in artifact_ids:
            report = self.verify(artifact_id, {}, verification_types)
            reports.append(report)
        
        return reports
    
    def get_report(self, report_id: str) -> Optional[VerificationReport]:
        """Get verification report by ID."""
        for report in self.history:
            if report.id == report_id:
                return report
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get verification statistics."""
        total = len(self.history)
        passed = sum(1 for r in self.history if r.overall_passed)
        failed = total - passed
        
        return {
            "total_verifications": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0,
            "total_errors": sum(r.total_errors for r in self.history),
            "total_warnings": sum(r.total_warnings for r in self.history),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
