# Phase 4: Autonomous Reasoning Kernel (ARK)

> **40% → 50%**

---

## 🎯 Goal

Build the **thinking method itself**.

```
Not the LLM.

The reasoning engine that USES the LLM.

LLM = Inference Engine (replaceable)
ARK = Reasoning Kernel (core)
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Autonomous Reasoning Kernel                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                   CORE BRAIN                            │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Reasoning Engine                               │ │ │
│  │  │  - Intent Analysis                             │ │ │
│  │  │  - Context Fusion                              │ │ │
│  │  │  - Option Generator                           │ │ │
│  │  │  - Decision Matrix                            │ │ │
│  │  │  - Risk Engine                                │ │ │
│  │  │  - Strategy Engine                            │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Planning Engine                              │ │ │
│  │  │  - Planning Graph                             │ │ │
│  │  │  - Dependency Resolver                      │ │ │
│  │  │  - Execution Policy                         │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────────────────────┐ │ │
│  │  │  Learning Engine                              │ │ │
│  │  │  - Reflection                                │ │ │
│  │  │  - Knowledge Extraction                      │ │ │
│  │  │  - Experience Engine                        │ │ │
│  │  └─────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ↓ Uses (not controlled by)                                 │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                   LLM Provider                          │ │
│  │           (Inference Engine - Replaceable)              │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Principle

```
LLM ≠ Brain

LLM is an INFERENCE ENGINE.
ARK is the REASONING KERNEL.

LLM can be replaced.
ARK is the CORE.
```

---

## 📁 Structure

```
Phase 4/
├── 01-Reasoning-Engine/
│   ├── 01-Goal-Object.md
│   ├── 02-Intent-Analysis.md
│   ├── 03-Context-Fusion.md
│   ├── 04-Reasoning-Graph.md
│   ├── 05-Option-Generator.md
│   ├── 06-Decision-Matrix.md
│   └── 07-Risk-Engine.md
│
├── 02-Decision-System/
│   ├── 01-Decision-System.md
│   ├── 02-Strategy-Engine.md
│   └── 03-Explainability.md
│
├── 03-Planning-Engine/
│   ├── 01-Planning-Graph.md
│   ├── 02-Dependency-Resolver.md
│   └── 03-Execution-Policy.md
│
├── 04-Self-Correction/
│   ├── 01-Reflection.md
│   ├── 02-Self-Correction.md
│   └── 03-Knowledge-Extraction.md
│
├── 05-ADRs/
│   ├── 01-ADR-007-LLM-is-not-Brain.md
│   ├── 02-ADR-008-Reasoning-Chain.md
│   └── 03-ADR-009-Core-Brain-Decisions.md
│
└── 06-Definition-of-Done.md
```

---

## 🧠 Reasoning Chain (ADR-008)

```
Core Brain NEVER sends commands directly to Providers.

Every decision passes through:

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

## 🚫 What Core Brain Does NOT Do

```
Core Brain does NOT:

❌ Send direct commands to Providers
❌ Execute code
❌ Make LLM calls directly
❌ Build prompts manually
❌ Choose Providers by name

Core Brain ONLY:

✅ Analyzes goals
✅ Reasons about options
✅ Makes decisions
✅ Selects capabilities
✅ Verifies results
✅ Learns from outcomes
```

---

## 📋 Deliverables

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | Universal Goal Object | ✅ |
| 2 | Intent Analysis Engine | ✅ |
| 3 | Context Fusion Engine | ✅ |
| 4 | Reasoning Graph | ✅ |
| 5 | Option Generator | ✅ |
| 6 | Decision Matrix | ✅ |
| 7 | Risk Engine | ✅ |
| 8 | Strategy Engine | ✅ |
| 9 | Planning Graph | ✅ |
| 10 | Dependency Resolver | ✅ |
| 11 | Execution Policy Engine | ✅ |
| 12 | Verification Before Execution | ✅ |
| 13 | Reflection Engine | ✅ |
| 14 | Knowledge Extraction | ✅ |
| 15 | Experience Engine | ✅ |
| 16 | Explainability Engine | ✅ |
| 17 | Self-Correction Engine | ✅ |
| 18 | ADR-007: LLM ≠ Brain | ✅ |
| 19 | ADR-008: Reasoning Chain | ✅ |
| 20 | ADR-009: Core Brain Only Decisions | ✅ |

---

## ✅ Exit Criteria

We do not move to Phase 5 unless:

1. ✅ System can receive complex goal
2. ✅ Extract constraints, assumptions, unknowns
3. ✅ Generate multiple alternative strategies
4. ✅ Evaluate with decision matrix and risk analysis
5. ✅ Select best strategy with explanation
6. ✅ Convert to task graph
7. ✅ Map each task to capability, not provider
8. ✅ Re-plan automatically if conditions change
9. ✅ Record experience for future decisions

---

## 📚 Related Documents

- [Phase 3: Universal Provider Layer](../phase-3/README.md)
- [ADR-007: LLM ≠ Brain](./05-ADRs/01-ADR-007-LLM-is-not-Brain.md)
