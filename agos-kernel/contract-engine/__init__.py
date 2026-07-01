"""Universal Contract Engine - Validates all contracts before execution."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type


class ContractType(Enum):
    """Contract types."""
    MISSION = "mission"
    CAPABILITY = "capability"
    PROVIDER = "provider"
    SKILL = "skill"
    EVENT = "event"


class ValidationStatus(Enum):
    """Validation status."""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"


@dataclass
class ValidationError:
    """Validation error."""
    field: str
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationResult:
    """Result of contract validation."""
    contract_type: ContractType
    contract_id: str
    status: ValidationStatus
    errors: List[ValidationError] = field(default_factory=list)
    validated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID
    
    @property
    def has_errors(self) -> bool:
        return any(e.severity == "error" for e in self.errors)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "contract_type": self.contract_type.value,
            "contract_id": self.contract_id,
            "status": self.status.value,
            "errors": [{"field": e.field, "message": e.message, "severity": e.severity} for e in self.errors],
            "validated_at": self.validated_at.isoformat()
        }


@dataclass
class ContractSchema:
    """Schema for a contract type."""
    contract_type: ContractType
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    field_types: Dict[str, Type] = field(default_factory=dict)
    version_range: str = ">=1.0.0"


class SchemaValidator:
    """Validates contracts against schemas."""
    
    SCHEMAS = {
        ContractType.MISSION: ContractSchema(
            contract_type=ContractType.MISSION,
            required_fields=["id", "name", "capability"],
            optional_fields=["description", "parameters"],
            field_types={"parameters": dict}
        ),
        ContractType.CAPABILITY: ContractSchema(
            contract_type=ContractType.CAPABILITY,
            required_fields=["name", "skills"],
            optional_fields=["description", "version", "priority"],
            field_types={"skills": list, "priority": (int, float)}
        ),
        ContractType.PROVIDER: ContractSchema(
            contract_type=ContractType.PROVIDER,
            required_fields=["name"],
            optional_fields=["version", "skills"],
            field_types={"skills": list}
        ),
        ContractType.SKILL: ContractSchema(
            contract_type=ContractType.SKILL,
            required_fields=["name"],
            optional_fields=["description", "version", "input_type", "output_type"],
        ),
        ContractType.EVENT: ContractSchema(
            contract_type=ContractType.EVENT,
            required_fields=["id", "type", "timestamp"],
            optional_fields=["mission_id", "data"],
            field_types={"data": dict}
        ),
    }
    
    def validate(self, contract_type: ContractType, data: Dict[str, Any]) -> List[ValidationError]:
        """Validate data against schema."""
        errors = []
        schema = self.SCHEMAS.get(contract_type)
        
        if not schema:
            errors.append(ValidationError("schema", f"Unknown contract type: {contract_type}"))
            return errors
        
        # Check required fields
        for field_name in schema.required_fields:
            if field_name not in data or data[field_name] is None:
                errors.append(ValidationError(field_name, f"Required field missing: {field_name}"))
        
        # Check field types
        for field_name, expected_type in schema.field_types.items():
            if field_name in data and data[field_name] is not None:
                if not isinstance(data[field_name], expected_type):
                    errors.append(ValidationError(
                        field_name,
                        f"Invalid type for {field_name}: expected {expected_type}, got {type(data[field_name])}"
                    ))
        
        return errors


class VersionValidator:
    """Validates version compatibility."""
    
    @staticmethod
    def is_compatible(version: str, required: str) -> bool:
        """Check if version is compatible with requirement."""
        try:
            # Simple semver check
            v_parts = [int(x) for x in version.split(".")]
            r_parts = [int(x) for x in required.replace(">=", "").replace(">", "").replace("=", "").split(".")]
            
            # Pad with zeros
            while len(v_parts) < len(r_parts):
                v_parts.append(0)
            while len(r_parts) < len(v_parts):
                r_parts.append(0)
            
            # Check >= comparison
            for v, r in zip(v_parts, r_parts):
                if v > r:
                    return True
                if v < r:
                    return False
            
            return True
        except:
            return True  # Default to compatible on parse error
    
    def validate_version(self, version: str, contract_id: str) -> List[ValidationError]:
        """Validate version format."""
        errors = []
        
        # Check format (simple semver)
        parts = version.split(".")
        if len(parts) < 2:
            errors.append(ValidationError("version", f"Invalid version format: {version}"))
        
        try:
            for part in parts:
                int(part)
        except ValueError:
            errors.append(ValidationError("version", f"Version parts must be integers: {version}"))
        
        return errors


class CompatibilityValidator:
    """Validates compatibility between contracts."""
    
    def validate_capability_provider_compatibility(
        self,
        capability_skills: List[str],
        provider_skills: List[str]
    ) -> List[ValidationError]:
        """Validate that provider supports all required capability skills."""
        errors = []
        
        missing_skills = set(capability_skills) - set(provider_skills)
        if missing_skills:
            errors.append(ValidationError(
                "skills",
                f"Provider missing required skills: {missing_skills}"
            ))
        
        return errors


class ContractValidator:
    """Main contract validator."""
    
    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.version_validator = VersionValidator()
        self.compatibility_validator = CompatibilityValidator()
    
    def validate_mission(self, mission: Any) -> ValidationResult:
        """Validate mission contract."""
        data = {
            "id": getattr(mission, "id", ""),
            "name": getattr(mission, "name", ""),
            "capability": getattr(mission, "capability", ""),
            "description": getattr(mission, "description", ""),
            "parameters": getattr(mission, "parameters", {}),
        }
        
        errors = self.schema_validator.validate(ContractType.MISSION, data)
        
        # Validate capability exists
        if not data["capability"]:
            errors.append(ValidationError("capability", "Capability is required"))
        
        return ValidationResult(
            contract_type=ContractType.MISSION,
            contract_id=data["id"],
            status=ValidationStatus.INVALID if any(e.severity == "error" for e in errors) else ValidationStatus.VALID,
            errors=errors
        )
    
    def validate_capability(self, capability: Any) -> ValidationResult:
        """Validate capability contract."""
        data = {
            "name": getattr(capability, "name", ""),
            "description": getattr(capability, "description", ""),
            "skills": getattr(capability, "skills", []),
            "version": getattr(capability, "version", "1.0.0"),
        }
        
        errors = self.schema_validator.validate(ContractType.CAPABILITY, data)
        
        # Validate skills
        if not data["skills"]:
            errors.append(ValidationError("skills", "At least one skill is required"))
        
        return ValidationResult(
            contract_type=ContractType.CAPABILITY,
            contract_id=data["name"],
            status=ValidationStatus.INVALID if any(e.severity == "error" for e in errors) else ValidationStatus.VALID,
            errors=errors
        )
    
    def validate_provider(self, provider: Any) -> ValidationResult:
        """Validate provider contract."""
        data = {
            "name": getattr(provider, "name", ""),
            "version": getattr(provider, "version", "1.0.0"),
        }
        
        errors = self.schema_validator.validate(ContractType.PROVIDER, data)
        
        return ValidationResult(
            contract_type=ContractType.PROVIDER,
            contract_id=data["name"],
            status=ValidationStatus.INVALID if any(e.severity == "error" for e in errors) else ValidationStatus.VALID,
            errors=errors
        )


class ContractRegistry:
    """Registry for contracts."""
    
    def __init__(self):
        self._contracts: Dict[ContractType, Dict[str, ValidationResult]] = {}
    
    def register(self, result: ValidationResult) -> None:
        """Register a validated contract."""
        if result.contract_type not in self._contracts:
            self._contracts[result.contract_type] = {}
        self._contracts[result.contract_type][result.contract_id] = result
    
    def get(self, contract_type: ContractType, contract_id: str) -> Optional[ValidationResult]:
        """Get a registered contract."""
        return self._contracts.get(contract_type, {}).get(contract_id)
    
    def list_all(self, contract_type: ContractType) -> List[ValidationResult]:
        """List all contracts of a type."""
        return list(self._contracts.get(contract_type, {}).values())
    
    def is_valid(self, contract_type: ContractType, contract_id: str) -> bool:
        """Check if contract is valid."""
        contract = self.get(contract_type, contract_id)
        return contract is not None and contract.is_valid


class ContractLoader:
    """Loads contracts from various sources."""
    
    def load_from_object(self, obj: Any) -> Dict[str, Any]:
        """Load contract from object."""
        return {
            "id": getattr(obj, "id", getattr(obj, "name", "")),
            "name": getattr(obj, "name", ""),
            "type": getattr(obj, "type", ""),
            "version": getattr(obj, "version", "1.0.0"),
        }


class ContractEngine:
    """
    Universal Contract Engine.
    Validates all contracts before execution.
    """
    
    def __init__(self):
        self.validator = ContractValidator()
        self.registry = ContractRegistry()
    
    def validate(self, contract_type: ContractType, obj: Any) -> ValidationResult:
        """Validate a contract."""
        if contract_type == ContractType.MISSION:
            result = self.validator.validate_mission(obj)
        elif contract_type == ContractType.CAPABILITY:
            result = self.validator.validate_capability(obj)
        elif contract_type == ContractType.PROVIDER:
            result = self.validator.validate_provider(obj)
        else:
            result = ValidationResult(
                contract_type=contract_type,
                contract_id=getattr(obj, "name", getattr(obj, "id", "")),
                status=ValidationStatus.INVALID,
                errors=[ValidationError("type", f"Unknown contract type: {contract_type}")]
            )
        
        # Register if valid
        if result.is_valid:
            self.registry.register(result)
        
        return result
    
    def validate_all(self, capabilities: List[Any], providers: List[Any]) -> Dict[str, Any]:
        """Validate all contracts."""
        results = {
            "capabilities": [],
            "providers": [],
            "errors": [],
            "warnings": []
        }
        
        for capability in capabilities:
            result = self.validate(ContractType.CAPABILITY, capability)
            results["capabilities"].append(result.to_dict())
            if not result.is_valid:
                results["errors"].extend([e.message for e in result.errors])
        
        for provider in providers:
            result = self.validate(ContractType.PROVIDER, provider)
            results["providers"].append(result.to_dict())
            if not result.is_valid:
                results["errors"].extend([e.message for e in result.errors])
        
        return results
