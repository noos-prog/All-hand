# ADR-R001: Providers Must Pass ARI

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: ACCEPTED

---

## Context

Currently, Providers can be added to AGOS Core Brain without verification.

This leads to:
- Untested Providers in production
- Quality variations
- Unexpected failures
- User trust issues

---

## Decision

> **Every Provider must pass ARI before Core Brain uses it.**

```
Provider wants to join AGOS:
    │
    ▼
Submit to ARI:
    │
    ▼
Benchmark:
    │
    ▼
Pass ARI Threshold?
    │
Yes │ No
    │   │
    │   ▼
    │   Reject
    │   │
    │   │
    ▼   │
Join Core Brain ◄───┘
```

---

## Requirements

### ARI Certification Requirements

```yaml
CertificationRequirements:
  benchamarks:
    minimum_benchmarks: 100
    minimum_tasks: 50
    
  success_rate:
    minimum_rate: 0.75
    
  latency:
    maximum_avg: "60 seconds"
    
  cost:
    maximum_avg: "$1.00 per task"
    
  security:
    no_critical_vulnerabilities: true
    no_high_vulnerabilities: true
    
  reliability:
    minimum_uptime: 0.95
```

---

## Certification Tiers

### Tier 1: Basic

```yaml
Tier1_Basic:
  description: "Can be used in non-critical tasks"
  requirements:
    benchmarks: 50
    success_rate: 0.60
    uptime: 0.90
```

### Tier 2: Standard

```yaml
Tier2_Standard:
  description: "Can be used in standard tasks"
  requirements:
    benchmarks: 100
    success_rate: 0.75
    uptime: 0.95
```

### Tier 3: Premium

```yaml
Tier3_Premium:
  description: "Can be used in critical tasks"
  requirements:
    benchmarks: 500
    success_rate: 0.90
    uptime: 0.99
```

### Tier 4: Enterprise

```yaml
Tier4_Enterprise:
  description: "Can be used in mission-critical tasks"
  requirements:
    benchmarks: 1000
    success_rate: 0.95
    uptime: 0.999
```

---

## Recertification

```yaml
Recertification:
  frequency: "monthly"
  
  requirements:
    - Must maintain minimum benchmarks
    - Must maintain minimum success rate
    - Must pass continuous monitoring
    
  declassification:
    - Below Tier requirements → Tier downgrade
    - 3 months below Tier → Removed from Core Brain
```

---

## Implementation

```python
class ARICertification:
    """
    ARI Certification for Providers.
    """
    
    async def certify_provider(
        self,
        provider: Provider
    ) -> CertificationResult:
        """
        Certify a provider through ARI.
        """
        
        # 1. Run benchmarks
        benchmarks = await self.run_benchmarks(provider, count=100)
        
        # 2. Calculate scores
        scores = self.calculate_scores(benchmarks)
        
        # 3. Check requirements
        tier = self.determine_tier(scores)
        
        # 4. Generate certification
        if tier:
            return CertificationResult(
                certified=True,
                tier=tier,
                scores=scores,
                certificate_id=self.generate_id()
            )
        else:
            return CertificationResult(
                certified=False,
                reason="Does not meet minimum requirements",
                scores=scores
            )
```

---

## Consequences

### Positive

1. **Quality Assurance** - Only tested providers in Core
2. **User Trust** - Users know providers are verified
3. **Predictability** - Consistent quality
4. **Competition** - Providers compete on quality

### Negative

1. **Barrier to Entry** - Some providers may not qualify
2. **Time** - Certification takes time
3. **Cost** - Running benchmarks costs resources

### Neutral

1. **Dynamic** - Can update certification anytime

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| **ADR-R001** | **Providers Must Pass ARI** | **This decision** |

---

## References

- [Research-Data-Lake.md](../01-Research-Data-Lake/README.md)
- [Evaluation-Engine.md](../06-Evaluation-Engine/README.md)
