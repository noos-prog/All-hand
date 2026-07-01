# AGOS Kernel v0.2.0

> **The only executable component in AGOS.**

---

## Directory Structure

```
agos-kernel/
├── core/                  # MissionManager, AGOSKernel
├── context/              # ExecutionContext, ContextBuilder
├── decision/             # DecisionEngine
├── execution/           # ExecutionEngine
├── mission/             # Mission types
├── registry/
│   ├── capability/       # CapabilityRegistry
│   └── provider/         # ProviderRegistry
├── contracts/            # RepositoryDNA, RepositorySnapshot
├── events/              # EventBus, Event types
├── interfaces/         # IProvider, ICapability, ISkill
├── shared/             # Shared types
├── capabilities/       # RepositoryAnalysis capability
├── providers/           # LocalRepositoryProvider
├── discovery/          # AutoDiscovery ←
├── resolvers/          # CapabilityResolver, ProviderResolver ←
├── pipeline/           # ExecutionPipeline ←
├── mission-engine/     # MissionEngine ←
├── skill-engine/       # SkillEngine ←
├── container/          # DI Container ←
├── event-engine/       # EventEngine ←
├── bootstrapper/       # Bootstrapper ←
├── main.py            # Entry point
└── test_integration.py # Integration test
```

---

## Mission Lifecycle

```
Created → Validated → Planned → Executing → Completed/Failed/Cancelled
```

---

## Engines

| Engine | Description |
|--------|-------------|
| MissionEngine | Universal Mission Execution |
| SkillEngine | Universal Skill Execution |
| EventEngine | Async Event Processing |
| Discovery | Auto-discovery of plugins |

---

## Version

```
v0.2.0 - EXEC-000011 to EXEC-000015
```

---

*AGOS Kernel - The foundation of everything.*
