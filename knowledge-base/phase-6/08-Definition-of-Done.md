# Phase 6 Definition of Done

> **We do not move to 70% unless we can architecturally do all of the following.**

---

## Exit Criteria

### 1. Manage Complete Project Lifecycle

**Scenario:** Complete lifecycle from idea to production.

**Required Architecture:**
```yaml
Lifecycle Phases:
  Goal → Discovery → Architecture → Planning
  → Execution → Verification → Deployment
  → Monitoring → Continuous Improvement

Each phase has:
  - Entry rules
  - Inputs
  - Capabilities
  - Exit rules
```

**Validation:**
```python
def test_lifecycle():
    # Start with goal
    mission = await system.create_mission(
        goal="Build e-commerce platform"
    )
    
    # Complete discovery
    await mission.transition_to("discovery")
    await mission.complete_discovery()
    assert mission.phase == "ARCHITECTURE"
    
    # Complete all phases
    await mission.transition_to("architecture")
    await mission.transition_to("planning")
    await mission.transition_to("execution")
    await mission.transition_to("verification")
    await mission.transition_to("deployment")
    
    assert mission.state == "DEPLOYED"
```

---

### 2. Understand Project Domain

**Scenario:** Analyze project and adjust strategy.

**Required Architecture:**
```yaml
Domain Analysis:
  - Mobile
  - Web
  - Desktop
  - Game
  - AI
  - Backend
  - SaaS
  - IoT
  
Domain adjusts:
  - Architecture patterns
  - Technology selection
  - Testing strategies
  - Security requirements
```

**Validation:**
```python
def test_domain_understanding():
    # Identify domain
    domain = await system.identify_domain(
        project="Mobile banking app"
    )
    
    assert domain == "MOBILE_BANKING"
    
    # Verify strategy adjustment
    strategy = system.get_strategy_for_domain(domain)
    assert "security" in strategy.priorities
    assert "PCI-DSS" in strategy.compliance
```

---

### 3. Build Architecture Before Code

**Scenario:** No code until architecture is approved.

**Required Architecture:**
```yaml
Architecture First:
  Requirements → System Design → Components
  → Data Flow → Services → Interfaces
  → Security → Deployment
  
All approved before:
  - Code generation
  - Component creation
  - Test writing
```

**Validation:**
```python
def test_architecture_first():
    mission = await system.create_mission(...)
    
    # Cannot execute until architecture
    assert not await mission.can_execute()
    
    # Complete architecture
    await mission.design_architecture()
    await mission.approve_architecture()
    
    # Now can execute
    assert await mission.can_execute()
```

---

### 4. Select Technology with Reasoning

**Scenario:** Technology selection with explanation.

**Required Architecture:**
```yaml
Technology Selection:
  - Compare options (React, Vue, Svelte, Angular)
  - Evaluate criteria (performance, community, learning curve)
  - Score and rank
  - Explain reasoning
  - Document decision
```

**Validation:**
```python
def test_technology_selection():
    options = await system.select_technology(
        context="Frontend SPA",
        requirements=["performance", "community", "learning_curve"]
    )
    
    # Selected with reasoning
    assert options.selected == "React"
    assert "Highest community score" in options.reasoning
    assert "Best ecosystem" in options.reasoning
    
    # Alternatives documented
    assert "Vue" in options.alternatives
    assert "Angular" in options.alternatives
```

---

### 5. Enforce Quality Gates

**Scenario:** Block deployment until quality gates pass.

**Required Architecture:**
```yaml
Quality Gates:
  Gate 1: Compilation (0 errors)
  Gate 2: Testing (80% coverage)
  Gate 3: Security (0 critical vulnerabilities)
  Gate 4: Performance (meet thresholds)
  Gate 5: Architecture (no violations)
```

**Validation:**
```python
def test_quality_gates():
    # Gate blocks on failure
    result = await system.run_quality_gate(
        gate="security",
        project=project
    )
    
    assert result.passed == False
    assert result.violations[0].severity == "CRITICAL"
    
    # Cannot deploy
    assert not await system.can_deploy(project)
    
    # Fix issue
    await project.fix_vulnerability()
    
    # Now can deploy
    assert await system.can_deploy(project)
```

---

### 6. Maintain Continuous Architecture

**Scenario:** Architecture evolves with the project.

**Required Architecture:**
```yaml
Continuous Architecture:
  - Monitor architecture
  - Detect drift
  - Suggest improvements
  - Approve changes
  - Apply refactoring
```

**Validation:**
```python
def test_continuous_architecture():
    # Detect drift
    drift = await system.detect_architecture_drift(project)
    
    assert drift.violations > 0
    assert drift.type == "LAYER_VIOLATION"
    
    # Suggest improvement
    improvement = await system.suggest_improvement(drift)
    
    assert improvement.action == "REFACTOR"
    assert improvement.priority == "HIGH"
    
    # Apply if approved
    await system.apply_improvement(improvement)
    assert system.architecture_compliant(project)
```

