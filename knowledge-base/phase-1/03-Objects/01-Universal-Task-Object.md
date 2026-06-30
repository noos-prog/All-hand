# Universal Task Object

> **Every task in the system transforms into this format.**

---

## Purpose

The Universal Task Object provides a standardized format for all tasks in the system, regardless of their source, type, or destination.

---

## Task Object Schema

```yaml
Task:
  # ========== Identification ==========
  id: string                    # Unique task identifier
  version: string              # Schema version
  created_at: datetime         # Creation timestamp
  
  # ========== Core Information ==========
  name: string                 # Human-readable name
  description: string          # Detailed description
  
  # ========== Goal Reference ==========
  goal_id: string             # Parent goal ID
  parent_task: string         # Parent task ID (if subtask)
  sub_tasks: list[string]     # Sub-task IDs
  
  # ========== Capability ==========
  capability: string          # Required capability
  sub_capabilities: list[string]  # Sub-capabilities if needed
  
  # ========== Input/Output ==========
  inputs:
    required: list            # Required inputs
    optional: list           # Optional inputs
    schema: object            # Input JSON schema
    
  outputs:
    expected: list            # Expected outputs
    schema: object            # Output JSON schema
    artifacts: list           # File artifacts
    
  # ========== Constraints ==========
  constraints:
    - name: string
      type: enum              # required, forbidden, limit
      value: any
      
  timeouts:
    max_duration: duration    # Maximum allowed time
    warning_threshold: duration  # When to warn
    
  resources:
    memory_mb: integer
    cpu_cores: decimal
    gpu: boolean
    
  # ========== Priority & Schedule ==========
  priority: enum              # Critical, High, Medium, Low
  deadline: datetime         # When must complete
  estimated_duration: duration
  
  # ========== Dependencies ==========
  dependencies:
    depends_on: list[string]  # Task IDs this depends on
    depended_by: list[string]  # Tasks depending on this
    blocking: list[string]    # Tasks blocked by this
    
  # ========== Status ==========
  status: enum                # See Status section
  progress: percentage        # 0-100
  
  # ========== Execution ==========
  assigned_tool: string       # Selected tool
  assigned_at: datetime       # When tool was assigned
  
  retry:
    count: integer           # Current retry count
    max_retries: integer     # Maximum allowed
    history: list            # Retry history
    
  # ========== Verification ==========
  verification:
    required: boolean        # Needs verification?
    type: enum                # full, quick, basic
    criteria: list           # What to verify
    status: enum              # pending, passed, failed
    result: object            # Verification result
    
  # ========== Metrics ==========
  metrics:
    start_time: datetime
    end_time: datetime
    duration: duration
    token_usage: integer
    api_calls: integer
    cost: decimal
    
  # ========== Results ==========
  result:
    status: enum              # success, failure, partial
    artifacts: list           # Output artifacts
    logs: list                # Execution logs
    errors: list               # Any errors
    
  # ========== Quality ==========
  quality:
    score: 0.0-1.0           # Quality score
    passed_verifications: integer
    failed_verifications: integer
    
  # ========== Context ==========
  context:
    environment: string       # dev, staging, prod
    tags: list[string]        # Searchable tags
    metadata: dict            # Additional metadata
```

---

## Task Status

```yaml
Status:
  # Lifecycle states
  
  PENDING: "Task created, not started"
  QUEUED: "Task in execution queue"
  READY: "Dependencies met, ready to execute"
  
  ASSIGNED: "Tool selected, awaiting execution"
  RUNNING: "Currently executing"
  
  VERIFYING: "Verification in progress"
  
  COMPLETED: "Successfully completed"
  COMPLETED_WITH_WARNING: "Done but with warnings"
  
  FAILED: "Execution failed"
  VERIFICATION_FAILED: "Verification failed"
  
  RETRYING: "Retrying after failure"
  
  CANCELLED: "Cancelled by user"
  ABORTED: "Aborted due to constraints"
  
  BLOCKED: "Waiting on dependencies"
```

