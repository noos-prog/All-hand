# Phase 3: Universal Provider Layer (UPL)

> **30% → 40%**

---

## 🎯 Goal

Transform **anything** in the world into a Provider.

```
Not just Agents.
Not just Tools.

ANYTHING that can execute a Capability:

- AI Agent → Provider
- MCP Server → Provider
- REST API → Provider
- CLI → Provider
- Docker Container → Provider
- SaaS → Provider
- Python Library → Provider
- Local Model → Provider
- Cloud Model → Provider
- Browser → Provider
- Database → Provider
- GitHub Action → Provider
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Core Brain                               │
│                                                             │
│  Knows ONLY: Capability                                     │
│  Knows NOTHING about: Provider names                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Universal Provider Layer                      │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Provider Registry                     │   │
│  │  All Providers registered here                         │   │
│  │  All Adapters registered here                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Adapters                                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  │OpenHands│ │  Cline │ │  Aider │ │  GitHub │         │
│  │Adapter  │ │ Adapter │ │ Adapter │ │ Adapter  │         │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  │Browser  │ │ Docker  │ │Playwright│ │ Postgres │        │
│  │Adapter  │ │ Adapter │ │ Adapter  │ │ Adapter  │        │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Providers                               │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐       │
│  │Agents │ │ APIs  │ │ CLIs  │ │Docker │ │Cloud  │       │
│  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘       │
│                                                             │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐       │
│  │Browser│ │  DBs  │ │ Search │ │ Git   │ │Storage │      │
│  └───────┘ └───────┘ └───────┘ └───────┘ └───────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure

```
Phase 3/
├── 01-Provider-Definition/
│   ├── 01-Provider-Overview.md
│   ├── 02-Provider-Object.md
│   └── 03-Provider-Capability-Profile.md
│
├── 02-Provider-Types/
│   └── 01-Types-Overview.md
│
├── 03-Provider-Interface/
│   ├── 01-Interface-Overview.md
│   └── 02-Execution-Flow.md
│
├── 04-Provider-Adapter/
│   ├── 01-Adapter-Overview.md
│   └── 02-Adapter-Examples.md
│
├── 05-Provider-Management/
│   ├── 01-Discovery.md
│   ├── 02-Health.md
│   ├── 03-Benchmark.md
│   ├── 04-Failover.md
│   └── 05-Chaining.md
│
├── 06-Provider-Policies/
│   ├── 01-Selection-Policy.md
│   └── 02-Voting.md
│
├── 07-Provider-Security/
│   ├── 01-Sandbox.md
│   └── 02-Security-Policy.md
│
├── 08-ADR-006-Everything-is-Provider.md
│
└── 09-Definition-of-Done.md
```

---

## 🔑 Key Principles

### 1. Everything is a Provider

```
OpenHands = Provider
Cline = Provider
Aider = Provider
GitHub = Provider
Playwright = Provider
Docker = Provider
PostgreSQL = Provider
Slack = Provider
Claude = Provider
Any future project = Provider
```

### 2. Provider Capability Profile

```
Not every Provider delivers the same capability at the same level.

Example: Code Review

Provider       Accuracy   Speed   Cost     Best For
─────────────────────────────────────────────────────────
OpenHands      High       Medium  High     Large projects
Aider          Good       High    Low      Small changes
Cline          High       Medium  Medium   Interactive dev
Semgrep        Excellent  High    Low      Static analysis

System selects best Provider for:
- THIS type of task
- THIS context
```

### 3. No Provider Names in Core

```
❌ Core Brain knows: "OpenHands"
❌ Core Brain knows: "GitHub"
❌ Core Brain knows: "PostgreSQL"

✅ Core Brain knows: "Provider"
✅ Core Brain knows: "Adapter"
✅ Core Brain knows: "Capability"
```

### 4. Provider Adapter Pattern

```
Every Provider has its own Adapter.
Core knows NOTHING about Provider internals.

Provider ──► Adapter ──► Universal Interface ──► Core
                 │
                 │ Adapter translates:
                 │ - Provider-specific API
                 │ - Provider-specific auth
                 │ - Provider-specific format
                 │ TO:
                 │ - Universal interface
```

---

## 📋 Deliverables

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | Provider Definition | ✅ |
| 2 | Provider Object Schema | ✅ |
| 3 | Provider Types | ✅ |
| 4 | Universal Provider Interface | ✅ |
| 5 | Provider Adapter | ✅ |
| 6 | Provider Manifest | ✅ |
| 7 | Provider Discovery | ✅ |
| 8 | Provider Health | ✅ |
| 9 | Provider Benchmark | ✅ |
| 10 | Provider Selection Policy | ✅ |
| 11 | Provider Chaining | ✅ |
| 12 | Provider Voting | ✅ |
| 13 | Provider Failover | ✅ |
| 14 | Provider Sandbox | ✅ |
| 15 | Provider Security Policy | ✅ |
| 16 | Provider Metrics | ✅ |
| 17 | Provider Learning | ✅ |
| 18 | ADR-006 | ✅ |
| 19 | Definition of Done | ✅ |

---

## ✅ Exit Criteria

We do not move to Phase 4 unless:

1. ✅ Every external system transforms into Provider
2. ✅ Every Provider has Adapter
3. ✅ Core Brain knows NOTHING about Provider internals
4. ✅ Provider Capability Profile enables context-aware selection
5. ✅ Provider can be added/removed without Core changes

---

## 📚 Related Documents

- [Phase 2: Capability Operating System](../phase-2/README.md)
- [ADR-006: Everything is Provider](./08-ADR-006-Everything-is-Provider.md)
