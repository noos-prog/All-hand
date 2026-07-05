"""
CAPABILITY-000010: Architecture Validation

PURPOSE: Detect architectural violations.

VERSION: 1.0.0
"""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class Violation:
    """An architectural violation."""
    rule: str
    description: str
    file: str
    severity: str = "warning"

@dataclass
class ValidationResult:
    """Architecture validation result."""
    violations: List[Violation] = field(default_factory=list)
    valid: bool = True
    validated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "violations": [{"rule": v.rule, "description": v.description, "file": v.file, "severity": v.severity} for v in self.violations],
            "valid": self.valid,
            "validated_at": self.validated_at.isoformat(),
        }

class ArchitectureValidationCapability:
    """
    CAPABILITY-000010: Architecture Validation
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000010"
    
    @property
    def name(self) -> str:
        return "ArchitectureValidation"
    
    @property
    def description(self) -> str:
        return "Detects architectural violations"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> ValidationResult:
        """Execute architecture validation."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        violations = []
        
        # Check for circular dependencies
        # Check for missing __init__.py in packages
        # Check for business logic in adapters
        # Check for hardcoded values
        
        for root, dirs, files in os.walk(path):
            if ".git" in root or "__pycache__" in root:
                continue
            
            # Check for missing __init__.py
            if "agos_kernel" in root or "capabilities" in root or "providers" in root:
                if not any(f == "__init__.py" for f in files):
                    violations.append(Violation(
                        rule="PACKAGE_MISSING_INIT",
                        description="Python package missing __init__.py",
                        file=root,
                        severity="error"
                    ))
        
        return ValidationResult(
            violations=violations,
            valid=len(violations) == 0,
        )
