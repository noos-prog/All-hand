# AGOS Canon

> **The Unbreakable Rules. The Single Source of Truth.**

---

## Purpose

```
Problem:
  After 2 years, there will be 100 different interpretations
  of the same contract.
  
  Developer A: "Capability contains Model"
  Developer B: "Provider contains Model"
  Developer C: "Mission contains Model"
  
  Project dies.

Solution:
  AGOS Canon
  One definition. One interpretation. Forever.
```

---

## Canon Status

| Canon | Title | Status |
|-------|-------|--------|
| CANON-001 | Vocabulary | **CRITICAL** |
| CANON-002 | Forbidden Words | **CRITICAL** |
| CANON-003 | Canonical Flow | **CRITICAL** |
| CANON-004 | Canonical Object Ownership | **CRITICAL** |
| CANON-005 | Canonical Decision Rules | HIGH |
| CANON-006 | Canonical Principles | HIGH |
| CANON-007 | Canonical Diagrams | MEDIUM |
| CANON-008 | Canonical Naming | HIGH |
| CANON-009 | Canonical Contracts | HIGH |
| CANON-010 | Canonical Testing | HIGH |

---

## CANON-001: Vocabulary

> **Every word has ONE definition. No exceptions.**

---

### Core Terms

```yaml
Vocabulary:

  GOAL:
    definition: |
      "The final outcome desired by the user.
       A goal is WHAT we want to achieve, not HOW we achieve it.
       Goals are declared by users and decomposed into missions by Core Brain."
    example: "Build an e-commerce platform"
    NOT: "The task to execute"
    
  MISSION:
    definition: |
      "A work unit that achieves part of a goal.
       A mission is a HOW in the context of a goal.
       Missions have lifecycle states and produce artifacts."
    example: "Build the authentication service"
    NOT: "A container running code"
    
  CAPABILITY:
    definition: |
      "A declaratively defined ability that can be provided by any provider.
       Capabilities are WHAT can be done, not WHO does it.
       A capability is a contract, not an implementation."
    example: "Generate REST API"
    NOT: "OpenHands or Claude"
    
  PROVIDER:
    definition: |
      "An external system that implements one or more capabilities.
       Providers are the HOW, capabilities are the WHAT.
       Providers can be swapped without changing the capability."
    example: "OpenHands AI Agent"
    NOT: "The AI model itself"
    
  EXECUTION:
    definition: |
      "A single invocation of a capability by a provider.
       Execution tracks the full lifecycle from creation to completion.
       Every execution produces artifacts and metrics."
    example: "OpenHands generated an API"
    NOT: "The running process"
    
  ARTIFACT:
    definition: |
      "Any output produced by an execution.
       Artifacts are immutable and versioned.
       Examples: source files, images, logs, test results."
    NOT: "Temporary files"
    
  KNOWLEDGE:
    definition: |
      "Structured information extracted from executions.
       Knowledge is validated before storage.
       Knowledge has evidence and confidence scores."
    NOT: "Raw logs or code"
    
  DECISION:
    definition: |
      "A recorded choice made by Core Brain.
       Every decision has context, options, evidence, and reasoning.
       Decisions are stored forever for audit and learning."
    NOT: "A random choice"
    
  POLICY:
    definition: |
      "A rule that governs system behavior.
       Policies are enforced by Policy Engine.
       Policies can be global, organizational, or mission-specific."
    NOT: "A law of physics"
    
  CONTEXT:
    definition: |
      "Information about the current state of a mission.
       Context is passed to capabilities and providers.
       Context is immutable within an execution."
    NOT: "Historical data"
    
  WORKSPACE:
    definition: |
      "An isolated execution environment for a mission.
       Workspaces provide isolation and resource limits.
       Workspaces are created and destroyed by the system."
    NOT: "A user's desktop"
    
  RESOURCE:
    definition: |
      "Any consumable asset in the system.
       Resources have limits, quotas, and allocation policies.
       Examples: CPU, memory, storage, API calls, budget."
    NOT: "An artifact"
    
  KERNEL:
    definition: |
      "The core of AGOS that makes all decisions.
       Kernel never executes code directly.
       Kernel orchestrates providers through capabilities."
    NOT: "The operating system kernel"
```

