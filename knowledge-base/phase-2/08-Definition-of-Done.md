# Phase 2 Definition of Done

> **We do not move to 30% unless we can do all of the following.**

---

## Exit Criteria

### 1. Add New Tool Without Core Changes

**Scenario:** Add a new agent (e.g., "NewAgent") to the system.

**Required Steps:**
```yaml
Steps to add NewAgent:
  1. Create adapter: adapters/newagent_adapter.py
  2. Register provider: Registry.add_provider("newagent")
  3. Map capabilities: Registry.map_capabilities("newagent", [...])
  4. DONE

Core Brain: NO CHANGES
Capability Engine: NO CHANGES
```

**Validation:**
```python
def test_add_tool_without_core_changes():
    # 1. Create new adapter
    adapter = create_adapter("newagent")
    
    # 2. Register
    registry.register_provider(adapter)
    
    # 3. Map capabilities
    registry.map_capabilities("newagent", ["generate_code", "edit_code"])
    
    # 4. Execute
    result = capability_engine.execute("generate_code", inputs)
    
    # 5. Verify
    assert result.provider_id == "newagent"
    assert result.success == True
    # Core unchanged
```

---

### 2. Remove Any Tool Without Breaking Workflow

**Scenario:** Remove "Goose" agent from the system.

**Required Behavior:**
```yaml
Before:
  - goose: active
  - goose capabilities: [generate_code, edit_code]
  
Action:
  - registry.disable_provider("goose")
  OR
  - registry.remove_provider("goose")
  
After:
  - System continues working
  - generate_code: handled by [openhands, cline, aider]
  - edit_code: handled by [openhands, cline]
  - No workflow broken
```

**Validation:**
```python
def test_remove_tool_without_breaking():
    # 1. Before removal
    result_before = capability_engine.execute("generate_code", inputs)
    assert result_before.success == True
    
    # 2. Remove provider
    registry.remove_provider("goose")
    
    # 3. Execute again
    result_after = capability_engine.execute("generate_code", inputs)
    
    # 4. Verify still works
    assert result_after.success == True
    assert result_after.provider_id != "goose"
```

---

### 3. Execute Task by Capability Name Only

**Scenario:** Run "Generate Backend API" without mentioning any tool name.

**Required Behavior:**
```yaml
Input:
  goal: "Generate REST API for user management"
  # NO mention of: OpenHands, Cline, Aider, Goose, etc.
  
Process:
  1. Planning Engine → tasks
  2. Task → capabilities
  3. Capability = "generate_api"
  4. Capability Engine selects best provider
  5. Execute via adapter
  
Output:
  - Result returned
  - No tool name mentioned in code
  - Provider selected by score only
```

**Validation:**
```python
def test_execute_by_capability_only():
    # 1. No tool names in code
    assert "openhands" not in source_code
    assert "aider" not in source_code
    assert "cline" not in source_code
    
    # 2. Execute capability
    result = capability_engine.execute_capability(
        capability_id="generate_api",
        inputs=inputs
    )
    
    # 3. Verify
    assert result.success == True
    assert "provider_id" in result
```

---

### 4. Measure Quality Per Provider Per Capability

**Scenario:** Measure how well each provider performs "generate_code" capability.

**Required Metrics:**
```yaml
Metrics: cap_generate_code

Provider Scores:
  openhands:
    executions: 500
    success_rate: 95%
    avg_duration: "3m"
    avg_cost: 0.05
    quality_score: 0.92
    
  cline:
    executions: 200
    success_rate: 88%
    avg_duration: "2m"
    avg_cost: 0.02
    quality_score: 0.85
    
  aider:
    executions: 150
    success_rate: 85%
    avg_duration: "1m"
    avg_cost: 0.01
    quality_score: 0.82

System automatically uses these metrics for selection.
```

