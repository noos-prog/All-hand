# Kernel Contracts Overview

> **The contracts that cannot be broken.**

---

## Concept

```
ADR-034: Everything is Replaceable

Even Core Brain itself must be replaceable with a newer version
while preserving contracts.

Any new version must respect these contracts.
```

---

## Contract Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                  Kernel Contracts (CANNOT BE BROKEN)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Goal Contract                                        │ │
│  │  - What can be a goal                               │ │
│  │  - Goal structure                                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Mission Contract                                    │ │
│  │  - Mission lifecycle                                 │ │
│  │  - Mission states                                   │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Capability Contract                                │ │
│  │  - Capability interface                             │ │
│  │  - Capability metadata                              │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Provider Contract                                 │ │
│  │  - Provider interface                             │ │
│  │  - Provider capabilities                          │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Execution Contract                                 │ │
│  │  - Execution lifecycle                             │ │
│  │  - Execution states                                │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Artifact Contract                                 │ │
│  │  - Artifact structure                              │ │
│  │  - Artifact metadata                               │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Knowledge Contract                                │ │
│  │  - Knowledge structure                            │ │
│  │  - Knowledge validation                            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Policy Contract                                   │ │
│  │  - Policy structure                                │ │
│  │  - Policy enforcement                              │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Resource Contract                                 │ │
│  │  - Resource identification                         │ │
│  │  - Resource lifecycle                              │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Contract Definition

```yaml
Contract:
  id: string
  name: string
  version: string
  
  # What this contract defines
  definitions:
    - name: string
      type: string
      required: boolean
      description: string
      
  # What this contract requires
  requirements:
    - name: string
      description: string
      
  # What this contract guarantees
  guarantees:
    - name: string
      description: string
      
  # Version compatibility
  compatibility:
    previous_version: string
    breaking_changes: list[string]
```

---

## Goal Contract

```yaml
GoalContract:
  contract_id: "contract:goal:v1"
  version: "1.0"
  
  definitions:
    - name: "goal_id"
      type: "string"
      required: true
      description: "Unique goal identifier"
      
    - name: "goal_type"
      type: "enum"
      required: true
      values: ["BUILD", "FIX", "REFACTOR", "REVIEW", "ANALYZE", "DEPLOY"]
      description: "Type of goal"
      
    - name: "mission"
      type: "string"
      required: true
      description: "Goal mission statement"
      
    - name: "constraints"
      type: "object"
      required: false
      description: "Goal constraints"
      
    - name: "success_criteria"
      type: "array"
      required: true
      description: "Success criteria"
      
  requirements:
    - "Must have unique identifier"
    - "Must have mission statement"
    - "Must have at least one success criterion"
    
  guarantees:
    - "Goal will be transformed into Mission"
    - "Goal will have execution tracking"
    - "Goal outcomes will be recorded"
```

---

## Execution Contract

```yaml
ExecutionContract:
  contract_id: "contract:execution:v1"
  version: "1.0"
  
  definitions:
    - name: "execution_id"
      type: "string"
      required: true
      description: "Unique execution identifier"
      
    - name: "state"
      type: "enum"
      required: true
      values: ["CREATED", "QUEUED", "SCHEDULED", "PREPARING", "RUNNING", 
               "WAITING", "VERIFYING", "COMPLETED", "FAILED", "CANCELLED"]
      description: "Current execution state"
      
    - name: "capability_id"
      type: "string"
      required: true
      description: "Capability being executed"
      
    - name: "provider_id"
      type: "string"
      required: true
      description: "Provider executing capability"
      
    - name: "inputs"
      type: "object"
      required: true
      description: "Execution inputs"
      
    - name: "outputs"
      type: "object"
      required: false
      description: "Execution outputs"
      
    - name: "metrics"
      type: "object"
      required: true
      description: "Execution metrics"
      
  requirements:
    - "Must have unique identifier"
    - "Must transition through valid states only"
    - "Must record all state transitions"
    - "Must produce metrics"
    
  guarantees:
    - "State transitions are atomic"
    - "Metrics are recorded"
    - "Outputs are persisted"
```

---

## Provider Contract

```yaml
ProviderContract:
  contract_id: "contract:provider:v1"
  version: "1.0"
  
  definitions:
    - name: "provider_id"
      type: "string"
      required: true
      description: "Unique provider identifier"
      
    - name: "name"
      type: "string"
      required: true
      description: "Provider name"
      
    - name: "type"
      type: "enum"
      required: true
      values: ["AI_AGENT", "LLM", "MCP", "REST_API", "CLI", "DOCKER", 
               "BROWSER", "DATABASE", "CICD", "SEARCH", "STORAGE"]
      description: "Provider type"
      
    - name: "capabilities"
      type: "array"
      required: true
      description: "Capabilities this provider offers"
      
    - name: "health"
      type: "enum"
      required: true
      values: ["HEALTHY", "DEGRADED", "UNHEALTHY", "UNKNOWN"]
      description: "Current health status"
      
    - name: "manifest"
      type: "object"
      required: true
      description: "Provider manifest"
      
  requirements:
    - "Must implement Universal Provider Interface"
    - "Must declare all capabilities"
    - "Must report health status"
    - "Must provide manifest"
    
  guarantees:
    - "Will be discoverable"
    - "Can be selected by Capability Engine"
    - "Will be monitored"
```

---

## Contract Validation

```python
class ContractValidator:
    """
    Validates implementations against contracts.
    """
    
    async def validate_implementation(
        self,
        implementation: Any,
        contract: Contract
    ) -> ValidationResult:
        """
        Validate that implementation follows contract.
        """
        
        errors = []
        warnings = []
        
        # Check all required fields
        for field in contract.definitions:
            if field.required:
                if not hasattr(implementation, field.name):
                    errors.append(f"Missing required field: {field.name}")
                    
        # Check types
        for field in contract.definitions:
            if hasattr(implementation, field.name):
                value = getattr(implementation, field.name)
                if not self.validate_type(value, field.type):
                    errors.append(
                        f"Invalid type for {field.name}: expected {field.type}"
                    )
                    
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
```

---

## Version Compatibility

```yaml
VersionCompatibility:
  # How versions evolve
  
  SEMVER:
    MAJOR: "Breaking changes (contract modified)"
    MINOR: "New optional features"
    PATCH: "Bug fixes, documentation"
    
  Contract_Versioning:
    v1.0: "Initial contract"
    v1.1: "Added optional fields"
    v2.0: "Breaking changes - requires migration"
    
  Migration:
    - "Old versions continue to work"
    - "New versions must support old contracts"
    - "Breaking changes require version bump"
```

---

## Breaking Changes

```yaml
BreakingChanges:
  # These require MAJOR version bump
  
  - Removing a required field
  - Changing a field type
  - Removing a state from enum
  - Changing a required behavior
  - Removing a guarantee
  
NonBreakingChanges:
  # These do NOT require version bump
  
  - Adding optional fields
  - Adding new states to enum
  - Adding new optional behaviors
  - Improving documentation
  - Performance improvements
```

---

## Related Documents

- [Goal-Contract.md](./02-Goal-Contract.md)
- [Execution-Contract.md](./03-Execution-Contract.md)
- [Provider-Contract.md](./04-Provider-Contract.md)
