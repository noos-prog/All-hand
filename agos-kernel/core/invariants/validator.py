"""
Invariant Validator
EXECUTION-KERNEL-FINALIZATION-000002

Validates kernel invariants and blocks violations.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast

from agos_kernel.core.invariants.runtime import InvariantRuntime, InvariantResult
from agos_kernel.core.invariants.registry import InvariantRegistry, get_registry


@dataclass
class ValidationReport:
    """Report from invariant validation."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    results: List[InvariantResult] = field(default_factory=list)
    critical_violations: List[InvariantResult] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """Returns True if all critical invariants passed."""
        return len(self.critical_violations) == 0
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'total_checks': self.total_checks,
            'passed': self.passed,
            'failed': self.failed,
            'is_valid': self.is_valid,
            'critical_violations': len(self.critical_violations),
            'results': [r.to_dict() for r in self.results],
        }


class InvariantValidator:
    """
    Validates kernel invariants.
    
    Violation immediately fails validation.
    Critical violations block any operation.
    """
    
    def __init__(self, kernel_root: Optional[Path] = None):
        self.runtime = InvariantRuntime(kernel_root)
        self.registry = get_registry()
        self._validation_history: List[ValidationReport] = []
    
    def validate_all(self) -> ValidationReport:
        """Run complete validation."""
        results = self.runtime.verify_all()
        
        report = ValidationReport(
            total_checks=len(results),
            passed=sum(1 for r in results.values() if r.passed),
            failed=sum(1 for r in results.values() if not r.passed),
            results=list(results.values()),
            critical_violations=[
                r for r in results.values() 
                if not r.passed and self._is_critical(r.invariant_id)
            ],
        )
        
        self._validation_history.append(report)
        return report
    
    def validate_category(self, category: str) -> ValidationReport:
        """Validate invariants in a specific category."""
        category_invariants = self.registry.get_by_category(category)
        results = {}
        
        all_results = self.runtime.verify_all()
        for inv in category_invariants:
            if inv.id in all_results:
                results[inv.id] = all_results[inv.id]
        
        report = ValidationReport(
            total_checks=len(results),
            passed=sum(1 for r in results.values() if r.passed),
            failed=sum(1 for r in results.values() if not r.passed),
            results=list(results.values()),
            critical_violations=[
                r for r in results.values() 
                if not r.passed and self._is_critical(r.invariant_id)
            ],
        )
        
        return report
    
    def quick_validate(self) -> Tuple[bool, List[str]]:
        """
        Quick validation check.
        
        Returns (is_valid, list_of_violations)
        """
        report = self.validate_all()
        violations = []
        
        for result in report.results:
            if not result.passed:
                violations.append(f"{result.invariant_id}: {result.violations}")
        
        return report.is_valid, violations
    
    def pre_commit_check(self) -> bool:
        """
        Check to run before any commit.
        
        Returns True if validation passes.
        Critical violations will block the commit.
        """
        report = self.validate_all()
        
        if not report.is_valid:
            print(f"❌ Pre-commit validation FAILED")
            print(f"   Critical violations: {len(report.critical_violations)}")
            for v in report.critical_violations:
                print(f"   - {v.invariant_id}")
            return False
        
        print(f"✅ Pre-commit validation PASSED")
        print(f"   Checks: {report.total_checks}, Passed: {report.passed}")
        return True
    
    def _is_critical(self, invariant_id: str) -> bool:
        """Check if an invariant is marked critical."""
        inv = self.registry.get(invariant_id)
        return inv is not None and inv.severity == 'critical'
    
    def get_history(self) -> List[ValidationReport]:
        """Get validation history."""
        return self._validation_history


def validate_kernel() -> bool:
    """
    Main entry point for kernel validation.
    
    Returns True if kernel passes all invariants.
    """
    validator = InvariantValidator()
    return validator.pre_commit_check()
