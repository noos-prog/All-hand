# Decision Matrix

> **Every option is evaluated against multiple criteria.**

---

## Matrix Structure

```yaml
DecisionMatrix:
  # Identification
  id: string
  goal_id: string
  context_id: string
  created_at: datetime
  
  # Options evaluated
  options: list[Option]
  
  # Criteria
  criteria: list[Criterion]
  
  # Scores
  scores: dict[option_id][criterion_id] = score
  weights: dict[criterion_id] = weight
  
  # Results
  rankings: list[RankedOption]
  recommendation: string
  confidence: 0.0-1.0
```

---

## Criteria Types

```yaml
Criteria:
  # Primary criteria
  
  QUALITY:
    weight_default: 0.20
    description: "Quality of solution"
    direction: "higher_is_better"
    
  COST:
    weight_default: 0.15
    description: "Implementation cost"
    direction: "lower_is_better"
    
  COMPLEXITY:
    weight_default: 0.15
    description: "Technical complexity"
    direction: "lower_is_better"
    
  TIME:
    weight_default: 0.15
    description: "Time to implement"
    direction: "lower_is_better"
    
  RISK:
    weight_default: 0.15
    description: "Implementation risk"
    direction: "lower_is_better"
    
  MAINTAINABILITY:
    weight_default: 0.10
    description: "Ease of maintenance"
    direction: "higher_is_better"
    
  SECURITY:
    weight_default: 0.10
    description: "Security posture"
    direction: "higher_is_better"
    
  SCALABILITY:
    weight_default: 0.10
    description: "Ability to scale"
    direction: "higher_is_better"
    
  FLEXIBILITY:
    weight_default: 0.10
    description: "Future flexibility"
    direction: "higher_is_better"
    
  VENDOR_LOCK_IN:
    weight_default: 0.05
    description: "Avoid vendor lock-in"
    direction: "lower_is_better"
```

---

## Option Schema

```yaml
Option:
  id: string
  name: string
  description: string
  
  # Scores per criterion (0-10)
  scores:
    quality: 0-10
    cost: 0-10
    complexity: 0-10
    time: 0-10
    risk: 0-10
    maintainability: 0-10
    security: 0-10
    scalability: 0-10
    flexibility: 0-10
    vendor_lock_in: 0-10
    
  # Supporting info
  pros:
    - string
    
  cons:
    - string
    
  risks:
    - risk: string
      probability: 0.0-1.0
      impact: enum
        
  dependencies: list[string]
  estimated_cost: decimal
  estimated_time: duration
  
  # Confidence
  confidence: 0.0-1.0
  evidence: list[string]
```

---

## Calculation

```python
def calculate_option_score(
    option: Option,
    criteria: list[Criterion],
    weights: dict
) -> float:
    """
    Calculate weighted score for an option.
    """
    
    total_score = 0.0
    total_weight = 0.0
    
    for criterion in criteria:
        # Get option's score for this criterion
        option_score = option.scores[criterion.id]
        
        # Normalize based on direction
        # For "higher_is_better": score is already 0-10
        # For "lower_is_better": invert: 10 - score
        if criterion.direction == "lower_is_better":
            option_score = 10 - option_score
            
        # Get weight
        weight = weights.get(criterion.id, criterion.weight_default)
        
        # Add weighted score
        total_score += option_score * weight
        total_weight += weight
        
    # Normalize to 0-1
    normalized_score = total_score / (total_weight * 10)
    
    return normalized_score


def rank_options(
    options: list[Option],
    criteria: list[Criterion],
    weights: dict
) -> list[RankedOption]:
    """
    Rank options by weighted score.
    """
    
    ranked = []
    
    for option in options:
        score = calculate_option_score(option, criteria, weights)
        ranked.append({
            "option": option,
            "score": score
        })
    
    # Sort by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)
    
    return ranked
```

---

## Example: E-commerce Platform Options

### Options Evaluated

```yaml
Options:
  option_a:
    name: "Monolithic Architecture"
    description: "Single unified application"
    
    scores:
      quality: 7
      cost: 6
      complexity: 8
      time: 9
      risk: 7
      maintainability: 6
      security: 7
      scalability: 5
      flexibility: 4
      vendor_lock_in: 6
      
    pros:
      - "Simple to develop"
      - "Easy deployment"
      - "Lower initial cost"
      
    cons:
      - "Hard to scale"
      - "Limited flexibility"
      - "Single point of failure"
      
    estimated_cost: 5000
    estimated_time: "3 weeks"
    
  option_b:
    name: "Microservices Architecture"
    description: "Distributed services"
    
    scores:
      quality: 9
      cost: 4
      complexity: 4
      time: 5
      risk: 5
      maintainability: 9
      security: 9
      scalability: 10
      flexibility: 10
      vendor_lock_in: 3
      
    pros:
      - "Highly scalable"
      - "Flexible"
      - "Fault isolation"
      - "Technology diversity"
      
    cons:
      - "Complex to develop"
      - "Higher operational cost"
      - "Requires DevOps expertise"
      
    estimated_cost: 15000
    estimated_time: "8 weeks"
    
  option_c:
    name: "Serverless Architecture"
    description: "Cloud-native serverless"
    
    scores:
      quality: 8
      cost: 7
      complexity: 6
      time: 8
      risk: 6
      maintainability: 8
      security: 8
      scalability: 9
      flexibility: 8
      vendor_lock_in: 2
      
    pros:
      - "No server management"
      - "Pay per use"
      - "Auto-scaling"
      
    cons:
      - "Vendor lock-in"
      - "Cold start latency"
      - "Limited control"
      
    estimated_cost: 8000
    estimated_time: "5 weeks"
```

