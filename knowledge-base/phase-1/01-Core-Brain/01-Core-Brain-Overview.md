# Core Brain Specification

> **Phase 1: 10% → 20%**

---

## Core Philosophy

```
The System consists of only three elements:

┌─────────────────────────────────────────────────────────────┐
│                         Core Brain                          │
│                    (The only "brain")                       │
│                    Only thinks, never executes              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Capability Engine                       │
│                (Routes requests to tools)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Universal Tool Adapter                     │
│              (Standardizes all external agents)              │
└─────────────────────────────────────────────────────────────┘

Anything else = Plugin
```

---

## Brain Responsibilities

> **The only one who can make decisions.**
> **No Tool has the right to decide.**

```
Receive Goal
      ↓
Understand Goal
      ↓
Analyze
      ↓
Plan
      ↓
Select Capabilities
      ↓
Execute
      ↓
Verify
      ↓
Retry
      ↓
Finish
```

---

## What Core Brain CANNOT Do

| Forbidden Action | Reason |
|------------------|-------|
| ❌ Write code itself | Only tools execute |
| ❌ Open GitHub | Only tools interact |
| ❌ Run Docker | Only tools execute |
| ❌ Use Browser | Only tools browse |
| ❌ Edit Files | Only tools modify |
| ❌ Deploy | Only tools deploy |
| ❌ Review Code | Only tools review |

**Core Brain only thinks.**

---

## Internal Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      Core Brain                              │
├─────────────────────────────────────────────────────────────┤
│  1. Goal Interpreter                                        │
│            ↓                                                │
│  2. Context Builder                                          │
│            ↓                                                │
│  3. Knowledge Engine                                         │
│            ↓                                                │
│  4. Decision Engine                                         │
│            ↓                                                │
│  5. Planning Engine                                         │
│            ↓                                                │
│  6. Capability Selector                                      │
│            ↓                                                │
│  7. Execution Manager                                       │
│            ↓                                                │
│  8. Verification Engine                                     │
│            ↓                                                │
│  9. Recovery Engine                                         │
│            ↓                                                │
│ 10. Learning Engine                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Brain Rules (Sacred)

```
Brain Never Executes
Brain Never Edits
Brain Never Browses
Brain Never Deploys
Brain Never Compiles
Brain Never Searches Web

Brain Only Thinks
Brain Only Decides
Brain Only Routes
Brain Only Verifies
```

---

## Key Principle: Explainability

> **Every decision Core Brain makes must be explainable.**

Not just: "Chose Tool X"
But also: "Why Tool X over Y and Z?"

This includes:
- Criteria used
- Weights applied
- Scores calculated
- Alternatives considered
- Rejection reasons

---

## Related Documents

- [02-Components](./02-Components/README.md) - Layer specifications
- [03-Objects](./03-Objects/README.md) - Data objects
- [04-Policies](./04-Policies/README.md) - Decision policies
