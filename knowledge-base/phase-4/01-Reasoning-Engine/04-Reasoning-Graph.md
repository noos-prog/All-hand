# Reasoning Graph

> **Instead of Chain of Thought, we build a Reasoning Graph.**

---

## Graph Concept

```
Not Chain of Thought:

Goal → Thought 1 → Thought 2 → Thought 3 → Decision

But Reasoning Graph:

Goal
  │
  ├── Facts
  │     ├── Fact 1
  │     ├── Fact 2
  │     └── Fact 3
  │
  ├── Constraints
  │     ├── Constraint 1
  │     └── Constraint 2
  │
  ├── Unknowns
  │     ├── Unknown 1
  │     └── Unknown 2
  │
  ├── Options
  │     ├── Option A
  │     ├── Option B
  │     └── Option C
  │
  ├── Decisions
  │     ├── Decision 1
  │     └── Decision 2
  │
  └── Execution
        ├── Task 1
        ├── Task 2
        └── Task 3
```

---

## Reasoning Graph Schema

```yaml
ReasoningGraph:
  # Identification
  id: string
  goal_id: string
  version: string
  created_at: datetime
  
  # Graph Structure
  nodes: list[ReasoningNode]
  edges: list[ReasoningEdge]
  
  # Verification
  is_complete: boolean
  completeness_score: 0.0-1.0
  confidence_score: 0.0-1.0
```

---

## Node Types

```yaml
ReasoningNode:
  id: string
  type: enum          # FACT, CONSTRAINT, UNKNOWN, OPTION, DECISION, TASK
  label: string
  content: string
  
  # For facts
  fact:
    statement: string
    source: string
    confidence: 0.0-1.0
    evidence: list[string]
    
  # For constraints
  constraint:
    type: enum        # budget, deadline, security, etc.
    value: string
    is_hard: boolean
    
  # For unknowns
  unknown:
    description: string
    impact: string
    investigation_required: boolean
    
  # For options
  option:
    description: string
    pros: list[string]
    cons: list[string]
    estimated_cost: decimal
    estimated_time: duration
    
  # For decisions
  decision:
    choice: string
    reasoning: string
    confidence: 0.0-1.0
    alternatives_rejected: list[string]
    
  # For tasks
  task:
    task_id: string
    capability: CapabilityID
    status: enum
```

---

## Edge Types

```yaml
ReasoningEdge:
  from_node: string
  to_node: string
  type: enum        # derives_from, contradicts, supports, requires, leads_to
  
  # For reasoning chains
  supports:
    strength: enum    # STRONG, MODERATE, WEAK
    explanation: string
    
  # For conflicts
  contradicts:
    explanation: string
    resolution: string
```

---

## Reasoning Process

```python
async def build_reasoning_graph(
    goal: Goal,
    context: Context
) -> ReasoningGraph:
    """
    Build reasoning graph for a goal.
    """
    
    graph = ReasoningGraph(goal_id=goal.id)
    
    # 1. Extract facts
    facts = await extract_facts(goal, context)
    graph.add_nodes(facts, type="FACT")
    
    # 2. Extract constraints
    constraints = await extract_constraints(goal)
    graph.add_nodes(constraints, type="CONSTRAINT")
    
    # 3. Identify unknowns
    unknowns = await identify_unknowns(goal, context)
    graph.add_nodes(unknowns, type="UNKNOWN")
    
    # 4. Generate options
    options = await generate_options(goal, facts, constraints)
    graph.add_nodes(options, type="OPTION")
    
    # 5. Make decisions
    decisions = await make_decisions(options, constraints)
    graph.add_nodes(decisions, type="DECISION")
    
    # 6. Create execution tasks
    tasks = await create_tasks(decisions)
    graph.add_nodes(tasks, type="TASK")
    
    # 7. Build edges
    graph.add_edges(build_edges(graph))
    
    # 8. Validate completeness
    graph.is_complete = validate_graph(graph)
    
    return graph
```

---

## Example: Build E-commerce Platform