### Weights by Context

```yaml
ContextWeights:
  default:
    quality: 0.20
    cost: 0.15
    complexity: 0.15
    time: 0.15
    risk: 0.15
    maintainability: 0.10
    security: 0.10
    
  fast_delivery:
    time: 0.30
    cost: 0.20
    quality: 0.10
    complexity: 0.10
    risk: 0.10
    maintainability: 0.10
    security: 0.10
    
  budget_constrained:
    cost: 0.35
    time: 0.20
    quality: 0.15
    risk: 0.10
    complexity: 0.10
    maintainability: 0.10
    
  production_ready:
    security: 0.25
    scalability: 0.20
    reliability: 0.20
    maintainability: 0.15
    cost: 0.10
    time: 0.10
```

### Calculations

```yaml
Context: "default"

Weights:
  quality: 0.20
  cost: 0.15
  complexity: 0.15
  time: 0.15
  risk: 0.15
  maintainability: 0.10
  security: 0.10
  scalability: 0.10
  flexibility: 0.10
  vendor_lock_in: 0.05

Option A (Monolithic):
  Score = 
    (7/10 * 0.20) +        # quality
    (4/10 * 0.15) +        # cost (inverted)
    (2/10 * 0.15) +        # complexity (inverted)
    (1/10 * 0.15) +        # time (inverted)
    (3/10 * 0.15) +        # risk (inverted)
    (6/10 * 0.10) +        # maintainability
    (7/10 * 0.10) +        # security
    (5/10 * 0.10) +        # scalability
    (4/10 * 0.10) +        # flexibility
    (4/10 * 0.05)          # vendor_lock_in
  = 0.14 + 0.06 + 0.03 + 0.015 + 0.045 + 0.06 + 0.07 + 0.05 + 0.04 + 0.02
  = 0.53

Option B (Microservices):
  Score = 
    (9/10 * 0.20) +        # quality
    (6/10 * 0.15) +        # cost (inverted)
    (6/10 * 0.15) +        # complexity (inverted)
    (5/10 * 0.15) +        # time (inverted)
    (5/10 * 0.15) +        # risk (inverted)
    (9/10 * 0.10) +        # maintainability
    (9/10 * 0.10) +        # security
    (10/10 * 0.10) +      # scalability
    (10/10 * 0.10) +      # flexibility
    (7/10 * 0.05)          # vendor_lock_in
  = 0.18 + 0.09 + 0.09 + 0.075 + 0.075 + 0.09 + 0.09 + 0.10 + 0.10 + 0.035
  = 0.84

Option C (Serverless):
  Score = 
    (8/10 * 0.20) +
    (3/10 * 0.15) +
    (4/10 * 0.15) +
    (2/10 * 0.15) +
    (4/10 * 0.15) +
    (8/10 * 0.10) +
    (8/10 * 0.10) +
    (9/10 * 0.10) +
    (8/10 * 0.10) +
    (8/10 * 0.05)
  = 0.16 + 0.045 + 0.06 + 0.03 + 0.06 + 0.08 + 0.08 + 0.09 + 0.08 + 0.04
  = 0.73
```

### Rankings

```yaml
Rankings:
  1. Option B (Microservices): 0.84
     Recommendation: "Best overall balance"
     
  2. Option C (Serverless): 0.73
     Recommendation: "Good balance, lower cost"
     
  3. Option A (Monolithic): 0.53
     Recommendation: "Fast delivery, lower quality"
```

---

## Visual Matrix

```
┌─────────────────┬───────────┬───────────┬───────────┐
│    Criterion    │  Weight   │ Option A  │ Option B  │ Option C │
├─────────────────┼───────────┼───────────┼───────────┤
│ Quality         │   20%    │    7     │    9     │    8     │
│ Cost            │   15%    │    4     │    4     │    7     │
│ Complexity      │   15%    │    8     │    4     │    6     │
│ Time            │   15%    │    9     │    5     │    8     │
│ Risk            │   15%    │    7     │    5     │    6     │
│ Maintainability │   10%    │    6     │    9     │    8     │
│ Security        │   10%    │    7     │    9     │    8     │
│ Scalability     │   10%    │    5     │   10     │    9     │
│ Flexibility     │   10%    │    4     │   10     │    8     │
├─────────────────┼───────────┼───────────┼───────────┤
│ **TOTAL**       │ **100%** │ **0.53** │ **0.84** │ **0.73** │
└─────────────────┴───────────┴───────────┴───────────┘

✅ Recommended: Option B (Microservices)
   Confidence: 84%
```

---

## Decision Output

```yaml
Decision:
  selected_option: "option_b"
  score: 0.84
  confidence: 0.85
  
  reasoning: |
    "Selected Microservices Architecture because:
    
    1. Highest overall score (0.84)
    2. Best scalability (10/10) - critical for SaaS
    3. Best flexibility (10/10) - future growth
    4. High maintainability (9/10) - long-term success
    5. Good security (9/10) - important for e-commerce
    
    Rejected Option A (Monolithic) because:
    - Lower scalability (5/10) - may not grow
    - Lower flexibility (4/10) - hard to adapt
    
    Rejected Option C (Serverless) because:
    - Higher vendor lock-in (2/10) - business risk
    - Medium complexity (6/10) - harder to manage"
    
  alternatives_considered:
    - option_a: "Not selected - scalability risk"
    - option_c: "Not selected - vendor lock-in"
```

---

## Related Documents

- [Reasoning-Graph.md](./04-Reasoning-Graph.md)
- [Risk-Engine.md](./07-Risk-Engine.md)
- [Strategy-Engine.md](../02-Decision-System/02-Strategy-Engine.md)
