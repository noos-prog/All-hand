# Capability Selection Algorithm

> **Selection is never based on name. Always based on scores.**

---

## Purpose

The Capability Selection Algorithm determines the best tool for each capability using multiple factors. Names are never considered - only capabilities and scores.

---

## Algorithm Overview

```python
def select_best_tool(
    capability: str,
    context: Context,
    constraints: Constraints
) -> ToolSelection:
    """
    Select best tool for capability.
    
    Never uses tool name - only scores.
    """
    
    # 1. Get all candidate tools
    candidates = capability_registry.get_tools(capability)
    
    # 2. Calculate scores for each candidate
    scored_candidates = []
    for tool in candidates:
        score = calculate_composite_score(tool, capability, context)
        scored_candidates.append((tool, score))
    
    # 3. Apply policies
    scored_candidates = apply_policies(scored_candidates, context)
    
    # 4. Sort by score
    ranked = sorted(scored_candidates, key=lambda x: x.score, reverse=True)
    
    # 5. Return top candidate with alternatives
    return ToolSelection(
        selected=ranked[0][0],
        alternatives=ranked[1:4],
        reasoning=generate_reasoning(ranked)
    )
```

---

## Scoring Components

```yaml
ScoreComponents:
  # All scores are 0.0 to 1.0
  
  1. Capability Score (30%)
     - How well tool fits the capability
     - Based on benchmark results
     
  2. Quality Score (20%)
     - Historical quality of outputs
     - Based on verification results
     
  3. Reliability Score (15%)
     - Success rate over time
     - Based on execution history
     
  4. Latency Score (10%)
     - Response time
     - Lower is better, normalized
     
  5. Cost Score (10%)
     - Cost per execution
     - Lower is better, normalized
     
  6. Availability Score (5%)
     - Current availability
     - Based on health checks
     
  7. Context Fit Score (5%)
     - Fits current context
     - Production vs development
     
  8. Historical Success Score (5%)
     - Success in similar tasks
     - Based on learning data
```

---

## Score Calculation

```python
def calculate_composite_score(
    tool: Tool,
    capability: str,
    context: Context
) -> float:
    """
    Calculate weighted composite score.
    """
    
    # Get component scores
    scores = {
        'capability': tool.capability_scores[capability],
        'quality': tool.quality_score,
        'reliability': tool.reliability_score,
        'latency': normalize_latency(tool.avg_latency),
        'cost': normalize_cost(tool.avg_cost),
        'availability': tool.availability,
        'context_fit': calculate_context_fit(tool, context),
        'historical': tool.historical_success[capability]
    }
    
    # Get weights (from context)
    weights = get_context_weights(context)
    
    # Calculate weighted sum
    total = sum(
        scores[key] * weights[key]
        for key in scores
    )
    
    # Apply adjustments
    total = apply_adjustments(total, tool, context)
    
    return total
```

---

## Context-Based Weights

```yaml
ContextWeights:
  
  # Default weights
  default:
    capability: 0.30
    quality: 0.20
    reliability: 0.15
    latency: 0.10
    cost: 0.10
    availability: 0.05
    context_fit: 0.05
    historical: 0.05
    
  # Speed priority
  speed_priority:
    latency: 0.45
    capability: 0.20
    cost: 0.15
    quality: 0.10
    reliability: 0.05
    availability: 0.05
    
  # Quality priority
  quality_priority:
    quality: 0.35
    capability: 0.25
    reliability: 0.15
    historical: 0.10
    latency: 0.05
    cost: 0.05
    
  # Budget priority
  budget_priority:
    cost: 0.40
    latency: 0.20
    capability: 0.20
    quality: 0.10
    reliability: 0.05
    
  # Production environment
  production:
    reliability: 0.30
    quality: 0.25
    capability: 0.20
    availability: 0.10
    latency: 0.05
    cost: 0.05
    
  # Development environment
  development:
    speed: 0.30
    capability: 0.25
    cost: 0.20
    quality: 0.15
    reliability: 0.05
```

---

## Normalization Functions

```python
def normalize_latency(latency_ms: float) -> float:
    """
    Convert latency to 0-1 score where lower is better.
    """
    # Benchmarks:
    # < 1 min: 1.0
    # 1-5 min: 0.7-1.0
    # 5-15 min: 0.4-0.7
    # > 15 min: 0.0-0.4
    
    if latency_ms < 60000:  # < 1 min
        return 1.0
    elif latency_ms < 300000:  # < 5 min
        return 1.0 - (latency_ms - 60000) / 240000 * 0.3
    elif latency_ms < 900000:  # < 15 min
        return 0.7 - (latency_ms - 300000) / 600000 * 0.3
    else:
        return max(0.0, 0.4 - (latency_ms - 900000) / 600000 * 0.4)

def normalize_cost(cost_usd: float) -> float:
    """
    Convert cost to 0-1 score where lower is better.
    """
    # Benchmarks:
    # Free: 1.0
    # < $0.05: 0.9
    # $0.05-$0.50: 0.7-0.9
    # > $1.00: < 0.5
    
    if cost_usd == 0:
        return 1.0
    elif cost_usd < 0.05:
        return 0.9 + (0.05 - cost_usd) * 2
    elif cost_usd < 0.50:
        return 0.7 + (0.50 - cost_usd) / 0.45 * 0.2
    elif cost_usd < 1.00:
        return 0.5 + (1.00 - cost_usd) / 0.50 * 0.2
    else:
        return max(0.0, 0.5 - (cost_usd - 1.00) * 0.1)
```

