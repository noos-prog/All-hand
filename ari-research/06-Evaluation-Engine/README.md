# Evaluation Engine

> **Every result evaluated on 10+ dimensions.**

---

## Evaluation Dimensions

```yaml
EvaluationDimensions:
  correctness:
    description: "Is the output correct?"
    metrics:
      - "syntax_valid"
      - "compiles"
      - "runs"
      - "output_correct"
    weight: 0.20
    
  quality:
    description: "Quality of the output"
    metrics:
      - "code_quality"
      - "readability"
      - "maintainability"
    weight: 0.15
    
  performance:
    description: "Performance of the output"
    metrics:
      - "execution_time"
      - "memory_usage"
      - "cpu_usage"
    weight: 0.10
    
  security:
    description: "Security of the output"
    metrics:
      - "vulnerabilities"
      - "injections"
      - "auth_issues"
    weight: 0.15
    
  scalability:
    description: "Scalability potential"
    metrics:
      - "architecture"
      - "patterns"
      - "design"
    weight: 0.10
    
  maintainability:
    description: "Ease of maintenance"
    metrics:
      - "complexity"
      - "duplication"
      - "documentation"
    weight: 0.10
    
  testability:
    description: "Ease of testing"
    metrics:
      - "test_coverage"
      - "test_quality"
      - "mockability"
    weight: 0.05
    
  cost:
    description: "Cost efficiency"
    metrics:
      - "compute_cost"
      - "api_cost"
      - "infra_cost"
    weight: 0.05
    
  latency:
    description: "Response latency"
    metrics:
      - "time_to_first_token"
      - "time_to_completion"
      - "perceived_speed"
    weight: 0.05
    
  reliability:
    description: "Reliability of execution"
    metrics:
      - "success_rate"
      - "error_rate"
      - "timeout_rate"
    weight: 0.05
```

---

## Evaluation Pipeline

```
Benchmark Result
       │
       ▼
┌─────────────────┐
│ Pre-Processing  │
│ - Parse output  │
│ - Normalize     │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Static Judge   │
│ - Lint          │
│ - Type check    │
│ - Format        │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Execution Judge│
│ - Run tests     │
│ - Run security   │
│ - Run perf      │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Quality Judge  │
│ - Complexity    │
│ - Duplication   │
│ - Readability   │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Human Judge    │
│ - Code review    │
│ - UX review     │
│ - Architecture   │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│  Score Fusion   │
│ - Weighted avg   │
│ - Per-dimension │
│ - Final score    │
└─────────────────┘
       │
       ▼
Evaluation Result
```

---

## Judge Types

### 1. Static Analysis Judge

```yaml
StaticJudge:
  checks:
    - syntax_valid
    - imports_valid
    - types_valid
    - format_valid
    - lint_passes
    - security_scan
    
  tools:
    - eslint
    - ruff
    - mypy
    - semgrep
    - bandit
    
  score: 0.0-1.0
```

### 2. Execution Judge

```yaml
ExecutionJudge:
  checks:
    - runs_successfully
    - tests_pass
    - performance_ok
    - memory_ok
    
  tools:
    - pytest
    - k6
    - locust
    
  score: 0.0-1.0
```

### 3. Security Judge

```yaml
SecurityJudge:
  checks:
    - no_secrets
    - no_sql_injection
    - no_xss
    - no_csrf
    - secure_dependencies
    - secure_auth
    
  tools:
    - semgrep
    - bandit
    - safety
    - owasp
    
  score: 0.0-1.0
```

### 4. Quality Judge

```yaml
QualityJudge:
  checks:
    - complexity_score
    - duplication_score
    - maintainability_score
    - readability_score
    
  tools:
    - radon
    - pylint
    - sonarqube
    
  score: 0.0-1.0
```

### 5. Human Judge (Optional)

```yaml
HumanJudge:
  checks:
    - code_style
    - architecture
    - design_patterns
    - best_practices
    
  process:
    - Assign reviewers
    - Collect scores
    - Aggregate feedback
    
  score: 0.0-1.0
```

---

## Score Calculation

```python
def calculate_final_score(
    judges: list[JudgeResult],
    weights: dict[str, float]
) -> EvaluationResult:
    """
    Calculate final evaluation score.
    """
    
    # Calculate dimension scores
    dimension_scores = {}
    for judge in judges:
        for dimension in judge.dimensions:
            score = judge.scores[dimension]
            weight = weights[dimension]
            
            if dimension not in dimension_scores:
                dimension_scores[dimension] = []
            dimension_scores[dimension].append((score, weight))
            
    # Calculate weighted dimension scores
    final_dimensions = {}
    for dimension, scores_weights in dimension_scores.items():
        total_score = sum(s * w for s, w in scores_weights)
        total_weight = sum(w for _, w in scores_weights)
        final_dimensions[dimension] = total_score / total_weight
        
    # Calculate overall score
    overall = sum(
        score * weights[dimension]
        for dimension, score in final_dimensions.items()
    )
    
    return EvaluationResult(
        overall_score=overall,
        dimension_scores=final_dimensions,
        judges=judges
    )
```

---

## Evaluation Report

```yaml
EvaluationReport:
  benchmark_id: string
  provider_id: string
  timestamp: datetime
  
  overall_score: 0.0-1.0
  
  dimension_scores:
    correctness: 0.0-1.0
    quality: 0.0-1.0
    performance: 0.0-1.0
    security: 0.0-1.0
    scalability: 0.0-1.0
    maintainability: 0.0-1.0
    testability: 0.0-1.0
    cost: 0.0-1.0
    latency: 0.0-1.0
    reliability: 0.0-1.0
    
  judge_details:
    - name: "StaticJudge"
      score: 0.95
      checks:
        syntax_valid: PASS
        imports_valid: PASS
        lint_passes: PASS
        
    - name: "ExecutionJudge"
      score: 0.90
      checks:
        tests_pass: PASS
        performance_ok: PASS
        
  recommendations:
    - "Improve test coverage"
    - "Add documentation"
    - "Reduce complexity"
    
  evidence:
    logs: "..."
    screenshots: [...]
    diffs: [...]
```

---

## Related Documents

- [Judge-Engine.md](../08-Judge-Engine/README.md)
- [Evidence-Collector.md ../08-Judge-Engine/README.md)