```yaml
ReasoningGraph:
  id: "rg_001"
  goal_id: "goal_2024_001"
  
  nodes:
    # Facts
    - id: "fact_1"
      type: "FACT"
      label: "User needs multi-tenant"
      content: "System must support multiple tenants"
      fact:
        statement: "Multi-tenancy is required"
        source: "User request"
        confidence: 1.0
        evidence: ["User explicitly stated"]
        
    - id: "fact_2"
      type: "FACT"
      label: "Budget constraint"
      content: "Budget is $500/month"
      fact:
        statement: "Budget limited to $500/month"
        source: "User constraints"
        confidence: 1.0
        
    # Constraints
    - id: "constraint_1"
      type: "CONSTRAINT"
      label: "Python required"
      content: "Must use Python"
      constraint:
        type: "language"
        value: "Python"
        is_hard: true
        
    - id: "constraint_2"
      type: "CONSTRAINT"
      label: "Deadline"
      content: "1 month deadline"
      constraint:
        type: "deadline"
        value: "2024-02-15"
        is_hard: true
        
    # Unknowns
    - id: "unknown_1"
      type: "UNKNOWN"
      label: "Payment processor"
      content: "Which payment processor?"
      unknown:
        description: "Payment processor not specified"
        impact: "Affects integration complexity"
        investigation_required: true
        
    # Options
    - id: "option_1"
      type: "OPTION"
      label: "Option A: Build custom"
      option:
        description: "Build multi-tenancy from scratch"
        pros: ["Full control", "Custom fit"]
        cons: ["Time consuming", "Complex"]
        estimated_cost: 300
        estimated_time: "4 weeks"
        
    - id: "option_2"
      type: "OPTION"
      label: "Option B: Use SaaS"
      option:
        description: "Use SaaS multi-tenancy solution"
        pros: ["Fast", "Managed"]
        cons: ["Vendor lock-in", "Cost"]
        estimated_cost: 500
        estimated_time: "2 weeks"
        
    # Decision
    - id: "decision_1"
      type: "DECISION"
      label: "Decision: Build custom"
      decision:
        choice: "Option A: Build custom"
        reasoning: "Budget allows it, gives full control"
        confidence: 0.8
        alternatives_rejected: ["Option B: Use SaaS (too expensive)"]
        
  edges:
    - from_node: "constraint_2"
      to_node: "option_1"
      type: "constrains"
      
    - from_node: "fact_2"
      to_node: "decision_1"
      type: "supports"
      supports:
        strength: "STRONG"
        explanation: "Budget sufficient for custom build"
```

---

## Graph Visualization

```
                    GOAL: Build E-commerce Platform
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
     FACTS               CONSTRAINTS            UNKNOWNS
        │                     │                     │
   Multi-tenant          Python               Payment
   required             required             processor?
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                           OPTIONS
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
         Option A                         Option B
      (Build Custom)                    (Use SaaS)
              │                               │
              │     ┌─────────────────────────┘
              │     │
              │     └───────────────────────────────┐
              │                                     │
              ▼                                     ▼
         DECISION                               REJECTED
      Build Custom                          (Too expensive)
              │
              │     ┌─────────────────────────┐
              │     │                         │
              └────►│        TASKS            │
                    │                         │
                    │   1. Design Database   │
                    │   2. Build Backend      │
                    │   3. Build Frontend      │
                    │   4. Setup Deployment   │
                    │                         │
                    └─────────────────────────┘
```

---

## Verification

```yaml
GraphVerification:
  completeness:
    required_nodes:
      - FACT: "At least 1 fact"
      - CONSTRAINT: "All constraints identified"
      - UNKNOWN: "All unknowns identified"
      - OPTION: "At least 2 options"
      - DECISION: "Decision made"
      
  reasoning:
    - "All facts link to options"
    - "All constraints considered"
    - "Unknowns addressed"
    - "Alternatives documented"
    
  confidence:
    - Calculate average confidence
    - Flag low confidence nodes
```

---

## Explainability

Every decision in the graph can be traced:

```
To explain Decision 1:
1. What facts led to it?
   - Fact 1 (supports)
   - Fact 2 (supports)
   
2. What constraints applied?
   - Constraint 1 (required)
   - Constraint 2 (required)
   
3. What alternatives existed?
   - Option A (chosen)
   - Option B (rejected: cost too high)
   
4. What is the confidence?
   - 0.8 (80% confident)
```

---

## Related Documents

- [Goal-Object.md](./01-Goal-Object.md)
- [Decision-Matrix.md](./06-Decision-Matrix.md)
- [Explainability.md](../02-Decision-System/03-Explainability.md)
