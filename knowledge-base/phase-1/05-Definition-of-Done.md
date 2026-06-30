# Phase 1 Definition of Done

> **We do not move to 20% unless we can execute the following scenario entirely in theory.**

---

## Exit Scenario

**Scenario:** "Build a multi-tenant SaaS platform"

### Step 1: Receive Complex Request

```
Input: "Build a multi-tenant SaaS platform with:
       - User authentication and authorization
       - Tenant management
       - Subscription billing
       - Real-time notifications
       - Admin dashboard
       - REST APIs
       - Frontend application
       - CI/CD pipeline
       - Production deployment"

Expected Output: Goal Object
```

✅ **Validated:** System can transform complex request into structured Goal Object

---

### Step 2: Build Task Graph with Dependencies

```
Goal Object
       ↓
Planning Engine
       ↓
TaskGraph:
  - task_1: Design Architecture (start)
  - task_2: Setup Backend Framework
  - task_3: Setup Database
  - task_4: Implement Auth
  - task_5: Implement Tenants
  - task_6: Implement Billing
  - task_7: Implement APIs
  - task_8: Implement Notifications
  - task_9: Build Frontend
  - task_10: Setup CI/CD
  - task_11: Deploy (end)

Dependencies mapped correctly
Parallel opportunities identified
```

✅ **Validated:** System can create DAG with correct dependencies

---

### Step 3: Identify Required Capabilities

```
For each task node:

task_1 → architect
task_2 → generate_backend
task_3 → setup_database
task_4 → generate_auth
task_5 → generate_backend
task_6 → generate_backend
task_7 → generate_api
task_8 → generate_notification_system
task_9 → generate_frontend
task_10 → setup_cicd
task_11 → deploy

All capabilities identified
```

✅ **Validated:** System can identify capabilities for each task

---

### Step 4: Select Best Tool for Each Capability

**For each capability, WITHOUT using tool names:**

```
Capability: generate_backend
       ↓
Capability Selector (no tool names)
       ↓
Candidates: [OpenHands, Aider, Claude Code, Goose, Cline]
       ↓
Scores calculated:
  - OpenHands: 0.91
  - Aider: 0.87
  - Claude Code: 0.85
  - Goose: 0.78
  - Cline: 0.75
       ↓
Selection: OpenHands (highest score)
Reasoning: "Best overall score for generate_backend capability"
       ↓
Alternative: Aider (second choice if OpenHands fails)
```

✅ **Validated:** System selects by capability, not name

---

### Step 5: Replace Any Tool Without Changing Core

**Scenario:** Replace OpenHands with Claude Code

```
Current: OpenHands selected for generate_backend
       ↓
New Requirement: Use Claude Code instead
       ↓
Action: Only change capability → tool mapping
       ↓
Core Brain Logic: NO CHANGE
       ↓
Same capability: generate_backend
       ↓
New tool: Claude Code
       ↓
Result: Task executes with Claude Code
```

✅ **Validated:** Tool replacement requires zero Core changes

---

### Step 6: All Decisions Are Explainable

```
Decision: Selected OpenHands for generate_backend

Explainability Record:
  """
  Decision: Tool Selection
  Capability: generate_backend
  Selected: OpenHands
  Confidence: 0.91 (HIGH)
  
  Reasoning:
  1. Highest composite score (0.91)
  2. Best capability fit (0.95) for generate_backend
  3. High quality score (0.92) based on 150+ executions
  4. Good reliability (0.95) with 96% success rate
  5. Within budget ($0.05/task)
  
  Alternatives considered:
  - Aider (0.87): Lower capability fit (0.85)
  - Claude Code (0.85): Higher cost ($0.50 vs $0.05)
  - Goose (0.78): Less experience with backend
  - Cline (0.75): VS Code dependency
  
  Policies applied:
  - PriorityBasedSelection
  - ProductionEnvironmentPolicy
  
  Why not others:
  - Aider: Lower quality score for this task type
  - Claude Code: Cost exceeds budget constraints
  """
```

✅ **Validated:** Every decision has full reasoning trace

---

## Self-Assessment Checklist

### Goal Interpretation
- [ ] Can parse complex natural language
- [ ] Extracts constraints automatically
- [ ] Generates complete Goal Object
- [ ] Handles ambiguous inputs
- [ ] Validates goal feasibility

### Context Building
- [ ] Aggregates from multiple sources
- [ ] Builds Unified Context
- [ ] Scores relevance
- [ ] Handles missing context
- [ ] Validates completeness

### Knowledge Engine
- [ ] Searches internal Knowledge Base
- [ ] Returns relevant results
- [ ] Handles multiple query types
- [ ] Updates knowledge
- [ ] Caches effectively

### Decision Engine
- [ ] Central hub for decisions
- [ ] Applies policies consistently
- [ ] Scores alternatives
- [ ] Generates reasoning
- [ ] Logs all decisions

### Planning Engine
- [ ] Creates Task Graphs (DAGs)
- [ ] Handles dependencies
- [ ] Identifies parallel opportunities
- [ ] Calculates critical path
- [ ] Validates graph

### Capability Selector
- [ ] Selects by capability, not name
- [ ] Calculates composite scores
- [ ] Applies context weights
- [ ] Provides alternatives
- [ ] Explains selection

### Execution Manager
- [ ] Routes tasks to tools
- [ ] Manages queue
- [ ] Handles timeouts
- [ ] Collects results
- [ ] Reports status

### Verification Engine
- [ ] Runs verification pipeline
- [ ] Validates outputs
- [ ] Reports issues
- [ ] Recommends fixes
- [ ] Tracks verification history

### Recovery Engine
- [ ] Handles failures
- [ ] Implements retry logic
- [ ] Selects alternatives
- [ ] Tracks failure patterns
- [ ] Implements circuit breaker

### Learning Engine
- [ ] Records executions
- [ ] Updates tool scores
- [ ] Detects patterns
- [ ] Refines weights
- [ ] Stores learning

---

## Quantitative Metrics

| Metric | Threshold | Validation |
|--------|-----------|------------|
| Goal parsing accuracy | > 95% | Test on 100+ goals |
| Task graph validity | 100% | No cycles, all deps met |
| Decision explainability | 100% | Every decision has reasoning |
| Tool selection accuracy | > 90% | Matches human selection |
| Recovery success rate | > 90% | Of failures recovered |
| Learning improvement | > 5% | Score accuracy over time |

---

## Final Validation

**Before moving to Phase 2 (20%):**

1. ✅ All 10 components specified
2. ✅ All data objects defined
3. ✅ All policies written
4. ✅ All rules documented
5. ✅ Explainability guaranteed
6. ✅ Tool replacement validated
7. ✅ Scenario executable in theory

---

## Related Documents

- [01-Core-Brain-Overview.md](./01-Core-Brain/01-Core-Brain-Overview.md)
- [Brain-Rules.md](./04-Policies/03-Brain-Rules.md)