---

### Supporting Terms

```yaml
  TASK:
    definition: |
      "A decomposition of a mission into executable units.
       Tasks have dependencies and can be parallelized.
       A task is executed by one capability from one provider."
       
  MODEL:
    definition: |
      "An AI model used by a provider.
       Models are not directly used by the system.
       Providers use models internally."
       
  SENSOR:
    definition: |
      "An LLM queried for evidence.
       Sensors never make decisions.
       Sensors provide data for decisions."
       
  ENGINE:
    definition: |
      "A library that performs specialized computation.
       Engines are not agents.
       Engines contribute to decisions but don't make them."
       
  GRAPH:
    definition: |
      "A data structure containing nodes and edges.
       All graphs are stored in the Knowledge Graph.
       Graphs represent relationships between objects."
```

---

### Forbidden Words

```yaml
FORBIDDEN_WORDS:

  AGENT:
    forbidden: true
    reason: "Too vague. Use 'Provider' instead."
    replacement: "Provider"
    
  MEMORY:
    forbidden: true
    reason: "Ambiguous. Always specify the type."
    replacement: "Mission Memory | Knowledge Memory | Execution Memory"
    
  BRAIN:
    forbidden: true
    reason: "Can mean Kernel or Engine. Always specify."
    replacement: "Core Brain | Meta Brain | Reasoning Engine"
    
  LAYER:
    forbidden: true
    reason: "Architectural slang. Use 'component' or 'module'."
    replacement: "Component | Module | System"
    
  SMART:
    forbidden: true
    reason: "Vague. Specify WHAT is smart."
    replacement: "Intelligent | Adaptive | Optimized"
    
  MAGIC:
    forbidden: true
    reason: "Hand-wavy. Everything must be explainable."
    replacement: "Automated | Implicit | Optimized"
```

---

## CANON-002: Forbidden Words

> **Some words are too dangerous to use.**

---

### Complete Forbidden Words List

```yaml
ForbiddenWords:
  
  # Generic AI Terms
  AGENT:
    why: "Vague, means different things to different people"
    use_instead: "Provider | Executor | Capability Implementer"
    
  AI:
    why: "Too generic"
    use_instead: "LLM | Model | AI System"
    
  SMART:
    why: "Non-specific"
    use_instead: "Intelligent | Adaptive | Optimized"
    
  MAGIC:
    why: "Everything must be explainable"
    use_instead: "Automated | Implicit"
    
  # Confusing Architecture Terms
  LAYER:
    why: "Often misused"
    use_instead: "Component | Module | Tier"
    
  CORE:
    why: "Often misused as everything"
    use_instead: "Kernel | Central Component"
    
  ENGINE:
    why: "Sometimes means brain, sometimes means tool"
    use_instead: "Computing Engine | Reasoning Engine"
    
  # Ambiguous Terms
  MEMORY:
    why: "What kind? How long?"
    use_instead: "Mission Memory | Knowledge Memory | Execution Memory"
    
  STATE:
    why: "Too generic"
    use_instead: "Execution State | Mission State | System State"
    
  CONTEXT:
    why: "Can mean anything"
    use_instead: "Mission Context | Execution Context"
    
  # Verb Terms
  THINK:
    why: "What does this mean technically?"
    use_instead: "Reason | Analyze | Compute"
    
  KNOW:
    why: "Vague"
    use_instead: "Have Evidence | Have Knowledge"
    
  UNDERSTAND:
    why: "What does this mean?"
    use_instead: "Process | Analyze | Interpret"
```

---

### Required Qualifiers

