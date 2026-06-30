# Capability Overview

> **Everything in the system is a Capability.**

---

## What is a Capability?

A Capability is a self-contained unit of work that:
- Has defined inputs
- Has defined outputs
- Can be executed by one or more providers
- Can be ranked by quality
- Can be versioned
- Can be verified

---

## Capability vs Tool

```
┌─────────────────────┐     ┌─────────────────────┐
│       TOOL          │     │    CAPABILITY       │
├─────────────────────┤     ├─────────────────────┤
│                     │     │                     │
│ OpenHands           │     │ Read Repository     │
│ Cline               │     │ Write Code         │
│ Aider               │     │ Review Code        │
│ Goose               │     │ Run Tests          │
│ Browser Use         │     │ Deploy             │
│ ...                 │     │ ...                │
│                     │     │                     │
│ Concrete            │     │ Abstract           │
│ Named               │     │ Unnamed            │
│ Project-specific    │     │ Platform-agnostic  │
└─────────────────────┘     └─────────────────────┘

Tools are IMPLEMENTATIONS
Capabilities are ABSTRACTIONS
```

---

## Core Principle

```
The System does NOT think in terms of:

❌ "Use OpenHands to generate code"
❌ "Use Aider to fix the bug"
❌ "Use Cline to run tests"

The System thinks in terms of:

✅ "Generate Code" capability
✅ "Fix Bugs" capability
✅ "Run Tests" capability

The Capability Engine then selects the BEST provider.
```

---

## Capability Examples

### Coding Capabilities
| Capability | Description |
|------------|-------------|
| `generate_code` | Generate new code from requirements |
| `edit_code` | Edit existing code |
| `delete_code` | Remove code |
| `refactor_code` | Refactor existing code |
| `generate_api` | Generate API endpoints |
| `generate_frontend` | Generate frontend code |
| `generate_backend` | Generate backend code |
| `generate_tests` | Generate test cases |
| `fix_bugs` | Fix identified bugs |

### Analysis Capabilities
| Capability | Description |
|------------|-------------|
| `read_repository` | Read and understand codebase |
| `analyze_architecture` | Analyze system architecture |
| `analyze_performance` | Analyze performance metrics |
| `analyze_security` | Analyze security vulnerabilities |
| `review_code` | Review code quality |

### Execution Capabilities
| Capability | Description |
|------------|-------------|
| `run_tests` | Execute test suite |
| `compile` | Compile code |
| `build` | Build artifacts |
| `deploy` | Deploy to environment |
| `execute_shell` | Execute shell commands |

### Communication Capabilities
| Capability | Description |
|------------|-------------|
| `use_browser` | Browse websites |
| `search_docs` | Search documentation |
| `search_code` | Search code |
| `read_database` | Read from database |

---

## Why Capabilities?

### 1. Abstraction
```
Providers can be swapped without changing the system.
New providers can be added without modifying the system.
```

### 2. Ranking
```
Same capability, different quality:
- Provider A: 95% success rate
- Provider B: 85% success rate
- Provider C: 75% success rate

Select best provider based on ranking.
```

### 3. Metrics
```
Track metrics per capability:
- Success rate
- Average cost
- Average time
- Quality distribution
```

### 4. Verification
```
Each capability has verification rules:
- Generate Code → Must pass lint, tests
- Deploy → Must pass security, health check
```

---

## Related Documents

- [Capability-Object.md](./02-Capability-Object.md)
- [Capability-Categories.md](./03-Capability-Categories.md)
