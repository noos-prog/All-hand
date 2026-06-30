# AGOS-001: Universal Object Model

> **The Foundation. The One Model to Rule Them All.**

---

## Status

```
Specification ID: AGOS-001
Version: 1.0.0
Status: FOUNDATIONAL
Type: Object Model
Priority: CRITICAL
Dependencies: None
```

---

## 1. Introduction

### 1.1 Purpose

This specification defines the **Universal Object Model (UOM)** - the single model that all AGOS components depend on.

```
If this is designed well:
  - Core Brain depends on it ✓
  - Execution depends on it ✓
  - Research Lab depends on it ✓
  - Providers depend on it ✓
  - SDK depends on it ✓
  - Database depends on it ✓
  - APIs depend on it ✓
  - Mobile/Web depend on it ✓

If this is designed poorly:
  - Everything must be redesigned
```

### 1.2 Design Principles

```yaml
Principles:
  1. COMPLETE
     - All entities are objects
     - No exceptions
     
  2. CONSISTENT
     - Same structure for all objects
     - Same patterns everywhere
     
  3. VALIDATABLE
     - Every object can be validated
     - Schema is the contract
     
  4. VERSIONABLE
     - Every object has version
     - Version history preserved
     
  5. RELATABLE
     - Objects link to objects
     - No orphan objects
```

---

## 2. Base Object

### 2.1 UniversalBase

Every object in AGOS inherits from `UniversalBase`.

```yaml
UniversalBase:
  # Identification
  id: UUID                      # Unique identifier
  rid: String                   # Resource ID (type:tenant:uuid:version)
  version: String               # Semantic version (x.y.z)
  
  # Timestamps
  created_at: DateTime          # ISO 8601
  updated_at: DateTime          # ISO 8601
  deleted_at: DateTime | null   # Soft delete
  
  # Ownership
  owner_id: UUID                # User or Organization
  tenant_id: UUID               # Multi-tenant isolation
  workspace_id: UUID            # Workspace isolation
  
  # State
  status: Enum                  # ACTIVE, INACTIVE, PENDING, FAILED
  health: Enum                  # HEALTHY, DEGRADED, UNHEALTHY
  
  # Metadata
  tags: Set[String]             # For filtering
  labels: Map[String, String]   # Custom labels
  annotations: Map[String, Any] # Extended metadata
  
  # Relationships
  created_by: UUID             # Actor who created
  updated_by: UUID             # Actor who last updated
  
  # Audit
  change_history: List[Change]  # Immutable audit trail
  version_history: List[Version # Semantic version history
```