```yaml
RequiredQualifiers:
  
  MEMORY:
    mandatory: true
    options:
      - "Mission Memory"       # Short-term, mission-scoped
      - "Knowledge Memory"    # Long-term, validated knowledge
      - "Execution Memory"    # Per-execution, ephemeral
      - "System Memory"       # Kernel's working memory
      
  BRAIN:
    mandatory: true
    options:
      - "Core Brain"         # Makes all decisions
      - "Meta Brain"         # Audits Core Brain
      - "Reasoning Brain"     # Part of AIE
      
  ENGINE:
    mandatory: true
    options:
      - "Logic Engine"        # Formal reasoning
      - "Planning Engine"     # Goal decomposition
      - "Optimization Engine" # Finding best solutions
      - "Simulation Engine"   # What-if analysis
      
  GRAPH:
    mandatory: true
    options:
      - "Decision Graph"      # Decision reasoning
      - "Knowledge Graph"      # Facts and relationships
      - "Dependency Graph"     # Task dependencies
      - "Resource Graph"       # Resource relationships
```

---

## CANON-003: Canonical Flow

> **There is ONE official flow. No alternatives.**

---

### The Canonical Mission Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     CANONICAL FLOW                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐                                                │
│  │  GOAL   │ ◄── User declares                            │
│  └────┬────┘                                              │
│       │                                                    │
│       ▼                                                    │
│  ┌─────────┐                                                │
│  │ MISSION │ ◄── Core Brain decomposes                    │
│  └────┬────┘                                              │
│       │                                                    │
│       ▼                                                    │
│  ┌─────────┐                                                │
│  │ PLANNING│ ◄── Tasks are created                        │
│  └────┬────┘                                              │
│       │                                                    │
│       ▼                                                    │
│  ┌───────────┐                                             │
│  │CAPABILITY │ ◄── What to execute                       │
│  └─────┬─────┘                                             │
│        │                                                   │
│        ▼                                                   │
│  ┌──────────┐                                              │
│  │ PROVIDER │ ◄── Who executes                           │
│  └────┬─────┘                                              │
│       │                                                    │
│       ▼                                                   │
│  ┌───────────┐                                             │
│  │ EXECUTION│ ◄── The actual work                       │
│  └─────┬─────┘                                             │
│        │                                                   │
│        ▼                                                   │
│  ┌────────────┐                                            │
│  │VERIFICATION│ ◄── Is it correct?                       │
│  └──────┬─────┘                                            │
│         │                                                  │
│         ▼                                                  │
│  ┌──────────┐                                              │
│  │KNOWLEDGE │ ◄── Extract what we learned                 │
│  └────┬─────┘                                              │
│       │                                                   │
│       ▼                                                  │
│  ┌──────────┐                                              │
│  │ LEARNING │ ◄── Update for next time                   │
│  └────┬─────┘                                              │
│       │                                                   │
│       ▼                                                  │
│  ┌──────────┐                                             │
│  │DECISION  │ ◄── What did we achieve?                   │
│  └──────────┘                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Forbidden Flows

```yaml
FORBIDDEN_FLOWS:

  # No direct execution
  WRONG: "User → Execution → Done"
  RIGHT: "User → Goal → Mission → Capability → Provider → Execution → Verification"
  
  # No skipping verification
  WRONG: "Execution → Done"
  RIGHT: "Execution → Verification → Done"
  
  # No execution without capability
  WRONG: "Provider → Execution"
  RIGHT: "Capability selection → Provider → Execution"
  
  # No decision without evidence
  WRONG: "Core Brain decides"
  RIGHT: "Evidence → Options → Simulation → Decision"
```

---

## CANON-004: Canonical Object Ownership

> **Ownership is strictly defined. No ambiguity.**

---

### Ownership Rules

```yaml
OwnershipRules:

  CAPABILITY_OWNS:
    - Nothing
    
    capability_is:
      - "A contract declared by Kernel"
      - "A capability is IMPLEMENTED by Provider"
      - "A capability is USED BY Task"
      
  PROVIDER_OWNS:
    - Its own execution state
    - Its own configuration
    - Its own health metrics
    
    provider_does_not_own:
      - "Capabilities (it implements them)"
      - "Missions (it serves them)"
      - "Decisions (Kernel makes them)"
      
  MISSION_OWNS:
    - Tasks (it decomposes into them)
    - Artifacts (it produces them)
    - Context (it defines it)
    
    mission_does_not_own:
      - "Capabilities (it uses them)"
      - "Providers (it selects them)"
      - "Knowledge (it references it)"
      
  TASK_OWNS:
    - Execution instances
    - Task-specific artifacts
    - Task checkpoints
    
    task_does_not_own:
      - "The capability (it uses it)"
      - "The provider (it selects it)"
      
  KNOWLEDGE_OWNS:
    - Evidence
    - Confidence scores
    - Source references
    
    knowledge_does_not_own:
      - "Artifacts (it references them)"
      - "Decisions (it informs them)"
      
  DECISION_OWNS:
    - Reasoning chain
    - Evidence used
    - Options considered
    
    decision_does_not_own:
      - "Execution (it reviews it)"
      - "Providers (it selects them)"
```

