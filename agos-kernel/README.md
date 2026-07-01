# AGOS Kernel v0.1.0

> **The only executable component in AGOS.**

---

## Directory Structure

```
agos-kernel/
├── core/                  # MissionManager, AGOSKernel
├── context/              # ExecutionContext, ContextBuilder
├── decision/             # DecisionEngine
├── execution/            # ExecutionEngine
├── mission/              # Mission types
├── registry/
│   ├── capability/       # CapabilityRegistry
│   └── provider/         # ProviderRegistry
├── contracts/            # RepositoryDNA, RepositorySnapshot
├── events/               # EventBus, Event types
├── interfaces/            # IProvider, ICapability, ISkill
├── shared/               # Shared types
├── capabilities/         # RepositoryAnalysis capability
├── providers/            # LocalRepositoryProvider
├── main.py              # Entry point
└── test_integration.py   # Integration test
```

---

## Mission Flow

```
Mission
    │
    ▼
MissionManager
    │
    ▼
ContextBuilder
    │
    ▼
DecisionEngine (selects Capability + Provider)
    │
    ▼
ExecutionEngine
    │
    ▼
RepositoryAnalysis Capability
    │
    ▼
RepositoryDNA
    │
    ▼
MissionCompleted
```

---

## Registered Components

### Capabilities
| Name | Skills |
|------|--------|
| RepositoryAnalysis | CloneRepository, ReadRepository, GenerateDNA |

### Providers
| Name | Skills |
|------|--------|
| LocalRepositoryProvider | CloneRepository, ReadRepository |

### Skills
- CloneRepository
- ReadRepository
- GenerateDNA

---

## Events Published

- MissionCreated
- MissionStarted
- CapabilitySelected
- ProviderSelected
- ExecutionStarted
- ExecutionCompleted
- MissionCompleted

---

## Constraints

```
❌ No UI
❌ No Dashboard
❌ No Marketplace
❌ No Authentication
❌ No Memory
❌ No Multi-Agent
❌ No AI Models
❌ No Global State
❌ No Singleton

✅ Kernel Only
✅ Capability Plugins
✅ Provider Plugins
✅ Event Bus
✅ Typed Everything
```

---

## Usage

```bash
# Run integration test
python test_integration.py

# Run with GitHub URL
python main.py https://github.com/All-Hands-AI/OpenHands
```

---

## Version

```
v0.1.0 - ML0 Bootstrap
```

---

*AGOS Kernel - The foundation of everything.*
