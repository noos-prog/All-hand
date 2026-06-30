# Learning Engine

> **Every execution increases knowledge.**

---

## Purpose

The Learning Engine learns from every execution, improving tool selection and decision-making over time.

---

## Core Concept

```
Task Executed
      ↓
Learning Engine Records:
      ↓
What was the task?
What tool was used?
How long did it take?
How many tokens?
How much did it cost?
What was the quality?
Did it succeed?
      ↓
Store in Memory
      ↓
Future decisions become smarter
```

---

## What Gets Learned

```yaml
LearningData:
  # Task Information
  task:
    id: string
    capability: string
    type: string
    complexity: enum  # simple, medium, complex
    duration: duration
    
  # Tool Information
  tool:
    name: string
    version: string
    
  # Execution Metrics
  metrics:
    execution_time: duration
    token_usage: integer
    api_calls: integer
    cost: decimal
    
  # Quality Metrics
  quality:
    verification_passed: boolean
    verification_score: 0.0-1.0
    user_feedback: string
    
  # Outcome
  outcome:
    success: boolean
    error: string  # if failed
    recovery_needed: boolean
    
  # Context
  context:
    priority: string
    environment: string
    deadline: string
```

---

## Learning Types

### 1. Execution Learning
```yaml
ExecutionLearning:
  # Learn from each execution
  
  what_learned:
    - Tool reliability for this task type
    - Average execution time
    - Cost patterns
    
  stored_as:
    - tool_performance[capability]
    - execution_time_models[capability]
    - cost_predictions[capability]
```

### 2. Pattern Learning
```yaml
PatternLearning:
  # Learn from recurring patterns
  
  what_learned:
    - Tasks that often fail together
    - Tools that work well for specific patterns
    - Success rate for task combinations
    
  stored_as:
    - success_patterns[]
    - failure_patterns[]
    - tool_synergies[]
```

### 3. Context Learning
```yaml
ContextLearning:
  # Learn from context
  
  what_learned:
    - How context affects success
    - Which context factors matter most
    - Best tools for specific contexts
    
  stored_as:
    - context_preferences[]
    - context_scores[]
```

---

## Learning Process

```
1. Task execution completes
        ↓
2. Collect execution data
        ↓
3. Calculate metrics
        ↓
4. Identify patterns
        ↓
5. Update knowledge base
        ↓
6. Adjust tool scores
        ↓
7. Update success rates
        ↓
8. Refine decision weights
```

---

## Score Updates

```python
class ToolScoreUpdater:
    """Updates tool scores based on execution."""
    
    async def update_scores(
        self,
        execution: ExecutionData
    ):
        """Update scores after each execution."""
        
        tool = execution.tool
        
        # 1. Update quality score (EMA)
        tool.quality_score = (
            0.9 * tool.quality_score +
            0.1 * execution.quality_score
        )
        
        # 2. Update reliability
        if execution.success:
            tool.success_count += 1
        else:
            tool.failure_count += 1
            
        tool.reliability = (
            tool.success_count /
            (tool.success_count + tool.failure_count)
        )
        
        # 3. Update latency estimate
        tool.avg_latency = (
            0.9 * tool.avg_latency +
            0.1 * execution.execution_time
        )
        
        # 4. Update cost estimate
        tool.avg_cost = (
            0.9 * tool.avg_cost +
            0.1 * execution.cost
        )
```

---

## Pattern Detection

```python
class PatternDetector:
    """Detects patterns in execution data."""
    
    def detect_patterns(self, executions: list):
        """
        Find patterns in execution history.
        """
        
        patterns = []
        
        # 1. Find failure correlations
        failure_patterns = self.find_failure_correlations(executions)
        patterns.extend(failure_patterns)
        
        # 2. Find success correlations
        success_patterns = self.find_success_correlations(executions)
        patterns.extend(success_patterns)
        
        # 3. Find timing patterns
        timing_patterns = self.find_timing_patterns(executions)
        patterns.extend(timing_patterns)
        
        # 4. Find context patterns
        context_patterns = self.find_context_patterns(executions)
        patterns.extend(context_patterns)
        
        return patterns
```

