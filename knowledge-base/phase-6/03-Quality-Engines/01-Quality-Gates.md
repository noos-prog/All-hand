# Quality Gate Engine

> **No transition until quality gates pass.**

---

## Quality Gate Concept

```
┌─────────────────────────────────────────────────────────────┐
│                  Quality Gate Engine                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Quality Gate 1 ──► Quality Gate 2 ──► Quality Gate 3      │
│       │                  │                  │              │
│       ▼                  ▼                  ▼              │
│    PASS/FAIL          PASS/FAIL          PASS/FAIL        │
│       │                  │                  │              │
│       ▼                  ▼                  ▼              │
│    Continue          Continue            Continue         │
│       │                  │                  │              │
│       └──────────────────┴──────────────────┘              │
│                        │                                    │
│                        ▼                                    │
│                    PRODUCTION                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Gate Definitions

### Gate 1: Compilation

```yaml
QualityGate:
  id: "gate_compilation"
  name: "Compilation Gate"
  phase: "EXECUTION"
  order: 1
  
  checks:
    - check: "syntax_valid"
      description: "Code compiles without syntax errors"
      
    - check: "imports_valid"
      description: "All imports resolve"
      
    - check: "types_valid"
      description: "Type checking passes"
      
  thresholds:
    errors: 0
    warnings: "ignored"
    
  actions:
    on_fail: "BLOCK"
    retry_allowed: true
```

### Gate 2: Testing

```yaml
QualityGate:
  id: "gate_testing"
  name: "Testing Gate"
  phase: "EXECUTION"
  order: 2
  
  checks:
    - check: "unit_tests_pass"
      description: "All unit tests pass"
      
    - check: "integration_tests_pass"
      description: "All integration tests pass"
      
    - check: "test_coverage"
      description: "Code coverage meets threshold"
      
    - check: "no_breaking_tests"
      description: "Existing tests still pass"
      
  thresholds:
    tests_passed: 100%
    coverage: 80%
    critical_coverage: 90%
    
  actions:
    on_fail: "BLOCK"
    retry_allowed: true
```

### Gate 3: Security

```yaml
QualityGate:
  id: "gate_security"
  name: "Security Gate"
  phase: "VERIFICATION"
  order: 1
  
  checks:
    - check: "no_secrets"
      description: "No hardcoded secrets"
      
    - check: "no_sql_injection"
      description: "SQL injection vulnerabilities"
      
    - check: "no_xss"
      description: "XSS vulnerabilities"
      
    - check: "secure_dependencies"
      description: "No vulnerable dependencies"
      
    - check: "authentication_required"
      description: "Auth on protected endpoints"
      
  thresholds:
    critical_vulnerabilities: 0
    high_vulnerabilities: 0
    medium_vulnerabilities: 5
    
  actions:
    on_fail: "BLOCK"
    retry_allowed: false
```

### Gate 4: Performance

```yaml
QualityGate:
  id: "gate_performance"
  name: "Performance Gate"
  phase: "VERIFICATION"
  order: 2
  
  checks:
    - check: "response_time"
      description: "API response time under threshold"
      
    - check: "throughput"
      description: "System handles required load"
      
    - check: "memory_usage"
      description: "Memory usage within limits"
      
    - check: "cpu_usage"
      description: "CPU usage within limits"
      
  thresholds:
    response_time_p95: "< 200ms"
    throughput: "> 1000 req/s"
    memory_usage: "< 512MB"
    
  actions:
    on_fail: "WARN"
    retry_allowed: true
```

### Gate 5: Architecture

```yaml
QualityGate:
  id: "gate_architecture"
  name: "Architecture Gate"
  phase: "VERIFICATION"
  order: 3
  
  checks:
    - check: "follows_architecture"
      description: "Code follows defined architecture"
      
    - check: "no_layer_violation"
      description: "No layer violations"
      
    - check: "proper_encapsulation"
      description: "Encapsulation respected"
      
    - check: "dependency_direction"
      description: "Dependencies point correctly"
      
  thresholds:
    violations: 0
    warnings: 5
    
  actions:
    on_fail: "BLOCK"
    retry_allowed: true
```

---

## Gate Execution

```python
class QualityGateEngine:
    """
    Executes quality gates.
    """
    
    async def execute_gate(
        self,
        mission: Mission,
        gate: QualityGate
    ) -> GateResult:
        """
        Execute a quality gate.
        """
        
        results = []
        
        # Execute each check
        for check in gate.checks:
            result = await self.execute_check(check, mission)
            results.append(result)
            
        # Aggregate results
        aggregated = self.aggregate_results(results)
        
        # Determine pass/fail
        passed = self.evaluate_thresholds(aggregated, gate.thresholds)
        
        return GateResult(
            gate_id=gate.id,
            passed=passed,
            checks=results,
            aggregated=aggregated,
            violations=aggregated.violations if not passed else []
        )
        
    async def execute_all_gates(
        self,
        mission: Mission,
        phase: Phase
    ) -> list[GateResult]:
        """
        Execute all gates for a phase.
        """
        
        gates = self.get_gates_for_phase(phase)
        results = []
        
        for gate in gates:
            result = await self.execute_gate(mission, gate)
            results.append(result)
            
            # Block on fail if required
            if not result.passed:
                if gate.actions.on_fail == "BLOCK":
                    return results
                    
        return results
```

---

## Gate Results

```yaml
GateResult:
  gate_id: string
  passed: boolean
  
  checks:
    - name: string
      passed: boolean
      duration: duration
      details: string
      evidence: list[string]
      
  aggregated:
    errors: integer
    warnings: integer
    score: 0.0-1.0
    
  violations:
    - severity: enum  # CRITICAL, HIGH, MEDIUM, LOW
      description: string
      location: string
      fix: string
      
  timestamp: datetime
```

---

## Example: Gate Execution

```yaml
Gate: "Testing Gate"

Checks:
  1. Unit Tests: PASSED (200/200)
  2. Integration Tests: PASSED (50/50)
  3. Test Coverage: FAILED
     - Required: 80%
     - Actual: 72%
  4. Breaking Tests: PASSED (0 broken)

Result: FAILED

Violations:
  - severity: MEDIUM
    description: "Test coverage below threshold"
    location: "src/api/users.py"
    fix: "Add 5 more tests"

Action: BLOCK
Reason: "Must reach 80% coverage before proceeding"
```

---

## Gate Policies

```yaml
GatePolicies:
  on_block:
    - "Notify team"
    - "Log violation"
    - "Create issue"
    - "Track debt"
    
  on_warn:
    - "Log warning"
    - "Add to report"
    - "Allow continue"
    
  on_critical_fail:
    - "Block immediately"
    - "Alert immediately"
    - "Escalate"
```

---

## Continuous Verification

```yaml
ContinuousVerification:
  # Run checks continuously
  
  triggers:
    - "On code change"
    - "On PR"
    - "On merge"
    - "Scheduled"
    
  checks:
    - "Compile"
    - "Lint"
    - "Type check"
    - "Unit tests"
    - "Security scan"
    
  gates:
    - "Must pass before merge"
    - "Must pass before deploy"
    - "Must pass before release"
```

---

## Related Documents

- [Continuous-Verification.md](./02-Continuous-Verification.md)
- [Architecture-Compliance.md](./03-Architecture-Compliance.md)
