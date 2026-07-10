#!/usr/bin/env python3
"""
AIE - Verification Engine
=======================

The Verification Engine validates, checks, and compares.
It ensures decisions are correct before execution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class VerificationType(Enum):
    """Types of verification."""
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    INVARIANT = "invariant"
    SAFETY = "safety"
    LIVENESS = "liveness"
    BOUNDEDNESS = "boundedness"
    TERMINATION = "termination"


class VerificationStatus(Enum):
    """Status of verification."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class Invariant:
    """
    An invariant that must hold.
    """
    invariant_id: str
    name: str
    description: str
    
    # Check function
    check: Callable[[Dict[str, Any]], bool]
    
    # Severity
    is_critical: bool = False
    
    def evaluate(self, state: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Evaluate invariant on state."""
        try:
            holds = self.check(state)
            return holds, None
        except Exception as e:
            return False, str(e)


@dataclass
class VerificationCheck:
    """A single verification check."""
    check_id: str
    name: str
    verification_type: VerificationType
    passed: bool
    duration_ms: int
    error_message: Optional[str] = None
    
    def summary(self) -> str:
        status = "✓" if self.passed else "✗"
        return f"{status} {self.name}"


@dataclass
class VerificationResult:
    """
    Result of verification.
    """
    result_id: str
    verification_type: VerificationType
    status: VerificationStatus
    passed: bool
    checks: Tuple[VerificationCheck, ...]
    total_checks: int
    passed_checks: int
    failed_checks: int
    duration_ms: int
    timestamp: str
    violations: Tuple[Dict[str, Any], ...] = ()
    recommendations: Tuple[str, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        lines = [
            f"Verification: {self.verification_type.value}",
            f"Status: {self.status.value}",
            f"Passed: {self.passed_checks}/{self.total_checks}",
            "",
        ]
        
        if self.violations:
            lines.append("Violations:")
            for v in self.violations:
                lines.append(f"  - {v.get('message', 'Unknown')}")
        
        if self.recommendations:
            lines.append("")
            lines.append("Recommendations:")
            for r in self.recommendations:
                lines.append(f"  - {r}")
        
        return "\n".join(lines)


class VerificationEngine:
    """
    The Verification Engine - sixth stage of AIE.
    
    Responsibilities:
    - Validate inputs
    - Check invariants
    - Verify safety properties
    - Compare outputs
    
    The Verification Engine does NOT:
    - Make decisions
    - Execute actions
    """
    
    def __init__(self):
        self._invariants: Dict[str, Invariant] = {}
        self._verification_history: List[VerificationResult] = []
        self._initialized = True
    
    def add_invariant(
        self,
        invariant_id: str,
        name: str,
        description: str,
        check: Callable[[Dict[str, Any]], bool],
        is_critical: bool = False
    ) -> Invariant:
        """Add an invariant to verify."""
        invariant = Invariant(
            invariant_id=invariant_id,
            name=name,
            description=description,
            check=check,
            is_critical=is_critical,
        )
        self._invariants[invariant_id] = invariant
        return invariant
    
    def remove_invariant(self, invariant_id: str) -> bool:
        """Remove an invariant."""
        if invariant_id in self._invariants:
            del self._invariants[invariant_id]
            return True
        return False
    
    def verify(
        self,
        verification_type: VerificationType,
        state: Dict[str, Any],
        data: Any = None
    ) -> VerificationResult:
        """Run verification."""
        start_time = datetime.utcnow()
        result_id = f"ver_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        checks = []
        violations = []
        recommendations = []
        
        # Run invariant checks
        for inv_id, invariant in self._invariants.items():
            check_start = datetime.utcnow()
            
            holds, error = invariant.evaluate(state)
            check_duration = int((datetime.utcnow() - check_start).total_seconds() * 1000)
            
            check = VerificationCheck(
                check_id=inv_id,
                name=invariant.name,
                verification_type=verification_type,
                passed=holds,
                duration_ms=check_duration,
                error_message=error,
            )
            checks.append(check)
            
            if not holds:
                violations.append({
                    "invariant_id": inv_id,
                    "invariant_name": invariant.name,
                    "message": f"Invariant '{invariant.name}' violated",
                    "is_critical": invariant.is_critical,
                })
                
                if invariant.is_critical:
                    recommendations.append(f"Critical: Fix invariant '{invariant.name}'")
        
        # Run type-specific verification
        if verification_type == VerificationType.SYNTAX:
            type_checks = self._verify_syntax(data)
        elif verification_type == VerificationType.SEMANTIC:
            type_checks = self._verify_semantic(data)
        elif verification_type == VerificationType.SAFETY:
            type_checks = self._verify_safety(state)
        else:
            type_checks = []
        
        checks.extend(type_checks)
        
        # Calculate totals
        total = len(checks)
        passed = sum(1 for c in checks if c.passed)
        failed = total - passed
        duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        # Determine overall status
        if failed == 0:
            status = VerificationStatus.PASSED
            passed_overall = True
        elif any(v.get("is_critical") for v in violations):
            status = VerificationStatus.FAILED
            passed_overall = False
        else:
            status = VerificationStatus.FAILED
            passed_overall = False
        
        # Generate recommendations if failed
        if not passed_overall:
            recommendations.extend(self._generate_recommendations(violations))
        
        result = VerificationResult(
            result_id=result_id,
            verification_type=verification_type,
            status=status,
            passed=passed_overall,
            checks=tuple(checks),
            total_checks=total,
            passed_checks=passed,
            failed_checks=failed,
            duration_ms=duration,
            violations=tuple(violations),
            recommendations=tuple(recommendations),
            timestamp=datetime.utcnow().isoformat(),
        )
        
        self._verification_history.append(result)
        return result
    
    def _verify_syntax(self, data: Any) -> List[VerificationCheck]:
        """Verify syntax of data."""
        checks = []
        
        if data is None:
            checks.append(VerificationCheck(
                check_id="syntax_null",
                name="Not Null",
                verification_type=VerificationType.SYNTAX,
                passed=False,
                duration_ms=0,
                error_message="Data is null",
            ))
            return checks
        
        # Check data type
        if isinstance(data, dict):
            checks.append(VerificationCheck(
                check_id="syntax_dict",
                name="Is Dictionary",
                verification_type=VerificationType.SYNTAX,
                passed=True,
                duration_ms=0,
            ))
            
            # Check required keys
            required_keys = ["id", "type"]
            for key in required_keys:
                if key not in data:
                    checks.append(VerificationCheck(
                        check_id=f"syntax_key_{key}",
                        name=f"Has Key '{key}'",
                        verification_type=VerificationType.SYNTAX,
                        passed=False,
                        duration_ms=0,
                        error_message=f"Missing required key: {key}",
                    ))
        
        return checks
    
    def _verify_semantic(self, data: Any) -> List[VerificationCheck]:
        """Verify semantic correctness."""
        checks = []
        
        # Check semantic constraints
        if isinstance(data, dict):
            # Check value ranges
            if "value" in data and isinstance(data["value"], (int, float)):
                if data["value"] < 0:
                    checks.append(VerificationCheck(
                        check_id="semantic_value",
                        name="Non-negative Value",
                        verification_type=VerificationType.SEMANTIC,
                        passed=False,
                        duration_ms=0,
                        error_message="Value must be non-negative",
                    ))
        
        return checks
    
    def _verify_safety(self, state: Dict[str, Any]) -> List[VerificationCheck]:
        """Verify safety properties."""
        checks = []
        
        # Safety: No negative resources
        if "resources" in state:
            resources = state["resources"]
            if isinstance(resources, dict):
                for name, value in resources.items():
                    if value < 0:
                        checks.append(VerificationCheck(
                            check_id=f"safety_resources_{name}",
                            name=f"Resource '{name}' Non-negative",
                            verification_type=VerificationType.SAFETY,
                            passed=False,
                            duration_ms=0,
                            error_message=f"Resource '{name}' is negative: {value}",
                        ))
        
        # Safety: No infinite loops
        if "iterations" in state:
            max_iterations = 10000
            if state["iterations"] > max_iterations:
                checks.append(VerificationCheck(
                    check_id="safety_iterations",
                    name="Iterations Bounded",
                    verification_type=VerificationType.SAFETY,
                    passed=False,
                    duration_ms=0,
                    error_message=f"Iterations ({state['iterations']}) exceed maximum ({max_iterations})",
                ))
        
        return checks
    
    def _generate_recommendations(self, violations: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on violations."""
        recommendations = []
        
        for violation in violations:
            inv_name = violation.get("invariant_name", "Unknown")
            
            if "null" in inv_name.lower():
                recommendations.append("Add null checks before accessing data")
            elif "range" in inv_name.lower():
                recommendations.append("Validate input ranges")
            elif "bounds" in inv_name.lower():
                recommendations.append("Add boundary checks")
            else:
                recommendations.append(f"Review logic for '{inv_name}'")
        
        return recommendations
    
    def verify_invariants(self, state: Dict[str, Any]) -> VerificationResult:
        """Verify all registered invariants."""
        return self.verify(VerificationType.INVARIANT, state)
    
    def compare_outputs(
        self,
        expected: Any,
        actual: Any
    ) -> VerificationResult:
        """Compare expected and actual outputs."""
        start_time = datetime.utcnow()
        result_id = f"cmp_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        checks = []
        
        # Structural comparison
        type_match = type(expected) == type(actual)
        checks.append(VerificationCheck(
            check_id="cmp_type",
            name="Types Match",
            verification_type=VerificationType.SEMANTIC,
            passed=type_match,
            duration_ms=0,
            error_message=None if type_match else f"Expected {type(expected).__name__}, got {type(actual).__name__}",
        ))
        
        # Value comparison
        if isinstance(expected, dict) and isinstance(actual, dict):
            for key in expected:
                if key in actual:
                    match = expected[key] == actual[key]
                    checks.append(VerificationCheck(
                        check_id=f"cmp_key_{key}",
                        name=f"Key '{key}' Matches",
                        verification_type=VerificationType.SEMANTIC,
                        passed=match,
                        duration_ms=0,
                        error_message=None if match else f"Value mismatch for key '{key}'",
                    ))
        
        duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        total = len(checks)
        passed = sum(1 for c in checks if c.passed)
        failed = total - passed
        
        return VerificationResult(
            result_id=result_id,
            verification_type=VerificationType.SEMANTIC,
            status=VerificationStatus.PASSED if failed == 0 else VerificationStatus.FAILED,
            passed=failed == 0,
            checks=tuple(checks),
            total_checks=total,
            passed_checks=passed,
            failed_checks=failed,
            duration_ms=duration,
            violations=tuple(),
            recommendations=tuple(),
            timestamp=datetime.utcnow().isoformat(),
        )
    
    def get_history(
        self,
        limit: int = 100,
        verification_type: Optional[VerificationType] = None
    ) -> List[VerificationResult]:
        """Get verification history."""
        history = self._verification_history
        
        if verification_type:
            history = [r for r in history if r.verification_type == verification_type]
        
        return history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        if not self._verification_history:
            return {
                "total_verifications": 0,
                "invariants_registered": len(self._invariants),
            }
        
        total = len(self._verification_history)
        passed = sum(1 for r in self._verification_history if r.passed)
        
        return {
            "total_verifications": total,
            "passed_verifications": passed,
            "pass_rate": passed / total if total > 0 else 0,
            "invariants_registered": len(self._invariants),
            "avg_duration_ms": (
                sum(r.duration_ms for r in self._verification_history) / total
                if total > 0 else 0
            ),
        }
