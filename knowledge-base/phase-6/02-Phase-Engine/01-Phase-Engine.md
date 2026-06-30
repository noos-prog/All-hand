# Phase Engine

> **Every phase has entry rules and exit rules.**

---

## Phase Engine Concept

```
┌─────────────────────────────────────────────────────────────┐
│                       Phase Engine                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                 PHASE: Architecture                       │  │
│  │                                                       │  │
│  │  Entry Rules ──► Inputs ──► Capabilities ──► Exit     │  │
│  │                                                       │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  Entry Rules:                                 │  │  │
│  │  │  - Domain understood                          │  │  │
│  │  │  - Requirements analyzed                      │  │  │
│  │  │  - Context established                        │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  Inputs:                                     │  │  │
│  │  │  - Goal Object                               │  │  │
│  │  │  - Domain Profile                           │  │  │
│  │  │  - Requirements Document                      │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  Capabilities Used:                           │  │  │
│  │  │  - design_architecture                        │  │  │
│  │  │  - select_technology                          │  │  │
│  │  │  - model_data                                 │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  Exit Rules:                                 │  │  │
│  │  │  - Architecture approved                     │  │  │
│  │  │  - Technology selected                       │  │  │
│  │  │  - Security designed                         │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase Definition Schema

```yaml
Phase:
  id: string
  name: string
  order: integer
  
  # Entry criteria
  entry_rules:
    - rule: string
      description: string
      validator: string  # Function that validates
      
  # Required inputs
  inputs:
    - name: string
      type: string
      required: boolean
      source: string  # Where it comes from
      
  # Capabilities used
  capabilities:
    - capability_id: string
      version: string
      providers: list[string]
      
  # Outputs produced
  outputs:
    - name: string
      type: string
      destination: string
      
  # Exit criteria
  exit_rules:
    - rule: string
      description: string
      validator: string
      
  # Phase-specific configuration
  config:
    timeout: duration
    max_retries: integer
    parallel_execution: boolean
    
  # State
  state:
    current: enum  # PENDING, IN_PROGRESS, COMPLETED, SKIPPED, FAILED
    started_at: datetime
    completed_at: datetime
```

---

## Lifecycle Phases

### Discovery Phase

```yaml
Phase_Discovery:
  id: "discovery"
  name: "Discovery"
  order: 1
  
  entry_rules:
    - rule: "goal_defined"
      description: "Goal object exists with clear mission"
      
  inputs:
    - name: "goal"
      type: "GoalObject"
      required: true
      
  capabilities:
    - capability_id: "analyze_domain"
    - capability_id: "extract_business_rules"
    - capability_id: "identify_stakeholders"
    - capability_id: "map_context"
      
  outputs:
    - name: "domain_profile"
      type: "DomainProfile"
    - name: "business_rules"
      type: "BusinessRules"
    - name: "stakeholder_map"
      type: "StakeholderMap"
      
  exit_rules:
    - rule: "domain_understood"
      description: "System understands the domain"
    - rule: "requirements_clear"
      description: "Business rules extracted"
```

### Architecture Phase

```yaml
Phase_Architecture:
  id: "architecture"
  name: "Architecture"
  order: 2
  
  entry_rules:
    - rule: "domain_understood"
      description: "Discovery phase completed"
    - rule: "requirements_available"
      description: "Requirements document exists"
      
  inputs:
    - name: "domain_profile"
      type: "DomainProfile"
      required: true
    - name: "requirements"
      type: "Requirements"
      required: true
      
  capabilities:
    - capability_id: "design_architecture"
    - capability_id: "select_technology"
    - capability_id: "model_data"
    - capability_id: "design_api"
    - capability_id: "plan_security"
      
  outputs:
    - name: "architecture_document"
      type: "ArchitectureDocument"
    - name: "technology_stack"
      type: "TechnologyStack"
    - name: "data_models"
      type: "DataModels"
    - name: "api_specifications"
      type: "APISpecifications"
      
  exit_rules:
    - rule: "architecture_approved"
      description: "Architecture passes review"
    - rule: "technology_selected"
      description: "Technology stack chosen"
    - rule: "security_designed"
      description: "Security design complete"
```

### Planning Phase

```yaml
Phase_Planning:
  id: "planning"
  name: "Planning"
  order: 3
  
  entry_rules:
    - rule: "architecture_approved"
      description: "Architecture phase completed"
      
  inputs:
    - name: "architecture"
      type: "ArchitectureDocument"
      required: true
      
  capabilities:
    - capability_id: "create_epics"
    - capability_id: "create_features"
    - capability_id: "create_tasks"
    - capability_id: "resolve_dependencies"
    - capability_id: "estimate_effort"
      
  outputs:
    - name: "planning_graph"
      type: "PlanningGraph"
    - name: "task_breakdown"
      type: "TaskBreakdown"
    - name: "timeline"
      type: "Timeline"
    - name: "effort_estimate"
      type: "EffortEstimate"
      
  exit_rules:
    - rule: "tasks_defined"
      description: "All tasks identified"
    - rule: "dependencies_resolved"
      description: "No circular dependencies"
    - rule: "timeline_approved"
      description: "Timeline within constraints"
