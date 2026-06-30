# Execution Manager

> **Traffic controller. Does NOT execute. Only routes.**

---

## Purpose

The Execution Manager is the traffic controller that sends tasks to tools. It does NOT execute anything itself - it only routes.

---

## Core Concept

```
Execution Manager is like an Air Traffic Controller:

❌ It does NOT fly planes
❌ It does NOT build planes
❌ It does NOT maintain planes

✅ It ONLY directs planes
   "Task 18, go to Runway 3 for Tool X"
```

---

## Input → Output

```
ExecutionRequest:
  task: Task
  tool: Tool
  context: Context
  
      ↓
Execution Manager
      
      ↓
ExecutionResult:
  status: "completed"
  artifacts: {...}
  metrics: {...}
```

---

## Routing Flow

```
Task 18
    ↓
Capability: "Repository Analysis"
    ↓
Best Tool: "Sourcegraph"
    ↓
Execute via Tool Adapter
    ↓
Return Result
```

---

## Manager Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Route Tasks** | Send tasks to correct tools |
| **Manage Queue** | Order task execution |
| **Monitor Progress** | Track task status |
| **Handle Timeouts** | Enforce task timeouts |
| **Collect Results** | Gather tool outputs |
| **Report Status** | Update task status |

---

## What It Does NOT Do

| Forbidden | Reason |
|-----------|--------|
| ❌ Write code | Tools execute |
| ❌ Run commands | Tools execute |
| ❌ Edit files | Tools execute |
| ❌ Compile | Tools compile |
| ❌ Deploy | Tools deploy |
| ❌ Make decisions | Decision Engine decides |

---

## Task Routing

```python
class ExecutionManager:
    """Routes tasks to appropriate tools."""
    
    async def execute_task(
        self,
        task: Task,
        context: ExecutionContext
    ) -> ExecutionResult:
        """
        Route task to tool adapter.
        Does NOT execute directly.
        """
        
        # 1. Get tool from selection
        tool = await self.capability_selector.select(task.capability)
        
        # 2. Prepare execution context
        exec_context = self.prepare_context(task, tool)
        
        # 3. Send to tool adapter
        adapter = self.get_adapter(tool.type)
        result = await adapter.execute(exec_context)
        
        # 4. Return result (don't modify)
        return result
```

---

## Queue Management

```yaml
QueueManagement:
  # Task ordering based on graph
  
  ready_queue:
    # Tasks with all dependencies complete
    
  waiting_queue:
    # Tasks waiting for dependencies
    
  running_queue:
    # Currently executing
    
  completed_queue:
    # Successfully completed
    
  failed_queue:
    # Failed tasks pending retry
    
  priority_ordering:
    CRITICAL: 1
    HIGH: 2
    MEDIUM: 3
    LOW: 4
```

---

## Parallel Execution

```yaml
ParallelExecution:
  # Multiple tools can run simultaneously
  
  max_parallel: 3  # Max concurrent tasks
  
  parallel_groups:
    # Tasks that can run together
    
    group_1:
      - task_2
      - task_3
      # Both ready, run in parallel
      
    group_2:
      - task_4
      - task_5
      - task_7
      # All ready, run in parallel
```

---

## Timeout Management

```yaml
TimeoutRules:
  # Default timeouts by capability
  
  generate_code: 300  # 5 minutes
  edit_code: 120      # 2 minutes
  review_code: 180    # 3 minutes
  deploy: 600         # 10 minutes
  search: 30          # 30 seconds
  browse: 120         # 2 minutes
  
  # Custom timeout
  if task.has_custom_timeout:
    use task.timeout
    
  # If exceeded
  → Recovery Engine notified
```

---

## Result Collection

```python
async def collect_results(
    task_ids: list[str]
) -> list[ExecutionResult]:
    """
    Collect results from multiple parallel executions.
    """
    
    results = []
    
    for task_id in task_ids:
        result = await self.result_store.get(task_id)
        results.append(result)
    
    return results
```

---

## Status Reporting

```yaml
ExecutionStatus:
  task_id: "task_18"
  
  status: "running"  # Pending, Ready, Running, Done, Failed
  
  progress:
    completed: 3
    running: 2
    pending: 5
    failed: 1
    
  current_tasks:
    - task_id: "task_4"
      started_at: "2024-01-15T10:30:00Z"
      tool: "openhands"
      
    - task_id: "task_5"
      started_at: "2024-01-15T10:30:05Z"
      tool: "aider"
      
  metrics:
    avg_task_duration: "2m 30s"
    success_rate: 0.85
    tool_usage:
      openhands: 5
      aider: 3
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Tool unavailable | Request reselection |
| Timeout | Notify Recovery Engine |
| Invalid result | Notify Verification Engine |
| Resource exhausted | Pause execution |

---

## Integration Points

```
Execution Manager connects to:

    → Decision Engine (get decisions)
    → Capability Selector (get tools)
    → Verification Engine (send results)
    → Recovery Engine (handle failures)
    → Learning Engine (report metrics)
```

---

## Related Documents

- [Verification-Engine.md](./04-Verification-Engine.md)
- [Recovery-Engine.md](./05-Recovery-Engine.md)
- [Learning-Engine.md](./06-Learning-Engine.md)
