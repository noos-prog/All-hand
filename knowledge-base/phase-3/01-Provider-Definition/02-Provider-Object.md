# Provider Object

> **Every external system transforms into this standardized Object.**

---

## Provider Object Schema

```yaml
Provider:
  # ========== Identification ==========
  id: string                    # Unique identifier
  name: string                 # Human-readable name
  slug: string                 # URL-safe identifier
  version: string              # Provider version
  vendor: string               # Vendor/company name
  
  # ========== Classification ==========
  type: enum                   # See Provider Types
  category: string            # Category within type
  subcategory: string          # Sub-category
  
  # ========== Description ==========
  description: string          # What it does
  long_description: string     # Detailed description
  website: string              # Provider website
  documentation: string        # Documentation URL
  
  # ========== Technical ==========
  interface:
    type: enum                # cli, api, sdk, docker, native
    endpoint: string          # For API type
    command: string           # For CLI type
    image: string              # For Docker type
    library: string            # For SDK/Library type
    
  authentication:
    type: enum                # none, api_key, oauth, token, key_file
    required_fields: list[string]
    secrets: list[string]     # Required secrets
    
  protocols:
    - name: string            # http, https, ws, grpc
      version: string
      port: integer           # If applicable
      
  # ========== Capabilities ==========
  capabilities:
    provided: list[CapabilityID]  # Capabilities this provides
    profiles: dict             # Capability profiles (see below)
    
  # ========== Capabilities Profiles ==========
  profiles:
    # For each capability, profile how well it performs
    
    cap_code_review:
      accuracy: enum          # excellent, high, good, medium, low
      speed: enum             # very_fast, fast, medium, slow
      cost: enum              # free, low, medium, high, very_high
      best_for:
        - "large_projects"
        - "complex_review"
      worst_for:
        - "quick_fixes"
      specializations:
        - "security_analysis"
        - "performance_review"
        
    cap_generate_code:
      accuracy: enum          # excellent, high, good, medium, low
      speed: enum             # very_fast, fast, medium, slow
      cost: enum              # free, low, medium, high, very_high
      best_for:
        - "new_features"
        - "complex_logic"
      worst_for:
        - "trivial_changes"
      specializations:
        - "api_generation"
        - "test_generation"
        
    # ... profile for each capability
    
  # ========== Performance ==========
  performance:
    latency:
      min: duration
      avg: duration
      max: duration
      p95: duration
      p99: duration
      
    throughput:
      requests_per_minute: integer
      concurrent_limit: integer
      
    reliability:
      uptime_percentage: decimal
      mtbf: duration          # Mean Time Between Failures
      mttr: duration          # Mean Time To Recovery
      
  # ========== Costs ==========
  costs:
    model: enum               # free, per_use, subscription, metered
    per_use: decimal          # Cost per execution
    monthly_subscription: decimal
    included_usage: integer   # For subscription
    overage_cost: decimal     # Per unit overage
    
  # ========== Resources ==========
  resources:
    memory_mb: integer
    cpu_cores: decimal
    gpu: boolean
    disk_mb: integer
    
  # ========== Deployment ==========
  deployment:
    type: enum               # cloud, local, hybrid
    regions: list[string]    # Available regions
    default_region: string
    latency_by_region:
      us-east: "50ms"
      eu-west: "150ms"
      ap-south: "250ms"
      
  # ========== Limits ==========
  limits:
    rate_limit:
      requests_per_minute: integer
      requests_per_day: integer
      burst: integer
    timeout:
      default: duration
      max: duration
    retry:
      max_attempts: integer
      backoff_strategy: enum
      
  # ========== Security ==========
  security:
    level: enum              # public, internal, restricted, confidential
    compliance: list[string]  # SOC2, HIPAA, GDPR, etc.
    data_residency: enum      # us, eu, ap, global
    encryption:
      in_transit: boolean
      at_rest: boolean
      
  # ========== Dependencies ==========
  dependencies:
    required: list[string]   # Required providers
    optional: list[string]    # Optional providers
    conflicts_with: list[string]  # Cannot run with
    
  # ========== Status ==========
  status:
    state: enum              # active, inactive, experimental, deprecated
    health: enum             # healthy, degraded, unhealthy, unknown
    last_health_check: datetime
    health_history: list[HealthRecord]
    
  # ========== Metadata ==========
  metadata:
    license: string
    repository: string
    source_available: boolean
    tags: list[string]
    rating: decimal          # Community rating
    reviews_count: integer
```

---

## Provider Capability Profile

> **Not every Provider delivers the same capability at the same level.**

