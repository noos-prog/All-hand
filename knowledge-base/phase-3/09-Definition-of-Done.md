# Phase 3 Definition of Done

> **We do not move to 40% unless we can do all of the following.**

---

## Exit Criteria

### 1. Every External System is a Provider

**Scenario:** Transform diverse external systems into providers.

**Required Transformations:**
```yaml
System Type        → Provider
─────────────────────────────────
AI Agent          → Provider
LLM               → Provider
REST API          → Provider
CLI               → Provider
Docker Container   → Provider
Browser           → Provider
Database          → Provider
GitHub            → Provider
CI/CD             → Provider
Search Engine     → Provider
```

**Validation:**
```python
def test_everything_is_provider():
    # All external systems must be registered
    for system_type in ALL_SYSTEM_TYPES:
        provider = registry.get_by_type(system_type)
        assert provider is not None
        assert provider.adapter is not None
```

---

### 2. Every Provider Has an Adapter

**Scenario:** Each provider has its own adapter.

**Required Adapters:**
```yaml
Provider       → Adapter
──────────────────────────
OpenHands     → OpenHandsAdapter
Cline         → ClineAdapter
Aider         → AiderAdapter
GitHub        → GitHubAdapter
Docker        → DockerAdapter
Playwright    → PlaywrightAdapter
PostgreSQL    → PostgresAdapter
Claude        → ClaudeAdapter
```

**Validation:**
```python
def test_provider_has_adapter():
    providers = registry.get_all()
    for provider in providers:
        adapter = adapter_registry.get(provider.id)
        assert adapter is not None
        assert isinstance(adapter, ProviderAdapter)
```

---

### 3. Core Knows NOTHING About Provider Internals

**Scenario:** Core Brain has zero knowledge of specific providers.

**Required:**
```yaml
Core Brain knows:
✅ Provider (abstract)
✅ Capability
✅ Selection
✅ Execution

Core Brain does NOT know:
❌ OpenHands
❌ GitHub
❌ PostgreSQL
❌ Docker
❌ Any specific provider name
```

**Validation:**
```python
def test_core_knows_nothing():
    # Scan Core Brain code
    core_code = read_core_brain_code()
    
    # No provider names in Core
    forbidden_names = [
        "openhands", "cline", "aider",
        "github", "postgresql", "docker",
        "playwright", "claude"
    ]
    
    for name in forbidden_names:
        assert name not in core_code.lower()
```

---

### 4. Provider Capability Profile Enables Context-Aware Selection

**Scenario:** Select best provider for THIS task in THIS context.

**Required:**
```yaml
Context: "Code review for large production project"

Selection Logic:
1. Identify capability = "code_review"
2. Get all providers
3. Score by capability profile
4. Context-aware weighting

Result:
- Semgrep selected (excellent for static analysis)
- OpenHands selected (high accuracy, production fit)
- Aider NOT selected (better for small changes)
```

**Validation:**
```python
def test_context_aware_selection():
    # Scenario: Large production code review
    context = Context(
        task_type="code_review",
        project_size="large",
        environment="production",
        priority="quality"
    )
    
    provider = selector.select("code_review", context)
    
    # Should select provider good for large production
    profile = provider.profiles["code_review"]
    assert profile.best_for.contains("large_projects")
```

---

### 5. Provider Can Be Added/Removed Without Core Changes

**Scenario:** Add new provider "NewAgent".

**Required Process:**
```yaml
Step 1: Create adapter
        → adapters/newagent_adapter.py
        
Step 2: Register provider
        → registry.register_provider("newagent")
        
Step 3: Map capabilities
        → registry.map_capabilities("newagent", [...])

Core Brain: ZERO CHANGES
```

**Validation:**
```python
def test_add_provider_without_core_changes():
    # Record Core Brain state
    core_before = get_core_brain_hash()
    
    # Add new provider
    adapter = create_adapter("newagent")
    registry.register("newagent", adapter)
    
    # Verify Core unchanged
    core_after = get_core_brain_hash()
    assert core_before == core_after
```

---

## Self-Assessment Checklist

### Provider Definition
- [x] Provider concept defined
- [x] Provider Object schema created
- [x] Provider Capability Profile created
- [x] 20+ provider types defined

### Provider Types
- [x] AI Agent type
- [x] LLM type
- [x] API type
- [x] CLI type
- [x] Docker type
- [x] Browser type
- [x] Database type
- [x] And more...

### Provider Interface
- [x] Universal interface defined
- [x] Execution flow specified
- [x] Request/Response schemas
- [x] Adapter examples

### Provider Adapter
- [x] Adapter concept defined
- [x] Adapter responsibilities listed
- [x] Multiple adapter examples
- [x] Adapter registry

### Provider Management
- [x] Discovery process
- [x] Health monitoring
- [x] Benchmark system
- [x] Failover handling
- [x] Chaining support

### Provider Policies
- [x] Selection policy
- [x] Voting policy
- [x] Context-aware weighting
- [x] Quality scoring

### Provider Security
- [x] Sandbox architecture
- [x] Isolation layers
- [x] Resource limits
- [x] Security policies

### ADR
- [x] ADR-006 written
- [x] Everything is Provider documented
- [x] Future-proof architecture

---

## Quantitative Validation

| Metric | Target | Validation |
|--------|--------|------------|
| Provider Types | 20+ | All types documented |
| Provider Adapters | 1 per type | Adapters exist |
| Core Provider Names | 0 | Zero in Core Brain |
| Selection Accuracy | > 90% | Context-aware works |
| Add Provider Time | < 1 hour | Adapter + registration |
| Remove Provider Time | < 5 min | Registry update |
| Sandbox Isolation | 100% | No cross-access |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Core Brain                               │
│                                                             │
│  Knows ONLY:                                               │
│  ✅ Capability                                             │
│  ✅ Provider (abstract)                                    │
│  ✅ Selection                                              │
│  ✅ Execution                                              │
│                                                             │
│  Knows NOTHING about:                                       │
│  ❌ OpenHands                                              │
│  ❌ GitHub                                                  │
│  ❌ PostgreSQL                                              │
│  ❌ Docker                                                  │
│  ❌ Any specific provider                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Universal Provider Layer                         │
│                                                             │
│  20+ Provider Types                                         │
│  20+ Adapters                                               │
│  Universal Interface                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       All Providers                              │
│                                                             │
│  AI Agents • APIs • Databases • Containers                  │
│  Browsers • Search Engines • CI/CD • Storage                │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Documents

- [Phase 2: Capability Operating System](../phase-2/README.md)
- [ADR-006: Everything is Provider](./08-ADR-006-Everything-is-Provider.md)