```

### Execution Phase

```yaml
Phase_Execution:
  id: "execution"
  name: "Execution"
  order: 4
  
  entry_rules:
    - rule: "plan_approved"
      description: "Planning phase completed"
    - rule: "resources_allocated"
      description: "Providers and workspace ready"
      
  inputs:
    - name: "planning_graph"
      type: "PlanningGraph"
      required: true
      
  capabilities:
    - capability_id: "generate_code"
    - capability_id: "write_tests"
    - capability_id: "create_documentation"
    - capability_id: "build_components"
    - capability_id: "integrate_systems"
      
  outputs:
    - name: "source_code"
      type: "CodeArtifacts"
    - name: "tests"
      type: "TestArtifacts"
    - name: "builds"
      type: "BuildArtifacts"
      
  exit_rules:
    - rule: "code_complete"
      description: "All tasks completed"
    - rule: "tests_written"
      description: "Test coverage meets threshold"
    - rule: "quality_gates_passed"
      description: "All quality gates green"
```

### Verification Phase

```yaml
Phase_Verification:
  id: "verification"
  name: "Verification"
  order: 5
  
  entry_rules:
    - rule: "code_complete"
      description: "Execution phase completed"
      
  inputs:
    - name: "code_artifacts"
      type: "CodeArtifacts"
      required: true
      
  capabilities:
    - capability_id: "run_tests"
    - capability_id: "security_scan"
    - capability_id: "performance_test"
    - capability_id: "architecture_compliance"
    - capability_id: "code_review"
      
  outputs:
    - name: "test_results"
      type: "TestResults"
    - name: "security_report"
      type: "SecurityReport"
    - name: "performance_report"
      type: "PerformanceReport"
    - name: "quality_score"
      type: "QualityScore"
      
  exit_rules:
    - rule: "tests_pass"
      description: "All critical tests pass"
    - rule: "security_approved"
      description: "No critical vulnerabilities"
    - rule: "performance_acceptable"
      description: "Meets performance targets"
    - rule: "quality_threshold_met"
      description: "Quality score above threshold"
```

---

## Phase Transitions

```python
class PhaseEngine:
    """
    Manages phase transitions.
    """
    
    async def can_transition(
        self,
        mission: Mission,
        from_phase: Phase,
        to_phase: Phase
    ) -> bool:
        """
        Check if transition is allowed.
        """
        
        # Check entry rules for target phase
        for rule in to_phase.entry_rules:
            if not await self.validate_rule(mission, rule):
                return False
                
        return True
        
    async def transition(
        self,
        mission: Mission,
        to_phase: Phase
    ) -> TransitionResult:
        """
        Execute phase transition.
        """
        
        # Check if transition is allowed
        if not await self.can_transition(mission, mission.current_phase, to_phase):
            raise TransitionError(
                f"Cannot transition from {mission.current_phase} to {to_phase}"
            )
            
        # Execute exit actions for current phase
        current = mission.current_phase
        await self.execute_exit_actions(mission, current)
        
        # Update mission state
        mission.current_phase = to_phase
        mission.phase_state = "IN_PROGRESS"
        mission.phase_started_at = datetime.now()
        
        # Execute entry actions for new phase
        await self.execute_entry_actions(mission, to_phase)
        
        return TransitionResult(
            success=True,
            from_phase=current,
            to_phase=to_phase
        )
```

---

## Phase Validation

```python
class PhaseValidator:
    """
    Validates phase completion.
    """
    
    async def validate_phase(
        self,
        mission: Mission,
        phase: Phase
    ) -> ValidationResult:
        """
        Validate phase completion.
        """
        
        violations = []
        
        # Check each exit rule
        for rule in phase.exit_rules:
            result = await self.validate_rule(mission, rule)
            
            if not result.passed:
                violations.append({
                    "rule": rule,
                    "reason": result.reason,
                    "evidence": result.evidence
                })
                
        # Check outputs exist
        for output in phase.outputs:
            if not await self.output_exists(mission, output):
                violations.append({
                    "rule": "output_exists",
                    "reason": f"Missing output: {output.name}"
                })
                
        return ValidationResult(
            passed=len(violations) == 0,
            violations=violations
        )
```

---

## Example: Phase Transition

```yaml
Transition: Discovery → Architecture

1. Check entry rules for Architecture:
   ✅ Domain understood - YES
   ✅ Requirements available - YES
   
2. Execute Discovery exit actions:
   - Save domain profile
   - Save business rules
   - Save stakeholder map
   
3. Update mission state:
   - Current phase: "architecture"
   - State: "IN_PROGRESS"
   - Started at: "2024-01-15T10:00:00Z"
   
4. Execute Architecture entry actions:
   - Load domain profile
   - Load requirements
   - Initialize architecture workspace
   
5. Start Architecture phase:
   - Select technology
   - Design system
   - Plan data models
```

---

## Related Documents

- [Lifecycle-Overview.md](../01-Mission-Lifecycle/01-Lifecycle-Overview.md)
- [Phase-Transitions.md](./02-Phase-Transitions.md)