---

### Relationship Types

```yaml
RelationshipRules:

  IMPLEMENTS:
    subject: "Provider"
    object: "Capability"
    meaning: "Provider declares it can fulfill Capability"
    example: "OpenHands implements 'generate_api' capability"
    
  USES:
    subject: "Task"
    object: "Capability"
    meaning: "Task requires this Capability"
    example: "Task uses 'generate_api' capability"
    
  SELECTS:
    subject: "Core Brain"
    object: "Provider"
    meaning: "Core Brain chooses this Provider for a Task"
    example: "Core Brain selects OpenHands for 'generate_api'"
    
  DECOMPOSES_INTO:
    subject: "Mission"
    object: "Task"
    meaning: "Mission is broken into Tasks"
    example: "Mission decomposes into 10 Tasks"
    
  DERIVES_FROM:
    subject: "Mission"
    object: "Goal"
    meaning: "Mission achieves part of Goal"
    example: "Mission derives from 'Build E-commerce' Goal"
    
  PRODUCES:
    subject: "Execution"
    object: "Artifact"
    meaning: "Execution creates Artifact"
    example: "Execution produces 'api.py' Artifact"
    
  REFERENCES:
    subject: "Mission"
    object: "Knowledge"
    meaning: "Mission uses existing Knowledge"
    example: "Mission references 'API patterns' Knowledge"
    
  INFORMS:
    subject: "Knowledge"
    object: "Decision"
    meaning: "Knowledge contributes to Decision"
    example: "Benchmark Knowledge informs Provider selection"
```

---

## CANON-005: Canonical Decision Rules

> **Every decision has rules. No arbitrary decisions.**

---

### Provider Selection Rules

```yaml
ProviderSelectionRules:
  
  MANDATORY_FACTORS:
    - capability_fit: "Does provider implement required capability?"
    - quality_score: "What's the provider's historical quality?"
    - reliability: "What's the provider's uptime?"
    
  WEIGHTED_FACTORS:
    latency:
      weight: 0.15
      direction: "lower is better"
    cost:
      weight: 0.10
      direction: "lower is better"
    security:
      weight: 0.20
      direction: "higher is better"
    track_record:
      weight: 0.25
      direction: "higher is better"
    certification:
      weight: 0.10
      direction: "higher is better"
      
  FORBIDDEN_FACTORS:
    - "Provider name"
    - "Provider popularity"
    - "Provider cost without quality"
    - "Last successful execution"
    
  REQUIRED_CHECKS:
    - "Provider implements capability"
    - "Provider passes policy checks"
    - "Provider has budget allocation"
    - "Provider is not blocked"
```

---

### Mission State Transition Rules

