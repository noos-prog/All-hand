"""
Invariant Reporter
EXECUTION-KERNEL-FINALIZATION-000002

Reports on invariant verification results.
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import json

from agos_kernel.core.invariants.runtime import InvariantResult
from agos_kernel.core.invariants.validator import ValidationReport


@dataclass
class InvariantViolation:
    """Represents a single invariant violation."""
    invariant_id: str
    invariant_name: str
    severity: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    details: Dict = field(default_factory=dict)


class InvariantReporter:
    """
    Reports on invariant verification results.
    
    Generates human-readable and machine-parseable reports.
    """
    
    def __init__(self):
        self.reports: List[ValidationReport] = []
    
    def add_report(self, report: ValidationReport) -> None:
        """Add a validation report."""
        self.reports.append(report)
    
    def generate_summary(self) -> str:
        """Generate human-readable summary."""
        if not self.reports:
            return "No validation reports available."
        
        latest = self.reports[-1]
        
        lines = [
            "=" * 60,
            "AGOS KERNEL INVARIANT VERIFICATION REPORT",
            "=" * 60,
            f"Timestamp: {latest.timestamp.isoformat()}",
            f"Total Checks: {latest.total_checks}",
            f"Passed: {latest.passed} ✅",
            f"Failed: {latest.failed} ❌",
            f"Status: {'VALID ✅' if latest.is_valid else 'INVALID ❌'}",
            "",
        ]
        
        if latest.critical_violations:
            lines.append("CRITICAL VIOLATIONS:")
            lines.append("-" * 40)
            for v in latest.critical_violations:
                lines.append(f"  ❌ {v.invariant_id}")
                for violation in v.violations:
                    lines.append(f"      Module: {violation.get('module', 'N/A')}")
                    lines.append(f"      Issue: {violation.get('issue', violation)}")
            lines.append("")
        
        # Group by category
        categories = {}
        for result in latest.results:
            cat = result.invariant_id.split('-')[0]
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0, 'results': []}
            categories[cat]['results'].append(result)
            if result.passed:
                categories[cat]['passed'] += 1
            else:
                categories[cat]['failed'] += 1
        
        lines.append("BREAKDOWN BY CATEGORY:")
        lines.append("-" * 40)
        for cat, data in sorted(categories.items()):
            status = "✅" if data['failed'] == 0 else "❌"
            lines.append(f"  {cat}: {data['passed']}/{data['passed']+data['failed']} {status}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def generate_json_report(self) -> Dict:
        """Generate machine-parseable JSON report."""
        if not self.reports:
            return {'error': 'No validation reports available'}
        
        latest = self.reports[-1]
        
        return {
            'timestamp': latest.timestamp.isoformat(),
            'summary': {
                'total_checks': latest.total_checks,
                'passed': latest.passed,
                'failed': latest.failed,
                'is_valid': latest.is_valid,
                'critical_violations_count': len(latest.critical_violations),
            },
            'violations': [
                {
                    'invariant_id': v.invariant_id,
                    'violations': v.violations,
                }
                for v in latest.results if not v.passed
            ],
            'results': [r.to_dict() for r in latest.results],
        }
    
    def generate_markdown_report(self) -> str:
        """Generate Markdown format report."""
        if not self.reports:
            return "# No Validation Reports Available"
        
        latest = self.reports[-1]
        
        lines = [
            "# AGOS Kernel Invariant Verification Report",
            "",
            f"**Timestamp:** {latest.timestamp.isoformat()}",
            f"**Status:** {'✅ VALID' if latest.is_valid else '❌ INVALID'}",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Checks | {latest.total_checks} |",
            f"| Passed | {latest.passed} |",
            f"| Failed | {latest.failed} |",
            f"| Critical Violations | {len(latest.critical_violations)} |",
            "",
        ]
        
        if latest.critical_violations:
            lines.extend([
                "## Critical Violations",
                "",
            ])
            for v in latest.critical_violations:
                lines.append(f"### ❌ {v.invariant_id}")
                lines.append("")
                for violation in v.violations:
                    lines.append(f"- **{violation.get('issue', 'Violation')}:**")
                    lines.append(f"  - Module: `{violation.get('module', 'N/A')}`")
                    if 'file' in violation:
                        lines.append(f"  - File: `{violation['file']}`")
                lines.append("")
        
        lines.extend([
            "## All Results",
            "",
        ])
        
        for result in latest.results:
            status = "✅" if result.passed else "❌"
            lines.append(f"- {status} **{result.invariant_id}**")
        
        return "\n".join(lines)
    
    def print_report(self) -> None:
        """Print report to console."""
        print(self.generate_summary())
    
    def save_report(self, path: str, format: str = 'json') -> None:
        """Save report to file."""
        if format == 'json':
            content = json.dumps(self.generate_json_report(), indent=2)
        elif format == 'markdown':
            content = self.generate_markdown_report()
        else:
            content = self.generate_summary()
        
        with open(path, 'w') as f:
            f.write(content)
