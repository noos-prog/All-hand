# Phase 2: Capability Operating System (COS)

> **20% → 30%**

---

## 🎯 Goal

In this phase, we do not build Agents, Tools, or MCP.

We build:

**Capability Operating System**

```
The System does NOT know:
- OpenHands
- Cline
- Goose
- Aider
- Browser Use
- Any other agent

It knows ONLY one thing:

CAPABILITY
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Core Brain                            │
│                                                             │
│  Knows ONLY: Capability Engine                               │
│  Knows NOTHING about specific tools                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Capability Engine                        │
│                                                             │
│  Goal → Tasks → Capabilities → Providers → Results            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Capability Registry                        │
│                                                             │
│  All capabilities registered here                            │
│  All providers mapped to capabilities                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Capability Providers                       │
│                                                             │
│  OpenHands ──┐                                              │
│  Cline ──────┼── All are EQUAL Providers                    │
│  Aider ──────┤                                              │
│  Goose ──────┤                                              │
│  Claude ────►│                                              │
│  ... ───────┘                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure

```
Phase 2/
├── 01-Capability-Definition/
│   ├── 01-Capability-Overview.md
│   ├── 02-Capability-Object.md
│   ├── 03-Capability-Categories.md
│   ├── 04-Capability-Dependencies.md
│   └── 05-All-Capabilities-List.md
│
├── 02-Capability-Registry/
│   ├── 01-Registry-Structure.md
│   ├── 02-Provider-Mapping.md
│   └── 03-Capability-Ranking.md
│
├── 03-Capability-Engine/
│   ├── 01-Engine-Overview.md
│   ├── 02-Request-Processing.md
│   └── 03-Provider-Selection.md
│
├── 04-Capability-Policies/
│   ├── 01-Policies-Overview.md
│   ├── 02-Constraints.md
│   └── 03-Verification-Rules.md
│
├── 05-Capability-Contracts/
│   ├── 01-Contracts-Overview.md
│   ├── 02-Input-Contract.md
│   ├── 03-Output-Contract.md
│   └── 04-Versioning.md
│
├── 06-Capability-Marketplace/
│   ├── 01-Marketplace-Overview.md
│   ├── 02-Provider-Database.md
│   └── 03-Metrics.md
│
└── 07-ADR-005-Capability-Providers.md
```

---

## 🔑 Key Principles

### 1. Everything is a Capability

```
Read Repository → Capability
Write Code → Capability
Review Code → Capability
Run Tests → Capability
Deploy → Capability
Analyze Logs → Capability
```

### 2. No Tool Names in Core

```
❌ Core Brain knows: OpenHands
❌ Core Brain knows: Cline
❌ Core Brain knows: Aider

✅ Core Brain knows ONLY: Capability
✅ Core Brain knows: Capability Engine
✅ Core Brain knows: Provider Selection
```

### 3. All Providers Are Equal

```
OpenHands = Cline = Aider = Goose = Claude = Browser Use

They are all:
- Capability Providers
- Interchangeable
- Replaceable
- Versionable
```

### 4. Zero Core Changes for New Tools

```
Adding a new tool:
1. Create Adapter
2. Register as Provider
3. Map to Capabilities
4. DONE

No Core Brain changes
No Capability Engine changes
```

---

## 📋 Deliverables

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | Capability Definition | ✅ |
| 2 | Capability Object Schema | ✅ |
| 3 | Capability Registry | ✅ |
| 4 | Capability Categories | ✅ |
| 5 | Capability Dependency Graph | ✅ |
| 6 | Capability Policies | ✅ |
| 7 | Capability Constraints | ✅ |
| 8 | Capability Inputs | ✅ |
| 9 | Capability Outputs | ✅ |
| 10 | Capability Scoring | ✅ |
| 11 | Capability Ranking | ✅ |
| 12 | Capability Marketplace | ✅ |
| 13 | Universal Capability Interface | ✅ |
| 14 | Capability Contracts | ✅ |
| 15 | Capability Versioning | ✅ |
| 16 | Capability Metrics | ✅ |
| 17 | Capability Learning | ✅ |
| 18 | Capability Rules | ✅ |
| 19 | Capability Engine | ✅ |
| 20 | Definition of Done | ✅ |

---

## ✅ Exit Criteria

We do not move to Phase 3 unless:

1. ✅ Can add a new tool without modifying Core Brain
2. ✅ Can remove any tool without breaking workflow
3. ✅ Can run any task by capability name only
4. ✅ Can measure quality per provider per capability

---

## 📚 Related Documents

- [Phase 1: Core Brain Specification](../phase-1/README.md)
- [ADR-005: Capability Providers](./07-ADR-005-Capability-Providers.md)
