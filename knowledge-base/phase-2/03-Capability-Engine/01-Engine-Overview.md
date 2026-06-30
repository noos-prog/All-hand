# Capability Engine Overview

> **The heart of the system. Brain knows ONLY the Capability Engine.**

---

## Engine Purpose

```
The Capability Engine is the most important component in Phase 2.

Goal
   ↓
Tasks
   ↓
Capabilities
   ↓
Candidates
   ↓
Ranking
   ↓
Provider
   ↓
Verification
   ↓
Result

The Brain knows ONLY:
- Capability Engine
- Capability Engine
- Capability Engine
```

---

## Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Capability Engine                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Request Handler │  │ Capability      │                  │
│  │                 │  │ Selector        │                  │
│  └────────┬────────┘  └────────┬────────┘                  │
│           │                     │                            │
│           ▼                     ▼                            │
│  ┌─────────────────────────────────────────┐                │
│  │           Provider Manager               │                │
│  │  - Select best provider                 │                │
│  │  - Load adapters                        │                │
│  │  - Route requests                       │                │
│  └────────────────────┬────────────────────┘                │
│                       │                                      │
│                       ▼                                      │
│  ┌─────────────────────────────────────────┐                │
│  │          Execution Controller            │                │
│  │  - Execute capability                   │                │
│  │  - Handle timeouts                      │                │
│  │  - Collect results                      │                │
│  └─────────────────────────────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Request Flow

```
1. GOAL RECEIVED
      ↓
2. Goal → Tasks
      ↓
3. Tasks → Capabilities
      ↓
4. For Each Capability:
      ↓
   4.1 Query Registry
      ↓
   4.2 Get Candidates
      ↓
   4.3 Calculate Rankings
      ↓
   4.4 Select Best Provider
      ↓
   4.5 Execute via Adapter
      ↓
   4.6 Verify Result
      ↓
   4.7 Store Result
      ↓
5. Return Aggregated Result
```

---

## Core Methods

### Execute Capability

```python
async def execute_capability(
    capability_id: str,
    inputs: dict,
    context: Context
) -> Result:
    """
    Execute a capability by ID.
    No tool name involved.
    """
    
    # 1. Validate inputs
    validate_inputs(inputs, capability_id)
    
    # 2. Select best provider
    provider = await selector.select_provider(
        capability_id=capability_id,
        context=context
    )
    
    # 3. Get adapter
    adapter = adapter_manager.get_adapter(provider.adapter_id)
    
    # 4. Execute
    result = await adapter.execute(
        capability_id=capability_id,
        inputs=inputs
    )
    
    # 5. Verify
    verified = await verification_engine.verify(
        capability_id=capability_id,
        result=result
    )
    
    # 6. Learn
    await learning_engine.record(
        capability_id=capability_id,
        provider_id=provider.id,
        result=result
    )
    
    return result
```

### Select Provider

```python
async def select_provider(
    capability_id: str,
    context: Context
) -> Provider:
    """
    Select best provider for capability.
    """
    
    # 1. Get all providers
    providers = registry.get_providers(capability_id)
    
    # 2. Filter by constraints
    providers = filter_by_constraints(providers, context)
    
    # 3. Calculate scores
    scored = []
    for provider in providers:
        score = calculator.calculate_score(
            provider=provider,
            capability_id=capability_id,
            context=context
        )
        scored.append((provider, score))
    
    # 4. Sort by composite score
    ranked = sorted(scored, key=lambda x: x[1].composite, reverse=True)
    
    # 5. Return best
    return ranked[0][0]
```

---

## Provider Selection Algorithm

```yaml
SelectionAlgorithm:
  Step 1: "Get Candidates"
    → Query Registry
    → Get all providers for capability
    → Filter by status (active only)
    
  Step 2: "Apply Constraints"
    → Filter by timeout constraints
    → Filter by cost constraints
    → Filter by permission constraints
    
  Step 3: "Calculate Scores"
    → Quality Score (30%)
    → Reliability Score (20%)
    → Speed Score (15%)
    → Cost Score (15%)
    → Context Fit Score (10%)
    → Historical Score (10%)
    
  Step 4: "Apply Policies"
    → Priority-based adjustments
    → Environment-based adjustments
    → User preferences
    
  Step 5: "Select"
    → Return highest scoring provider
    → Also return alternatives for fallback
```

---

## Context-Aware Selection

```python
class ContextAwareSelector:
    """
    Selects provider based on context.
    """
    
    CONTEXT_WEIGHTS = {
        "development": {
            "speed": 0.40,
            "cost": 0.20,
            "quality": 0.20,
            "reliability": 0.10,
            "context_fit": 0.10
        },
        "staging": {
            "quality": 0.30,
            "reliability": 0.25,
            "speed": 0.15,
            "cost": 0.15,
            "context_fit": 0.15
        },
        "production": {
            "reliability": 0.35,
            "quality": 0.30,
            "context_fit": 0.15,
            "speed": 0.10,
            "cost": 0.10
        }
    }
    
    async def select(
        self,
        capability_id: str,
        context: Context
    ) -> Provider:
        """
        Context-aware provider selection.
        """
        
        # Get weights for this context
        weights = self.CONTEXT_WEIGHTS.get(
            context.environment,
            self.CONTEXT_WEIGHTS["development"]
        )
        
        # Apply weights to scoring
        # ... (rest of selection logic)
```

---

## Fallback Handling

```python
async def execute_with_fallback(
    capability_id: str,
    inputs: dict,
    context: Context
) -> Result:
    """
    Execute with automatic fallback if primary fails.
    """
    
    # 1. Get ranked providers
    providers = await selector.get_ranked_providers(
        capability_id=capability_id,
        context=context
    )
    
    errors = []
    
    # 2. Try each provider
    for provider in providers:
        try:
            # Execute
            result = await execute_capability(
                capability_id=capability_id,
                provider=provider,
                inputs=inputs
            )
            
            # If successful, return
            if result.success:
                return result
                
        except Exception as e:
            errors.append({
                "provider": provider.id,
                "error": str(e)
            })
            continue
    
    # 3. If all failed, return last error
    raise AllProvidersFailedError(
        capability_id=capability_id,
        errors=errors
    )
```

---

## Result Schema

```python
@dataclass
class CapabilityResult:
    # Identity
    request_id: str
    capability_id: str
    provider_id: str
    
    # Status
    success: bool
    status: str
    
    # Output
    artifacts: list[Artifact]
    data: dict
    message: str
    
    # Metrics
    execution_time: duration
    cost: decimal
    quality_score: float
    
    # Context
    provider_used: str
    providers_tried: list[str]
    
    # Debug
    logs: list[LogEntry]
    errors: list[Error]
```

---

## Metrics Collected

```yaml
Metrics:
  per_capability:
    - executions
    - success_rate
    - avg_duration
    - avg_cost
    
  per_provider:
    - executions per capability
    - success_rate per capability
    - avg_duration per capability
    - avg_cost per capability
    
  system:
    - total_executions
    - avg_provider_selection_time
    - fallback_rate
    - avg_result_quality
```

---

## Related Documents

- [Request-Processing.md](./02-Request-Processing.md)
- [Provider-Selection.md](./03-Provider-Selection.md)
- [Registry-Structure.md](../02-Capability-Registry/01-Registry-Structure.md)