```yaml
MissionStateRules:
  
  VALID_TRANSITIONS:
    DISCOVERY_EXPLORING → [DISCOVERY_COMPLETED, FAILED]
    DISCOVERY_COMPLETED → [ARCHITECTURE_DESIGNING]
    ARCHITECTURE_DESIGNING → [ARCHITECTURE_REVIEWING, FAILED]
    ARCHITECTURE_REVIEWING → [ARCHITECTURE_APPROVED, ARCHITECTURE_DESIGNING]
    ARCHITECTURE_APPROVED → [PLANNING_PLANNING]
    PLANNING_PLANNING → [PLANNING_APPROVED, FAILED]
    PLANNING_APPROVED → [EXECUTION_QUEUED]
    EXECUTION_QUEUED → [EXECUTION_RUNNING, EXECUTION_FAILED]
    EXECUTION_RUNNING → [EXECUTION_COMPLETED, EXECUTION_PAUSED, EXECUTION_FAILED]
    EXECUTION_COMPLETED → [VERIFICATION_TESTING]
    VERIFICATION_TESTING → [VERIFICATION_PASSED, VERIFICATION_FAILED]
    VERIFICATION_PASSED → [DEPLOYMENT_DEPLOYING]
    DEPLOYMENT_DEPLOYING → [DEPLOYMENT_DEPLOYED, DEPLOYMENT_ROLLED_BACK]
    DEPLOYMENT_DEPLOYED → [MONITORING_ACTIVE]
    
  REQUIRED_BEFORE_TRANSITION:
    DISCOVERY_COMPLETED:
      - "At least one requirement documented"
      - "At least one constraint identified"
    ARCHITECTURE_APPROVED:
      - "Architecture reviewed by Meta Brain"
      - "Architecture meets policy requirements"
    PLANNING_APPROVED:
      - "All tasks estimated"
      - "Budget approved"
    EXECUTION_COMPLETED:
      - "All tasks completed"
      - "All artifacts produced"
```

---

## CANON-006: Canonical Principles

> **These principles are absolute. Non-negotiable.**

---

### The 10 AgOS Principles

```yaml
Principles:

  1. EVERYTHING_REPLACEABLE:
     statement: "No component is irreplaceable."
     implications:
       - "Core Brain can be upgraded"
       - "Providers can be swapped"
       - "Models can be changed"
       - "Capabilities can be reimplemented"
       
  2. EVERYTHING_VERSIONED:
     statement: "Every object has a version."
     implications:
       - "No unversioned objects"
       - "Version history preserved"
       - "Breaking changes require major version"
       
  3. EVERYTHING_OBSERVABLE:
     statement: "Everything can be monitored."
     implications:
       - "Metrics available"
       - "Tracing enabled"
       - "Logs captured"
       
  4. EVERYTHING_VERIFIABLE:
     statement: "Everything can be verified."
     implications:
       - "Tests exist"
       - "Benchmarks exist"
       - "Quality scores exist"
       
  5. EVERYTHING_MEASURABLE:
     statement: "Everything can be measured."
     implications:
       - "Metrics collected"
       - "Costs tracked"
       - "Quality scored"
       
  6. EVERYTHING_EXPLAINABLE:
     statement: "Every decision has reasoning."
     implications:
       - "Evidence stored"
       - "Options documented"
       - "Context preserved"
       
  7. EVERYTHING_RECOVERABLE:
     statement: "Everything can be recovered."
     implications:
       - "Checkpoints exist"
       - "State persisted"
       - "Rollback possible"
       
  8. EVERYTHING_TESTABLE:
     statement: "Everything can be tested."
     implications:
       - "Unit tests exist"
       - "Integration tests exist"
       - "E2E tests exist"
       
  9. EVERYTHING_DOCUMENTED:
     statement: "Everything has documentation."
     implications:
       - "APIs documented"
       - "Schemas documented"
       - "Behavior documented"
       
  10. EVERYTHING_POLICIED:
      statement: "Everything has policy constraints."
      implications:
        - "Security policies"
        - "Budget policies"
        - "Compliance policies"
```

---

## CANON-007: Canonical Diagrams

> **Every diagram type has an official format.**

---

### Diagram Standards

```yaml
DiagramStandards:

  FLOW_DIAGRAM:
    tool: "Mermaid"
    syntax: "flowchart LR"
    shapes:
      - "Rectangle: Process"
      - "Diamond: Decision"
      - "Circle: Start/End"
      - "Parallelogram: Input/Output"
      
  STATE_MACHINE:
    tool: "Mermaid"
    syntax: "stateDiagram-v2"
    format:
      - "State names: UPPERCASE_WITH_UNDERSCORES"
      - "Transitions: -->"
      - "Guards: [condition]"
      
  SEQUENCE_DIAGRAM:
    tool: "Mermaid"
    syntax: "sequenceDiagram"
    format:
      - "Actors: rectangles"
      - "Messages: arrows"
      - "Loops: rect with note"
      
  CLASS_DIAGRAM:
    tool: "Mermaid"
    syntax: "classDiagram"
    format:
      - "Classes: rectangles"
      - "Relationships: arrows"
      - "Inheritance: --|>"
      
  ER_DIAGRAM:
    tool: "Mermaid"
    syntax: "erDiagram"
    format:
      - "Entities: rectangles"
      - "Relationships: lines with markers"
```