---

## Context Fit Calculation

```python
def calculate_context_fit(
    tool: Tool,
    context: Context
) -> float:
    """
    Calculate how well tool fits current context.
    """
    
    score = 1.0
    
    # Environment fit
    if context.environment == "production":
        if not tool.production_ready:
            score *= 0.5
    elif context.environment == "development":
        if tool.production_ready:
            score *= 1.1  # Bonus for production-ready in dev
            
    # Language fit
    if context.languages:
        language_overlap = set(tool.supported_languages) & set(context.languages)
        if language_overlap:
            score *= (1.0 + len(language_overlap) * 0.05)
        else:
            score *= 0.7
            
    # Framework fit
    if context.frameworks:
        framework_overlap = set(tool.supported_frameworks) & set(context.frameworks)
        if framework_overlap:
            score *= (1.0 + len(framework_overlap) * 0.05)
            
    # Scale fit
    if context.scale == "high":
        if not tool.supports_high_scale:
            score *= 0.7
            
    return min(1.0, score)
```

---

## Policy Adjustments

```python
def apply_adjustments(
    score: float,
    tool: Tool,
    context: Context
) -> float:
    """
    Apply policy-based adjustments.
    """
    
    # Failed tool adjustment
    if tool.recent_failures > 0:
        multiplier = 1.0 - (tool.recent_failures * 0.15)
        score *= multiplier
        
    # Circuit breaker adjustment
    if tool.circuit_breaker == "open":
        score = 0.0  # Completely exclude
        
    elif tool.circuit_breaker == "half_open":
        score *= 0.5  # Reduced confidence
        
    # New tool adjustment
    if tool.is_new:
        score *= 0.9  # Slight penalty for untested
        
    # Proven tool bonus
    if tool.sample_size > 100:
        score *= 1.05  # Confidence bonus
        
    return min(1.0, max(0.0, score))
```

---

## Selection Example

```yaml
Context:
  goal: "Build REST API"
  priority: "balanced"
  environment: "staging"
  languages: ["python"]
  frameworks: ["fastapi"]
  
  weights:
    capability: 0.30
    quality: 0.20
    reliability: 0.15
    latency: 0.10
    cost: 0.10
    context_fit: 0.05
    historical: 0.05
    availability: 0.05

Candidates:

  OpenHands:
    capability: 0.95
    quality: 0.92
    reliability: 0.95
    latency: 0.85 (2 min)
    cost: 0.70 ($0.05)
    context_fit: 0.95
    historical: 0.90
    availability: 1.0
    
    Score: 
    0.95×0.30 + 0.92×0.20 + 0.95×0.15 + 0.85×0.10 + 
    0.70×0.10 + 0.95×0.05 + 0.90×0.05 + 1.0×0.05
    = 0.285 + 0.184 + 0.143 + 0.085 + 0.070 + 
      0.048 + 0.045 + 0.050
    = 0.910

  Aider:
    capability: 0.85
    quality: 0.88
    reliability: 0.90
    latency: 0.95 (1 min)
    cost: 0.90 (free)
    context_fit: 0.85
    historical: 0.85
    availability: 1.0
    
    Score: 0.865

  Claude Code:
    capability: 0.90
    quality: 0.95
    reliability: 0.98
    latency: 0.90 (90 sec)
    cost: 0.40 ($0.50)
    context_fit: 0.88
    historical: 0.88
    availability: 1.0
    
    Score: 0.845

Ranking:
  1. OpenHands: 0.910
  2. Aider: 0.865
  3. Claude Code: 0.845

Decision: OpenHands
Confidence: HIGH (0.91)
```

---

## Explainability Output

```yaml
Selection:
  selected: "openhands"
  confidence: 0.91
  
Reasoning:
  """
  Selected OpenHands because:
  
  1. Highest composite score (0.91)
  2. Best capability fit (0.95) for 'generate_backend'
  3. High quality score (0.92) based on 150+ executions
  4. Good reliability (0.95) with 96% success rate
  5. Context fit (0.95) for Python/FastAPI
  6. Within budget ($0.05/task)
  
  Rejected Aider (0.865) because:
  - Lower capability fit (0.85 vs 0.95)
  - Fewer features for backend generation
  
  Rejected Claude Code (0.845) because:
  - Higher cost ($0.50 vs $0.05)
  - Lower context fit for FastAPI
  """
```

---

## Related Documents

- [Decision-Policies.md](./01-Decision-Policies.md)
- [Brain-Rules.md](./03-Brain-Rules.md)
