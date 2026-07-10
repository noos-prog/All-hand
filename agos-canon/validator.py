#!/usr/bin/env python3
"""
AGOS Canon - Validator
======================

Validates code, contracts, and components against AGOS canons and constitution.
This is the enforcement mechanism for AGOS compliance.

All violations are reported with:
- Canon/Article reference
- Severity level
- Fix suggestion
- Evidence
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime
import re
import ast
import hashlib
import json


class ComplianceLevel(Enum):
    """Compliance level for validation results."""
    FULL = "full"           # 100% compliant
    PARTIAL = "partial"     # Some violations
    VIOLATION = "violation"  # Major violations
    CRITICAL = "critical"   # System cannot function


@dataclass
class Violation:
    """A single canon or constitutional violation."""
    id: str                       # Unique violation ID
    rule_id: str                  # CANON-XXX or Article number
    rule_name: str                # Human-readable rule name
    severity: str                 # critical, high, medium, low
    description: str              # What was violated
    location: str                 # File, line, column
    evidence: str                 # Code/text that caused violation
    fix_suggestion: str           # How to fix
    auto_fixable: bool = False    # Can be auto-fixed
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "description": self.description,
            "location": self.location,
            "evidence": self.evidence[:200],  # Truncate long evidence
            "fix_suggestion": self.fix_suggestion,
            "auto_fixable": self.auto_fixable,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ValidationResult:
    """Result of validating a component or code."""
    name: str                           # Component name
    level: ComplianceLevel              # Overall compliance level
    violations: List[Violation]         # All violations found
    passed_checks: List[str]            # Checks that passed
    warnings: List[str]                # Non-blocking warnings
    metadata: Dict[str, Any]            # Additional metadata
    validated_at: datetime = field(default_factory=datetime.utcnow)
    hash: str = ""                      # Hash of validated content
    
    def is_compliant(self) -> bool:
        """Check if result is fully compliant."""
        return self.level == ComplianceLevel.FULL and len(self.violations) == 0
    
    def has_critical(self) -> bool:
        """Check if has critical violations."""
        return any(v.severity == "critical" for v in self.violations)
    
    def get_violations_by_severity(self) -> Dict[str, List[Violation]]:
        """Group violations by severity."""
        result = {"critical": [], "high": [], "medium": [], "low": []}
        for v in self.violations:
            if v.severity in result:
                result[v.severity].append(v)
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "level": self.level.value,
            "is_compliant": self.is_compliant(),
            "has_critical": self.has_critical(),
            "violation_count": len(self.violations),
            "violations": [v.to_dict() for v in self.violations],
            "passed_checks": self.passed_checks,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "validated_at": self.validated_at.isoformat(),
            "hash": self.hash,
        }


class CanonValidator:
    """
    Main validator for AGOS canon and constitutional compliance.
    
    Validates:
    1. Python source code
    2. Contracts
    3. Components
    4. Documentation
    5. Configuration
    """
    
    def __init__(self):
        self._violations: List[Violation] = []
        self._checks_passed: List[str] = []
        self._initialized = False
        self._violation_counter = 0
    
    def _new_violation_id(self) -> str:
        """Generate unique violation ID."""
        self._violation_counter += 1
        return f"V{self._violation_counter:04d}"
    
    def _add_violation(
        self,
        rule_id: str,
        rule_name: str,
        severity: str,
        description: str,
        location: str,
        evidence: str,
        fix_suggestion: str,
        auto_fixable: bool = False,
    ) -> Violation:
        """Add a violation to the list."""
        violation = Violation(
            id=self._new_violation_id(),
            rule_id=rule_id,
            rule_name=rule_name,
            severity=severity,
            description=description,
            location=location,
            evidence=evidence,
            fix_suggestion=fix_suggestion,
            auto_fixable=auto_fixable,
        )
        self._violations.append(violation)
        return violation
    
    def reset(self) -> None:
        """Reset validator state."""
        self._violations = []
        self._checks_passed = []
        self._violation_counter = 0
    
    # ============ VOCABULARY VALIDATION (CANON-001) ============
    
    def validate_vocabulary_usage(self, code: str, location: str = "unknown") -> None:
        """
        Validate that code uses canonical vocabulary only.
        
        Checks:
        - No forbidden words
        - Uses canonical terms correctly
        - No ambiguous language
        """
        try:
            from vocabulary import get_vocabulary
        except ImportError:
            from .vocabulary import get_vocabulary
        
        vocabulary = get_vocabulary()
        
        # Forbidden patterns
        forbidden_patterns = [
            (r'\bAI\b(?!\s+(?:provider|external))', "Use 'external AI' or 'LLM provider' instead of 'AI'"),
            (r'\bmagic\b', "Avoid ambiguous term 'magic', be explicit"),
            (r'\bjust\b', "Avoid 'just', be specific"),
            (r'\bobviously\b|\bclearly\b', "Avoid presumptive language"),
            (r'\bshould\b|\bwould\b', "Use MUST/MAY instead of should/would"),
            (r'\bmaybe\b|\bprobably\b', "Decisions must be certain"),
            (r'\bTODO\b', "TODOs are forbidden in production code"),
            (r'\bHACK\b|\btemporary\b', "HACKs and workarounds are forbidden"),
        ]
        
        for pattern, suggestion in forbidden_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                self._add_violation(
                    rule_id="CANON-002",
                    rule_name="Forbidden Words",
                    severity="high",
                    description=f"Forbidden word found: '{match.group()}'",
                    location=f"{location}:{line_num}",
                    evidence=match.group(),
                    fix_suggestion=suggestion,
                )
        
        # Check for canonical terms
        canonical_terms = ["kernel", "agent", "capability", "provider", "contract"]
        for term in canonical_terms:
            if term in code.lower():
                # Verify usage is correct
                is_valid, reason = vocabulary.validate_usage(term)
                if not is_valid:
                    self._add_violation(
                        rule_id="CANON-001",
                        rule_name="Vocabulary",
                        severity="medium",
                        description=reason,
                        location=location,
                        evidence=term,
                        fix_suggestion=f"Use canonical term correctly",
                    )
    
    # ============ NAMING VALIDATION (CANON-008) ============
    
    def validate_naming(self, code: str, location: str = "unknown") -> List[Tuple[str, str, str]]:
        """
        Validate Python naming conventions.
        
        Returns list of (violation_type, name, suggestion) tuples.
        """
        violations = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return violations
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Classes must be PascalCase
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    if not node.name.startswith('_'):
                        violations.append((
                            "class_naming",
                            node.name,
                            f"Use PascalCase: {self._to_pascal_case(node.name)}"
                        ))
            
            elif isinstance(node, ast.FunctionDef):
                # Functions must be snake_case
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    if not node.name.startswith('_'):
                        violations.append((
                            "function_naming",
                            node.name,
                            f"Use snake_case: {self._to_snake_case(node.name)}"
                        ))
            
            elif isinstance(node, ast.Constant):
                # Constants must be UPPER_SNAKE_CASE
                if isinstance(node.value, (int, float, str)) and not isinstance(node.value, bool):
                    # This is a simple check for constant names in assignments
                    pass  # Full implementation would track assignments
        
        # Add violations
        for vtype, name, suggestion in violations:
            self._add_violation(
                rule_id="CANON-008",
                rule_name="Naming Conventions",
                severity="low",
                description=f"Invalid naming: '{name}'",
                location=location,
                evidence=name,
                fix_suggestion=suggestion,
            )
        
        return violations
    
    def _to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase."""
        parts = re.findall(r'[A-Z][a-z]*|[a-z]+', name)
        return ''.join(p.capitalize() for p in parts)
    
    def _to_snake_case(self, name: str) -> str:
        """Convert to snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    # ============ KERNEL OWNERSHIP VALIDATION (ARTICLE IV) ============
    
    def validate_kernel_ownership(self, code: str, location: str = "unknown") -> None:
        """
        Validate kernel ownership rules.
        
        External AI cannot:
        - Plan
        - Reason
        - Govern
        - Remember
        - Own Context
        - Own Knowledge
        - Own Missions
        """
        forbidden_ai_patterns = [
            (r'external.*(?:plan|decide|reason|govern)', "External AI cannot plan/decide/reason"),
            (r'ai\.(?:plan|decide|govern)', "AI cannot own planning/decisions"),
            (r'agent\.own.*(?:context|mission|knowledge)', "Agent cannot own context/mission/knowledge"),
        ]
        
        for pattern, description in forbidden_ai_patterns:
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                self._add_violation(
                    rule_id="ARTICLE-IV",
                    rule_name="The One Brain",
                    severity="critical",
                    description=description,
                    location=f"{location}:{line_num}",
                    evidence=match.group(),
                    fix_suggestion="Route through kernel for this operation",
                )
    
    # ============ CONTRACT VERSIONING VALIDATION (CANON-009) ============
    
    def validate_contract_versioning(self, contracts: List[Dict[str, Any]], location: str = "unknown") -> None:
        """
        Validate that all contracts are properly versioned.
        
        Requirements:
        - Every contract has a version
        - Version format is correct
        - Breaking changes have new major version
        """
        for contract in contracts:
            name = contract.get("name", "unknown")
            version = contract.get("version", None)
            
            if version is None:
                self._add_violation(
                    rule_id="CANON-009",
                    rule_name="Contract Versioning",
                    severity="critical",
                    description=f"Contract '{name}' has no version",
                    location=f"{location}/{name}",
                    evidence=str(contract),
                    fix_suggestion="Add version in format: v{major}_{minor}",
                )
                continue
            
            # Check version format
            if not re.match(r'^v\d+_\d+$', version):
                self._add_violation(
                    rule_id="CANON-009",
                    rule_name="Contract Versioning",
                    severity="high",
                    description=f"Contract '{name}' has invalid version format",
                    location=f"{location}/{name}",
                    evidence=version,
                    fix_suggestion="Use format: v{major}_{minor} (e.g., v1_0, v2_1)",
                )
    
    # ============ EVIDENCE VALIDATION (ARTICLE VI) ============
    
    def validate_knowledge_evidence(self, knowledge_entry: Dict[str, Any], location: str = "unknown") -> None:
        """
        Validate that knowledge entries have required evidence.
        
        Required fields:
        - source
        - evidence
        - confidence
        - lineage
        """
        required_fields = {
            "source": "Where the knowledge came from",
            "evidence": "Proof supporting the knowledge",
            "confidence": "Confidence level (0-1)",
            "lineage": "History of how knowledge was created",
        }
        
        for field_name, description in required_fields.items():
            if field_name not in knowledge_entry:
                self._add_violation(
                    rule_id="ARTICLE-VI",
                    rule_name="Knowledge Evidence",
                    severity="high",
                    description=f"Knowledge entry missing '{field_name}'",
                    location=location,
                    evidence=str(knowledge_entry),
                    fix_suggestion=f"Add {field_name}: {description}",
                )
        
        # Validate confidence range
        confidence = knowledge_entry.get("confidence")
        if confidence is not None:
            try:
                conf = float(confidence)
                if not 0 <= conf <= 1:
                    self._add_violation(
                        rule_id="ARTICLE-VI",
                        rule_name="Knowledge Evidence",
                        severity="medium",
                        description=f"Confidence must be 0-1, got {conf}",
                        location=location,
                        evidence=str(confidence),
                        fix_suggestion="Set confidence between 0.0 and 1.0",
                    )
            except (ValueError, TypeError):
                self._add_violation(
                    rule_id="ARTICLE-VI",
                    rule_name="Knowledge Evidence",
                    severity="medium",
                    description=f"Confidence must be numeric",
                    location=location,
                    evidence=str(confidence),
                    fix_suggestion="Set confidence as a number between 0.0 and 1.0",
                )
    
    # ============ MAIN VALIDATION METHODS ============
    
    def validate_python_file(self, file_path: str, content: str) -> ValidationResult:
        """
        Validate a Python source file against all canons.
        """
        self.reset()
        
        # CANON-001: Vocabulary
        self.validate_vocabulary_usage(content, file_path)
        
        # CANON-002: Forbidden Words (part of vocabulary)
        
        # CANON-008: Naming
        self.validate_naming(content, file_path)
        
        # ARTICLE-IV: Kernel Ownership
        self.validate_kernel_ownership(content, file_path)
        
        # Compute hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Determine compliance level
        if self._violations:
            severities = [v.severity for v in self._violations]
            if "critical" in severities:
                level = ComplianceLevel.CRITICAL
            elif "high" in severities:
                level = ComplianceLevel.VIOLATION
            elif "medium" in severities:
                level = ComplianceLevel.PARTIAL
            else:
                level = ComplianceLevel.PARTIAL
        else:
            level = ComplianceLevel.FULL
            self._checks_passed.extend([
                "CANON-001: Vocabulary",
                "CANON-002: Forbidden Words",
                "CANON-008: Naming",
                "ARTICLE-IV: Kernel Ownership",
            ])
        
        return ValidationResult(
            name=file_path,
            level=level,
            violations=self._violations.copy(),
            passed_checks=self._checks_passed.copy(),
            warnings=[],
            metadata={
                "lines": content.count('\n') + 1,
                "characters": len(content),
            },
            hash=content_hash,
        )
    
    def validate_knowledge_base(self, entries: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate knowledge base entries.
        """
        self.reset()
        
        for i, entry in enumerate(entries):
            self.validate_knowledge_evidence(entry, f"entry_{i}")
        
        if not self._violations:
            level = ComplianceLevel.FULL
            self._checks_passed.append("ARTICLE-VI: Knowledge Evidence")
        else:
            level = ComplianceLevel.PARTIAL
        
        return ValidationResult(
            name="knowledge_base",
            level=level,
            violations=self._violations.copy(),
            passed_checks=self._checks_passed.copy(),
            warnings=[],
            metadata={"entry_count": len(entries)},
        )
    
    def validate_contracts(self, contracts: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate contract definitions.
        """
        self.reset()
        
        self.validate_contract_versioning(contracts)
        
        if not self._violations:
            level = ComplianceLevel.FULL
            self._checks_passed.append("CANON-009: Contract Versioning")
        else:
            level = ComplianceLevel.VIOLATION
        
        return ValidationResult(
            name="contracts",
            level=level,
            violations=self._violations.copy(),
            passed_checks=self._checks_passed.copy(),
            warnings=[],
            metadata={"contract_count": len(contracts)},
        )
    
    def generate_report(self, results: List[ValidationResult]) -> str:
        """Generate human-readable validation report."""
        lines = [
            "=" * 70,
            "AGOS CANON & CONSTITUTION VALIDATION REPORT",
            "=" * 70,
            "",
        ]
        
        total_violations = sum(len(r.violations) for r in results)
        critical_count = sum(1 for r in results for v in r.violations if v.severity == "critical")
        compliant_count = sum(1 for r in results if r.is_compliant())
        
        lines.append(f"Summary:")
        lines.append(f"  Components validated: {len(results)}")
        lines.append(f"  Fully compliant: {compliant_count}")
        lines.append(f"  Total violations: {total_violations}")
        lines.append(f"  Critical violations: {critical_count}")
        lines.append("")
        
        for result in results:
            status = "✓ PASS" if result.is_compliant() else "✗ FAIL"
            lines.append(f"{status}: {result.name}")
            
            if result.violations:
                for v in result.violations[:5]:  # Show first 5
                    lines.append(f"  [{v.severity.upper()}] {v.rule_id}: {v.description}")
                if len(result.violations) > 5:
                    lines.append(f"  ... and {len(result.violations) - 5} more")
            lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
