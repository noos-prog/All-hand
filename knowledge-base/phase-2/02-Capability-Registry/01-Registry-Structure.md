# Capability Registry Structure

> **Registry of Capabilities, not Tools.**

---

## Registry Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Capability Registry                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Generate Backend                                           │
│       │                                                     │
│       ├── Requirements                                      │
│       ├── Compatible Tools                                  │
│       ├── Ranking Rules                                     │
│       ├── Policies                                          │
│       └── Verification                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Registry Structure

```yaml
CapabilityRegistry:
  # ========== Metadata ==========
  id: string
  version: string
  created_at: datetime
  updated_at: datetime
  
  # ========== Capabilities ==========
  capabilities:
    cap_id:
      object: Capability
      providers: list[ProviderMapping]
      rankings: list[Rank]
      metrics: Metrics
      
  # ========== Providers ==========
  providers:
    provider_id:
      name: string
      capabilities: list[CapabilityID]
      adapter: string
      status: enum
      
  # ========== Rankings ==========
  rankings:
    cap_id:
      # Rankings by different criteria
      by_quality: list[ProviderID]
      by_speed: list[ProviderID]
      by_cost: list[ProviderID]
      by_reliability: list[ProviderID]
      by_context: list[ProviderID]
      
  # ========== Policies ==========
  policies:
    selection_policy: Policy
    fallback_policy: Policy
    verification_policy: Policy
    
  # ========== Metrics ==========
  metrics:
    system:
      total_capabilities: integer
      total_providers: integer
      avg_capabilities_per_provider: decimal
      
    performance:
      avg_selection_time: duration
      avg_execution_time: duration
      success_rate: percentage
```

---

## Registry Entry Example

```yaml
RegistryEntry:
  capability_id: "cap_generate_backend"
  
  capability:
    name: "Generate Backend"
    category: "coding"
    description: "Generate backend code from requirements"
    
  providers:
    - provider_id: "provider_openhands"
      adapter: "openhands-adapter"
      status: "active"
      supported_features:
        - "fastapi"
        - "django"
        - "flask"
        - "express"
        - "spring"
      unsupported_features: []
      
    - provider_id: "provider_aider"
      adapter: "aider-adapter"
      status: "active"
      supported_features:
        - "fastapi"
        - "flask"
        - "express"
      unsupported_features:
        - "django"
        - "spring"
        
    - provider_id: "provider_claude"
      adapter: "claude-adapter"
      status: "active"
      supported_features:
        - "fastapi"
        - "django"
        - "express"
        - "spring"
      unsupported_features: []
      
  rankings:
    by_quality:
      1. provider_claude (0.95)
      2. provider_openhands (0.92)
      3. provider_aider (0.85)
      
    by_speed:
      1. provider_aider (1 min)
      2. provider_openhands (3 min)
      3. provider_claude (5 min)
      
    by_cost:
      1. provider_aider ($0.01)
      2. provider_openhands ($0.05)
      3. provider_claude ($0.50)
      
    by_reliability:
      1. provider_claude (98%)
      2. provider_openhands (95%)
      3. provider_aider (90%)
      
    composite:
      1. provider_openhands (0.91)
      2. provider_aider (0.87)
      3. provider_claude (0.85)
      
  metrics:
    total_executions: 500
    success_rate: 0.93
    avg_duration: "3m"
    avg_cost: 0.04
    
  policies:
    verification_required: true
    verification_types: ["syntax", "lint", "tests"]
    retry_policy:
      max_retries: 2
```

---

## Provider Mapping

```yaml
ProviderMapping:
  provider_id: string
  capability_id: string
  
  # Adapter information
  adapter:
    type: enum              # cli, api, sdk, docker
    version: string
    endpoint: string        # For API adapters
    command: string         # For CLI adapters
    image: string           # For Docker adapters
    
  # Feature support
  supported_features: list[string]
  unsupported_features: list[string]
  
  # Configuration
  config:
    timeout: duration
    retries: integer
    custom_params: dict
    
  # Status
  status: enum              # active, inactive, experimental
  health: enum              # healthy, degraded, unhealthy
  
  # Scoring
  scores:
    quality: 0.0-1.0
    speed: 0.0-1.0
    cost: 0.0-1.0
    reliability: 0.0-1.0
    composite: 0.0-1.0
    
  # History
  history:
    total_executions: integer
    successful_executions: integer
    failed_executions: integer
    avg_duration: duration
    last_execution: datetime
```

