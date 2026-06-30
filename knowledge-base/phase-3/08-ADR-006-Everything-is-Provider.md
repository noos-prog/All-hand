# ADR-006: Everything is a Provider

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

The system needs to integrate diverse external systems:
- AI Agents (OpenHands, Cline, Aider)
- APIs (GitHub, Slack, Stripe)
- Databases (PostgreSQL, MongoDB)
- Container platforms (Docker, Kubernetes)
- Browsers (Playwright, Selenium)
- Search engines (Sourcegraph)
- CI/CD systems (GitHub Actions, Jenkins)

Previous approach:
- Treat each type differently
- Custom integration for each
- No uniform interface
- Hard to add new types

---

## Decision

> **Everything is a Provider.**

With this decision:
- Every external system is a Provider
- Every Provider implements the same interface
- Core Brain knows ONLY Provider
- Core Brain knows NOTHING about specific systems

---

## Provider Universe

```
┌─────────────────────────────────────────────────────────────┐
│                        All Providers                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  AI Agents                                                  │
│  ├── OpenHands ──► Provider                                │
│  ├── Cline ──────► Provider                                │
│  ├── Aider ──────► Provider                                │
│  ├── Goose ──────► Provider                                │
│  └── Claude ─────► Provider                                │
│                                                             │
│  APIs                                                       │
│  ├── GitHub ─────► Provider                                │
│  ├── Slack ──────► Provider                                │
│  ├── Stripe ─────► Provider                                │
│  └── AWS ────────► Provider                                │
│                                                             │
│  Databases                                                   │
│  ├── PostgreSQL ─► Provider                                │
│  ├── MongoDB ─────► Provider                                │
│  ├── Redis ───────► Provider                                │
│  └── Elasticsearch ► Provider                              │
│                                                             │
│  Containers                                                  │
│  ├── Docker ─────► Provider                                │
│  └── Kubernetes ─► Provider                                │
│                                                             │
│  Browsers                                                   │
│  ├── Playwright ─► Provider                                │
│  └── Selenium ───► Provider                                │
│                                                             │
│  And 100+ more...                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Consequences

### Positive

1. **Uniform Interface** - All providers work the same way
2. **Easy Addition** - Add new types without changing Core
3. **Provider Swapping** - Swap any provider without breaking system
4. **Vendor Agnostic** - Core doesn't know vendor names
5. **Type Agnostic** - Core doesn't know provider types
6. **Extensibility** - Future systems automatically supported

### Negative

1. **Adapter Overhead** - One adapter per provider type
2. **Interface Complexity** - Must handle all provider quirks
3. **Testing Effort** - Must test all adapters

### Neutral

1. **Documentation** - Must document all provider types
2. **Registry** - Must maintain provider registry

---

## Core Brain View

```
Core Brain NEVER knows:

❌ "OpenHands"
❌ "GitHub"
❌ "PostgreSQL"
❌ "Docker"
❌ "Playwright"
❌ "Stripe"

Core Brain ONLY knows:

✅ "Provider"
✅ "Capability"
✅ "Selection"
✅ "Execution"
```

---

## Adapter Pattern

```
External System
      │
      ▼
┌─────────────────┐
│  Provider       │
│  Adapter        │
│                 │
│  - Translates   │
│  - Authenticates│
│  - Formats      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Universal      │
│  Provider       │
│  Interface      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Core         │
│    Brain        │
└─────────────────┘
```

---

## Provider Types

| Type | Examples | Interface |
|------|----------|-----------|
| AI Agent | OpenHands, Cline, Aider | CLI/API |
| LLM | Claude, GPT-4, Gemini | API |
| MCP | Filesystem MCP, Git MCP | SDK |
| REST API | GitHub, Slack, Stripe | HTTP |
| CLI | Git, Docker, kubectl | Shell |
| Docker | Database containers, Build containers | Docker |
| Browser | Playwright, Selenium | SDK |
| Database | PostgreSQL, MongoDB, Redis | Native |
| Search | Sourcegraph, Algolia | API |
| CI/CD | GitHub Actions, Jenkins | API |
| Storage | S3, GCS, R2 | API |
| Queue | SQS, RabbitMQ, Kafka | API |
| Notification | Slack, Discord, PagerDuty | API |

---

## Adding New Provider Type

### Before ADR-006 (If it existed)

```
Adding "NewSystem":
1. Modify Core Brain
2. Add integration code
3. Handle authentication
4. Handle formatting
5. Handle errors
6. Test everything
7. Deploy
```

### After ADR-006

```
Adding "NewSystem":
1. Create adapter: NewSystemAdapter
2. Register in Provider Registry
3. Map capabilities
4. DONE - No Core changes
```

---

## Universal Provider Interface

```python
class UniversalProviderInterface:
    """
    Every provider must implement this.
    """
    
    async def validate(self, request) -> ValidationResult:
        pass
        
    async def authorize(self, request) -> AuthResult:
        pass
        
    async def prepare(self, request) -> PreparationResult:
        pass
        
    async def execute(self, request) -> ExecutionResult:
        pass
        
    async def collect(self, execution) -> CollectedResult:
        pass
        
    async def verify(self, result) -> VerificationResult:
        pass
```

---

## Provider Capability Profile

Not every provider delivers the same capability equally.

```yaml
cap_code_review:

  provider_openhands:
    accuracy: "high"
    speed: "medium"
    cost: "medium"
    best_for:
      - "large_projects"
      - "complex_review"

  provider_aider:
    accuracy: "good"
    speed: "fast"
    cost: "low"
    best_for:
      - "quick_fixes"
      - "small_changes"

  provider_semgrep:
    accuracy: "excellent"
    speed: "fast"
    cost: "low"
    best_for:
      - "static_analysis"
      - "security"
```

System selects best provider for:
- THIS type of task
- THIS context
- THIS priority

---

## Future-Proof

With this architecture, any future system is automatically supported:

```
Future Systems (2025-2030):
├── New AI Agent ────► Add Adapter ────► Done
├── New Database ────► Add Adapter ────► Done
├── New Platform ────► Add Adapter ────► Done
└── New Protocol ───► Add Adapter ────► Done

Core Brain: UNCHANGED
```

---

## Migration Guide

### For Existing Systems

1. Identify current integrations
2. Create adapters for each
3. Register as providers
4. Map capabilities
5. Test adapters
6. Switch to provider model
7. Remove old integration code

### For New Systems

1. Only use adapter pattern
2. Never call external systems directly
3. Always go through universal interface

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-001 | Single Core Brain | Foundation |
| ADR-002 | Agents as Tools | Foundation |
| ADR-003 | Cloud First | Constraint |
| ADR-004 | Universal Adapter | Foundation |
| ADR-005 | Capability Providers | Foundation |
| **ADR-006** | **Everything is Provider** | **This decision** |

---

## References

- [Provider Object](./01-Provider-Definition/02-Provider-Object.md)
- [Provider Types](./02-Provider-Types/01-Types-Overview.md)
- [Universal Interface](./03-Provider-Interface/01-Interface-Overview.md)