---

### 7. Evolve and Learn

**Scenario:** System improves over time.

**Required Architecture:**
```yaml
Learning:
  - Extract knowledge from projects
  - Update organizational memory
  - Optimize capabilities
  - Improve recommendations
  - Evolve patterns
```

**Validation:**
```python
def test_learning():
    # Complete project
    mission = await system.complete_mission(...)
    
    # Knowledge extracted
    memory = system.get_organizational_memory()
    assert memory.total_projects > 0
    
    # Recommendations updated
    recommendations = await memory.get_recommendations(
        domain="e-commerce"
    )
    assert len(recommendations) > 0
    
    # Next project benefits
    new_project = await system.create_mission(...)
    recommendations = await system.get_recommendations(new_project)
    assert "Use microservices" in recommendations
```

---

### 8. Treat Projects as Living Entities

**Scenario:** Project evolves throughout its life.

**Required Architecture:**
```yaml
Living Entity:
  - Digital Twin maintained
  - State persisted
  - Metrics tracked
  - Quality monitored
  - Continuous improvement
  - Version history
```

**Validation:**
```python
def test_living_entity():
    # Project has digital twin
    twin = system.get_digital_twin(project)
    
    assert twin.architecture is not None
    assert twin.knowledge is not None
    assert twin.history is not None
    assert twin.metrics is not None
    
    # Project evolves
    await project.add_feature("new_feature")
    await project.refactor("performance")
    await project.optimize("database")
    
    # Twin updated
    twin = system.get_digital_twin(project)
    assert twin.version > 1
    assert twin.state == "EVOLVED"
```

---

## Self-Assessment Checklist

### Mission Lifecycle
- [x] Lifecycle phases defined
- [x] Phase transitions documented
- [x] Digital Twin concept created

### Phase Engine
- [x] Entry rules defined
- [x] Exit rules defined
- [x] Phase validation designed

### Quality Engines
- [x] Quality Gate Engine built
- [x] Continuous Verification designed
- [x] Architecture Compliance documented

### Architecture Engine
- [x] Architecture Engine documented
- [x] Technology Selection designed
- [x] Continuous Architecture created

### Continuous Learning
- [x] Knowledge Mining designed
- [x] Capability Optimization documented
- [x] Organizational Memory created

### Domain Intelligence
- [x] Domain Engine designed
- [x] Domain Profiles documented

### ADRs
- [x] ADR-016: No Independent Agents
- [x] ADR-017: Continuous Evolution
- [x] ADR-018: Digital Twin
- [x] ADR-019: No Final Version
- [x] ADR-020: Data-Driven Reviews
- [x] ADR-021: Capability Not Framework

---

## Quantitative Validation

| Metric | Target | Validation |
|--------|--------|------------|
| Lifecycle Phases | 9 | All phases defined |
| Domain Types | 12+ | All domains documented |
| Quality Gates | 5+ | All gates designed |
| Learning Sources | 5+ | All sources defined |
| ADRs | 6 | All written |

---

## Architecture Validation

```
┌─────────────────────────────────────────────────────────────┐
│                 System Architecture (Phase 6)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Mission Lifecycle                                          │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Goal → Discovery → Architecture → Planning        │  │
│  │  → Execution → Verification → Deployment          │  │
│  │  → Monitoring → Continuous Improvement            │  │
│  └─────────────────────────────────────────────────────┘  │
│       │                                                     │
│       ▼                                                     │
│  Phase Engine                                               │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Entry Rules → Inputs → Capabilities → Exit Rules  │  │
│  └─────────────────────────────────────────────────────┘  │
│       │                                                     │
│       ▼                                                     │
│  Quality Engines                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Quality Gates → Verification → Compliance          │  │
│  └─────────────────────────────────────────────────────┘  │
│       │                                                     │
│       ▼                                                     │
│  Continuous Learning                                        │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Knowledge Mining → Optimization → Memory          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Final Validation

Before moving to Phase 7, confirm:

1. ✅ **Lifecycle**: System manages complete project lifecycle
2. ✅ **Domain**: System understands and adjusts for domain
3. ✅ **Architecture**: System builds architecture before code
4. ✅ **Technology**: System selects technology with reasoning
5. ✅ **Quality**: System enforces quality gates
6. ✅ **Continuous**: System maintains continuous architecture
7. ✅ **Learning**: System evolves and learns
8. ✅ **Living**: System treats projects as living entities

---

## Related Documents

- [Phase 5: Autonomous Execution Fabric](../phase-5/README.md)
- [Mission-Lifecycle.md](./01-Mission-Lifecycle/01-Lifecycle-Overview.md)
