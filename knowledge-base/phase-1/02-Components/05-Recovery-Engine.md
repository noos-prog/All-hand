# Recovery Engine

> **If a Tool fails, the Brain doesn't stop.**

---

## Purpose

The Recovery Engine handles failures and implements fallback strategies. The Brain never stops - it always has a plan B, C, D...

---

## Core Concept

```
Tool Fails
      ↓
Recovery Engine
      ↓
Retry?
      ↓
Failed again?
      ↓
Use Alternative Tool
      ↓
Failed?
      ↓
Use Another Alternative
      ↓
Success!
```

---

## Recovery Strategies

```yaml
RecoveryStrategies:
  # Strategy hierarchy (tried in order)
  
  1. RETRY:
     - Try same tool again
     - Max retries: 2
     - With exponential backoff
     
  2. ALTERNATIVE_TOOL:
     - Try next best tool
     - From Capability Selector
     
  3. SIMPLIFY_TASK:
     - Break task into smaller parts
     - Retry with simpler approach
     
  4. ESCALATE:
     - Notify human
     - Provide options
     
  5. ABORT:
     - Stop goal
     - Report failure
```

---

## Recovery Flow

```
1. Tool fails
        ↓
2. Log failure
        ↓
3. Check retry count
        ↓
   < 2 retries?
   → RETRY (same tool)
        ↓
   >= 2 retries?
   → Get alternatives
        ↓
4. Any alternatives left?
   → YES → Try next best
        ↓
   NO → Try simplify task
        ↓
5. Simplified worked?
   → YES → Continue
        ↓
   NO → Escalate
        ↓
6. Return recovery action
```

---

## Tool Failure Record

```yaml
ToolFailure:
  # Identity
  id: string
  timestamp: datetime
  
  # Failure details
  tool: string
  task_id: string
  capability: string
  
  # Failure info
  error_type: enum  # timeout, error, crash, api_failure
  error_message: string
  error_code: string
  
  # Recovery attempts
  retry_count: integer
  retry_history: list
    - retry_number: 1
      action: "retry"
      result: "failed"
    - retry_number: 2
      action: "retry"
      result: "failed"
      
  # Alternatives tried
  alternatives_tried: list
    - tool: "aider"
      result: "not_attempted"
    - tool: "claude-code"
      result: "not_attempted"
      
  # Resolution
  resolution: enum  # recovered, escalated, aborted
  final_action: string
```

---

## Retry Policy

```yaml
RetryPolicy:
  # When to retry
  
  retry_on:
    - timeout
    - temporary_error
    - rate_limit
    - connection_error
    
  do_not_retry_on:
    - auth_failure  # Credentials issue
    - permission_denied  # Access issue
    - quota_exceeded  # Payment needed
    - invalid_input  # Bad input
    
  # Retry parameters
  max_retries: 2
  base_delay: 1  # seconds
  max_delay: 30  # seconds
  exponential_base: 2
  
  # Delay calculation
  # delay = min(base_delay * (exponential_base ^ retry), max_delay)
  
  delays:
    retry_1: 1 second
    retry_2: 2 seconds
    retry_3: 4 seconds (if allowed)
```

---

## Alternative Tool Selection

```python
async def get_alternative_tool(
    failed_tool: Tool,
    task: Task,
    context: Context
) -> Optional[Tool]:
    """
    Get next best tool after failure.
    """
    
    # 1. Get full ranking from Capability Selector
    candidates = await selector.get_ranked_tools(
        capability=task.capability
    )
    
    # 2. Filter out failed tool
    candidates = [c for c in candidates if c.name != failed_tool.name]
    
    # 3. Filter out recently failed tools
    recent_failures = get_recent_failures(task.capability)
    candidates = [c for c in candidates if c.name not in recent_failures]
    
    # 4. Return best remaining
    if candidates:
        return candidates[0]
    
    return None
```

---

## Recovery Examples

### Example 1: Single Retry Success

```
Situation: OpenHands timed out on task "Generate API"

Recovery Flow:
1. Log failure (timeout, 1st attempt)
2. retry_count = 0 < 2
3. → RETRY OpenHands
4. Wait 1 second
5. Second attempt succeeds
6. Record: recovered after 1 retry
```

### Example 2: Tool Switch

```
Situation: OpenHands failed twice

Recovery Flow:
1. Log failure (error, 2nd attempt)
2. retry_count = 2 >= 2
3. → Get alternatives: [Aider, Claude Code]
4. Try Aider
5. Aider succeeds
6. Record: recovered with Aider
7. Update scores: OpenHands ↓, Aider ↑
```

### Example 3: Full Recovery Chain

```
Situation: Task fails all retries

Recovery Flow:
1. OpenHands → FAIL
2. OpenHands retry 1 → FAIL
3. OpenHands retry 2 → FAIL
4. Try Aider → FAIL
5. Try Claude Code → FAIL
6. Try simplify task
7. Simplified version works
8. Record: recovered with simplified approach
```

### Example 4: Escalation

```
Situation: All recovery attempts failed

Recovery Flow:
1. All tools failed
2. Simplify task failed
3. → ESCALATE
4. Notify human with:
   - What was attempted
   - All error messages
   - Available options
5. Human decides: retry, abort, or manual
```

---

## Failure Tracking

```yaml
FailureTracking:
  # Track tool reliability
  
  tool_stats:
    openhands:
      total_tasks: 150
      failures: 5
      success_rate: 96.7%
      avg_retries: 0.3
      
      failure_types:
        timeout: 2
        error: 2
        crash: 1
        
      last_failure: "2024-01-15T10:30:00Z"
      
    aider:
      total_tasks: 80
      failures: 3
      success_rate: 96.3%
      ...
```

---

## Circuit Breaker

```yaml
CircuitBreaker:
  # If a tool fails too much, pause using it
  
  openhands:
    failure_threshold: 5  # failures in window
    failure_window: 60  # minutes
    pause_duration: 15  # minutes
    
    state: "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    # State transitions
    CLOSED → OPEN: failure_threshold reached
    OPEN → HALF_OPEN: pause_duration passed
    HALF_OPEN → CLOSED: success
    HALF_OPEN → OPEN: failure
```

---

## Recovery Metrics

```yaml
RecoveryMetrics:
  # Overall
  recovery_rate: 0.95  # % of failures recovered
  avg_recovery_time: "45 seconds"
  
  # By strategy
  retry_success_rate: 0.70
  alt_tool_success_rate: 0.85
  simplify_success_rate: 0.60
  escalation_rate: 0.05
  
  # By tool
  openhands_recovery_rate: 0.92
  aider_recovery_rate: 0.88
  claude_recovery_rate: 0.95
```

---

## Integration

```
Recovery Engine connects to:

    → Execution Manager (receives failure notifications)
    → Capability Selector (gets alternatives)
    → Learning Engine (records failure patterns)
    → Decision Engine (decides recovery strategy)
```

---

## Related Documents

- [Verification-Engine.md](./04-Verification-Engine.md)
- [Learning-Engine.md](./06-Learning-Engine.md)
