# ADR-016: No Independent Agents

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

Common misconception:
- "Let the agent decide"
- "Agent has autonomy"
- "Agent chooses approach"

This leads to:
- Unpredictable behavior
- No accountability
- Strategy fragmentation
- Loss of control

---

## Decision

> **There is no independent agent that makes decisions.**

All Providers wait for Core Brain commands.

```
❌ Agent: "I'll decide what to do"
✅ Provider: "Waiting for Core Brain command"
```

---

## What Providers Do

```yaml
Provider Responsibilities:

  ✅ Execute capability when commanded
  ✅ Return results to Core Brain
  ✅ Report status
  ✅ Handle errors
  ✅ Follow security policies
  
  ❌ Decide what to execute
  ❌ Choose approach
  ❌ Skip verification
  ❌ Ignore policies
  ❌ Act independently
```

---

## What Core Brain Does

```yaml
Core Brain Responsibilities:

  ✅ Decide what to execute
  ✅ Choose approach
  ✅ Verify results
  ✅ Enforce policies
  ✅ Learn from outcomes
  
  ❌ Execute code directly
  ❌ Generate code
  ❌ Run tests
```

---

## Communication Flow

```
Core Brain
    │
    │ "Execute: generate_api"
    ▼
Provider (e.g., OpenHands)
    │
    │ (Executes command)
    ▼
Provider
    │
    │ "Result: API generated"
    ▼
Core Brain
    │
    │ (Verifies result)
    ▼
Core Brain
    │
    │ "Next: generate_tests"
    ▼
Provider
```

---

## Example

### WRONG: Independent Agent

```
Agent: "I think I should build the database first"
Agent: "Let me skip testing this time"
Agent: "I'll use MongoDB instead of PostgreSQL"

Problem:
- Agent making decisions
- No coordination
- No accountability
```

### RIGHT: Provider Pattern

```
Core Brain: "We need a database"
Core Brain: "Based on requirements: PostgreSQL"
Core Brain: "Provider: execute generate_database"

Provider: (Executes command)
Provider: "Database created"

Core Brain: "Good. Next: generate_api"
```

---

## Consequences

### Positive

1. **Predictability** - Always know what will happen
2. **Accountability** - Clear who made each decision
3. **Coordination** - All actions coordinated
4. **Control** - Full control over behavior
5. **Learnability** - Easy to trace and learn

### Negative

1. **Speed** - Slightly slower (adds coordination)
2. **Flexibility** - Less "autonomous" behavior

### Neutral

1. **Complexity** - Adds messaging layer

---

## Enforcement

```python
class ProviderPolicy:
    """
    Enforce no independent decisions.
    """
    
    def validate_provider_action(self, action: Action) -> bool:
        """
        Validate provider is following commands.
        """
        
        # Provider must have command
        if not action.command_id:
            raise PolicyViolation(
                "Provider cannot act without command"
            )
            
        # Provider must follow policy
        if not self.follows_policy(action):
            raise PolicyViolation(
                "Provider action violates policy"
            )
            
        return True
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-009 | Core Brain Only Decisions | Foundation |
| **ADR-016** | **No Independent Agents** | **This decision** |
| ADR-017 | Continuous Evolution | Related |

---

## References

- [Mission-Lifecycle.md](../01-Mission-Lifecycle/01-Lifecycle-Overview.md)
