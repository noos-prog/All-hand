# ADR-036: Architecture Over Intelligence

> **Architecture Decision Record — The Most Important ADR**

---

## Status

**Proposed**: 2024-01-15  
**Status**: ACCEPTED — FOUNDATIONAL

---

## Context

The AI industry is changing rapidly:
- Models appear and disappear
- Providers come and go
- Technologies evolve

Most platforms build around:
- A single AI model
- A single provider
- A single tool

When the underlying technology changes, they must rebuild.

---

## Decision

> **"Architecture Over Intelligence"**

If the architecture is right, we can replace and improve models and tools for the next 10 years without rebuilding.

If the architecture is wrong, even the most powerful AI will not save the platform.

---

## The Hierarchy

```
ARCHITECTURE
    ↓
Contracts
    ↓
Core Brain
    ↓
Capabilities
    ↓
Providers
    ↓
Models
    ↓
Tools

Everything above can change.
Architecture and Contracts must remain.
```

---

## Why This Matters

### If Architecture is Wrong

```
Platform: "We use GPT-4 for everything"

Year 2025: GPT-4 is deprecated
Problem: Platform built around GPT-4
Result: Must rebuild from scratch

Cost: 2+ years of work
```

### If Architecture is Right

```
Platform: "We use Providers that implement Contracts"

Year 2025: GPT-4 is deprecated
Problem: One Provider no longer available
Action: Add new Provider that implements Contract
Result: Platform continues

Cost: 1 week of integration
```

---

## The Proof

```
IF we have:
- Contracts (fixed)
- Core Brain (stable)
- Capability Layer (stable)
- Provider Layer (extensible)

THEN we can:
- Replace Models ✓
- Replace Providers ✓
- Replace Tools ✓
- Add Capabilities ✓
- Improve Intelligence ✓

WITHOUT rebuilding the platform.
```

---

## Consequences

### Positive

1. **Longevity** - Platform survives technology changes
2. **Flexibility** - Can adopt new technologies quickly
3. **Innovation** - Can experiment without risk
4. **Vendor Freedom** - Not locked to any vendor

### Negative

1. **Complexity** - Architecture is more complex
2. **Abstraction** - Some overhead in layers

### Neutral

1. **Learning Curve** - Teams must understand architecture

---

## Implementation

### Correct Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Contracts (FIXED)                          │
│     Goal, Mission, Capability, Provider, Execution     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                    Core Brain (STABLE)                        │
│        Reasoning, Decision, Planning, Learning        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Capability Layer (STABLE)                     │
│           Registry, Selection, Verification             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                   Provider Layer (EXTENSIBLE)                   │
│           Adapters, Health, Failover, Ranking          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│               Model/Tool Layer (REPLACEABLE)                    │
│            Claude, GPT, OpenHands, Aider              │
└─────────────────────────────────────────────────────────┘
```

### Wrong Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      GPT-4 (SINGLE)                         │
│              Everything built around GPT-4             │
└─────────────────────────────────────────────────────────┘
                              ↓
        Platform depends on GPT-4
                              ↓
        If GPT-4 changes → Platform breaks
```

---

## The Key Insight

```
Architecture defines:
- WHAT can change
- WHAT must remain fixed

Technology is:
- WHAT changes frequently
- WHAT we want flexibility with

Therefore:
- Architecture = Fixed
- Technology = Flexible
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-001 | Single Core Brain | Foundation |
| ADR-034 | Everything Replaceable | Foundation |
| ADR-035 | Contracts Over Technologies | Foundation |
| **ADR-036** | **Architecture Over Intelligence** | **This decision** |

---

## References

- [Vision Document v1.0](./07-Vision-Document.md)
- [Kernel Contracts](./01-Kernel-Contracts/01-Contract-Overview.md)