---

## Registry Operations

### Add Capability

```python
def add_capability(capability: Capability) -> RegistryResult:
    """
    Add new capability to registry.
    """
    
    # 1. Validate capability
    validate(capability)
    
    # 2. Check for duplicates
    if exists(capability.id):
        raise DuplicateError(f"Capability {capability.id} exists")
    
    # 3. Validate dependencies
    validate_dependencies(capability)
    
    # 4. Add to registry
    registry.capabilities[capability.id] = capability
    
    # 5. Initialize rankings
    registry.rankings[capability.id] = Rankings()
    
    # 6. Initialize metrics
    registry.metrics[capability.id] = Metrics()
    
    return RegistryResult(success=True)
```

### Register Provider

```python
def register_provider(
    provider: Provider,
    capabilities: list[CapabilityID]
) -> RegistryResult:
    """
    Register a provider for capabilities.
    """
    
    # 1. Validate provider
    validate(provider)
    
    # 2. Add to registry
    registry.providers[provider.id] = provider
    
    # 3. Map to capabilities
    for cap_id in capabilities:
        if cap_id in registry.capabilities:
            registry.capabilities[cap_id].providers.append(
                ProviderMapping(provider=provider)
            )
        else:
            raise NotFoundError(f"Capability {cap_id} not found")
    
    # 4. Recalculate rankings
    recalculate_rankings(capabilities)
    
    return RegistryResult(success=True)
```

### Update Rankings

```python
def update_rankings(capability_id: str) -> Rankings:
    """
    Recalculate rankings for a capability.
    """
    
    # 1. Get all providers for this capability
    providers = registry.capabilities[capability_id].providers
    
    # 2. Calculate scores
    for provider in providers:
        provider.scores = calculate_scores(provider)
    
    # 3. Sort by different criteria
    rankings = Rankings(
        by_quality=sorted(providers, key=lambda p: p.scores.quality, reverse=True),
        by_speed=sorted(providers, key=lambda p: p.scores.speed, reverse=True),
        by_cost=sorted(providers, key=lambda p: p.scores.cost, reverse=True),
        by_reliability=sorted(providers, key=lambda p: p.scores.reliability, reverse=True),
        composite=sorted(providers, key=lambda p: p.scores.composite, reverse=True)
    )
    
    # 4. Store rankings
    registry.rankings[capability_id] = rankings
    
    return rankings
```

---

## Registry Search

```python
def search_capabilities(
    query: str,
    filters: Filters
) -> list[Capability]:
    """
    Search capabilities by name, description, tags.
    """
    
    results = []
    
    for cap in registry.capabilities.values():
        # Text search
        if query:
            if (query.lower() in cap.name.lower() or
                query.lower() in cap.description.lower() or
                any(query.lower() in tag.lower() for tag in cap.tags)):
                results.append(cap)
        else:
            results.append(cap)
    
    # Apply filters
    if filters.category:
        results = [r for r in results if r.category == filters.category]
        
    if filters.min_success_rate:
        results = [r for r in results 
                   if r.metrics.success_rate >= filters.min_success_rate]
    
    return results


def find_capability_for_task(task: Task) -> Capability:
    """
    Find the best matching capability for a task.
    """
    
    # 1. Extract required capabilities from task
    required = extract_capabilities(task)
    
    # 2. Search registry
    matches = []
    for cap_id in required:
        if cap_id in registry.capabilities:
            matches.append(registry.capabilities[cap_id])
    
    return matches
```

---

## Registry Metrics

```yaml
RegistryMetrics:
  # Capability metrics
  by_capability:
    cap_generate_code:
      total_executions: 1500
      success_rate: 0.92
      avg_duration: "3m 30s"
      avg_cost: 0.04
      provider_distribution:
        provider_openhands: 800
        provider_aider: 500
        provider_claude: 200
        
  # Provider metrics
  by_provider:
    provider_openhands:
      total_executions: 2500
      capabilities_offered: 45
      avg_success_rate: 0.93
      avg_cost: 0.05
      
  # System metrics
  system:
    total_capabilities: 91
    total_providers: 15
    avg_executions_per_capability: 150
    avg_providers_per_capability: 5.2
```

---

## Related Documents

- [Capability-Overview.md](../01-Capability-Definition/01-Capability-Overview.md)
- [Provider-Mapping.md](./02-Provider-Mapping.md)
- [Capability-Ranking.md](./03-Capability-Ranking.md)
