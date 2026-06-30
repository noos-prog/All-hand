# Decision Policies

> **Rules for making decisions without randomness.**

---

## Purpose

Decision Policies define how the Decision Engine makes choices. They ensure consistent, explainable, and optimal decisions.

---

## Policy Categories

```yaml
PolicyCategories:
  TOOL_SELECTION:
    - PriorityBasedSelection
    - CostBasedSelection
    - QualityBasedSelection
    - SpeedBasedSelection
    - ReliabilityBasedSelection
    
  RETRY_DECISIONS:
    - RetryPolicy
    - CircuitBreakerPolicy
    - FallbackPolicy
    
  QUALITY_POLICIES:
    - MinimumQualityThreshold
    - VerificationRequired
    
  ESCALATION_POLICIES:
    - EscalationTrigger
    - HumanInterventionRequired
```

---

## Policy Examples

### Policy 1: Priority-Based Selection

```yaml
Policy: PriorityBasedSelection

Trigger: "When priority is set in context"

Rules:
  if context.priority == "speed":
    weights:
      latency: 0.50  # Much higher
      quality: 0.20
      cost: 0.15
      
  if context.priority == "quality":
    weights:
      quality: 0.45  # Much higher
      reliability: 0.25
      latency: 0.10
      
  if context.priority == "cost":
    weights:
      cost: 0.50  # Much higher
      latency: 0.20
      quality: 0.15
      
  if context.priority == "balanced":
    weights:
      quality: 0.30
      cost: 0.25
      latency: 0.25
      reliability: 0.20
```

### Policy 2: Quality Over Speed

```yaml
Policy: QualityOverSpeed

Trigger: "When quality constraint is critical"

Condition: context.constraints.quality == "critical"

Action:
  - Increase quality weight to 0.50
  - Increase reliability weight to 0.25
  - Decrease latency weight to 0.05
  - Require minimum quality score of 0.85
  
Result: "Select best quality tool, even if slower"
```

### Policy 3: Speed Over Quality

```yaml
Policy: SpeedOverQuality

Trigger: "When speed constraint is critical"

Condition: context.constraints.speed == "critical"

Action:
  - Increase latency weight to 0.50
  - Decrease quality weight to 0.15
  - Require maximum latency of 30 seconds
  
Result: "Select fastest tool, even if lower quality"
```

### Policy 4: Failed Tool Policy

```yaml
Policy: FailedToolPolicy

Trigger: "When a tool has failed"

Rules:
  # If tool failed twice, don't use for remaining goal tasks
  if tool.failure_count >= 2 AND tool.failure_context == goal.id:
    action: "exclude_from_goal"
    reason: "Failed twice in this goal"
    
  # If tool failed recently, reduce confidence
  if tool.last_failure.within(1, "hour"):
    action: "reduce_score"
    factor: 0.80
    reason: "Recent failure"
    
  # If tool has declining success rate
  if tool.success_rate_trend.declining:
    action: "add_verification"
    reason: "Declining reliability"
```

### Policy 5: Quality Degradation Policy

```yaml
Policy: QualityDegradationPolicy

Trigger: "When tool quality decreases"

Rules:
  # Track rolling quality score
  baseline = tool.quality_score.last_week_average
  current = tool.quality_score.current
  
  if current < baseline * 0.90:
    action: "lower_ranking"
    factor: 0.85
    reason: "10%+ quality drop detected"
    
  if current < baseline * 0.75:
    action: "flag_for_review"
    reason: "Significant quality degradation"
    
  if current < baseline * 0.50:
    action: "circuit_breaker"
    reason: "Critical quality failure"
```

---

## Selection Decision Policies

### When Choosing Tools

```yaml
ToolSelectionPolicies:

  Rule 1: "Best fit for capability"
    → Select tool with highest capability fit score
    
  Rule 2: "Always have alternatives"
    → Provide top 3 options ranked
    → Second option if first fails
    → Third option if second fails
    
  Rule 3: "Consider context"
    → Adjust weights based on context
    → Production → higher reliability weight
    → Development → higher speed weight
    
  Rule 4: "Consider history"
    → If tool succeeded in similar task, boost score
    → If tool failed in similar task, reduce score
    
  Rule 5: "Consider cost"
    → If budget is limited, weight cost higher
    → If budget is unlimited, weight quality higher
    
  Rule 6: "No single points of failure"
    → Never select tool that is the ONLY option
    → Must have at least 2 viable alternatives
```

---

## Retry Decision Policies

```yaml
RetryPolicies:

  Rule 1: "Retry on transient failures"
    conditions:
      - error_type in [timeout, rate_limit, temporary_error]
      - retry_count < max_retries
    action: retry_same_tool
    
  Rule 2: "Switch on persistent failures"
    conditions:
      - error_type in [error, crash]
      - retry_count >= 2
    action: try_alternative_tool
    
  Rule 3: "Never retry on auth failures"
    conditions:
      - error_type in [auth_failure, permission_denied]
    action: do_not_retry
    reason: "Credentials or permissions issue"
    
  Rule 4: "Retry with backoff"
    delay = base_delay * (2 ^ retry_count)
    max_delay = 30 seconds
```

---

## Escalation Policies

```yaml
EscalationPolicies:

  Escalate when:
    - All tools have failed
    - Tool failures > 5 for single task
    - Error is security-related
    - Budget exceeded by 50%
    - Deadline missed
    
  Escalation includes:
    - What was attempted
    - All error messages
    - Available options
    - Recommendations
    
  Human can decide:
    - Retry with human guidance
    - Abort goal
    - Modify goal parameters
    - Handle manually
```

---

## Decision Flow with Policies

```
Decision Request
        ↓
Load Applicable Policies
        ↓
For each Policy:
  Check Trigger
        ↓
  Match?
  → YES → Apply Policy Rules
        ↓
  NO → Continue
        ↓
Merge All Policy Effects
        ↓
Calculate Final Scores
        ↓
Select Best Option
        ↓
Generate Reasoning
        ↓
Return Decision
```

---

## Policy Application Example

```yaml
Context:
  priority: "quality"
  environment: "production"
  budget: "medium"
  
  history:
    openhands_succeeded: true
    aider_failed: true
    
Policies Applied:
  1. PriorityBasedSelection
     → quality weight: 0.45
     
  2. ProductionEnvironmentPolicy
     → reliability weight: 0.35
     
  3. HistoryBasedAdjustment
     → openhands: +0.10
     → aider: -0.15
     
Final Weights:
  quality: 0.45
  reliability: 0.35
  context_fit: 0.10
  cost: 0.05
  latency: 0.05
  
Decision:
  Selected: "openhands"
  Reason: "Highest adjusted score after policies"
```

---

## Policy Management

```yaml
PolicyManagement:
  # Policy storage
  policies:
    - name: "PriorityBasedSelection"
      version: "1.0"
      status: "active"
      
    - name: "QualityOverSpeed"
      version: "1.0"
      status: "active"
      
  # Policy updates
  update_triggers:
    - benchmark_updates
    - user_feedback
    - performance_analysis
    
  # Policy versioning
  - Track policy changes
  - Can rollback if needed
  - A/B test new policies
```

---

## Related Documents

- [Capability-Selection-Algorithm.md](./02-Capability-Selection-Algorithm.md)
- [Brain-Rules.md](./03-Brain-Rules.md)
