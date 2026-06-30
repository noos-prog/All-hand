# Capability Policies Overview

> **Rules that govern how each capability operates.**

---

## Policy Categories

```yaml
Policies:
  # ===== EXECUTION POLICIES =====
  execution:
    - timeout_policy
    - retry_policy
    - resource_policy
    - concurrency_policy
    
  # ===== VERIFICATION POLICIES =====
  verification:
    - required_verifications
    - quality_thresholds
    - acceptance_criteria
    
  # ===== SELECTION POLICIES =====
  selection:
    - provider_preferences
    - cost_limits
    - priority_rules
    
  # ===== SECURITY POLICIES =====
  security:
    - permission_requirements
    - data_handling
    - audit_requirements
```

---

## Execution Policies

### Timeout Policy

```yaml
TimeoutPolicy:
  # Default timeouts by category
  
  coding:
    generate_code: "5 minutes"
    edit_code: "2 minutes"
    refactor_code: "3 minutes"
    fix_bugs: "5 minutes"
    
  testing:
    run_tests: "10 minutes"
    generate_tests: "3 minutes"
    integration_tests: "15 minutes"
    
  deployment:
    deploy: "15 minutes"
    build: "10 minutes"
    health_check: "2 minutes"
    
  analysis:
    analyze_architecture: "10 minutes"
    analyze_performance: "5 minutes"
    review_code: "5 minutes"
    
  # Override rules
  overrides:
    - condition: "complexity == 'high'"
      multiplier: 2.0
      
    - condition: "priority == 'critical'"
      multiplier: 0.5
```

### Retry Policy

```yaml
RetryPolicy:
  # Default retry rules
  
  defaults:
    max_retries: 2
    backoff_strategy: "exponential"
    base_delay: "1 second"
    max_delay: "30 seconds"
    
  # By error type
  error_handling:
    timeout:
      max_retries: 2
      action: "retry_same_provider"
      
    rate_limit:
      max_retries: 3
      action: "retry_with_backoff"
      backoff: "exponential"
      
    temporary_error:
      max_retries: 2
      action: "retry_same_provider"
      
    auth_failure:
      max_retries: 0
      action: "switch_provider"
      
    permission_denied:
      max_retries: 0
      action: "fail_and_report"
      
    quota_exceeded:
      max_retries: 0
      action: "fail_and_report"
```

---

## Verification Policies

### Required Verifications

```yaml
VerificationPolicies:
  # By capability
  
  cap_generate_code:
    required:
      - syntax_check
      - lint_check
      - test_check
    optional:
      - security_scan
      - performance_check
      
  cap_deploy:
    required:
      - security_scan
      - health_check
      - rollback_test
    optional:
      - integration_check
      - load_test
      
  cap_fix_bugs:
    required:
      - syntax_check
      - test_check
      - regression_check
    optional:
      - security_scan
      
  cap_review_code:
    required:
      - style_check
      - best_practice_check
    optional:
      - security_review
      - performance_review
```

### Quality Thresholds

```yaml
QualityThresholds:
  # Minimum quality scores by capability
  
  cap_generate_code:
    syntax_valid: 1.0       # Must compile
    lint_passed: 0.95       # 95% lint rules passed
    test_coverage: 0.80     # 80% coverage
    overall: 0.85           # 85% overall
    
  cap_deploy:
    security_score: 1.0      # No vulnerabilities
    health_check: 1.0       # Must pass
    rollback_ready: 1.0      # Must be rollback-able
    overall: 1.0             # 100% required
    
  cap_review_code:
    issues_identified: 5     # Minimum issues found
    accuracy: 0.90          # 90% accurate
    overall: 0.85
```

---

## Selection Policies

### Provider Preferences

```yaml
ProviderPreferences:
  # When multiple providers available
  
  defaults:
    prefer_reliable: true
    prefer_proven: true
    require_healthy: true
    
  # By environment
  by_environment:
    development:
      prefer_cost_effective: true
      allow_experimental: true
      
    staging:
      prefer_reliable: true
      prefer_quality: true
      allow_experimental: false
      
    production:
      require_proven: true
      require_reliable: true
      require_healthy: true
```

### Cost Limits

```yaml
CostPolicies:
  # Cost limits by capability
  
  cap_generate_code:
    max_cost_per_execution: 1.00
    max_cost_per_hour: 10.00
    budget_priority: "medium"
    
  cap_deploy:
    max_cost_per_execution: 10.00
    max_cost_per_hour: 50.00
    budget_priority: "high"
    
  # Override rules
  overrides:
    - condition: "priority == 'critical'"
      max_cost_multiplier: 2.0
      
    - condition: "budget == 'unlimited'"
      max_cost: null  # No limit
```

---

## Security Policies

### Permission Requirements

```yaml
PermissionRequirements:
  # Required permissions by capability
  
  cap_deploy:
    required:
      - "deploy:production"
      - "infra:configure"
    audit_required: true
    
  cap_manage_secrets:
    required:
      - "secrets:read"
      - "secrets:write"
    audit_required: true
    require_approval: true
    
  cap_git_merge:
    required:
      - "git:merge"
      - "git:approve"
    audit_required: true
```

### Data Handling

```yaml
DataHandlingPolicies:
  # Data classification by capability output
  
  cap_generate_code:
    output_classification: "internal"
    can_contain_secrets: false
    
  cap_deploy:
    output_classification: "restricted"
    can_contain_secrets: true
    encryption_required: true
    
  cap_analyze_logs:
    output_classification: "confidential"
    can_contain_secrets: true
    redaction_required: true
```

---

## Example: Generate Code Policy Set

```yaml
PolicySet: cap_generate_code

# Execution
execution:
  timeout:
    default: "5 minutes"
    max: "10 minutes"
    
  retry:
    max_retries: 2
    on_error_types: [timeout, rate_limit]
    
  resources:
    max_memory_mb: 2048
    max_cpu_cores: 2
    
# Verification
verification:
  required:
    - name: "syntax"
      tool: "compiler"
      must_pass: true
      
    - name: "lint"
      tool: "linter"
      threshold: 0.95
      
    - name: "tests"
      tool: "test_runner"
      threshold: 0.80
      
  optional:
    - name: "security"
      tool: "security_scanner"
      
    - name: "performance"
      tool: "profiler"
      
# Selection
selection:
  prefer_providers:
    - provider_openhands
    - provider_aider
    - provider_claude
    
  exclude_providers:
    - provider_experimental  # Unless no other option
    
  cost_limit:
    max: 0.50
    warn_at: 0.25
    
# Quality
quality:
  min_score: 0.85
  min_test_coverage: 0.80
  require_documentation: true
```

---

## Related Documents

- [Constraints.md](./02-Constraints.md)
- [Verification-Rules.md](./03-Verification-Rules.md)
