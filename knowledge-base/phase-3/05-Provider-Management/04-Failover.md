# Provider Failover

> **If a Provider fails, the system automatically switches to the next one.**

---

## Failover Concept

```
Primary Provider
      │
      │ Fails
      ▼
Secondary Provider
      │
      │ Fails
      ▼
Third Provider
      │
      │ Success!
      ▼
Continue...
```

---

## Failover Levels

```yaml
FailoverLevels:
  RETRY:
    description: "Same provider, retry"
    triggers:
      - timeout
      - temporary_error
    max_attempts: 3
    
  SWITCH_PROVIDER:
    description: "Switch to another provider"
    triggers:
      - repeated_failure
      - provider_unavailable
    action: "select_next_best"
    
  SWITCH_CAPABILITY:
    description: "Switch to alternative capability"
    triggers:
      - all_providers_failed
      - capability_not_supported
    action: "find_alternative"
    
  ESCALATE:
    description: "Escalate to human"
    triggers:
      - all_options_exhausted
      - security_issue
    action: "notify_human"
```

---

## Provider Ranking for Failover

```yaml
FailoverRanking:
  # Providers ordered by failover priority
  
  for_capability: "generate_code"
  
  ranking:
    1: openhands        # Primary
    2: cline           # Secondary
    3: aider           # Tertiary
    4: claude          # Last resort
```

---

## Failover Implementation

```python
class ProviderFailover:
    """
    Handles provider failover automatically.
    """
    
    async def execute_with_failover(
        self,
        capability_id: str,
        inputs: dict,
        context: Context
    ) -> ProviderResult:
        """
        Execute with automatic failover.
        """
        
        # 1. Get ranked providers
        providers = await self.get_ranked_providers(
            capability_id=capability_id,
            context=context
        )
        
        errors = []
        
        # 2. Try each provider
        for provider in providers:
            try:
                # Execute
                result = await self.execute(
                    provider=provider,
                    capability_id=capability_id,
                    inputs=inputs
                )
                
                # If successful, return
                if result.success:
                    # Update metrics
                    await self.record_success(provider, capability_id)
                    return result
                    
            except ProviderError as e:
                # Log error
                errors.append({
                    "provider": provider.id,
                    "error": str(e)
                })
                
                # Record failure
                await self.record_failure(provider, capability_id)
                
                # Check if should continue
                if not self.should_continue(provider, e):
                    break
                    
                continue
                
        # 3. All providers failed
        raise AllProvidersFailedError(
            capability_id=capability_id,
            errors=errors
        )
```

---

## Failover Decision Tree

```
Provider Fails
      │
      ▼
Is it retryable?
      │
  Yes │ No
      │    │
      ▼    │
Try   │    ▼
same  │    Is it switchable?
prov- │    │
ider  │    │
      │ Yes│ No
      │    │
      ▼    │
Try   │    ▼
again │    Is capability switchable?
      │    │
      │ Yes│ No
      │    │
      ▼    │
Success?│  ▼
      │   Try
 Yes   │  other
      │  capab-
      ▼  ility
Return │    │
result │ Yes│ No
       │    │
       ▼    │
      Try   │  ▼
      oth- │  Esca-
      er   │  late
      cap- │    │
      abil- │    ▼
      ity  │   Human
            │
            ▼
       Return Error
```

---

## Circuit Breaker Pattern

```yaml
CircuitBreaker:
  # Prevents repeated calls to failing provider
  
  states:
    CLOSED:
      description: "Normal operation"
      action: "Allow requests"
      
    OPEN:
      description: "Provider is failing"
      action: "Reject requests, use fallback"
      
    HALF_OPEN:
      description: "Testing recovery"
      action: "Allow limited requests"
      
  transitions:
    CLOSED → OPEN:
      trigger: "5 failures in 60 seconds"
      
    OPEN → HALF_OPEN:
      trigger: "30 seconds passed"
      
    HALF_OPEN → CLOSED:
      trigger: "3 consecutive successes"
      
    HALF_OPEN → OPEN:
      trigger: "Any failure"
```

---

## Example: Deploy with Failover

```
Capability: deploy

Providers ranked:
1. GitHub Actions (Primary)
2. GitLab CI (Secondary)
3. Jenkins (Tertiary)
4. ArgoCD (Last resort)

Execution:
1. Try GitHub Actions
   - Fails (rate limit)
   
2. Try GitLab CI
   - Fails (auth error)
   
3. Try Jenkins
   - Success!
   
4. Return Jenkins result
5. Update metrics: GitHub ↓, GitLab ↓, Jenkins ↑

User sees: Deployment successful (via Jenkins)
```

---

## Failover Metrics

```yaml
FailoverMetrics:
  # Track failover effectiveness
  
  overall:
    total_failovers: 500
    successful_failovers: 480
    failover_success_rate: 96%
    avg_failover_time: "2.5 seconds"
    
  by_capability:
    deploy:
      failovers: 50
      success_rate: 98%
      avg_providers_tried: 1.5
      
    generate_code:
      failovers: 200
      success_rate: 95%
      avg_providers_tried: 1.3
      
  by_provider:
    openhands:
      times_failed: 30
      failovers_from: 25
      failover_success: 23
```

---

## Related Documents

- [Health.md](./02-Health.md)
- [Provider-Selection.md](../06-Provider-Policies/01-Selection-Policy.md)
