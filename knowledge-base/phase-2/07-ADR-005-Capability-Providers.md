# ADR-005: Capability Providers

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

The system needs to integrate multiple AI coding agents (OpenHands, Cline, Aider, Goose, Browser Use, etc.) in a way that:
- Allows easy addition/removal of agents
- Enables quality-based selection
- Maintains flexibility for future agents
- Avoids vendor lock-in

Current approaches treat agents as:
1. **Standalone tools** - requiring direct integration
2. **Primary vs secondary** - creating hierarchy
3. **Replaceable** - but difficult to swap

---

## Decision

> **Agents are not private entities within the system; all are treated as Capability Providers.**

With this decision:
- OpenHands, Cline, Aider, Browser Use, Goose, and others become equal
- No "primary agent" exists except Core Brain
- Everything else is a replaceable, swappable, disableable provider

---

## Implementation

### Provider Model

```
Every agent becomes a Provider:

Provider
├── ID
├── Name
├── Adapter
├── Capabilities (list of what they can do)
├── Scores (quality per capability)
└── Status (active, inactive, experimental)
```

### Provider Examples

```yaml
Provider: OpenHands
  adapter: "openhands-adapter"
  capabilities:
    - generate_code
    - generate_api
    - edit_code
    - deploy
  scores:
    generate_code: 0.95
    generate_api: 0.92
  status: "active"

Provider: Cline
  adapter: "cline-adapter"
  capabilities:
    - generate_code
    - edit_code
    - search_code
  scores:
    generate_code: 0.88
    edit_code: 0.85
  status: "active"

Provider: Aider
  adapter: "aider-adapter"
  capabilities:
    - generate_code
    - edit_code
    - fix_bugs
  scores:
    generate_code: 0.85
    fix_bugs: 0.80
  status: "active"
```

---

## Consequences

### Positive

1. **No vendor lock-in** - Any agent can be replaced
2. **Quality selection** - Best agent for each task
3. **Easy addition** - New agents = new providers
4. **No hierarchy** - All agents equal from system view
5. **Flexibility** - Disable any agent without breaking system
6. **Testability** - Can mock providers for testing

### Negative

1. **Abstraction overhead** - Requires adapter layer
2. **Score maintenance** - Need to track quality metrics
3. **Selection complexity** - More decisions to make

### Neutral

1. **Adapter development** - One adapter per agent type
2. **Registry maintenance** - Keep capability mappings updated

---

## Rules

### System Rules

```
1. Core Brain does NOT know agent names
   - Only knows "Capability"
   
2. Capability Engine does NOT hardcode agents
   - Only knows "Provider"
   
3. Adapter translates "Provider" → "Agent"
   - No agent logic in Core
   
4. Registry maps Capability → Providers
   - Dynamic, configurable
```

### Provider Rules

```
1. Every provider must have an adapter
2. Every provider must register capabilities
3. Every provider must report scores
4. Providers can be enabled/disabled independently
5. Providers can be added without code changes
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Core Brain                            │
│                                                             │
│  Knows ONLY: Capability                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Capability Engine                            │
│                                                             │
│  Knows ONLY: Provider                                        │
│  Does NOT know: Agent names                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Provider Registry                          │
│                                                             │
│  Maps: Capability → [Provider, Provider, Provider]           │
│  Stores: Scores per provider per capability                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Adapters                               │
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ OpenHands   │ │ Cline       │ │ Aider       │        │
│  │ Adapter     │ │ Adapter     │ │ Adapter     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                          Agents                               │
│                                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │OpenHands│ │ Cline │ │ Aider │ │ Goose │              │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Adding a New Agent

```
Old Way (Before ADR-005):
1. Modify Core Brain
2. Add agent integration
3. Update decision logic
4. Test entire system
5. Deploy

New Way (After ADR-005):
1. Create adapter for agent
2. Register agent as Provider
3. Map capabilities
4. DONE - No Core changes
```

### Step-by-Step

```yaml
Step 1: Create Adapter
  - File: adapters/myagent_adapter.py
  - Implement: translate_requests, translate_responses
  
Step 2: Register Provider
  - Add to Provider Registry:
    provider_id: "myagent"
    adapter: "myagent_adapter"
    capabilities: ["generate_code", "edit_code"]
    
Step 3: Map Capabilities
  - Add to Registry:
    cap_generate_code.providers: ["myagent"]
    
Step 4: Done
  - System now uses myagent
  - No Core Brain changes
```

---

## Removing an Agent

```
Scenario: Remove "Goose" agent

Before:
  Provider Registry:
    - openhands: active
    - cline: active
    - aider: active
    - goose: active
    
Action:
  1. Set goose.status = "disabled"
  OR
  2. Remove goose from providers
  
After:
  - System continues with remaining providers
  - goose capabilities mapped to other providers
  - No workflow broken
```

---

## Selection Flow

```
Request: "Generate API for user management"

Step 1: Identify Capability
  → cap_generate_api

Step 2: Query Registry
  → Providers: [openhands, cline, aider, goose]

Step 3: Get Scores
  → openhands: 0.92
  → cline: 0.85
  → aider: 0.88
  → goose: 0.82

Step 4: Apply Context
  → Context: production, quality priority
  
Step 5: Select Best
  → openhands (highest score)

Step 6: Execute via Adapter
  → Adapter translates request
  → Calls OpenHands
  → Translates response
  → Returns Result

Step 7: Update Scores
  → Record execution result
  → Update success rate
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-001 | Single Core Brain | Foundation |
| ADR-002 | Agents as Tools | Foundation |
| ADR-003 | Cloud First | Constraint |
| ADR-004 | Universal Adapter | Foundation |
| **ADR-005** | **Capability Providers** | **This decision** |

---

## References

- [Capability Engine](../03-Capability-Engine/01-Engine-Overview.md)
- [Provider Registry](../02-Capability-Registry/01-Registry-Structure.md)
