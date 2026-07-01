# AGOS Kernel v0.3.0

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
├── contract-engine/    ← EXEC-000016
├── diagnostics/        ← EXEC-000017
├── sdks/              ← EXEC-000018, EXEC-000019
│   ├── capability/
│   └── provider/
├── main.py
├── test_integration.py
└── test_validation.py  ← EXEC-000020
```

---

## Engines

| Engine | Description |
|--------|-------------|
| MissionEngine | Universal Mission Execution |
| SkillEngine | Universal Skill Execution |
| EventEngine | Async Event Processing |
| ContractEngine | Universal Contract Validation |
| Discovery | Auto-discovery of plugins |

---

## SDKs

| SDK | Description |
|-----|-------------|
| Capability SDK | Base class for all capabilities |
| Provider SDK | Base class for all providers |

---

## Version

```
v0.3.0 - EXEC-000016 to EXEC-000020
```

---

*AGOS Kernel - The foundation of everything.*