**Validation:**
```python
def test_quality_metrics():
    # 1. Execute multiple times
    for _ in range(100):
        capability_engine.execute_capability("generate_code", inputs)
    
    # 2. Get metrics
    metrics = registry.get_metrics("cap_generate_code")
    
    # 3. Verify per-provider metrics
    assert "openhands" in metrics.by_provider
    assert "cline" in metrics.by_provider
    assert "aider" in metrics.by_provider
    
    # 4. Verify metrics are used for selection
    best = capability_engine.select_provider("generate_code")
    assert best.quality_score > 0.8
```

---

## Self-Assessment Checklist

### Capability Definition
- [x] Capability concept defined
- [x] Capability Object schema created
- [x] All 91+ capabilities listed
- [x] Categories defined
- [x] Dependencies mapped

### Capability Registry
- [x] Registry structure defined
- [x] Provider mapping created
- [x] Ranking system designed
- [x] Search functionality specified

### Capability Engine
- [x] Engine architecture defined
- [x] Request processing flow designed
- [x] Provider selection algorithm created
- [x] Fallback handling specified

### Capability Policies
- [x] Execution policies defined
- [x] Verification policies created
- [x] Selection policies designed
- [x] Security policies specified

### Capability Contracts
- [x] Input contract defined
- [x] Output contract defined
- [x] Error contract created
- [x] Version contract specified

### Capability Marketplace
- [x] Marketplace concept defined
- [x] Provider database schema created
- [x] Metrics tracking designed
- [x] Comparison tools specified

### ADR
- [x] ADR-005 written
- [x] Provider model defined
- [x] Addition process documented
- [x] Removal process documented

---

## Quantitative Validation

| Metric | Target | Validation |
|--------|--------|------------|
| Capabilities defined | 90+ | All major capabilities |
| Provider mappings | All capabilities | Can add/remove providers |
| Selection accuracy | > 90% | Matches expected provider |
| Quality tracking | Per-capability | Metrics collected |
| Add tool time | < 1 hour | Adapter + registration |
| Remove tool time | < 5 min | Registry update |

---

## Scenario Walkthrough

### Scenario: "Build a complete web application"

```
Input:
  "Build a complete e-commerce web application with:
   - User authentication
   - Product catalog
   - Shopping cart
   - Payment processing
   - Admin dashboard
   - CI/CD pipeline"

Step 1: Goal → Tasks
  - Design Architecture
  - Setup Backend
  - Setup Database
  - Implement Auth
  - Implement Products
  - Implement Cart
  - Implement Payments
  - Build Frontend
  - Setup CI/CD
  - Deploy

Step 2: Tasks → Capabilities
  - Design Architecture → cap_plan_architecture
  - Setup Backend → cap_generate_backend
  - Setup Database → cap_schema_design
  - Implement Auth → cap_generate_code + cap_generate_tests
  - ...

Step 3: For each Capability:
  - Query Registry
  - Get best provider
  - Execute via adapter
  - Verify result

Step 4: Final output
  - Complete web application
  - Deployed
  - All tests passing
  
NO TOOL NAMES IN ANY STEP
```

---

## Final Validation

Before moving to Phase 3 (30%), confirm:

1. ✅ **Zero tool names in Core**
   - Code contains zero references to: OpenHands, Cline, Aider, Goose, Claude, Browser Use
   
2. ✅ **Zero Core changes for new tools**
   - Adding a tool requires only: adapter + registry
   
3. ✅ **All tasks executable by capability**
   - Every task can be executed by capability ID only
   
4. ✅ **Quality metrics per provider**
   - Metrics tracked per provider per capability
   
5. ✅ **System resilience**
   - Removing any tool doesn't break workflow

---

## Related Documents

- [Phase 1: Core Brain Specification](../phase-1/README.md)
- [Capability Engine](../03-Capability-Engine/01-Engine-Overview.md)
- [ADR-005: Capability Providers](./07-ADR-005-Capability-Providers.md)
