# ADR-008: Reasoning Chain

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

The system must have a **structured reasoning process**.

Without it:
- Decisions are arbitrary
- No trace of reasoning
- No learning from decisions
- No explainability
- No self-correction

---

## Decision

> **Core Brain NEVER sends commands directly to Providers.**

Every decision passes through this chain:

```
Goal
    ↓
Reasoning
    ↓
Decision
    ↓
Capability
    ↓
Provider Selection
    ↓
Execution Policy
    ↓
Provider
    ↓
Verification
    ↓
Learning

Any decision bypassing this chain = Architecture Error
```

---

## Chain Steps

### Step 1: Goal

```
The reasoning starts with a Goal.

Goal = What needs to be achieved
```

### Step 2: Reasoning

```
ARK analyzes and reasons:

- What does this goal mean?
- What are the constraints?
- What are the options?
- What are the risks?
- What are the unknowns?

Output: Reasoning Graph
```

### Step 3: Decision

```
Based on reasoning, a decision is made.

Decision = Chosen approach

Must include:
- Why this approach?
- Why not alternatives?
- Confidence level
- Evidence
```

### Step 4: Capability

```
Decision is translated to a Capability.

Capability = What ability is needed

Example:
Decision: "Build backend API"
Capability: "generate_api"
```

### Step 5: Provider Selection

```
Capability is mapped to a Provider.

Provider = Who will execute

Selection based on:
- Capability match
- Health
- Reliability
- Quality
- Cost
- Latency
```

### Step 6: Execution Policy

```
Before execution, policy is set:

- Timeout?
- Retry policy?
- Fallback providers?
- Verification requirements?
- Approval needed?
```

### Step 7: Provider

```
Execute via the selected Provider.

Provider executes the capability.
```

### Step 8: Verification

```
Results are verified:

- Did it succeed?
- Is quality acceptable?
- Are constraints met?
- Should we retry?
- Should we fallback?
```

### Step 9: Learning

```
After verification, learn:

- What worked?
- What didn't?
- What can we improve?
- Update metrics
- Update recommendations
```

---

## Visualization

```
┌─────────────────────────────────────────────────────────────┐
│                     Reasoning Chain                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [1] GOAL                                                   │
│      │                                                      │
│      ▼                                                      │
│  [2] REASONING ──► Reasoning Graph                          │
│      │                                                      │
│      ▼                                                      │
│  [3] DECISION ───► Decision Matrix                          │
│      │                                                      │
│      ▼                                                      │
│  [4] CAPABILITY ──► Capability Registry                      │
│      │                                                      │
│      ▼                                                      │
│  [5] PROVIDER ────► Provider Selection                      │
│      │                                                      │
│      ▼                                                      │
│  [6] POLICY ──────► Execution Policy                        │
│      │                                                      │
│      ▼                                                      │
│  [7] PROVIDER ────► Execute                                │
│      │                                                      │
│      ▼                                                      │
│  [8] VERIFICATION ─► Verify Results                         │
│      │                                                      │
│      ▼                                                      │
│  [9] LEARNING ────► Update Knowledge                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Enforcement

```python
def enforce_reasoning_chain(decision: Decision):
    """
    Verify decision followed the chain.
    """
    
    required_steps = [
        "goal",
        "reasoning",
        "decision",
        "capability",
        "provider_selection",
        "execution_policy",
        "provider",
        "verification",
        "learning"
    ]
    
    missing = []
    for step in required_steps:
        if step not in decision.steps:
            missing.append(step)
            
    if missing:
        raise ArchitectureError(
            f"Decision bypassing reasoning chain: {missing}"
        )
```

---

## Examples

### Example 1: Build Feature

```
WRONG (bypassing chain):
  LLM: "I'll just use OpenHands to build this"

RIGHT (following chain):
  [1] Goal: "Build user authentication"
  [2] Reasoning: "Need secure auth with OAuth2"
  [3] Decision: "Use OAuth2 with JWT"
  [4] Capability: "generate_auth"
  [5] Provider: "openhands" (score: 0.92)
  [6] Policy: "retry: 2x, verify: full"
  [7] Execute: Via OpenHands adapter
  [8] Verify: Syntax, tests, security scan
  [9] Learn: "OpenHands good for auth"
```

### Example 2: Fix Bug

```
[1] Goal: "Fix login bug"
[2] Reasoning: "Bug in authentication flow"
[3] Decision: "Fix auth module"
[4] Capability: "fix_bugs"
[5] Provider: "aider" (score: 0.88)
[6] Policy: "retry: 1x, verify: tests"
[7] Execute: Via Aider adapter
[8] Verify: Tests pass
[9] Learn: "Aider fast for quick fixes"
```

---

## Self-Correction Example

```
During Execution:

[7] Execute: Provider fails
         │
         ▼
Should we continue chain?

YES:
  [8] Verify: Failed
         │
         ▼
  [3] Re-Decide: "Try alternative"
         │
         ▼
  [4] Capability: Same
         │
         ▼
  [5] Provider: "cline" (fallback)
         │
         ▼
  [6] Policy: "retry: 1x"
         │
         ▼
  [7] Execute: Via Cline
         │
         ▼
  [8] Verify: Success!
         │
         ▼
  [9] Learn: "Cline good fallback for bugs"
```

---

## Architecture Violation

```yaml
Violations:

  1. "LLM said use X directly"
     → Violation: No reasoning chain
     
  2. "Provider selected by name"
     → Violation: Must select by capability
     
  3. "Skipped verification"
     → Violation: Must verify
     
  4. "No learning recorded"
     → Violation: Must learn
     
  5. "Direct provider call"
     → Violation: Must use adapter
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-001 | Single Core Brain | Foundation |
| ADR-007 | LLM is NOT Brain | Foundation |
| **ADR-008** | **Reasoning Chain** | **This decision** |
| ADR-009 | Core Brain Only Decisions | Related |

---

## References

- [Decision-System.md](../02-Decision-System/01-Decision-System.md)
- [Reasoning-Graph.md](../01-Reasoning-Engine/04-Reasoning-Graph.md)
