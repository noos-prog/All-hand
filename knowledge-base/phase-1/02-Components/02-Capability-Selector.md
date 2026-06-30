# Capability Selector

> **Chooses the best tool for each capability. Does NOT know project names.**

---

## Purpose

The Capability Selector receives a capability need and selects the best tool. It only knows capabilities, not project names.

---

## Core Concept

```
❌ Old Way (Wrong):
"Use OpenHands" or "Use Aider"

✅ New Way (Correct):
"Need: Generate Backend API"
     ↓
"Best Tool for: Generate Backend API"
     ↓
"Answer: OpenHands"
```

**The Core Brain doesn't say "use OpenHands". It says "need capability X" and the Selector finds the best tool for X.**

---

## Input → Output

```
CapabilityRequest:
  capability: "generate_backend"
  context: {...}
  constraints: {...}
  
      ↓
Capability Selector
      
      ↓
ToolSelection:
  selected_tool: "openhands"
  alternatives: ["aider", "claude-code"]
  reasoning: "..."
```

---

## Selection Process

```
1. Receive capability need
        ↓
2. Query Capability Registry
        ↓
3. Get candidate tools
        ↓
4. Apply Decision Policies
        ↓
5. Calculate Capability Score for each
        ↓
6. Rank candidates
        ↓
7. Select best match
        ↓
8. Return ToolSelection with alternatives
```

---

## Capability Registry Structure

```yaml
CapabilityRegistry:
  # For each capability
  
  "generate_backend":
    description: "Generate backend code/APIs"
    category: "code_generation"
    
    tools:
      - name: "openhands"
        score: 0.95
        latency: "medium"
        cost: "medium"
        reliability: 0.95
        
      - name: "aider"
        score: 0.85
        latency: "low"
        cost: "low"
        reliability: 0.90
        
      - name: "claude-code"
        score: 0.90
        latency: "low"
        cost: "high"
        reliability: 0.98
        
      - name: "goose"
        score: 0.78
        latency: "medium"
        cost: "low"
        reliability: 0.85
        
      - name: "cline"
        score: 0.75
        latency: "low"
        cost: "medium"
        reliability: 0.88
        
    ranking_criteria:
      - quality_score (weight: 0.30)
      - reliability (weight: 0.20)
      - latency (weight: 0.15)
      - cost (weight: 0.15)
      - context_fit (weight: 0.10)
      - historical_success (weight: 0.10)
```

---

## Scoring Algorithm

```python
def calculate_capability_score(
    tool: Tool,
    capability: Capability,
    context: Context
) -> Score:
    """
    Calculate how well a tool fits a capability.
    """
    
    scores = {}
    
    # 1. Quality Score (30%)
    scores['quality'] = tool.quality_score * 0.30
    
    # 2. Reliability (20%)
    scores['reliability'] = tool.reliability * 0.20
    
    # 3. Latency (15%) - Lower is better
    scores['latency'] = (1.0 - tool.latency_score) * 0.15
    
    # 4. Cost (15%) - Lower is better
    scores['cost'] = (1.0 - tool.cost_score) * 0.15
    
    # 5. Context Fit (10%)
    scores['context'] = calculate_context_fit(tool, context) * 0.10
    
    # 6. Historical Success (10%)
    scores['historical'] = get_historical_success(tool, capability) * 0.10
    
    # Total
    total = sum(scores.values())
    
    return Score(
        total=total,
        breakdown=scores,
        confidence=calculate_confidence(scores)
    )
```

---

## Context-Aware Selection

```yaml
ContextFactors:
  # Speed is critical
  if context.priority == "speed":
    weights:
      latency: 0.40  # Much higher
      quality: 0.20
      
  # Quality is critical  
  if context.priority == "quality":
    weights:
      quality: 0.45  # Much higher
      reliability: 0.25
      
  # Budget is tight
  if context.budget == "low":
    weights:
      cost: 0.40    # Much higher
      latency: 0.10
      
  # Production deployment
  if context.environment == "production":
    weights:
      reliability: 0.35  # Much higher
      quality: 0.30
```

---

## Example: Generate Backend

**Context:**
```yaml
Context:
  goal: "Build e-commerce API"
  priority: "balanced"
  budget: "$500/month"
  environment: "staging"
```

**Selection Process:**
```
1. Query: "generate_backend"
2. Candidates: [openhands, aider, claude-code, goose, cline]

3. Score each:

   OpenHands:
     quality: 0.95 * 0.30 = 0.285
     reliability: 0.95 * 0.20 = 0.190
     latency: 0.7 * 0.15 = 0.105
     cost: 0.5 * 0.15 = 0.075
     context: 0.9 * 0.10 = 0.090
     historical: 0.92 * 0.10 = 0.092
     TOTAL: 0.837
   
   Aider:
     quality: 0.85 * 0.30 = 0.255
     reliability: 0.90 * 0.20 = 0.180
     latency: 0.9 * 0.15 = 0.135
     cost: 0.9 * 0.15 = 0.135
     context: 0.8 * 0.10 = 0.080
     historical: 0.88 * 0.10 = 0.088
     TOTAL: 0.873
   
   Claude Code:
     quality: 0.90 * 0.30 = 0.270
     reliability: 0.98 * 0.20 = 0.196
     latency: 0.9 * 0.15 = 0.135
     cost: 0.3 * 0.15 = 0.045
     context: 0.85 * 0.10 = 0.085
     historical: 0.90 * 0.10 = 0.090
     TOTAL: 0.821

4. Rank:
   1. Aider: 0.873
   2. OpenHands: 0.837
   3. Claude Code: 0.821

5. Select: Aider
```

---

## Alternatives Always Provided

Every selection includes alternatives:

```yaml
ToolSelection:
  selected: "aider"
  confidence: 0.85
  
  alternatives:
    - tool: "openhands"
      score: 0.837
      reason: "Second best, higher quality but slower"
      
    - tool: "claude-code"
      score: 0.821
      reason: "Third best, more expensive"
      
  reasoning: |
    "Selected Aider because:
    1. Best overall score (0.873) for 'generate_backend'
    2. Excellent latency (0.9) for staging environment
    3. Cost-effective ($0.02/task) for budget
    4. High reliability (0.90) for task type"
```

---

## No Tool Name, Only Capability

```python
# WRONG:
def select_tool(tool_name: str):
    execute(tool_name)

# CORRECT:
def select_capability(capability: str, context: dict):
    tool = selector.get_best_tool(capability, context)
    # Tool is selected based on capability, not name
    execute(tool)
```

---

## Registry Updates

```yaml
UpdateTriggers:
  - new_tool_added:
      recalculate_all_scores()
      
  - tool_failed:
      decrease_tool_score(tool, capability)
      
  - tool_succeeded:
      increase_tool_score(tool, capability)
      
  - benchmark_updated:
      recalculate_quality_scores()
      
  - user_feedback:
      adjust_weights(tool, feedback)
```

---

## Related Documents

- [Knowledge-Engine.md](../01-Core-Brain/04-Knowledge-Engine.md)
- [Decision-Engine.md](../01-Core-Brain/05-Decision-Engine.md)