```yaml
CapabilityProfile:
  capability_id: string
  
  # How well this Provider performs this capability
  
  # Accuracy/Quality
  accuracy: enum
    values: [excellent, high, good, medium, low]
    description: "Quality of output"
    
  # Speed
  speed: enum
    values: [very_fast, fast, medium, slow]
    description: "Execution speed"
    
  # Cost
  cost: enum
    values: [free, low, medium, high, very_high]
    description: "Cost per execution"
    
  # Quality Attributes
  quality_attributes:
    completeness: 0.0-1.0    # How complete is the output
    correctness: 0.0-1.0     # How correct is the output
    consistency: 0.0-1.0     # How consistent across runs
    
  # Use Case Fit
  best_for:
    - list[string]          # Task types this excels at
    
  worst_for:
    - list[string]           # Task types this struggles with
    
  # Specializations
  specializations:
    - list[string]           # Areas of expertise
    
  # Context Fit
  context_fit:
    development:
      score: 0.0-1.0
      notes: string
    staging:
      score: 0.0-1.0
      notes: string
    production:
      score: 0.0-1.0
      notes: string
      
  # Task Size Fit
  task_size_fit:
    small:
      score: 0.0-1.0
      description: "Quick fixes, small changes"
    medium:
      score: 0.0-1.0
      description: "Feature development"
    large:
      score: 0.0-1.0
      description: "Complex systems, architecture"
```

---

## Provider Profile Examples

### Code Review Capability

```yaml
cap_code_review:

  provider_openhands:
    accuracy: "high"
    speed: "medium"
    cost: "medium"
    quality_attributes:
      completeness: 0.92
      correctness: 0.95
      consistency: 0.88
    best_for:
      - "large_projects"
      - "complex_review"
      - "security_focus"
    worst_for:
      - "quick_fixes"
      - "trivial_changes"
    specializations:
      - "security_analysis"
      - "performance_review"
      - "architecture_review"
    context_fit:
      development: {score: 0.85, notes: "Good for PR reviews"}
      staging: {score: 0.90, notes: "Great for pre-prod"}
      production: {score: 0.95, notes: "Excellent for critical"}
      
  provider_aider:
    accuracy: "good"
    speed: "fast"
    cost: "low"
    quality_attributes:
      completeness: 0.82
      correctness: 0.85
      consistency: 0.90
    best_for:
      - "quick_fixes"
      - "small_changes"
      - "iterative_review"
    worst_for:
      - "large_projects"
      - "complex_analysis"
    specializations:
      - "syntax_errors"
      - "obvious_bugs"
    context_fit:
      development: {score: 0.92, notes: "Fast for quick review"}
      staging: {score: 0.80, notes: "Good for quick checks"}
      production: {score: 0.70, notes: "May miss complex issues"}
      
  provider_semgrep:
    accuracy: "excellent"
    speed: "fast"
    cost: "low"
    quality_attributes:
      completeness: 0.95
      correctness: 0.98
      consistency: 0.99
    best_for:
      - "security_analysis"
      - "pattern_detection"
      - "static_analysis"
    worst_for:
      - "architecture_review"
      - "business_logic"
    specializations:
      - "vulnerability_detection"
      - "code_smells"
      - "best_practice_enforcement"
```

### Generate Code Capability

```yaml
cap_generate_code:

  provider_openhands:
    accuracy: "high"
    speed: "medium"
    cost: "medium"
    quality_attributes:
      completeness: 0.95
      correctness: 0.93
      consistency: 0.90
    best_for:
      - "new_features"
      - "complex_logic"
      - "full_modules"
    worst_for:
      - "trivial_changes"
      - "one_liners"
    specializations:
      - "api_generation"
      - "test_generation"
      - "documentation"
      
  provider_claude:
    accuracy: "high"
    speed: "fast"
    cost: "high"
    quality_attributes:
      completeness: 0.97
      correctness: 0.95
      consistency: 0.92
    best_for:
      - "complex_logic"
      - "algorithm_implementation"
      - "architectural_decisions"
    worst_for:
      - "bulk_generation"
      - "template_based"
    specializations:
      - "reasoning"
      - "context_understanding"
```

---

## Selection with Profiles

```python
def select_best_provider(
    capability_id: str,
    context: Context
) -> Provider:
    """
    Select best provider using capability profiles.
    """
    
    # 1. Get all providers for this capability
    providers = registry.get_providers(capability_id)
    
    # 2. Score each provider based on context
    scored = []
    for provider in providers:
        profile = provider.profiles[capability_id]
        
        score = calculate_profile_score(
            profile=profile,
            context=context
        )
        
        scored.append((provider, score))
    
    # 3. Sort by score
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    
    return ranked[0][0]


def calculate_profile_score(
    profile: CapabilityProfile,
    context: Context
) -> float:
    """
    Calculate score based on profile and context.
    """
    
    score = 0.0
    
    # Match accuracy to priority
    if context.priority == "quality":
        score += accuracy_to_score(profile.accuracy) * 0.40
        
    # Match speed to time constraint
    if context.time_critical:
        score += speed_to_score(profile.speed) * 0.35
        
    # Match cost to budget
    if context.budget == "tight":
        score += cost_to_score(profile.cost) * 0.25
        
    # Context fit bonus
    score += profile.context_fit.get(context.environment, 0.5) * 0.20
    
    # Task size fit
    score += profile.task_size_fit.get(context.task_size, 0.5) * 0.15
    
    return score
```

---

## Related Documents

- [Provider-Overview.md](./01-Provider-Overview.md)
- [Interface-Overview.md](../03-Provider-Interface/01-Interface-Overview.md)
