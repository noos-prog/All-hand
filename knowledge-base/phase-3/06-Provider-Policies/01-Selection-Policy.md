# Provider Selection Policy

> **Selection based on Capability Match, Health, Reliability, Quality, Cost, Latency.**

---

## Selection Criteria

```yaml
SelectionCriteria:
  # In order of priority
  
  1. CAPABILITY_MATCH
     weight: 0.25
     description: "Does provider support this capability?"
     
  2. HEALTH
     weight: 0.20
     description: "Is provider currently healthy?"
     
  3. RELIABILITY
     weight: 0.20
     description: "Historical reliability"
     
  4. QUALITY
     weight: 0.15
     description: "Quality of output"
     
  5. COST
     weight: 0.10
     description: "Cost efficiency"
     
  6. LATENCY
     weight: 0.10
     description: "Response time"
```

---

## Selection Algorithm

```python
def select_provider(
    capability_id: str,
    context: Context
) -> Provider:
    """
    Select best provider based on criteria.
    """
    
    # 1. Get all providers for this capability
    providers = registry.get_providers(capability_id)
    
    # 2. Score each provider
    scored = []
    for provider in providers:
        score = calculate_selection_score(
            provider=provider,
            capability_id=capability_id,
            context=context
        )
        scored.append((provider, score))
    
    # 3. Sort by score
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    
    # 4. Return best
    return ranked[0][0]


def calculate_selection_score(
    provider: Provider,
    capability_id: str,
    context: Context
) -> float:
    """
    Calculate composite selection score.
    """
    
    score = 0.0
    
    # 1. Capability match (fixed)
    score += 0.25 * provider.capability_match(capability_id)
    
    # 2. Health (dynamic)
    health_score = get_health_score(provider)
    score += 0.20 * health_score
    
    # 3. Reliability (historical)
    reliability_score = provider.reliability_score
    score += 0.20 * reliability_score
    
    # 4. Quality (context-dependent)
    quality_score = get_quality_score(provider, capability_id, context)
    score += 0.15 * quality_score
    
    # 5. Cost (context-dependent)
    cost_score = get_cost_score(provider, context)
    score += 0.10 * cost_score
    
    # 6. Latency (context-dependent)
    latency_score = get_latency_score(provider, context)
    score += 0.10 * latency_score
    
    return score
```

---

## Context-Aware Weighting

```yaml
ContextWeights:
  # Adjust weights based on context
  
  development:
    latency: 0.30   # Speed matters
    cost: 0.20     # Budget matters
    quality: 0.15
    reliability: 0.15
    health: 0.10
    capability: 0.10
    
  staging:
    quality: 0.30   # Quality matters
    reliability: 0.25
    health: 0.15
    latency: 0.10
    cost: 0.10
    capability: 0.10
    
  production:
    reliability: 0.35   # Must work
    quality: 0.30
    health: 0.15
    capability: 0.10
    latency: 0.05
    cost: 0.05
    
  critical:
    reliability: 0.40
    quality: 0.30
    health: 0.15
    capability: 0.10
    latency: 0.05
    cost: 0.00
    
  budget_constrained:
    cost: 0.40
    latency: 0.20
    reliability: 0.15
    quality: 0.10
    health: 0.10
    capability: 0.05
```

---

## Health Score Calculation

```yaml
HealthScore:
  HEALTHY: 1.0
  DEGRADED: 0.6
  UNKNOWN: 0.8
  MAINTENANCE: 0.0
  OFFLINE: 0.0
  UNHEALTHY: 0.0
  
  # With history
  consecutive_failures: 1 → score = 0.8
  consecutive_failures: 2 → score = 0.6
  consecutive_failures: 3 → score = 0.3
  consecutive_failures: 5 → score = 0.0
```

---

## Quality Score Calculation

```yaml
QualityScore:
  # Based on capability profile
  
  accuracy_weights:
    excellent: 1.0
    high: 0.85
    good: 0.70
    medium: 0.50
    low: 0.30
    
  # Based on historical performance
  historical_score = provider.metrics.quality_scores[capability_id]
  
  # Combined
  quality_score = (
    accuracy_score * 0.4 +
    historical_score * 0.4 +
    consistency_score * 0.2
  )
```

---

## Example: Select for Code Generation

```yaml
Context:
  environment: "production"
  priority: "quality"
  budget: "medium"
  
Providers:
  openhands:
    capability_match: 1.0
    health: HEALTHY (1.0)
    reliability: 0.95
    quality: 0.92
    cost: 0.70 ($0.05)
    latency: 0.85 (3 min)
    
  cline:
    capability_match: 1.0
    health: DEGRADED (0.6)
    reliability: 0.88
    quality: 0.85
    cost: 0.90 ($0.02)
    latency: 0.90 (2 min)
    
  aider:
    capability_match: 1.0
    health: HEALTHY (1.0)
    reliability: 0.85
    quality: 0.82
    cost: 0.95 ($0.01)
    latency: 0.95 (1 min)

Calculation (production weights):
  openhands: 0.25*1.0 + 0.20*1.0 + 0.20*0.95 + 0.15*0.92 + 0.10*0.70 + 0.10*0.85 = 0.92
  cline: 0.25*1.0 + 0.20*0.6 + 0.20*0.88 + 0.15*0.85 + 0.10*0.90 + 0.10*0.90 = 0.82
  aider: 0.25*1.0 + 0.20*1.0 + 0.20*0.85 + 0.15*0.82 + 0.10*0.95 + 0.10*0.95 = 0.91

Selection: OpenHands (0.92)
```

---

## Related Documents

- [Provider-Object.md](../01-Provider-Definition/02-Provider-Object.md)
- [Voting.md](./02-Voting.md)
