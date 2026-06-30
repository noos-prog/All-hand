# Core Brain Components

> **All 10 internal layers of the Core Brain.**

---

## Components Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Core Brain                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Goal Interpreter         → Transform user input          │
│            ↓                                                │
│  2. Context Builder         → Build unified context          │
│            ↓                                                │
│  3. Knowledge Engine        → Search internal knowledge      │
│            ↓                                                │
│  4. Decision Engine         → Make all decisions            │
│            ↓                                                │
│  5. Planning Engine         → Create task graphs             │
│            ↓                                                │
│  6. Capability Selector     → Choose best tool              │
│            ↓                                                │
│  7. Execution Manager       → Route tasks to tools          │
│            ↓                                                │
│  8. Verification Engine     → Validate results              │
│            ↓                                                │
│  9. Recovery Engine         → Handle failures               │
│            ↓                                                │
│ 10. Learning Engine         → Learn from execution          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Index

| # | Component | Purpose | Type |
|---|-----------|---------|------|
| 1 | Goal Interpreter | Transform input to Goal Object | Input |
| 2 | Context Builder | Aggregate context | Input |
| 3 | Knowledge Engine | Search internal knowledge | Input |
| 4 | Decision Engine | Make all decisions | Core |
| 5 | Planning Engine | Create Task Graph | Core |
| 6 | Capability Selector | Choose best tool | Core |
| 7 | Execution Manager | Route to tools | Output |
| 8 | Verification Engine | Validate results | Quality |
| 9 | Recovery Engine | Handle failures | Quality |
| 10 | Learning Engine | Learn from experience | Feedback |

---

## Data Flow

```
User Input
     │
     ▼
┌────────────────┐
│Goal Interpreter│ → Goal Object
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Context Builder │ → UnifiedContext
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Knowledge Engine│ → KnowledgeContext
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Decision Engine │ ← All components
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Planning Engine │ → TaskGraph
└───────┬────────┘
        │
        ▼
┌────────────────────┐
│Capability Selector │ → ToolSelection
└───────┬────────────┘
        │
        ▼
┌────────────────┐
│Execution Mgr   │ → ToolExecution
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Verification    │ → VerificationResult
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Recovery Engine│ → RecoveryAction
└───────┬────────┘
        │
        ▼
┌────────────────┐
│Learning Engine│ → KnowledgeUpdate
└────────────────┘
```

---

## Component Specifications

Each component follows this interface:

```yaml
Component:
  name: string
  version: string
  
  inputs: list        # Expected inputs
  outputs: list      # Produced outputs
  
  dependencies: list  # Other components needed
  
  responsibilities: list
  boundaries: list    # What it does NOT do
  
  error_handling: dict
  timeout: duration
  
  metrics: list       # What to measure
```

---

## Related Documents

- [Execution-Manager.md](./02-Execution-Manager.md)
- [Verification-Engine.md](./03-Verification-Engine.md)
- [Recovery-Engine.md](./04-Recovery-Engine.md)
- [Learning-Engine.md](./05-Learning-Engine.md)
- [Capability-Selector.md](./06-Capability-Selector.md)
