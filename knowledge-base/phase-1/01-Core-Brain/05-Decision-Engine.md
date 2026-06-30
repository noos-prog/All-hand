# Decision Engine

> **The most important part. Every decision passes through here.**

---

## Purpose

The Decision Engine is the central hub for all decisions in the Core Brain. It ensures no random choice is made and all decisions are explainable.

---

## Decision Flow

```
Question: Use Tool A, B, or C?

              ↓
      Decision Engine
              ↓
      Analyze Options
              ↓
      Apply Policies
              ↓
      Calculate Scores
              ↓
      Select Best
              ↓
      Record Reasoning
              ↓
      Return Decision
```

---

## Decision Types

| Type | Description | Example |
|------|-------------|---------|
| `TOOL_SELECTION` | Choose best tool | "Which tool for API generation?" |
| `CAPABILITY_CHOICE` | Select capability | "Need code gen, what type?" |
| `RETRY_DECISION` | Retry or switch | "Tool failed, retry?" |
| `VERDICT` | Accept or reject | "Is this result acceptable?" |
| `PRIORITY` | Set priority | "What runs first?" |
| `FALLBACK` | Use fallback | "Primary failed, use backup?" |
| `ESCALATION` | Escalate issue | "Need human intervention?" |

---

## Decision Request Schema

```yaml
DecisionRequest:
  id: string              # Unique decision ID
  type: enum              # Decision type
  
  # Context
  goal: Goal              # Current goal
  context: UnifiedContext # Current context
  
  # Options
  options: list           # Available choices
  constraints: list       # Hard constraints
  
  # Criteria
  criteria: list          # Evaluation criteria
  weights: dict           # Criteria weights
  policies: list          # Applicable policies
  
  # Meta
  requester: string       # Who requested
  priority: enum          # Decision priority
  timeout: duration       # Max decision time
```

---

## Decision Response Schema

```yaml
DecisionResponse:
  id: string              # Matches request ID
  
  # Decision
  decision: string        # Selected option
  confidence: 0.0-1.0    # Confidence score
  
  # Reasoning
  reasoning: string       # Human-readable explanation
  criteria_scores: dict   # Scores per criterion
  alternative_scores: dict # Scores for alternatives
  
  # Trace
  alternatives: list      # Options considered
  rejected: list          # Why alternatives rejected
  
  # Metadata
  policies_applied: list # Which policies used
  confidence_factors: list # What affected confidence
  timestamp: datetime     # When decided
  
  # For Learning
  decision_type: enum    # Type of decision
  outcome: pending        # Will be updated later
```

---

## Decision Process

```
1. Receive DecisionRequest
        ↓
2. Validate request completeness
        ↓
3. Load applicable policies
        ↓
4. Get context from Knowledge Engine
        ↓
5. For each option:
   - Evaluate against criteria
   - Apply policy rules
   - Calculate weighted score
        ↓
6. Rank options by score
        ↓
7. Apply tie-breaking rules
        ↓
8. Generate reasoning
        ↓
9. Record decision trace
        ↓
10. Return DecisionResponse
```

---

## Criteria Weights

Default weights for tool selection:

```yaml
CriteriaWeights:
  # Primary (Must consider)
  capability_fit: 0.25    # How well it fits capability need
  quality_score: 0.20     # Historical quality
  reliability: 0.15       # Uptime and consistency
  
  # Secondary (Important)
  latency: 0.10           # Response time
  cost: 0.10             # Cost efficiency
  availability: 0.10      # Current availability
  
  # Contextual (Depends on situation)
  context_fit: 0.05      # Fits current context
  historical_success: 0.05 # Worked before in similar tasks
```

---

## Policy Application

```python
class DecisionPolicy:
    """Base policy class"""
    
    def apply(self, request: DecisionRequest, options: list) -> list:
        """
        Takes options, applies policy rules.
        Returns filtered/ranked options.
        """
        pass

# Example policies:

class SpeedOverQuality(DecisionPolicy):
    """If speed is priority"""
    def apply(self, request, options):
        # Reorder by latency, not quality
        return sorted(options, key=lambda x: x.latency)

class QualityOverSpeed(DecisionPolicy):
    """If quality is priority"""
    def apply(self, request, options):
        # Reorder by quality, not speed
        return sorted(options, key=lambda x: x.quality_score)

class NoCompromisedTool(DecisionPolicy):
    """If tool failed twice, don't use for this goal"""
    def apply(self, request, options):
        # Filter out failed tools
        return [o for o in options if o.failure_count < 2]
```

---

## Explainability Requirements

Every decision MUST include:

```yaml
Explainability:
  # Required fields
  - "What was decided"
  - "What options were considered"
  - "Why this option was chosen"
  - "What criteria were used"
  - "What weights were applied"
  - "Why alternatives were rejected"
  
  # Example
  decision: "Chose OpenHands"
  reasoning: |
    "Selected OpenHands over alternatives because:
    1. Highest capability fit (0.95) for 'generate_backend'
    2. Best historical success rate (92%) for similar tasks
    3. API availability confirmed
    4. Cost within budget ($0.05/task)
    
    Rejected Aider because: lower quality score (0.78)
    Rejected Goose because: less experience with backend (0.65)"
```

---

## Confidence Scoring

```yaml
ConfidenceFactors:
  # Increases confidence
  + Strong criteria match
  + High historical success
  + Clear winner (large score gap)
  + Policies strongly support
  + Multiple sources agree
  
  # Decreases confidence
  - Close scores between options
  - Missing data
  - Conflicting policies
  - Low historical success
  - Unknown tool

ConfidenceLevels:
  HIGH: 0.8-1.0    # Proceed
  MEDIUM: 0.5-0.8 # Proceed with monitoring
  LOW: 0.3-0.5    # Gather more info
  VERY_LOW: 0-0.3 # Reconsider approach
```

---

## Decision Logging

Every decision is logged for audit:

```yaml
DecisionLog:
  id: string
  timestamp: datetime
  
  request: DecisionRequest
  response: DecisionResponse
  
  # For analysis
  goal_id: string
  execution_time: duration
  
  # Future reference
  outcome: string        # Set when outcome known
  feedback: string        # User feedback if any
```

---

## Decision Examples

### Example 1: Tool Selection

```
Request: "Which tool for generating REST API?"
Options: [OpenHands, Aider, Goose]

Process:
1. Apply policies → All valid
2. Score OpenHands → 0.92
3. Score Aider → 0.78
4. Score Goose → 0.71

Decision: OpenHands
Confidence: 0.85 (HIGH)
Reasoning: "Best overall fit, highest quality score"
```

### Example 2: Retry Decision

```
Request: "OpenHands failed. Retry or switch?"
Context: 1 previous failure, time constraint exists

Process:
1. Check failure count → 1 (< 2)
2. Check time constraint → Allow retry
3. Apply retry policy

Decision: Retry OpenHands
Confidence: 0.75 (MEDIUM)
Reasoning: "First failure, retry policy allows 2 retries"
```

---

## Related Documents

- [04-Policies/Decision-Policies.md](./04-Policies/01-Decision-Policies.md)
- [02-Components/Recovery-Engine.md](./02-Components/08-Recovery-Engine.md)
