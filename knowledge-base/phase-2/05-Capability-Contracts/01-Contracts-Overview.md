# Capability Contracts Overview

> **Every Capability has fixed contracts.**

---

## Contract Types

```
┌─────────────────────────────────────────────────────────────┐
│                   Capability Contract                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Contract                                             │
│  ├── Schema                                                 │
│  ├── Validation Rules                                       │
│  └── Required Fields                                        │
│                                                             │
│  Output Contract                                           │
│  ├── Schema                                                 │
│  ├── Required Fields                                        │
│  └── Artifact Types                                         │
│                                                             │
│  Error Contract                                             │
│  ├── Error Types                                            │
│  ├── Error Schema                                           │
│  └── Recovery Actions                                       │
│                                                             │
│  Timeout Contract                                           │
│  ├── Default Timeout                                        │
│  ├── Max Timeout                                            │
│  └── Timeout Actions                                        │
│                                                             │
│  Version Contract                                           │
│  ├── Version                                                │
│  ├── Compatibility                                          │
│  └── Deprecation Policy                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Input Contract

```yaml
InputContract:
  capability_id: string
  
  # Schema
  schema:
    type: "object"
    properties: {...}
    required: [...]
    additionalProperties: boolean
    
  # Validation Rules
  validation:
    - field: "..."
      rules:
        - type: "required"
        - type: "type"
          expected: "string"
        - type: "min_length"
          value: 10
        - type: "max_length"
          value: 10000
        - type: "pattern"
          regex: "..."
        - type: "enum"
          values: [...]
          
  # Custom Validators
  custom_validators:
    - name: "validate_dependencies"
      description: "Check that referenced files exist"
      
  # Default Values
  defaults:
    - field: "output_format"
      value: "files"
    - field: "include_tests"
      value: true
      
  # Examples
  examples:
    - name: "simple_generation"
      inputs:
        requirements: "Create a login endpoint"
        language: "python"
    - name: "complex_generation"
      inputs:
        requirements: "..."
        language: "python"
        framework: "fastapi"
        context:
          existing_files: [...]
```

---

## Output Contract

```yaml
OutputContract:
  capability_id: string
  
  # Schema
  schema:
    type: "object"
    properties:
      success:
        type: "boolean"
      data:
        type: "object"
      artifacts:
        type: "array"
      metadata:
        type: "object"
        
  # Required Fields
  required_fields:
    - success
    - artifacts
        
  # Artifact Types
  artifact_types:
    - type: "source_code"
      extensions: [".py", ".js", ".ts", ".go"]
      required: true
    - type: "test_code"
      extensions: ["_test.py", ".test.js"]
      required: false
    - type: "documentation"
      extensions: [".md", ".txt"]
      required: false
      
  # Output Examples
  examples:
    success_example:
      success: true
      artifacts:
        - type: "source_code"
          path: "src/auth.py"
          content: "..."
      metadata:
        token_usage: 1500
        cost: 0.03
        
    failure_example:
      success: false
      error:
        code: "VALIDATION_ERROR"
        message: "Invalid requirements format"
```

---

## Error Contract

```yaml
ErrorContract:
  capability_id: string
  
  # Error Types
  error_types:
    VALIDATION_ERROR:
      description: "Input validation failed"
      recoverable: true
      action: "retry_after_fix"
      
    TIMEOUT_ERROR:
      description: "Execution timed out"
      recoverable: true
      action: "retry_or_fallback"
      
    AUTH_ERROR:
      description: "Authentication failed"
      recoverable: false
      action: "report"
      
    PERMISSION_ERROR:
      description: "Permission denied"
      recoverable: false
      action: "report"
      
    RATE_LIMIT_ERROR:
      description: "Rate limit exceeded"
      recoverable: true
      action: "retry_with_backoff"
      
    PROVIDER_ERROR:
      description: "Provider internal error"
      recoverable: true
      action: "fallback"
      
    SYSTEM_ERROR:
      description: "System error"
      recoverable: true
      action: "retry"
      
  # Error Schema
  error_schema:
    type: "object"
    properties:
      code:
        type: "string"
      message:
        type: "string"
      details:
        type: "object"
      recoverable:
        type: "boolean"
      action:
        type: "string"
