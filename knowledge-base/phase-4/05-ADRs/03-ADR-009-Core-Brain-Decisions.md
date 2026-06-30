# ADR-009: Core Brain Only Decisions

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

External agents can provide **execution capabilities** and **analytical capabilities**.

But who makes strategic decisions?

Without clear separation:
- Agents become decision-makers
- System loses control
- Strategy becomes fragmented
- No accountability

---

## Decision

> **The system does NOT rely on any external agent for strategic decisions.**

External agents provide only **execution capabilities** or **analytical capabilities**.

**Strategic decisions are EXCLUSIVE to Core Brain.**

---

## Exclusive Core Brain Decisions

```yaml
ExclusiveDecisions:
  # These are Core Brain ONLY
  
  GOAL_DEFINITION:
    description: "Define and clarify goals"
    can_agent_do: false
    reason: "Core Brain understands context"
    
  STRATEGY_SELECTION:
    description: "Choose execution strategy"
    can_agent_do: false
    reason: "Core Brain weighs all factors"
    
  RISK_ASSESSMENT:
    description: "Evaluate and mitigate risks"
    can_agent_do: false
    reason: "Core Brain has system-wide view"
    
  PRIORITIZATION:
    description: "Set and adjust priorities"
    can_agent_do: false
    reason: "Core Brain knows dependencies"
    
  RESULT_ACCEPTANCE:
    description: "Accept or reject results"
    can_agent_do: false
    reason: "Core Brain verifies against criteria"
    
  RE_PLANNING:
    description: "Re-plan when conditions change"
    can_agent_do: false
    reason: "Core Brain understands impact"
```

---

## What External Agents CAN Do

```yaml
AgentCapabilities:
  # These are what agents CAN do
  
  EXECUTION:
    - "Generate code"
    - "Edit files"
    - "Run tests"
    - "Deploy applications"
    - "Execute commands"
    
  ANALYSIS:
    - "Analyze code quality"
    - "Find bugs"
    - "Suggest improvements"
    - "Review security"
    
  INFORMATION:
    - "Search documentation"
    - "Read files"
    - "Query databases"
    - "Browse websites"
```

---

## Decision Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 Strategic Decisions (Core Brain Only)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ External Agent decides goal                            │
│  ❌ External Agent chooses strategy                         │
│  ❌ External Agent accepts result                          │
│  ❌ External Agent re-plans                                │
│                                                             │
│  ✅ Core Brain: Goal Definition                            │
│  ✅ Core Brain: Strategy Selection                         │
│  ✅ Core Brain: Result Acceptance                          │
│  ✅ Core Brain: Re-planning                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Execution & Analysis (Agents Can Help)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ External Agent: Generate code                           │
│  ✅ External Agent: Analyze code                           │
│  ✅ External Agent: Execute commands                       │
│  ✅ External Agent: Find bugs                              │
│  ✅ External Agent: Review security                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Example: Building a Feature

```
WRONG APPROACH:
  Agent: "I'll build this feature using React"
  Problem: Agent decided strategy
  
RIGHT APPROACH:
  Core Brain:
    1. Analyzes goal → "Build feature X"
    2. Generates options → [React, Vue, Angular]
    3. Evaluates → Decision: React
    4. Selects capability → "generate_frontend"
    5. Selects provider → "openhands"
    
  Agent (OpenHands):
    1. Executes: Generate frontend code
    2. Returns result to Core Brain
    
  Core Brain:
    6. Verifies result
    7. Accepts or rejects
    8. Decides next step
```

---

## Example: Fixing a Bug

```
WRONG APPROACH:
  Agent: "I'll fix this bug using Aider"
  Problem: Agent decided approach
  
RIGHT APPROACH:
  Core Brain:
    1. Analyzes bug → "Login failure"
    2. Assesses risk → "HIGH (affects all users)"
    3. Selects strategy → "Fix and verify thoroughly"
    4. Selects capability → "fix_bugs"
    5. Selects provider → "openhands" (high quality)
    
  Agent (OpenHands):
    1. Analyzes bug
    2. Creates fix
    3. Runs tests
    4. Returns result
    
  Core Brain:
    6. Verifies fix
    7. If quality insufficient → Request rework
    8. If acceptable → Accept
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Core Brain                               │
│                                                             │
│  Strategic Decisions:                                        │
│  ✅ Goal Definition                                         │
│  ✅ Strategy Selection                                      │
│  ✅ Risk Assessment                                         │
│  ✅ Prioritization                                          │
│  ✅ Result Acceptance                                       │
│  ✅ Re-planning                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Capability Engine                            │
│                                                             │
│  Translates decisions to capabilities:                        │
│  Strategy → Capabilities → Providers                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Agents                             │
│                                                             │
│  Execution & Analysis ONLY:                                  │
│  - Generate code                                           │
│  - Analyze code                                            │
│  - Execute commands                                         │
│  - Find bugs                                               │
│  - Review security                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Why This Matters

### Without ADR-009

```
Agent: "I think we should use NoSQL"
Agent: "I'll deploy to production now"
Agent: "This fix is good enough"

Result:
- Uncontrolled decisions
- No accountability
- Inconsistent strategy
- Risk of failures
```

### With ADR-009

```
Core Brain: "Based on analysis, use PostgreSQL"
Core Brain: "Deploy after verification"
Core Brain: "This fix doesn't meet criteria, rework"

Result:
- Consistent decisions
- Clear accountability
- Strategic alignment
- Controlled risk
```

---

## Enforcement

```python
class DecisionEnforcement:
    """
    Enforce Core Brain exclusive decisions.
    """
    
    def validate_decision(self, decision: Decision):
        """
        Validate this is Core Brain's decision.
        """
        
        exclusive_for_core = [
            "GOAL_DEFINITION",
            "STRATEGY_SELECTION",
            "RISK_ASSESSMENT",
            "PRIORITIZATION",
            "RESULT_ACCEPTANCE",
            "RE_PLANNING"
        ]
        
        if decision.type in exclusive_for_core:
            if decision.decided_by != "core_brain":
                raise DecisionError(
                    f"Exclusive decision must be made by Core Brain: {decision.type}"
                )
                
        return True
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-007 | LLM is NOT Brain | Foundation |
| ADR-008 | Reasoning Chain | Foundation |
| **ADR-009** | **Core Brain Only Decisions** | **This decision** |

---

## References

- [Decision-System.md](../02-Decision-System/01-Decision-System.md)
- [Strategy-Engine.md](../02-Decision-System/02-Strategy-Engine.md)
