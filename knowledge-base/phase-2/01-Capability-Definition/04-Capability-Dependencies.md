# Capability Dependency Graph

> **Every Capability knows what it depends on.**

---

## Dependency Overview

```
Deploy
   ↓
Build
   ↓
Tests
   ↓
Compile
   ↓
Code

Every Capability knows:
- What it depends on
- What depends on it
```

---

## Dependency Graph

```
                    ┌──────────────────┐
                    │   Read Code    │
                    └────────┬───────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌────────────┐    ┌────────────┐    ┌────────────┐
    │   Design   │    │   Write    │    │  Analyze   │
    │Architecture│    │   Code     │    │   Logs     │
    └─────┬──────┘    └─────┬──────┘    └────────────┘
          │                 │
          │    ┌────────────┴────────────┐
          │    │                         │
          ▼    ▼                         ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │   Plan     │    │   Edit     │    │   Test     │
   │   Tasks    │    │   Code     │    │   Code     │
   └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
         │                 │                 │
         │                 └────────┬────────┘
         │                          │
         ▼                          ▼
   ┌────────────────────────────────────────────┐
   │              Review Code                   │
   └─────────────────────┬──────────────────────┘
                         │
                         ▼
   ┌────────────────────────────────────────────┐
   │                 Deploy                     │
   └────────────────────────────────────────────┘
```

---

## Dependency Types

### 1. Sequential Dependency
```yaml
Dependency:
  type: "sequential"
  example: |
    Tests must complete before Deploy
  meaning: "B depends on A completing"
```

### 2. Parallel Capability
```yaml
Dependency:
  type: "parallel"
  example: |
    Build Frontend and Backend can run together
  meaning: "A and B can run simultaneously"
```

### 3. Optional Dependency
```yaml
Dependency:
  type: "optional"
  example: |
    Security Scan is optional for Deploy
  meaning: "A can proceed without B"
```

### 4. Conflict Dependency
```yaml
Dependency:
  type: "conflict"
  example: |
    Cannot run both Python 2 and Python 3 generators
  meaning: "A and B cannot run together"
```

---

## Detailed Dependency Map

### Deployment Flow

```
cap_deploy
    │
    ├─── depends_on: [cap_build, cap_health_check]
    │
cap_build
    │
    ├─── depends_on: [cap_run_tests]
    │
cap_health_check
    │
    ├─── depends_on: []
    │
cap_run_tests
    │
    ├─── depends_on: [cap_generate_tests, cap_compile]
    │
cap_generate_tests
    │
    ├─── depends_on: []
    │
cap_compile
    │
    ├─── depends_on: [cap_read_repository]
    │
cap_read_repository
    │
    ├─── depends_on: []
```

---

### Code Generation Flow

```
cap_generate_code
    │
    ├─── depends_on: []
    │
    ├─── enables: [cap_edit_code, cap_review_code, cap_test]
    │
cap_edit_code
    │
    ├─── depends_on: [cap_generate_code]
    │
    ├─── enables: [cap_review_code]
    │
cap_review_code
    │
    ├─── depends_on: [cap_generate_code, cap_edit_code]
    │
    ├─── enables: [cap_fix_bugs]
    │
cap_fix_bugs
    │
    ├─── depends_on: [cap_review_code]
    │
    ├─── enables: [cap_deploy]
```

---

### Full Dependency List

```yaml
Dependencies:
  # ===== DEPLOYMENT =====
  cap_deploy:
    depends_on:
      - cap_build
      - cap_health_check
      
  cap_build:
    depends_on:
      - cap_run_tests
      
  cap_health_check:
    depends_on: []
    
  cap_rollback:
    depends_on:
      - cap_health_check
      
  # ===== CODING =====
  cap_generate_code:
    depends_on: []
    enables:
      - cap_edit_code
      - cap_review_code
      - cap_test
      
  cap_edit_code:
    depends_on:
      - cap_generate_code
      
  cap_refactor_code:
    depends_on:
      - cap_read_repository
      
  cap_optimize_code:
    depends_on:
      - cap_profile_code
      
  # ===== TESTING =====
  cap_run_tests:
    depends_on:
      - cap_generate_tests
      - cap_compile
      
  cap_generate_tests:
    depends_on:
      - cap_read_repository
      
  cap_integration_tests:
    depends_on:
      - cap_deploy
      
  # ===== REVIEW =====
  cap_review_code:
    depends_on:
      - cap_generate_code
      - cap_edit_code
      
  cap_review_pr:
    depends_on:
      - cap_read_repository
      
  cap_review_architecture:
    depends_on:
      - cap_analyze_architecture
      
  # ===== DATABASE =====
  cap_migrate_db:
    depends_on:
      - cap_backup_db
      
  cap_optimize_db:
    depends_on:
      - cap_query_db
      
  # ===== INFRASTRUCTURE =====
  cap_create_infra:
    depends_on:
      - cap_design_architecture
      
  cap_deploy:
    depends_on:
      - cap_create_infra
```

---

## Dependency Validation

```python
def validate_dependencies(capability: Capability) -> ValidationResult:
    """
    Validate capability dependencies.
    """
    
    errors = []
    warnings = []
    
    # 1. Check for circular dependencies
    if has_circular_dependency(capability):
        errors.append("Circular dependency detected")
    
    # 2. Check all dependencies exist
    for dep_id in capability.depends_on:
        if not capability_exists(dep_id):
            errors.append(f"Dependency {dep_id} does not exist")
    
    # 3. Check for deep nesting (performance)
    depth = calculate_dependency_depth(capability)
    if depth > 10:
        warnings.append(f"Deep nesting detected: {depth} levels")
    
    # 4. Check for conflicts
    for conflict_id in capability.conflicts_with:
        if conflict_id in capability.depends_on:
            errors.append(f"Capability cannot depend on and conflict with {conflict_id}")
    
    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

---

## Capability Execution Order

```python
def get_execution_order(capabilities: list[Capability]) -> list[Capability]:
    """
    Determine execution order based on dependencies.
    Uses topological sort.
    """
    
    # Build dependency graph
    graph = build_graph(capabilities)
    
    # Topological sort
    order = topological_sort(graph)
    
    return order
```

---

## Example: Build Pipeline

```
Required Capabilities:
- cap_deploy

Execution Order:
1. cap_read_repository (no deps)
2. cap_generate_code (no deps)
3. cap_generate_tests (depends on 1)
4. cap_compile (depends on 1)
5. cap_run_tests (depends on 3, 4)
6. cap_build (depends on 5)
7. cap_health_check (no deps)
8. cap_deploy (depends on 6, 7)
```

---

## Dependency Metrics

```yaml
Metrics:
  # Per capability
  dependency_count: integer      # Number of dependencies
  dependent_count: integer      # Number of things depending on it
  critical_path_count: integer  # How many critical paths it's on
  
  # System-wide
  max_depth: integer           # Maximum dependency depth
  parallel_opportunities: integer  # Capabilities that can run together
  critical_path: list          # The longest path
  
  # Analysis
  shared_dependencies: list     # Capabilities with shared deps
  potential_bottlenecks: list  # High-dependency capabilities
```

---

## Related Documents

- [Capability-Object.md](./02-Capability-Object.md)
- [Capability-Categories.md](./03-Capability-Categories.md)
