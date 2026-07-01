# AGOS Kernel v1.0.0

> **The only executable component in AGOS.**

---

## Directory Structure

```
agos-kernel/
├── core/
├── context/
├── decision/
├── execution/
├── mission/
├── registry/
├── contracts/
├── events/
├── interfaces/
├── shared/
├── capabilities/
├── providers/
├── discovery/
├── resolvers/
├── pipeline/
├── mission-engine/
├── skill-engine/
├── container/
├── event-engine/
├── bootstrapper/
├── contract-engine/
├── diagnostics/
├── knowledge/              ← EXEC-000021
├── models/                ← EXEC-000022
├── decision-pipeline/     ← EXEC-000023
├── execution-context/      ← EXEC-000024
├── api/                   ← EXEC-000025
├── sdks/
├── main.py
├── test_integration.py
└── test_validation.py
```

---

## Public APIs

| API | Description |
|-----|-------------|
| IKernelAPI | Kernel operations |
| ICapabilityAPI | Capability operations |
| IProviderAPI | Provider operations |
| IMissionAPI | Mission operations |
| IExecutionAPI | Execution operations |
| IKnowledgeAPI | Knowledge operations |

---

## Version

```
v1.0.0 - EXEC-000021 to EXEC-000025
API SPECIFICATION v1.0 - FROZEN
```

---

*AGOS Kernel - The foundation of everything.*
