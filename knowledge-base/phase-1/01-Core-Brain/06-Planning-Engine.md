# Planning Engine

> **Transforms Goals into Task Graphs (DAGs), not Task Lists.**

---

## Purpose

The Planning Engine's only job is to convert a Goal Object into a Task Graph (DAG - Directed Acyclic Graph) with proper dependencies.

---

## Task Graph vs Task List

```
Task LIST (Wrong)                    Task GRAPH (Correct)
─────────────────                    ─────────────────────
Task 1                               ┌─────────┐
Task 2                               │Task 1   │
Task 3                               └────┬────┘
Task 4                                    │
                                    ┌─────┴─────┐
                                    │           │
                               ┌────┴───┐  ┌───┴────┐
                               │Task 2  │  │Task 3  │
                               └────┬───┘  └────┬───┘
                                    │           │
                                    └─────┬─────┘
                                          │
                                    ┌─────┴─────┐
                                    │  Task 4   │
                                    └───────────┘
```

**Task Graph shows:**
- Dependencies
- Parallel execution opportunities
- Critical path
- Execution order

---

## Task Graph Schema

```yaml
TaskGraph:
  # Identity
  id: string
  goal_id: string
  version: string
  
  # Graph Structure
  nodes: list[TaskNode]
  edges: list[TaskEdge]
  
  # Metadata
  created_at: datetime
  estimated_duration: duration
  critical_path: list[string]
  parallel_opportunities: integer
  
  # Quality
  completeness_score: 0.0-1.0
  dependency_depth: integer
```

---

## Task Node Schema

```yaml
TaskNode:
  # Identity
  id: string
  name: string
  description: string
  
  # Capability
  capability: string      # Required capability
  sub_capabilities: list  # Sub-capabilities if needed
  
  # Execution
  inputs: dict           # Required inputs
  outputs: dict          # Expected outputs
  
  # Constraints
  constraints: list      # Task-specific constraints
  timeout: duration      # Max execution time
  
  # Dependencies
  depends_on: list[string]  # Task IDs
  depended_by: list[string] # Tasks depending on this
  
  # Priority
  priority: enum         # Critical, High, Medium, Low
  parallel_with: list[string]  # Can run in parallel
  
  # Status
  status: enum           # Pending, Ready, Running, Done, Failed
  
  # Verification
  verification_steps: list
  acceptance_criteria: list
```

---

## Task Edge Schema

```yaml
TaskEdge:
  # Connection
  from_task: string      # Source task ID
  to_task: string       # Target task ID
  
  # Relationship
  type: enum            # dependency, parallel, conditional
  condition: string      # For conditional edges
  
  # Data Flow
  data_transfer: list[DataMapping]
    - from_output: string
    - to_input: string
```

---

## Graph Generation Process

```
1. Receive Goal Object
        ↓
2. Analyze goal requirements
        ↓
3. Identify capabilities needed
        ↓
4. Break down into atomic tasks
        ↓
5. Identify dependencies
        ↓
6. Create task nodes
        ↓
7. Create edges (dependencies)
        ↓
8. Identify parallel opportunities
        ↓
9. Calculate critical path
        ↓
10. Validate graph (no cycles)
        ↓
11. Optimize for execution
        ↓
12. Return TaskGraph
```

---

## Dependency Types

| Type | Symbol | Description |
|------|--------|-------------|
| `REQUIRES` | → | Must complete before |
| `ENABLES` | ⇢ | Makes next possible |
| `PARALLEL` | ∥ | Can run simultaneously |
| `CONDITIONAL` | ? | Run if condition met |
| `OPTIONAL` | ○ | Run if resources allow |

---

## Example: E-commerce Store

**Goal:** "Build an e-commerce store"

```
TaskGraph:
  nodes:
    - id: "task_1"
      name: "Design Architecture"
      capability: "architect"
      depends_on: []
      
    - id: "task_2"
      name: "Setup Backend"
      capability: "generate_backend"
      depends_on: ["task_1"]
      
    - id: "task_3"
      name: "Setup Database"
      capability: "setup_database"
      depends_on: ["task_1"]
      
    - id: "task_4"
      name: "Build Auth"
      capability: "generate_auth"
      depends_on: ["task_2"]
      
    - id: "task_5"
      name: "Build Products API"
      capability: "generate_api"
      depends_on: ["task_2", "task_3"]
      
    - id: "task_6"
      name: "Build Frontend"
      capability: "generate_frontend"
      depends_on: ["task_4", "task_5"]
      
    - id: "task_7"
      name: "Setup CI/CD"
      capability: "setup_cicd"
      depends_on: ["task_2"]
      
    - id: "task_8"
      name: "Deploy"
      capability: "deploy"
      depends_on: ["task_6", "task_7"]
```

**Graph Visualization:**
```
[task_1: Architecture]
         │
    ┌────┴────┐
    │         │
[task_2]    [task_3]
 Backend   Database
    │
    ├────┬────┐
    │    │    │
[task_4][task_5][task_7]
  Auth   Products  CI/CD
    │    │    │
    └────┴────┘
         │
    [task_6: Frontend]
         │
    [task_8: Deploy]
```

---

## Parallel Execution Opportunities

```yaml
Parallelization:
  level_1:
    # task_2, task_3 can run in parallel
    # (after task_1 completes)
    
  level_2:
    # task_4, task_5, task_7 can run in parallel
    # (after their dependencies complete)
    
  level_3:
    # task_6 runs alone
    
  level_4:
    # task_8 runs alone

Optimization:
  parallel_tasks: 3  # Max at once
  estimated_speedup: 40%
```

---

## Graph Validation Rules

| Rule | Description |
|------|-------------|
| `no_cycles` | Graph must be acyclic |
| `has_start` | Must have at least one start node |
| `has_end` | Must have at least one end node |
| `all_deps_met` | All dependencies reference existing tasks |
| `reachable` | All nodes reachable from start |
| `terminable` | All paths lead to end |

---

## Critical Path

```yaml
CriticalPath:
  # The longest path determines minimum time
  path: [task_1, task_2, task_5, task_6, task_8]
  duration: 8 hours
  
  # Tasks on critical path
  critical_tasks:
    - task_1: 1 hour
    - task_2: 2 hours
    - task_5: 2 hours
    - task_6: 2 hours
    - task_8: 1 hour
    
  # Optimization opportunities
  optimizations:
    - "Parallelize task_4 with task_5"
    - "Use faster tool for task_6"
```

---

## Graph Optimization

```python
def optimize_graph(graph: TaskGraph) -> TaskGraph:
    """Optimize graph for execution"""
    
    # 1. Identify parallel opportunities
    parallel_groups = find_parallel_groups(graph)
    
    # 2. Minimize critical path
    optimize_critical_path(graph)
    
    # 3. Balance workload
    balance_tasks_across_workers(graph)
    
    # 4. Add fallback paths
    add_fallback_edges(graph)
    
    return graph
```

---

## Dynamic Replanning

```
During execution, if task fails:

1. Identify affected tasks
        ↓
2. Check if task can be retried
        ↓
3. If not, replan subgraph
        ↓
4. Update dependencies
        ↓
5. Recalculate critical path
        ↓
6. Notify Execution Manager
        ↓
7. Continue execution
```

---

## Related Documents

- [03-Objects/Universal-Task-Object.md](./03-Objects/01-Universal-Task-Object.md)
- [02-Components/Execution-Manager.md](./02-Components/06-Execution-Manager.md)