---

## Learning Storage

```yaml
LearningStore:
  # Tool Performance
  tool_performance:
    openhands:
      capabilities:
        generate_backend:
          success_rate: 0.95
          avg_time: "3 minutes"
          avg_cost: "$0.05"
          sample_size: 150
          
        generate_frontend:
          success_rate: 0.92
          avg_time: "4 minutes"
          avg_cost: "$0.06"
          sample_size: 120
          
  # Context Preferences
  context_preferences:
    priority_high:
      preferred_tools:
        - tool: "openhands"
          weight: 0.4
        - tool: "claude-code"
          weight: 0.3
          
    environment_production:
      preferred_tools:
        - tool: "openhands"
          weight: 0.5
        - tool: "aider"
          weight: 0.2
          
  # Pattern Memory
  patterns:
    - type: "failure_chain"
      description: "If task fails on OpenHands, Aider often succeeds"
      confidence: 0.85
      occurrences: 25
      
    - type: "timing"
      description: "Weekend tasks take 20% longer"
      confidence: 0.72
      occurrences: 50
```

---

## Learning Feedback Loop

```
    ┌─────────────────────────────────────┐
    │                                     │
    │    Decision Engine                  │
    │    selects tool                     │
    │                                     │
    └─────────────────┬───────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │    Execution Manager                 │
    │    executes task                     │
    │                                     │
    └─────────────────┬───────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │    Learning Engine                   │
    │    records outcome                   │
    │                                     │
    └─────────────────┬───────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │    Knowledge Base                    │
    │    updates scores                   │
    │                                     │
    └─────────────────┬───────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │    Next decision uses               │
    │    updated knowledge                │
    │                                     │
    └─────────────────────────────────────┘
```

---

## Learning Metrics

```yaml
LearningMetrics:
  # Data collection
  executions_recorded: integer
  patterns_identified: integer
  scores_updated: integer
  
  # Quality
  learning_accuracy: 0.0-1.0  # How accurate predictions are
  model_freshness: duration   # How recent is data
  
  # Impact
  score_adjustment_impact: percentage
  pattern_discovered_impact: percentage
  
  # Trends
  tool_reliability_trends:
    openhands: [0.95, 0.94, 0.93, 0.95]  # over time
```

---

## Example Learning Session

```yaml
Task: "Generate REST API for users"
Tool: "OpenHands"
Duration: "3 minutes"
Cost: "$0.05"
Success: true
Quality Score: 0.92

Learning:
1. OpenHands.generate_api success_rate: 0.95 → 0.952
2. OpenHands.avg_time: 3.2min → 3.15min
3. Pattern: "Backend generation with OpenHands = high success"
4. Confidence in OpenHands for generate_api: ↑ 0.90 → 0.92
```

---

## Continuous Learning

```yaml
LearningSchedule:
  # Continuous updates
  on_execution_complete:
    - Update tool scores
    - Record metrics
    - Detect patterns
    
  hourly:
    - Analyze recent executions
    - Identify trends
    - Adjust weights
    
  daily:
    - Full pattern analysis
    - Model retraining
    - Anomaly detection
    
  weekly:
    - Deep analysis
    - Strategy review
    - Benchmark updates
```

---

## Anti-Learning (Negative Learning)

```yaml
NegativeLearning:
  # Learn from failures
  
  when_tool_declines:
    - Decrease trust score
    - Increase scrutiny
    - Add verification steps
    
  when_tool_repeatedly_fails:
    - Add to circuit breaker
    - Lower priority in selection
    - Require more verification
    
  when_tool_overpromises:
    - Track accuracy vs claims
    - Adjust expectations
    - Increase verification depth
```

---

## Related Documents

- [Decision-Engine.md](../01-Core-Brain/05-Decision-Engine.md)
- [Capability-Selector.md](./02-Capability-Selector.md)
