# Universal Result Object

> **Every Tool, no matter what, returns in this format.**

---

## Purpose

The Universal Result Object provides a standardized output format for all tools, ensuring consistent handling regardless of the tool used.

---

## Result Object Schema

```yaml
Result:
  # ========== Identification ==========
  id: string                    # Unique result ID
  task_id: string             # Associated task ID
  version: string             # Schema version
  
  # ========== Execution Info ==========
  execution:
    tool: string              # Tool that executed
    tool_version: string      # Tool version
    adapter: string           # Adapter used
    started_at: datetime
    completed_at: datetime
    duration: duration        # Total execution time
    
  # ========== Status ==========
  status: enum                # See status values
  status_reason: string       # Why this status
  
  # ========== Primary Output ==========
  output:
    # Success output
    artifacts: list[Artifact]  # Files, configs, etc.
    data: object              # Structured data
    message: string           # Human-readable message
    
  # ========== Secondary Output ==========
  logs:
    - level: enum             # debug, info, warn, error
      timestamp: datetime
      message: string
      context: object         # Additional context
      
  # ========== Metrics ==========
  metrics:
    # Resource usage
    token_usage: integer
    api_calls: integer
    network_requests: integer
    
    # Performance
    execution_time: duration
    waiting_time: duration
    total_time: duration
    
    # Cost
    cost: decimal
    cost_breakdown:
      api_cost: decimal
      compute_cost: decimal
      storage_cost: decimal
      
    # Quality
    confidence: 0.0-1.0      # Confidence in result
    quality_score: 0.0-1.0    # Quality assessment
    
  # ========== Errors ==========
  errors:
    - code: string            # Error code
      message: string          # Error message
      severity: enum           # warning, error, critical
      recoverable: boolean     # Can be recovered?
      context: object          # Error context
      
  # ========== Warnings ==========
  warnings:
    - code: string
      message: string
      impact: string          # Impact description
      
  # ========== Evidence ==========
  evidence:
    # Proof of execution
    steps_executed: list       # Steps that ran
    validations_passed: list   # Validations that passed
    tests_passed: integer     # Number of tests passed
    tests_total: integer      # Total tests run
    
  # ========== Context ==========
  context:
    environment: string        # Execution environment
    region: string            # Geographic region
    execution_mode: enum       # production, test, debug
    metadata: dict            # Additional metadata
    
  # ========== For Learning ==========
  learning:
    success_indicators: list   # What worked well
    failure_indicators: list   # What didn't work
    improvement_suggestions: list
```

---

## Status Values

```yaml
Status:
  # Success statuses
  SUCCESS: "Completed successfully"
  PARTIAL_SUCCESS: "Completed with warnings"
  
  # Failure statuses
  FAILED: "Execution failed"
  TIMEOUT: "Execution timed out"
  RATE_LIMITED: "Rate limit exceeded"
  AUTH_FAILED: "Authentication failed"
  PERMISSION_DENIED: "Permission denied"
  QUOTA_EXCEEDED: "Quota exceeded"
  
  # System statuses
  CANCELLED: "Cancelled by user"
  ABORTED: "Aborted by system"
  UNAVAILABLE: "Tool unavailable"
  
  # Validation statuses
  VALIDATION_FAILED: "Output validation failed"
  SECURITY_FAILED: "Security check failed"
```

---

## Artifact Schema

```yaml
Artifact:
  # File artifacts
  type: enum                  # file, directory, config, image, etc.
  
  # Identification
  name: string               # File/artifact name
  path: string              # Path if file
  url: string               # URL if remote
  
  # Content
  content: string            # Text content or reference
  encoding: string           # utf-8, base64, etc.
  size: integer             # Size in bytes
  hash: string              # Content hash (SHA256)
  
  # Metadata
  mime_type: string         # application/json, etc.
  language: string          # Programming language
  line_count: integer       # Lines of code if applicable
  
  # Relationships
  created_by: string        # Tool that created
  dependencies: list        # Other artifacts this depends on
```

---

## Result Example: Success