### 2.2 JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://agos.dev/schemas/universal-base/v1",
  "title": "UniversalBase",
  "type": "object",
  "required": ["id", "rid", "version", "created_at", "updated_at", "status"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier"
    },
    "rid": {
      "type": "string",
      "pattern": "^[a-z]+:[a-z0-9]+:[a-z0-9-]+:v\\d+$",
      "description": "Resource ID: type:tenant:uuid:version"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last update timestamp"
    },
    "deleted_at": {
      "type": ["string", "null"],
      "format": "date-time",
      "description": "Soft delete timestamp"
    },
    "owner_id": {
      "type": "string",
      "format": "uuid"
    },
    "tenant_id": {
      "type": "string",
      "format": "uuid"
    },
    "workspace_id": {
      "type": ["string", "null"],
      "format": "uuid"
    },
    "status": {
      "type": "string",
      "enum": ["ACTIVE", "INACTIVE", "PENDING", "FAILED"]
    },
    "health": {
      "type": "string",
      "enum": ["HEALTHY", "DEGRADED", "UNHEALTHY"]
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    },
    "labels": {
      "type": "object",
      "additionalProperties": { "type": "string" }
    },
    "annotations": {
      "type": "object",
      "additionalProperties": true
    },
    "created_by": {
      "type": "string",
      "format": "uuid"
    },
    "updated_by": {
      "type": "string",
      "format": "uuid"
    },
    "change_history": {
      "type": "array",
      "items": { "$ref": "#/$defs/Change" }
    },
    "version_history": {
      "type": "array",
      "items": { "$ref": "#/$defs/Version" }
    }
  }
}
```

---

## 3. Core Objects

### 3.1 Goal Object

```yaml
Goal:
  inherits: UniversalBase
  type: "goal"
  
  # Goal Definition
  name: String                  # Human-readable name
  description: String          # Detailed description
  type: Enum                   # BUILD, FIX, REFACTOR, REVIEW, ANALYZE, DEPLOY
  priority: Enum               # CRITICAL, HIGH, MEDIUM, LOW
  
  # Goal Content
  statement: String            # The goal in natural language
  requirements: List[Requirement]
  constraints: List[Constraint]
  success_criteria: List[Criterion]
  
  # Goal State
  state: Enum                  # DRAFT, SUBMITTED, APPROVED, REJECTED, ARCHIVED
  approval_status: Enum        # PENDING, APPROVED, REJECTED
  approved_by: UUID | null
  approved_at: DateTime | null
  
  # Goal Relationships
  parent_goal_id: UUID | null  # For goal decomposition
  child_missions: List[Mission # Missions derived from this goal
  artifacts: List[Artifact]    # Artifacts produced
  
  # Goal Metrics
  estimated_cost: Decimal
  estimated_duration: Duration
  actual_cost: Decimal | null
  actual_duration: Duration | null
  
  # Goal Context
  domain: String               # E-commerce, Finance, etc.
  industry: String            # Technology, Healthcare, etc.
  scale: Enum                 # STARTUP, SMB, ENTERPRISE
```

### 3.2 Mission Object

```yaml
Mission:
  inherits: UniversalBase
  type: "mission"
  
  # Mission Definition
  name: String
  description: String
  goal_id: UUID               # Parent goal
  type: Enum                  # DISCOVERY, ARCHITECTURE, IMPLEMENTATION, TESTING, DEPLOYMENT, MONITORING
  
  # Mission State Machine
  state: Enum
    # DISCOVERY: EXPLORING, COMPLETED
    # ARCHITECTURE: DESIGNING, REVIEWING, APPROVED
    # PLANNING: PLANNING, APPROVED
    # EXECUTION: QUEUED, RUNNING, PAUSED, COMPLETED, FAILED
    # VERIFICATION: TESTING, PASSED, FAILED
    # DEPLOYMENT: DEPLOYING, DEPLOYED, ROLLED_BACK
    # MONITORING: ACTIVE, STABLE, UNSTABLE
  
  # Mission Content
  context: Context             # Mission context
  tasks: List[Task]          # Decomposed tasks
  decisions: List[Decision]   # Decisions made
  
  # Mission Progress
  progress: Decimal           # 0.0 - 1.0
  completion_percentage: Integer
  
  # Mission Resources
  budget: Budget
  time_allocation: Duration
  assigned_capabilities: List[UUID]
  assigned_providers: List[UUID]
  
  # Mission Quality
  quality_score: Decimal      # 0.0 - 1.0
  test_coverage: Decimal      # 0.0 - 1.0
  security_score: Decimal      # 0.0 - 1.0
  
  # Mission Output
  artifacts: List[Artifact]
  knowledge_extracted: List[Knowledge]
  lessons_learned: List[Lesson]
```

### 3.3 Capability Object

```yaml
Capability:
  inherits: UniversalBase
  type: "capability"
  
  # Capability Definition
  name: String                # e.g., "generate_api"
  display_name: String        # e.g., "Generate REST API"
  description: String
  category: Enum              # CODING, EDITING, REVIEW, ANALYSIS, DATABASE, DEVOPS, BROWSER, TESTING
  subcategory: String        # e.g., "Backend", "Frontend"
  
  # Capability Interface
  input_schema: JSONSchema    # Valid JSON Schema
  output_schema: JSONSchema    # Valid JSON Schema
  error_schema: JSONSchema    # Valid JSON Schema
  
  # Capability Constraints
  timeout: Duration           # Max execution time
  max_retries: Integer       # Max retry attempts
  required_capabilities: List[UUID]  # Dependencies
  
  # Capability Requirements
  required_permissions: List[Permission]
  required_resources: ResourceRequirements
  required_environment: Map[String, String]
  
  # Capability Quality
  success_rate: Decimal      # Historical success rate
  avg_duration: Duration      # Historical average duration
  avg_cost: Decimal          # Historical average cost
  
  # Capability Relationships
  providers: List[Provider]  # Providers that implement this
  tasks: List[Task]          # Tasks using this capability
  benchmarks: List[Benchmark] # Benchmark results
  
  # Capability Genome
  genome: CapabilityGenome   # Dimensions for matching
  
  # Capability Versioning
  contract_version: String    # Current contract version
  breaking_changes: List[String]
```

### 3.4 Provider Object

```yaml
Provider:
  inherits: UniversalBase
  type: "provider"
  
  # Provider Definition
  name: String               # e.g., "openhands"
  display_name: String       # e.g., "OpenHands AI Agent"
  description: String
  provider_type: Enum        # AI_AGENT, LLM, MCP, REST_API, CLI, DOCKER, BROWSER, DATABASE, CICD, SEARCH, STORAGE
  version: String            # Provider version
  
  # Provider Interface
  adapter_type: String       # Type of adapter
  connection_config: ConnectionConfig
  health_check_endpoint: String
  
  # Provider Capabilities
  capabilities: List[ProviderCapability]  # What this provider can do
  supported_inputs: List[String]
  supported_outputs: List[String]
  
  # Provider Performance
  reliability: Decimal       # 0.0 - 1.0
  avg_latency: Duration
  avg_cost: Decimal
  uptime: Decimal            # 0.0 - 1.0
  
  # Provider Genome
  genome: ProviderGenome     # Capability fingerprint
  
  # Provider Configuration
  config_schema: JSONSchema
  default_config: Map[String, Any]
  secrets_required: List[String]
  
  # Provider Limits
  rate_limit: RateLimit
  concurrent_limit: Integer
  resource_limits: ResourceLimits
  
  # Provider State
  health_status: Enum        # HEALTHY, DEGRADED, UNHEALTHY, UNKNOWN
  last_health_check: DateTime
  last_successful_call: DateTime
  last_failed_call: DateTime
  
  # Provider Certification
  certified: Boolean
  certification_tier: Enum   # BASIC, STANDARD, PREMIUM, ENTERPRISE
  certification_date: DateTime
  last_recertification: DateTime
```

### 3.5 Task Object

```yaml
Task:
  inherits: UniversalBase
  type: "task"
  
  # Task Definition
  name: String
  description: String
  mission_id: UUID           # Parent mission
  parent_task_id: UUID | null  # For task decomposition
  child_tasks: List[UUID]    # Sub-tasks
  
  # Task Specification
  capability_id: UUID        # Required capability
  provider_id: UUID | null  # Selected provider
  input: Object             # Task input (matches capability input_schema)
  
  # Task State Machine
  state: Enum
    # CREATED, QUEUED, SCHEDULED, PREPARING
    # RUNNING, WAITING, VERIFYING
    # COMPLETED, FAILED, CANCELLED, RETRYING
  
  # Task Execution
  execution_id: UUID | null # Active execution
  execution_history: List[ExecutionSummary]
  
  # Task Progress
  progress: Decimal          # 0.0 - 1.0
  checkpoints: List[Checkpoint]
  
  # Task Quality
  quality_score: Decimal     # 0.0 - 1.0
  verification_status: Enum  # PENDING, PASSED, FAILED
  
  # Task Output
  output: Object | null     # Task output (matches capability output_schema)
  artifacts: List[Artifact]
  errors: List[Error]
  
  # Task Timing
  estimated_duration: Duration
  actual_duration: Duration | null
  started_at: DateTime | null
  completed_at: DateTime | null
  
  # Task Cost
  estimated_cost: Decimal
  actual_cost: Decimal | null
  
  # Task Dependencies
  depends_on: List[UUID]    # Tasks this depends on
  depended_by: List[UUID]   # Tasks depending on this
  blocking: Boolean         # If true, blocks dependent tasks
```

### 3.6 Artifact Object

```yaml
Artifact:
  inherits: UniversalBase
  type: "artifact"
  
  # Artifact Definition
  name: String               # e.g., "api.py", "README.md"
  display_name: String
  description: String
  artifact_type: Enum       # SOURCE, DOCUMENT, CONFIG, DATA, IMAGE, VIDEO, LOG, ARCHIVE
  
  # Artifact Content
  content_type: String      # MIME type
  size_bytes: Integer
  checksum: String          # SHA-256
  content: Binary | String | Object  # Actual content or reference
  
  # Artifact Location
  storage_type: Enum        # INLINE, FILE, OBJECT_STORAGE, DATABASE
  storage_path: String      # Path or URL
  storage_region: String    # For multi-region
  
  # Artifact Relationships
  task_id: UUID | null      # Task that produced this
  mission_id: UUID | null   # Mission that owns this
  parent_artifact_id: UUID | null  # Parent artifact (for versions)
  versions: List[UUID]      # All versions of this artifact
  
  # Artifact Metadata
  language: String | null   # For source code
  framework: String | null
  line_count: Integer | null
  test_coverage: Decimal | null
  
  # Artifact Quality
  quality_score: Decimal    # 0.0 - 1.0
  lint_status: Enum         # PASSED, FAILED, SKIPPED
  scan_status: Enum         # PASSED, FAILED, SKIPPED
  
  # Artifact Access
  access_level: Enum        # PUBLIC, INTERNAL, PRIVATE, RESTRICTED
  encryption: Boolean
  retention_policy: String
```

### 3.7 Knowledge Object

```yaml
Knowledge:
  inherits: UniversalBase
  type: "knowledge"
  
  # Knowledge Definition
  name: String
  display_name: String
  description: String
  knowledge_type: Enum      # FACT, PATTERN, LESSON, RULE, METRIC, REFERENCE
  
  # Knowledge Content
  content: Object           # Structured knowledge
  summary: String          # Brief summary
  confidence: Decimal       # 0.0 - 1.0
  
  # Knowledge Evidence
  evidence: List[Evidence]
  sources: List[Source]
  verified: Boolean
  verification_method: String
  
  # Knowledge Context
  domain: List[String]      # Applicable domains
  capability_id: UUID | null # Related capability
  task_id: UUID | null      # Related task
  
  # Knowledge Relationships
  related_knowledge: List[UUID]
  contradicts: List[UUID]    # Contradicting knowledge
  supports: List[UUID]      # Supporting knowledge
  
  # Knowledge Lifecycle
  state: Enum               # ACTIVE, DEPRECATED, ARCHIVED
  deprecated_at: DateTime | null
  deprecation_reason: String | null
  
  # Knowledge Usage
  usage_count: Integer
  last_used_at: DateTime
  success_rate: Decimal     # When used, how often succeeded
```

### 3.8 Decision Object

```yaml
Decision:
  inherits: UniversalBase
  type: "decision"
  
  # Decision Definition
  name: String
  description: String
  decision_type: Enum       # STRATEGIC, TACTICAL, OPERATIONAL
  
  # Decision Context
  mission_id: UUID
  task_id: UUID | null
  context: Object           # Decision context
  
  # Decision Content
  question: String          # What was being decided
  options: List[Option]     # Options considered
  selected_option: Option   # What was selected
  
  # Decision Reasoning
  reasoning: String         # Why this option was selected
  evidence: List[Evidence]  # Evidence supporting decision
  assumptions: List[String] # Assumptions made
  unknowns: List[String]    # Unknowns acknowledged
  
  # Decision Graph Reference
  graph_id: UUID | null     # Associated decision graph
  graph_snapshot: Object    # Frozen decision graph
  
  # Decision Outcome
  outcome: Enum             # SUCCESS, FAILURE, PARTIAL, UNKNOWN
  outcome_reason: String | null
  outcome_evidence: Object
  
  # Decision Quality
  quality_score: Decimal    # 0.0 - 1.0
  bias_score: Decimal       # 0.0 - 1.0 (lower is better)
  
  # Decision Impact
  impact: Enum              # LOW, MEDIUM, HIGH, CRITICAL
  reversible: Boolean
  
  # Decision Audit
  made_by: UUID             # Who made the decision
  made_at: DateTime
  reviewed_by: UUID | null
  reviewed_at: DateTime | null
```

### 3.9 Policy Object

```yaml
Policy:
  inherits: UniversalBase
  type: "policy"
  
  # Policy Definition
  name: String
  display_name: String
  description: String
  policy_type: Enum         # SECURITY, BUDGET, RETRY, TIMEOUT, GOVERNANCE, APPROVAL, COMPLIANCE
  
  # Policy Scope
  scope: Enum               # GLOBAL, ORGANIZATION, PROJECT, MISSION
  scope_id: UUID | null     # ID of the scope
  
  # Policy Content
  rules: List[Rule]
  conditions: List[Condition]
  actions: List[Action]
  exceptions: List[Exception]
  
  # Policy Configuration
  priority: Integer         # Higher = more important
  enforcement: Enum         # ENFORCED, AUDIT, DISABLED
  conflict_resolution: Enum # FIRST, HIGHEST_PRIORITY, MOST_SPECIFIC
  
  # Policy State
  state: Enum               # DRAFT, ACTIVE, SUSPENDED, ARCHIVED
  effective_from: DateTime
  effective_until: DateTime | null
  
  # Policy Validation
  validation_schema: JSONSchema
  validator: String         # Validator implementation
  
  # Policy Relationships
  parent_policy_id: UUID | null
  child_policies: List[UUID]
  related_policies: List[UUID]
```

### 3.10 Execution Object

```yaml
Execution:
  inherits: UniversalBase
  type: "execution"
  
  # Execution Definition
  task_id: UUID
  provider_id: UUID
  capability_id: UUID
  
  # Execution State Machine
  state: Enum
    # CREATED, QUEUED, SCHEDULED, PREPARING
    # STARTING, RUNNING, WAITING, VERIFYING
    # COMPLETING, COMPLETED, FAILED, CANCELLED
    # RETRYING, RECOVERING
  
  # Execution Timeline
  created_at: DateTime
  started_at: DateTime | null
  completed_at: DateTime | null
  duration: Duration | null
  
  # Execution Input
  input: Object
  input_schema_version: String
  
  # Execution Output
  output: Object | null
  output_schema_version: String
  errors: List[Error]
  
  # Execution Resources
  cpu_seconds: Decimal
  memory_mb_seconds: Decimal
  gpu_seconds: Decimal | null
  
  # Execution Cost
  compute_cost: Decimal
  api_cost: Decimal
  total_cost: Decimal
  currency: String
  
  # Execution Quality
  quality_score: Decimal     # 0.0 - 1.0
  verification_score: Decimal
  
  # Execution Checkpoints
  checkpoints: List[Checkpoint]
  can_resume: Boolean
  
  # Execution Workspace
  workspace_id: UUID
  sandbox_id: UUID | null
  
  # Execution Logs
  logs: List[LogEntry]
  trace_id: String          # For distributed tracing
  
  # Execution Retry
  retry_count: Integer
  max_retries: Integer
  last_retry_at: DateTime | null
  retry_reason: String | null
```

---

## 4. Supporting Objects

### 4.1 Resource Object

```yaml
Resource:
  inherits: UniversalBase
  type: "resource"
  
  # Resource Definition
  name: String
  resource_type: Enum       # COMPUTE, STORAGE, NETWORK, MEMORY, GPU
  
  # Resource Configuration
  config: Object
  capacity: Object
  utilization: Object
  
  # Resource Limits
  limits: ResourceLimits
  quotas: ResourceQuotas
  
  # Resource State
  state: Enum               # AVAILABLE, ALLOCATED, RESERVED, MAINTENANCE
  health: Enum
  
  # Resource Usage
  current_usage: Object
  peak_usage: Object
  usage_history: List[UsageRecord]
```

### 4.2 User Object

```yaml
User:
  inherits: UniversalBase
  type: "user"
  
  # User Definition
  email: String
  name: String
  avatar_url: String | null
  
  # User Roles
  roles: List[Role]
  permissions: List[Permission]
  
  # User Organizations
  organizations: List[OrganizationMembership]
  default_organization_id: UUID
  
  # User Preferences
  preferences: Map[String, Any]
  notification_settings: NotificationSettings
  
  # User Activity
  last_login_at: DateTime
  login_count: Integer
```

### 4.3 Organization Object

```yaml
Organization:
  inherits: UniversalBase
  type: "organization"
  
  # Organization Definition
  name: String
  display_name: String
  description: String
  logo_url: String | null
  
  # Organization Settings
  settings: OrganizationSettings
  policies: List[UUID]
  budget: Budget
  
  # Organization Members
  members: List[OrganizationMembership]
  teams: List[Team]
  
  # Organization Resources
  workspaces: List[UUID]
  projects: List[UUID]
  
  # Organization Billing
  billing_plan: Enum        # FREE, STARTER, PROFESSIONAL, ENTERPRISE
  billing_info: BillingInfo
```

### 4.4 Workspace Object

```yaml
Workspace:
  inherits: UniversalBase
  type: "workspace"
  
  # Workspace Definition
  name: String
  display_name: String
  description: String
  organization_id: UUID
  
  # Workspace Configuration
  settings: WorkspaceSettings
  environment: Map[String, String]
  
  # Workspace Resources
  resources: ResourceAllocation
  quotas: WorkspaceQuotas
  
  # Workspace Isolation
  isolated: Boolean         # Full isolation
  shared_with: List[UUID]   # Shared workspaces
  
  # Workspace State
  state: Enum               # ACTIVE, SUSPENDED, ARCHIVED
  auto_cleanup: Boolean      # Auto-cleanup after completion
  retention_days: Integer
```

---

## 5. Relationships

### 5.1 Object Relationships

```yaml
Relationships:
  PARENT_OF:
    description: "Parent contains children"
    examples:
      - Goal → Mission
      - Mission → Task
      - Task → Subtask
      
  IMPLEMENTS:
    description: "Implements a contract"
    examples:
      - Provider → Capability
      - Provider → Contract
      
  USES:
    description: "Uses for execution"
    examples:
      - Task → Capability
      - Task → Provider
      
  DEPENDS_ON:
    description: "Depends on"
    examples:
      - Task → Task
      - Capability → Capability
      
  PRODUCES:
    description: "Produces output"
    examples:
      - Execution → Artifact
      - Task → Knowledge
      
  CONTAINS:
    description: "Contains within"
    examples:
      - Mission → Decision
      - Mission → Artifact
      
  RELATES_TO:
    description: "General relationship"
    examples:
      - Knowledge → Knowledge
      - Artifact → Artifact
```

### 5.2 Relationship Schema

```yaml
Relationship:
  from_object_id: UUID
  from_object_type: String
  to_object_id: UUID
  to_object_type: String
  relationship_type: Enum
  properties: Map[String, Any]
  created_at: DateTime
  created_by: UUID
  valid_from: DateTime
  valid_until: DateTime | null
```

---

## 6. Enumerations

```yaml
Enumerations:
  Status:
    - ACTIVE
    - INACTIVE
    - PENDING
    - FAILED
    
  Health:
    - HEALTHY
    - DEGRADED
    - UNHEALTHY
    
  Priority:
    - CRITICAL (100)
    - HIGH (75)
    - MEDIUM (50)
    - LOW (25)
    
  GoalType:
    - BUILD
    - FIX
    - REFACTOR
    - REVIEW
    - ANALYZE
    - DEPLOY
    
  MissionType:
    - DISCOVERY
    - ARCHITECTURE
    - PLANNING
    - IMPLEMENTATION
    - TESTING
    - DEPLOYMENT
    - MONITORING
    
  MissionState:
    - DISCOVERY_EXPLORING
    - DISCOVERY_COMPLETED
    - ARCHITECTURE_DESIGNING
    - ARCHITECTURE_REVIEWING
    - ARCHITECTURE_APPROVED
    - PLANNING_PLANNING
    - PLANNING_APPROVED
    - EXECUTION_QUEUED
    - EXECUTION_RUNNING
    - EXECUTION_PAUSED
    - EXECUTION_COMPLETED
    - EXECUTION_FAILED
    - VERIFICATION_TESTING
    - VERIFICATION_PASSED
    - VERIFICATION_FAILED
    - DEPLOYMENT_DEPLOYING
    - DEPLOYMENT_DEPLOYED
    - DEPLOYMENT_ROLLED_BACK
    - MONITORING_ACTIVE
    - MONITORING_STABLE
    - MONITORING_UNSTABLE
    
  TaskState:
    - CREATED
    - QUEUED
    - SCHEDULED
    - PREPARING
    - RUNNING
    - WAITING
    - VERIFYING
    - COMPLETED
    - FAILED
    - CANCELLED
    - RETRYING
    
  ProviderType:
    - AI_AGENT
    - LLM
    - MCP
    - REST_API
    - CLI
    - DOCKER
    - BROWSER
    - DATABASE
    - CICD
    - SEARCH
    - STORAGE
    
  CapabilityCategory:
    - CODING
    - EDITING
    - REVIEW
    - ANALYSIS
    - DATABASE
    - DEVOPS
    - BROWSER
    - TESTING
    
  DecisionType:
    - STRATEGIC
    - TACTICAL
    - OPERATIONAL
    
  PolicyType:
    - SECURITY
    - BUDGET
    - RETRY
    - TIMEOUT
    - GOVERNANCE
    - APPROVAL
    - COMPLIANCE
```

---

## 7. Object Factory

### 7.1 Creating Objects

```python
class ObjectFactory:
    """
    Factory for creating AGOS objects.
    """
    
    def create_goal(self, spec: GoalSpec) -> Goal:
        """Create a Goal object."""
        goal = Goal(
            id=self.generate_id(),
            rid=f"goal:{spec.tenant_id}:{goal.id}:v1",
            version="1.0.0",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            status="ACTIVE",
            health="HEALTHY",
            # ... rest of spec
        )
        goal.validate()
        return goal
        
    def create_mission(self, spec: MissionSpec) -> Mission:
        """Create a Mission object."""
        pass
        
    def create_capability(self, spec: CapabilitySpec) -> Capability:
        """Create a Capability object."""
        pass
        
    def create_provider(self, spec: ProviderSpec) -> Provider:
        """Create a Provider object."""
        pass
        
    def create_task(self, spec: TaskSpec) -> Task:
        """Create a Task object."""
        pass
        
    def create_artifact(self, spec: ArtifactSpec) -> Artifact:
        """Create an Artifact object."""
        pass
        
    def create_knowledge(self, spec: KnowledgeSpec) -> Knowledge:
        """Create a Knowledge object."""
        pass
        
    def create_decision(self, spec: DecisionSpec) -> Decision:
        """Create a Decision object."""
        pass
        
    def create_policy(self, spec: PolicySpec) -> Policy:
        """Create a Policy object."""
        pass
        
    def create_execution(self, spec: ExecutionSpec) -> Execution:
        """Create an Execution object."""
        pass
```

### 7.2 Object Validation

```python
class ObjectValidator:
    """
    Validates AGOS objects.
    """
    
    def validate(self, obj: UniversalBase) -> ValidationResult:
        """
        Validate an object against its schema.
        """
        schema = self.get_schema(type(obj))
        return schema.validate(obj.to_dict())
        
    def validate_relationships(self, obj: UniversalBase) -> ValidationResult:
        """
        Validate object relationships.
        """
        # Check all related objects exist
        # Check for circular dependencies
        # Check for orphaned relationships
        pass
        
    def validate_state_transition(
        self, 
        obj: UniversalBase, 
        new_state: Enum
    ) -> ValidationResult:
        """
        Validate state transition is allowed.
        """
        # Check state machine rules
        pass
```

---

## 8. Object Persistence

### 8.1 Storage Schema

```yaml
StorageSchema:
  goals:
    primary_key: "id"
    indexes:
      - "rid"
      - "owner_id"
      - "tenant_id"
      - "status"
      - "created_at"
    partition_key: "tenant_id"
    
  missions:
    primary_key: "id"
    indexes:
      - "rid"
      - "goal_id"
      - "tenant_id"
      - "status"
    partition_key: "tenant_id"
    
  capabilities:
    primary_key: "id"
    indexes:
      - "rid"
      - "category"
      - "name"
    partition_key: "global"  # Shared across tenants
    
  providers:
    primary_key: "id"
    indexes:
      - "rid"
      - "name"
      - "type"
      - "certified"
    partition_key: "global"
    
  tasks:
    primary_key: "id"
    indexes:
      - "rid"
      - "mission_id"
      - "status"
      - "capability_id"
    partition_key: "tenant_id"
    
  artifacts:
    primary_key: "id"
    indexes:
      - "rid"
      - "task_id"
      - "checksum"
    partition_key: "tenant_id"
    
  knowledge:
    primary_key: "id"
    indexes:
      - "rid"
      - "type"
      - "confidence"
    partition_key: "global"
    
  decisions:
    primary_key: "id"
    indexes:
      - "rid"
      - "mission_id"
      - "type"
    partition_key: "tenant_id"
    
  policies:
    primary_key: "id"
    indexes:
      - "rid"
      - "type"
      - "scope"
    partition_key: "scope_id"
    
  executions:
    primary_key: "id"
    indexes:
      - "task_id"
      - "provider_id"
      - "state"
      - "created_at"
    partition_key: "tenant_id"
```

---

## 9. Complete Object Hierarchy

```
UniversalBase (All objects inherit from this)
    │
    ├── Goal
    │   └── (has many) Mission
    │
    ├── Mission
    │   └── (has many) Task
    │   └── (has many) Decision
    │   └── (has many) Artifact
    │
    ├── Capability
    │   └── (implemented by many) Provider
    │   └── (used by many) Task
    │
    ├── Provider
    │   └── (implements) Capability
    │   └── (executes) Task
    │
    ├── Task
    │   └── (has) Execution
    │   └── (produces) Artifact
    │   └── (depends on) Task
    │
    ├── Artifact
    │   └── (versioned) Artifact
    │
    ├── Knowledge
    │   └── (relates to) Knowledge
    │
    ├── Decision
    │   └── (has) DecisionGraph
    │
    ├── Policy
    │   └── (inherits from) Policy
    │
    ├── Execution
    │   └── (has) Checkpoint
    │
    ├── Resource
    │
    ├── User
    │
    ├── Organization
    │   └── (has many) User
    │   └── (has many) Workspace
    │
    └── Workspace
        └── (isolates) Mission
```

---

## 10. Implementation Example

### 10.1 TypeScript Interfaces

```typescript
// Universal Base
interface UniversalBase {
  id: string;
  rid: string;
  version: string;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
  owner_id: string;
  tenant_id: string;
  workspace_id: string | null;
  status: 'ACTIVE' | 'INACTIVE' | 'PENDING' | 'FAILED';
  health: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
  tags: string[];
  labels: Record<string, string>;
  annotations: Record<string, unknown>;
  created_by: string;
  updated_by: string;
  change_history: Change[];
  version_history: Version[];
}

// Goal
interface Goal extends UniversalBase {
  type: 'goal';
  name: string;
  description: string;
  goal_type: 'BUILD' | 'FIX' | 'REFACTOR' | 'REVIEW' | 'ANALYZE' | 'DEPLOY';
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  statement: string;
  requirements: Requirement[];
  constraints: Constraint[];
  success_criteria: Criterion[];
  state: 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED' | 'ARCHIVED';
  approval_status: 'PENDING' | 'APPROVED' | 'REJECTED';
  approved_by: string | null;
  approved_at: string | null;
  parent_goal_id: string | null;
  child_missions: string[];
  artifacts: string[];
  estimated_cost: number;
  estimated_duration: string;
  actual_cost: number | null;
  actual_duration: string | null;
  domain: string;
  industry: string;
  scale: 'STARTUP' | 'SMB' | 'ENTERPRISE';
}

// Mission
interface Mission extends UniversalBase {
  type: 'mission';
  name: string;
  description: string;
  goal_id: string;
  mission_type: 'DISCOVERY' | 'ARCHITECTURE' | 'IMPLEMENTATION' | 'TESTING' | 'DEPLOYMENT' | 'MONITORING';
  state: string; // See MissionState enum
  context: Context;
  tasks: string[];
  decisions: string[];
  progress: number;
  completion_percentage: number;
  budget: Budget;
  time_allocation: string;
  assigned_capabilities: string[];
  assigned_providers: string[];
  quality_score: number;
  test_coverage: number;
  security_score: number;
  artifacts: string[];
  knowledge_extracted: string[];
  lessons_learned: Lesson[];
}

// ... Continue for all objects
```

### 10.2 Python Classes

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4

class UniversalBase(BaseModel):
    """Base class for all AGOS objects."""
    
    id: UUID = Field(default_factory=uuid4)
    rid: str
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    owner_id: UUID
    tenant_id: UUID
    workspace_id: Optional[UUID] = None
    status: str = "ACTIVE"
    health: str = "HEALTHY"
    tags: List[str] = []
    labels: Dict[str, str] = {}
    annotations: Dict[str, Any] = {}
    created_by: UUID
    updated_by: UUID
    change_history: List[Dict] = []
    version_history: List[Dict] = []

class Goal(UniversalBase):
    """Goal object."""
    
    type: str = "goal"
    name: str
    description: str
    goal_type: str
    priority: str
    statement: str
    requirements: List[Dict] = []
    constraints: List[Dict] = []
    success_criteria: List[Dict] = []
    state: str = "DRAFT"
    approval_status: str = "PENDING"
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    parent_goal_id: Optional[UUID] = None
    child_missions: List[UUID] = []
    artifacts: List[UUID] = []
    estimated_cost: float = 0.0
    estimated_duration: str = "0s"
    actual_cost: Optional[float] = None
    actual_duration: Optional[str] = None
    domain: str = ""
    industry: str = ""
    scale: str = "STARTUP"
    
    class Config:
        json_schema_extra = {
            "example": {
                "rid": "goal:tenant1:12345678:v1",
                "goal_type": "BUILD",
                "priority": "HIGH"
            }
        }

class Mission(UniversalBase):
    """Mission object."""
    
    type: str = "mission"
    name: str
    description: str
    goal_id: UUID
    mission_type: str
    state: str = "EXECUTION_QUEUED"
    context: Dict = {}
    tasks: List[UUID] = []
    decisions: List[UUID] = []
    progress: float = 0.0
    completion_percentage: int = 0
    budget: Dict = {}
    time_allocation: str = "0s"
    assigned_capabilities: List[UUID] = []
    assigned_providers: List[UUID] = []
    quality_score: float = 0.0
    test_coverage: float = 0.0
    security_score: float = 0.0
    artifacts: List[UUID] = []
    knowledge_extracted: List[UUID] = []
    lessons_learned: List[Dict] = []

# ... Continue for all objects
```

---

## 11. Validation Rules

### 11.1 Universal Validation

```python
class UniversalValidation:
    """Validation rules for all objects."""
    
    rules = {
        "id": {
            "type": "uuid",
            "required": True
        },
        "rid": {
            "type": "string",
            "pattern": r"^[a-z]+:[a-z0-9]+:[a-z0-9-]+:v\d+$",
            "required": True
        },
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+\.\d+$",
            "required": True
        },
        "created_at": {
            "type": "datetime",
            "required": True,
            "max_future": "1 hour"
        },
        "updated_at": {
            "type": "datetime",
            "required": True,
            "min_value": "created_at"
        },
        "status": {
            "type": "enum",
            "values": ["ACTIVE", "INACTIVE", "PENDING", "FAILED"],
            "required": True
        },
        "health": {
            "type": "enum",
            "values": ["HEALTHY", "DEGRADED", "UNHEALTHY"],
            "required": True
        }
    }
```

### 11.2 Object-Specific Validation

```python
class GoalValidation:
    """Validation rules for Goal objects."""
    
    rules = {
        **UniversalValidation.rules,
        "name": {
            "type": "string",
            "min_length": 3,
            "max_length": 200,
            "required": True
        },
        "goal_type": {
            "type": "enum",
            "values": ["BUILD", "FIX", "REFACTOR", "REVIEW", "ANALYZE", "DEPLOY"],
            "required": True
        },
        "priority": {
            "type": "enum",
            "values": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            "required": True
        },
        "success_criteria": {
            "type": "array",
            "min_items": 1,
            "required": True
        },
        "estimated_cost": {
            "type": "number",
            "min": 0,
            "required": True
        }
    }
```

---

## 12. Indexes and Queries

### 12.1 Common Queries

```python
class CommonQueries:
    """Common queries for AGOS objects."""
    
    # Goal queries
    get_goal_by_id: "SELECT * FROM goals WHERE id = ?"
    get_goals_by_owner: "SELECT * FROM goals WHERE owner_id = ?"
    get_goals_by_status: "SELECT * FROM goals WHERE status = ?"
    get_child_missions: "SELECT * FROM missions WHERE goal_id = ?"
    
    # Mission queries
    get_mission_by_id: "SELECT * FROM missions WHERE id = ?"
    get_missions_by_state: "SELECT * FROM missions WHERE state = ?"
    get_mission_tasks: "SELECT * FROM tasks WHERE mission_id = ?"
    get_mission_decisions: "SELECT * FROM decisions WHERE mission_id = ?"
    
    # Capability queries
    get_capability_by_id: "SELECT * FROM capabilities WHERE id = ?"
    get_capabilities_by_category: "SELECT * FROM capabilities WHERE category = ?"
    get_providers_for_capability: "SELECT * FROM providers WHERE capabilities CONTAINS ?"
    
    # Provider queries
    get_provider_by_id: "SELECT * FROM providers WHERE id = ?"
    get_certified_providers: "SELECT * FROM providers WHERE certified = true"
    get_providers_by_type: "SELECT * FROM providers WHERE type = ?"
    
    # Task queries
    get_task_by_id: "SELECT * FROM tasks WHERE id = ?"
    get_tasks_by_state: "SELECT * FROM tasks WHERE state = ?"
    get_ready_tasks: "SELECT * FROM tasks WHERE state = 'CREATED' AND depends_on all completed"
    
    # Execution queries
    get_execution_by_id: "SELECT * FROM executions WHERE id = ?"
    get_executions_by_task: "SELECT * FROM executions WHERE task_id = ?"
    get_recent_executions: "SELECT * FROM executions ORDER BY created_at DESC LIMIT 100"
```

---

## 13. Version History

```yaml
VersionHistory:
  v1.0.0:
    date: "2024-01-15"
    author: "AGOS Team"
    changes:
      - "Initial specification"
      - "10 core objects defined"
      - "UniversalBase introduced"
      - "Relationships defined"
      - "Validation rules specified"
```

---

## 14. References

- AGOS-002: Contracts Specification
- AGOS-003: Graph Model
- AGOS-004: Lifecycle Specification
- JSON Schema: https://json-schema.org/
- Pydantic: https://pydantic-docs.helpmanual.io/
