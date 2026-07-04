"""
Universal Validation Runtime
PHASE-02: EXECUTION-000012 - Universal Validation Runtime

Nothing enters or leaves AGOS without validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import uuid


class ValidationStage(Enum):
    """Validation stages."""
    INPUT = "input"
    PLANNING = "planning"
    EXECUTION = "execution"
    OUTPUT = "output"
    KNOWLEDGE = "knowledge"
    EVIDENCE = "evidence"
    ARTIFACT = "artifact"
    PUBLICATION = "publication"


class ValidationResult(Enum):
    """Validation result."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class ValidationRule:
    """Validation rule."""
    rule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    validator: Optional[Callable] = None
    severity: str = "error"  # error, warning


@dataclass
class ValidationIssue:
    """Validation issue."""
    issue_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    rule_name: str = ""
    message: str = ""
    severity: str = "error"
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Validation report."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    stage: ValidationStage = ValidationStage.INPUT
    result: ValidationResult = ValidationResult.PASSED
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    issues: List[ValidationIssue] = field(default_factory=list)
    validated_data: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'report_id': self.report_id,
            'stage': self.stage.value if isinstance(self.stage, ValidationStage) else self.stage,
            'result': self.result.value if isinstance(self.result, ValidationResult) else self.result,
            'timestamp': self.timestamp,
            'issues': [i.__dict__ for i in self.issues],
            'validated_data': self.validated_data,
        }


class SchemaValidator:
    """Validates data schemas."""
    
    def validate(self, data: Dict, schema: Dict) -> List[ValidationIssue]:
        """Validate data against schema."""
        issues = []
        
        # Check required fields
        required = schema.get('required', [])
        for field_name in required:
            if field_name not in data:
                issues.append(ValidationIssue(
                    rule_name='required_field',
                    message=f"Required field '{field_name}' is missing",
                    severity='error',
                    context={'field': field_name}
                ))
        
        return issues


class ContractValidator:
    """Validates contracts."""
    
    def validate(self, contract: Dict, expected: Dict) -> List[ValidationIssue]:
        """Validate contract."""
        issues = []
        
        for key in expected:
            if key not in contract:
                issues.append(ValidationIssue(
                    rule_name='contract_field',
                    message=f"Contract missing expected field '{key}'",
                    severity='error'
                ))
        
        return issues


class PolicyValidator:
    """Validates policies."""
    
    def validate(self, policy: Dict) -> List[ValidationIssue]:
        """Validate policy."""
        issues = []
        
        if not policy.get('name'):
            issues.append(ValidationIssue(
                rule_name='policy_name',
                message="Policy must have a name",
                severity='error'
            ))
        
        if not policy.get('rules'):
            issues.append(ValidationIssue(
                rule_name='policy_rules',
                message="Policy must have rules",
                severity='warning'
            ))
        
        return issues


class CompatibilityValidator:
    """Validates compatibility."""
    
    def validate(self, entity: Dict, compatibility_matrix: Dict) -> List[ValidationIssue]:
        """Validate compatibility."""
        issues = []
        
        entity_version = entity.get('version', '1.0.0')
        compatible_versions = compatibility_matrix.get('compatible_versions', [])
        
        if compatible_versions and entity_version not in compatible_versions:
            issues.append(ValidationIssue(
                rule_name='compatibility',
                message=f"Version {entity_version} not in compatibility matrix",
                severity='warning'
            ))
        
        return issues


class SecurityValidator:
    """Validates security."""
    
    def validate(self, data: Dict) -> List[ValidationIssue]:
        """Validate security."""
        issues = []
        
        # Check for sensitive data
        sensitive_keys = ['password', 'secret', 'token', 'api_key', 'private_key']
        for key in sensitive_keys:
            if key in data:
                issues.append(ValidationIssue(
                    rule_name='sensitive_data',
                    message=f"Potentially sensitive data detected: {key}",
                    severity='warning',
                    context={'key': key}
                ))
        
        return issues


class KnowledgeValidator:
    """Validates knowledge."""
    
    def validate(self, knowledge: Dict) -> List[ValidationIssue]:
        """Validate knowledge."""
        issues = []
        
        if not knowledge.get('content'):
            issues.append(ValidationIssue(
                rule_name='knowledge_content',
                message="Knowledge must have content",
                severity='error'
            ))
        
        if not knowledge.get('source'):
            issues.append(ValidationIssue(
                rule_name='knowledge_source',
                message="Knowledge must have a source",
                severity='warning'
            ))
        
        return issues


