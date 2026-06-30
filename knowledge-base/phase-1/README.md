# Phase 1: Core Brain Specification

> **10% → 20%**

---

## 🎯 Goal

Build the single, true Brain of the system.

```
There is only ONE Brain.

Everything else is a tool.

Even OpenHands is a tool.
Even Cline is a tool.
Even Aider is a tool.
Even Browser Use is a tool.
Even any future agent is a tool.
```

---

## 📁 Structure

```
Phase 1/
├── 01-Core-Brain/
│   ├── 01-Core-Brain-Overview.md
│   ├── 02-Goal-Interpreter.md
│   ├── 03-Context-Builder.md
│   ├── 04-Knowledge-Engine.md
│   ├── 05-Decision-Engine.md
│   └── 06-Planning-Engine.md
│
├── 02-Components/
│   ├── 01-Components-Overview.md
│   ├── 02-Capability-Selector.md
│   ├── 03-Execution-Manager.md
│   ├── 04-Verification-Engine.md
│   ├── 05-Recovery-Engine.md
│   └── 06-Learning-Engine.md
│
├── 03-Objects/
│   ├── 01-Universal-Task-Object.md
│   └── 02-Universal-Result-Object.md
│
├── 04-Policies/
│   ├── 01-Decision-Policies.md
│   ├── 02-Capability-Selection-Algorithm.md
│   └── 03-Brain-Rules.md
│
└── 05-Definition-of-Done.md
```

---

## 🧠 Core Brain Layers

```
1. Goal Interpreter        → Transform user input
2. Context Builder        → Build unified context
3. Knowledge Engine       → Search internal knowledge
4. Decision Engine        → Make all decisions
5. Planning Engine        → Create task graphs (DAG)
6. Capability Selector    → Choose best tool (by capability)
7. Execution Manager      → Route tasks to tools
8. Verification Engine    → Validate results
9. Recovery Engine        → Handle failures
10. Learning Engine       → Learn from execution
```

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Core Brain                            │
│                                                             │
│  Brain NEVER:                                               │
│  ❌ Executes                                                 │
│  ❌ Edits                                                    │
│  ❌ Browses                                                  │
│  ❌ Deploys                                                  │
│  ❌ Compiles                                                 │
│  ❌ Searches Web                                             │
│                                                             │
│  Brain ONLY:                                                │
│  ✅ Thinks                                                   │
│  ✅ Decides                                                  │
│  ✅ Routes                                                   │
│  ✅ Verifies                                                 │
│  ✅ Learns                                                   │
│  ✅ Explains                                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Deliverables

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | Brain Responsibilities | ✅ |
| 2 | Forbidden Actions | ✅ |
| 3 | Internal Layers | ✅ |
| 4 | Goal Interpreter | ✅ |
| 5 | Context Builder | ✅ |
| 6 | Knowledge Engine | ✅ |
| 7 | Decision Engine | ✅ |
| 8 | Capability Selector | ✅ |
| 9 | Planning Engine | ✅ |
| 10 | Execution Manager | ✅ |
| 11 | Verification Engine | ✅ |
| 12 | Recovery Engine | ✅ |
| 13 | Learning Engine | ✅ |
| 14 | Capability Registry | ✅ |
| 15 | Universal Task Object | ✅ |
| 16 | Universal Result Object | ✅ |
| 17 | Decision Policies | ✅ |
| 18 | Selection Algorithm | ✅ |
| 19 | Brain Rules | ✅ |
| 20 | Definition of Done | ✅ |

---

## 🔑 Key Principles

### 1. Brain Never Executes
Brain only thinks, decides, routes, verifies, learns, and explains. All execution is delegated to tools.

### 2. No Tool Names in Decisions
```
❌ "Use OpenHands"
✅ "Need: Generate Backend API"
    → Best tool selected by score
```

### 3. Every Decision is Explainable
```
Not just: "Chose Tool X"
But also: "Why X over Y and Z?"
    - Criteria used
    - Weights applied
    - Scores calculated
```

### 4. Tool Replacement = Zero Core Changes
Any tool can be replaced without modifying Core Brain logic.

### 5. Task Graph over Task List
```
❌ Task List: [1, 2, 3, 4]
✅ Task Graph: DAG with dependencies
```

---

## 📊 Key Specifications

### Universal Task Object
Every task in the system:
- Task ID, Goal, Capability, Inputs, Outputs
- Constraints, Priority, Deadline
- Dependencies, Status, Retry
- Verification, Metrics, Quality

### Universal Result Object
Every tool returns:
- Status, Artifacts, Logs, Metrics
- Cost, Duration, Confidence
- Errors, Warnings, Evidence

### Capability Selection
Based on:
- Capability Score (30%)
- Quality Score (20%)
- Reliability (15%)
- Latency (10%)
- Cost (10%)
- Availability (5%)
- Context Fit (5%)
- Historical Success (5%)

---

## ✅ Exit Criteria

We do not move to Phase 2 unless:

1. ✅ System can receive complex request and convert to Goal Object
2. ✅ System can build Task Graph with dependencies
3. ✅ System can identify capabilities for each task
4. ✅ System can select best tool by capability (no names)
5. ✅ System can replace any tool without Core changes
6. ✅ All decisions are explainable

---

## 📚 Related Documents

- [Phase 0: Knowledge Base](../README.md)
- [Phase 2: Core Implementation] (pending)