```

---

## Timeout Contract

```yaml
TimeoutContract:
  capability_id: string
  
  # Default timeout by complexity
  timeouts:
    simple:
      default: "1 minute"
      max: "2 minutes"
    medium:
      default: "5 minutes"
      max: "10 minutes"
    complex:
      default: "10 minutes"
      max: "30 minutes"
    critical:
      default: "30 seconds"
      max: "1 minute"
      
  # Timeout Actions
  timeout_actions:
    primary:
      action: "cancel_execution"
      notify: true
      
    fallback:
      action: "try_alternative_provider"
      notify: true
      
  # Extended Timeout
  extended_timeout:
    requires_approval: true
    max_extension: "2x"
    approver_role: "admin"
```

---

## Version Contract

```yaml
VersionContract:
  capability_id: string
  
  # Versioning
  current_version: "1.0.0"
  versions:
    - version: "1.0.0"
      status: "stable"
      released: "2024-01-01"
      changes: "Initial version"
      
    - version: "1.1.0"
      status: "planned"
      planned_release: "2024-03-01"
      changes:
        - "Added new parameters"
        - "Improved verification"
        
  # Compatibility
  compatibility:
    breaking_changes: false
    migration_guide: "..."
    deprecated_features: []
    
  # Deprecation
  deprecation:
    sunset_date: null
    replacement_capability: null
    migration_path: "..."
```

---

## Contract Example: Generate Code

```yaml
CapabilityContract: cap_generate_code

# Input Contract
input:
  schema:
    type: "object"
    properties:
      requirements:
        type: "string"
        minLength: 10
        maxLength: 10000
      language:
        type: "string"
        enum: ["python", "javascript", "typescript", "go", "rust", "java"]
      framework:
        type: "string"
      context:
        type: "object"
    required: ["requirements", "language"]
    
  validation:
    - field: "requirements"
      rules:
        - type: "min_length"
          value: 10
          message: "Requirements too short"
        - type: "max_length"
          value: 10000
          message: "Requirements too long"
          
  defaults:
    - field: "include_tests"
      value: true

# Output Contract
output:
  schema:
    type: "object"
    properties:
      success:
        type: "boolean"
      files:
        type: "array"
      metadata:
        type: "object"
    required: ["success"]
    
  artifact_types:
    source_code:
      required: true
      extensions: [".py", ".js", ".ts"]
    test_code:
      required: false
      extensions: ["_test.py", ".test.js"]

# Error Contract
error:
  VALIDATION_ERROR:
    action: "retry_after_fix"
  TIMEOUT_ERROR:
    action: "fallback"
  PROVIDER_ERROR:
    action: "fallback"

# Timeout Contract
timeout:
  default: "5 minutes"
  max: "10 minutes"
  simple: "2 minutes"
  complex: "10 minutes"
```

---

## Contract Validation

```python
def validate_contract(
    capability: Capability,
    contract_type: str
) -> ValidationResult:
    """
    Validate that a capability follows contract rules.
    """
    
    errors = []
    warnings = []
    
    # 1. Check required fields
    if contract_type == "input":
        if not capability.inputs.schema:
            errors.append("Missing input schema")
            
    elif contract_type == "output":
        if not capability.outputs.schema:
            errors.append("Missing output schema")
            
    # 2. Check validation rules
    if not capability.inputs.validation:
        warnings.append("No validation rules defined")
        
    # 3. Check examples
    if not capability.inputs.examples:
        warnings.append("No input examples provided")
        
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

---

## Related Documents

- [Input-Contract.md](./02-Input-Contract.md)
- [Output-Contract.md](./03-Output-Contract.md)
- [Versioning.md](./04-Versioning.md)
