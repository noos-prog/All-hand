# Verification Engine

> **Any result is NOT considered correct until verified.**

---

## Purpose

The Verification Engine validates all tool outputs before they're accepted. It ensures quality and correctness.

---

## Core Concept

```
Code Generated
      ↓
┌─────────────────────────┐
│   Verification Engine   │
│                          │
│  - Compile              │
│  - Tests                │
│  - Lint                 │
│  - Security             │
│  - Architecture         │
│  - Manual Review        │
└─────────────────────────┘
      ↓
Accepted OR Rejected
```

---

## Verification Pipeline

```yaml
VerificationPipeline:
  stages:
    - name: "syntax"
      check: "Does it compile?"
      required: true
      
    - name: "lint"
      check: "Does it pass linting?"
      required: true
      
    - name: "tests"
      check: "Do tests pass?"
      required: true
      
    - name: "security"
      check: "Any vulnerabilities?"
      required: true
      
    - name: "architecture"
      check: "Follows architecture?"
      required: false
      
    - name: "performance"
      check: "Meets perf requirements?"
      required: false
      
    - name: "integration"
      check: "Works with rest of system?"
      required: false
      
    - name: "review"
      check: "Human review needed?"
      required: false
```

---

## Verification Request

```yaml
VerificationRequest:
  id: string
  task_id: string
  
  # What to verify
  artifact: Artifact    # Code, config, etc.
  artifact_type: enum   # code, config, deployment, etc.
  
  # Verification criteria
  verification_type: enum  # full, quick, critical
  criteria: list        # Specific checks needed
  
  # Context
  goal: Goal
  context: UnifiedContext
  
  # Constraints
  time_limit: duration  # Max verification time
  depth: enum          # Shallow, Medium, Deep
```

---

## Verification Result

```yaml
VerificationResult:
  id: string
  request_id: string
  
  # Overall status
  status: enum  # PASSED, FAILED, PARTIAL, PENDING
  
  # Stage results
  stages:
    - name: "syntax"
      status: "PASSED"
      details: "Compiles successfully"
      
    - name: "lint"
      status: "PASSED"
      details: "No linting errors"
      
    - name: "tests"
      status: "FAILED"
      details: "2 tests failed"
      errors:
        - "test_login_failed: AssertionError"
        - "test_logout_failed: TimeoutError"
        
    - name: "security"
      status: "PASSED"
      details: "No vulnerabilities found"
  
  # Summary
  passed_count: 6
  failed_count: 2
  skipped_count: 0
  
  # Recommendations
  recommendations: list
  must_fix: list        # Issues that must be fixed
  
  # Metrics
  verification_time: duration
  tools_used: list      # Verification tools invoked
```

---

## Verification Flow

```
1. Receive artifact
        ↓
2. Determine verification type
        ↓
3. Run syntax check
        ↓
   Pass? → Continue
   Fail? → Report failure
        ↓
4. Run lint check
        ↓
   Pass? → Continue
   Fail? → Report failure
        ↓
5. Run tests
        ↓
   Pass? → Continue
   Fail? → Report failure
        ↓
6. Run security scan
        ↓
   Pass? → Continue
   Fail? → Report failure
        ↓
... (more stages)
        ↓
7. Generate report
        ↓
8. Return VerificationResult
```

---

## Verification Types

| Type | Stages | Time | Use Case |
|------|--------|------|----------|
| `FULL` | All | 5-10 min | Production deployment |
| `QUICK` | Syntax, Lint | 30 sec | Development iteration |
| `CRITICAL` | Security, Tests | 2 min | Security-sensitive |
| `BASIC` | Syntax, Basic Tests | 1 min | CI/CD pipeline |

---

## Stage Specifications

### Syntax Check
```yaml
syntax:
  tool: "compiler"  # language-specific
  checks:
    - "Compilation"
    - "Type checking"
    - "Import resolution"
```

### Lint Check
```yaml
lint:
  tool: "linter"  # eslint, ruff, golangci-lint
  checks:
    - "Code style"
    - "Best practices"
    - "Potential bugs"
```

### Test Check
```yaml
tests:
  tool: "test_runner"  # pytest, jest, go test
  checks:
    - "Unit tests"
    - "Integration tests"
    - "Coverage"
```

### Security Check
```yaml
security:
  tool: "security_scanner"  # semgrep, bandit, gosec
  checks:
    - "Vulnerability scan"
    - "Secret detection"
    - "Dependency audit"
```

---

## Pass/Fail Criteria

```yaml
Criteria:
  syntax:
    PASS: "Compiles without errors"
    FAIL: "Compilation errors"
    
  lint:
    PASS: "No errors, < 10 warnings"
    FAIL: "> 10 warnings or any error"
    
  tests:
    PASS: "> 80% pass rate"
    FAIL: "< 80% pass rate"
    
  security:
    PASS: "No critical/high vulnerabilities"
    FAIL: "Any critical/high vulnerability"
```

---

## Handling Failures

```python
async def handle_verification_failure(
    result: VerificationResult
) -> Action:
    """
    Determine what to do when verification fails.
    """
    
    if result.must_fix:
        # Critical issues must be fixed
        return Action(
            type="RETURN_TO_TOOL",
            message="Fix must-fix issues",
            issues=result.must_fix
        )
    
    elif result.failed_count > result.passed_count:
        # More failures than passes
        return Action(
            type="RETRY",
            reason="Poor quality result"
        )
    
    else:
        # Minor issues, can proceed with warning
        return Action(
            type="ACCEPT_WITH_WARNING",
            warnings=result.recommendations
        )
```

---

## Verification Metrics

```yaml
VerificationMetrics:
  per_artifact:
    verification_time: duration
    stages_run: list
    issues_found: integer
    issues_fixed: integer
    
  per_tool:
    reliability: 0.0-1.0  # How often it catches issues
    false_positive_rate: 0.0-1.0
    
  overall:
    avg_verification_time: duration
    pass_rate: percentage
    avg_issues_per_artifact: number
```

---

## Example: Failed Verification

```yaml
VerificationRequest:
  task_id: "task_15"
  artifact_type: "code"
  verification_type: "FULL"
  
VerificationResult:
  status: "FAILED"
  
  stages:
    syntax: PASSED
    lint: PASSED
    tests: FAILED  ←
    security: PASSED
    architecture: PASSED
    performance: FAILED  ←
    
  must_fix:
    - "test_user_login failed: Expected 200, got 401"
    - "Response time exceeds 200ms SLA"
    
  recommendations:
    - "Add caching for user data"
    - "Consider using connection pooling"
    
  Action:
    type: "RETURN_TO_TOOL"
    message: "Fix test failures and performance issues"
```

---

## Related Documents

- [Recovery-Engine.md](./05-Recovery-Engine.md)
- [Learning-Engine.md](./06-Learning-Engine.md)