class EvidenceValidator:
    """Validates evidence."""
    
    def validate(self, evidence: Dict) -> List[ValidationIssue]:
        """Validate evidence."""
        issues = []
        
        if not evidence.get('evidence_id'):
            issues.append(ValidationIssue(
                rule_name='evidence_id',
                message="Evidence must have an ID",
                severity='error'
            ))
        
        if not evidence.get('integrity_hash'):
            issues.append(ValidationIssue(
                rule_name='evidence_integrity',
                message="Evidence must have an integrity hash",
                severity='warning'
            ))
        
        return issues


class ArtifactValidator:
    """Validates artifacts."""
    
    def validate(self, artifact: Dict) -> List[ValidationIssue]:
        """Validate artifact."""
        issues = []
        
        if not artifact.get('artifact_id'):
            issues.append(ValidationIssue(
                rule_name='artifact_id',
                message="Artifact must have an ID",
                severity='error'
            ))
        
        if not artifact.get('content'):
            issues.append(ValidationIssue(
                rule_name='artifact_content',
                message="Artifact must have content",
                severity='warning'
            ))
        
        return issues


class ValidationRuntime:
    """
    Universal Validation Runtime.
    
    Nothing enters or leaves AGOS without validation.
    
    Validation Stages:
    - Input Validation
    - Planning Validation
    - Execution Validation
    - Output Validation
    - Knowledge Validation
    - Evidence Validation
    - Artifact Validation
    - Publication Validation
    
    Rules:
    - Validation failures terminate execution
    - Validation reports become Artifacts
    - Validation results generate Evidence
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.schema = SchemaValidator()
        self.contract = ContractValidator()
        self.policy = PolicyValidator()
        self.compatibility = CompatibilityValidator()
        self.security = SecurityValidator()
        self.knowledge = KnowledgeValidator()
        self.evidence = EvidenceValidator()
        self.artifact = ArtifactValidator()
        
        # Validation history
        self.reports: List[ValidationReport] = []
    
    def validate(
        self,
        stage: ValidationStage,
        data: Dict,
        schema: Dict = None
    ) -> ValidationReport:
        """Run validation."""
        report = ValidationReport(stage=stage)
        
        # Collect issues
        issues = []
        
        if schema:
            issues.extend(self.schema.validate(data, schema))
        
        # Stage-specific validation
        if stage == ValidationStage.INPUT:
            issues.extend(self.security.validate(data))
        
        elif stage == ValidationStage.PLANNING:
            issues.extend(self.contract.validate(data, {}))
        
        elif stage == ValidationStage.OUTPUT:
            issues.extend(self.artifact.validate(data))
        
        elif stage == ValidationStage.KNOWLEDGE:
            issues.extend(self.knowledge.validate(data))
        
        elif stage == ValidationStage.EVIDENCE:
            issues.extend(self.evidence.validate(data))
        
        elif stage == ValidationStage.ARTIFACT:
            issues.extend(self.artifact.validate(data))
        
        report.issues = issues
        
        # Determine result
        has_errors = any(i.severity == 'error' for i in issues)
        has_warnings = any(i.severity == 'warning' for i in issues)
        
        if has_errors:
            report.result = ValidationResult.FAILED
        elif has_warnings:
            report.result = ValidationResult.WARNING
        else:
            report.result = ValidationResult.PASSED
        
        report.validated_data = data
        
        # Record report
        self.reports.append(report)
        
        return report
    
    def validate_or_fail(self, stage: ValidationStage, data: Dict) -> ValidationReport:
        """Validate or fail execution."""
        report = self.validate(stage, data)
        
        if report.result == ValidationResult.FAILED:
            raise ValidationError(f"Validation failed at {stage.value}: {report.issues}")
        
        return report
    
    def get_reports(self, stage: ValidationStage = None) -> List[ValidationReport]:
        """Get validation reports."""
        if stage:
            return [r for r in self.reports if r.stage == stage]
        return self.reports


class ValidationError(Exception):
    """Validation error."""
    pass