```yaml
Result:
  id: "result_150"
  task_id: "task_15"
  version: "1.0"
  
  execution:
    tool: "openhands"
    tool_version: "1.5.0"
    adapter: "universal-openhands-adapter"
    started_at: "2024-01-15T10:30:00Z"
    completed_at: "2024-01-15T10:35:00Z"
    duration: "5 minutes"
    
  status: "SUCCESS"
  status_reason: "Task completed successfully"
  
  output:
    artifacts:
      - name: "auth.py"
        type: "file"
        path: "src/auth.py"
        language: "python"
        line_count: 150
        
      - name: "auth_test.py"
        type: "file"
        path: "tests/auth_test.py"
        language: "python"
        line_count: 80
        
    data:
      endpoints_created: 5
      functions_generated: 10
    message: "Authentication module generated successfully"
    
  logs:
    - level: "info"
      timestamp: "2024-01-15T10:30:01Z"
      message: "Starting authentication generation"
      
    - level: "info"
      timestamp: "2024-01-15T10:30:05Z"
      message: "Generated login endpoint"
      
    - level: "info"
      timestamp: "2024-01-15T10:35:00Z"
      message: "Task completed"
      
  metrics:
    token_usage: 2500
    api_calls: 3
    execution_time: "4m 30s"
    waiting_time: "30s"
    total_time: "5m 0s"
    cost: 0.05
    confidence: 0.92
    quality_score: 0.95
    
  errors: []
  warnings:
    - code: "DEPRECATION_WARNING"
      message: "Using deprecated method"
      impact: "Minor, will work fine"
      
  evidence:
    steps_executed:
      - "Parse requirements"
      - "Generate code"
      - "Run linter"
      - "Run tests"
    validations_passed:
      - "syntax_check"
      - "lint_check"
      - "test_check"
    tests_passed: 12
    tests_total: 12
```

---

## Result Example: Failure

```yaml
Result:
  id: "result_151"
  task_id: "task_16"
  
  execution:
    tool: "openhands"
    started_at: "2024-01-15T10:40:00Z"
    completed_at: "2024-01-15T10:42:00Z"
    duration: "2 minutes"
    
  status: "FAILED"
  status_reason: "Compilation error in generated code"
  
  output:
    artifacts: []
    data: {}
    message: "Failed to compile: syntax error in auth.py"
    
  logs:
    - level: "error"
      timestamp: "2024-01-15T10:42:00Z"
      message: "Compilation failed"
      context:
        file: "src/auth.py"
        line: 42
        error: "SyntaxError: invalid syntax"
        
  metrics:
    token_usage: 1200
    execution_time: "2m 0s"
    cost: 0.02
    confidence: 0.10
    quality_score: 0.30
    
  errors:
    - code: "COMPILATION_ERROR"
      message: "SyntaxError: invalid syntax at line 42"
      severity: "error"
      recoverable: true
      context:
        file: "src/auth.py"
        line: 42
        column: 15
        
  warnings: []
  
  evidence:
    steps_executed:
      - "Parse requirements"
      - "Generate code"
    validations_passed:
      - "syntax_check"  # FAILED
    tests_passed: 0
    tests_total: 0
```

---

## Result Example: Partial Success

```yaml
Result:
  id: "result_152"
  task_id: "task_17"
  
  status: "PARTIAL_SUCCESS"
  status_reason: "Generated with warnings"
  
  output:
    artifacts:
      - name: "api.py"
        type: "file"
        path: "src/api.py"
    message: "API generated with warnings"
    
  warnings:
    - code: "PERFORMANCE_WARNING"
      message: "Response time may exceed 100ms"
      impact: "May need optimization"
      
    - code: "DEPRECATION"
      message: "Using deprecated library version"
      impact: "Upgrade recommended"
      
  metrics:
    quality_score: 0.78  # Lower due to warnings
```

---

## Tool → Result Mapping

```
Every tool returns a Result:

OpenHands → Result
Claude Code → Result  
Aider → Result
Cline → Result
Browser Use → Result
SWE-Agent → Result

All through Universal Tool Adapter
All return Universal Result Object
```

---

## Result Validation

```python
def validate_result(result: Result) -> ValidationResult:
    """Validate result matches schema."""
    
    required_fields = [
        'id', 'task_id', 'status',
        'execution', 'output', 'metrics'
    ]
    
    for field in required_fields:
        if field not in result:
            return ValidationResult(
                valid=False,
                errors=[f"Missing required field: {field}"]
            )
    
    # Validate status is enum value
    if result.status not in VALID_STATUSES:
        return ValidationResult(
            valid=False,
            errors=[f"Invalid status: {result.status}"]
        )
    
    return ValidationResult(valid=True)
```

---

## Related Documents

- [Universal-Task-Object.md](./01-Universal-Task-Object.md)
- [Verification-Engine.md](../02-Components/04-Verification-Engine.md)