---

## CANON-008: Canonical Naming

> **Naming follows strict rules.**

---

### Naming Conventions

```yaml
NamingConventions:

  OBJECTS:
    format: "{Name}Object"
    examples:
      - "GoalObject"
      - "MissionObject"
      - "CapabilityObject"
      
  GRAPHS:
    format: "{Name}Graph"
    examples:
      - "DecisionGraph"
      - "KnowledgeGraph"
      - "DependencyGraph"
      
  ENGINES:
    format: "{Name}Engine"
    examples:
      - "ReasoningEngine"
      - "OptimizationEngine"
      - "SimulationEngine"
      
  POLICIES:
    format: "{Name}Policy"
    examples:
      - "SecurityPolicy"
      - "BudgetPolicy"
      - "RetryPolicy"
      
  CONTRACTS:
    format: "{Name}Contract"
    examples:
      - "CapabilityContract"
      - "ProviderContract"
      - "ExecutionContract"
      
  SCHEMAS:
    format: "{Name}Schema"
    examples:
      - "GoalSchema"
      - "MissionSchema"
      - "ExecutionSchema"
```

---

## CANON-009: Canonical Contracts

> **Contracts are immutable. Changes require versioning.**

---

### Contract Versioning Rules

```yaml
ContractVersioning:

  SEMVER_RULES:
    MAJOR:
      - "Removing a required field"
      - "Changing a field type"
      - "Removing an enum value"
      - "Changing behavior"
      
    MINOR:
      - "Adding optional field"
      - "Adding enum value"
      - "Adding optional parameter"
      
    PATCH:
      - "Documentation changes"
      - "Bug fixes"
      - "Clarifications"
      
  COMPATIBILITY:
    STRICT:
      - "All versions must be backward compatible"
      - "Newer providers must work with older consumers"
      
    GRACEFUL:
      - "Breaking changes require major version"
      - "Deprecation period required"
```

---

## CANON-010: Canonical Testing

> **Everything must be tested. No exceptions.**

---

### Testing Requirements

```yaml
TestingRequirements:

  PROVIDER_TESTING:
    mandatory:
      - "Unit tests: 80% coverage minimum"
      - "Integration tests with mock capabilities"
      - "Contract compliance tests"
      - "Benchmark tests"
      
    certification_required:
      - "All tests must pass"
      - "Performance benchmarks must meet threshold"
      - "Security scan must pass"
      
  CAPABILITY_TESTING:
    mandatory:
      - "Input validation tests"
      - "Output format tests"
      - "Error handling tests"
      - "Timeout tests"
      
  KERNEL_TESTING:
    mandatory:
      - "Decision logic tests"
      - "State machine tests"
      - "Policy enforcement tests"
      - "Graph consistency tests"
```

---

## Enforcement

```yaml
Enforcement:

  LINTING:
    tool: "AGOS Canon Linter"
    checks:
      - "No forbidden words"
      - "Naming conventions"
      - "Flow violations"
      - "Ownership violations"
      
  CODE_REVIEW:
    rules:
      - "Canon violations block merge"
      - "Two reviewers minimum for Canon changes"
      - "Breaking Canon requires Architecture Decision Record"
      
  AUTOMATED:
    - "Pre-commit hooks for Canon checks"
    - "CI/CD validation"
    - "Documentation generation from Canon"
```

---

## Change Process

```yaml
ChangeProcess:

  MINOR_CHANGES:
    - "Propose change"
    - "Discussion in community"
    - "Architecture team review"
    - "Vote (simple majority)"
    
  MAJOR_CHANGES:
    - "Propose ADR"
    - "Public discussion (30 days)"
    - "Community vote (2/3 majority)"
    - "Graceful deprecation period"
```

---

*This is Canon 001-010 of AGOS.*
*These rules are absolute and unbreakable.*