---

## Task Priority

```yaml
Priority:
  CRITICAL:
    value: 1
    description: "Production down, must fix now"
    sla: "1 hour"
    escalation: "Immediate"
    
  HIGH:
    value: 2
    description: "Major feature blocked"
    sla: "4 hours"
    escalation: "4 hours"
    
  MEDIUM:
    value: 3
    description: "Feature enhancement"
    sla: "24 hours"
    escalation: "24 hours"
    
  LOW:
    value: 4
    description: "Nice to have"
    sla: "72 hours"
    escalation: "None"
```

---

## Task Types

```yaml
TaskType:
  GENERATE: "Generate new code/artifacts"
  EDIT: "Modify existing code"
  DELETE: "Remove code/artifacts"
  
  REVIEW: "Review code/docs"
  ANALYZE: "Analyze code/performance"
  TEST: "Run/create tests"
  
  DEPLOY: "Deploy to environment"
  CONFIGURE: "Configure system/settings"
  MIGRATE: "Migrate data/system"
  
  MONITOR: "Monitor system"
  ALERT: "Send alerts"
  REPORT: "Generate reports"
```

---

## Task Lifecycle

```
PENDING
   ↓ (dependencies met)
QUEUED
   ↓ (tool selected)
ASSIGNED
   ↓ (execution started)
RUNNING
   ↓ (execution complete)
VERIFYING
   ↓ (verification done)
COMPLETED / COMPLETED_WITH_WARNING / FAILED
   ↓ (if failed and retries left)
RETRYING → RUNNING
   ↓ (if failed and no retries)
FAILED → ESCALATE
```

---

## Task Dependencies

```yaml
Dependencies:
  # Example task graph
  
  task_1 (start):
    depended_by: [task_2, task_3]
    
  task_2:
    depends_on: [task_1]
    depended_by: [task_4]
    
  task_3:
    depends_on: [task_1]
    depended_by: [task_4]
    
  task_4:
    depends_on: [task_2, task_3]
    depended_by: [task_5]
    
  task_5 (end):
    depends_on: [task_4]
```

---

## Example Task

```yaml
Task:
  id: "task_15"
  version: "1.0"
  name: "Generate User Authentication"
  
  goal_id: "goal_3"
  
  capability: "generate_auth"
  
  inputs:
    required:
      - "user_model"
      - "auth_requirements"
    schema:
      type: "object"
      properties:
        user_model: {type: "object"}
        auth_requirements: {type: "object"}
        
  outputs:
    expected:
      - "login_endpoint"
      - "register_endpoint"
      - "auth_middleware"
    artifacts:
      - "src/auth/login.py"
      - "src/auth/register.py"
      
  constraints:
    - name: "framework"
      type: "required"
      value: "FastAPI"
    - name: "security"
      type: "required"
      value: "OAuth2"
      
  priority: "HIGH"
  deadline: "2024-01-20T12:00:00Z"
  estimated_duration: "15 minutes"
  
  dependencies:
    depends_on: ["task_14"]  # Database setup
    depended_by: ["task_16", "task_17"]
    
  verification:
    required: true
    type: "FULL"
    criteria: ["syntax", "lint", "tests", "security"]
```

---

## Validation Rules

```yaml
ValidationRules:
  - id: "valid_id"
    check: "Must be unique"
    
  - id: "has_capability"
    check: "Must have capability"
    
  - id: "has_inputs"
    check: "Required inputs must be specified"
    
  - id: "no_circular_deps"
    check: "No circular dependencies"
    
  - id: "valid_timeout"
    check: "Timeout must be positive"
    
  - id: "valid_priority"
    check: "Priority must be enum value"
```

---

## Related Documents

- [Universal-Result-Object.md](./02-Universal-Result-Object.md)
- [Planning-Engine.md](../01-Core-Brain/06-Planning-Engine.md)
