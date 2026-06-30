# Capability Library

> **10,000+ Capabilities. Each independent. Each benchmarked.**

---

## Vision

```
Traditional Approach:
- 1000 projects
- Agents that do everything

ARI Approach:
- 10,000+ capabilities
- Providers that specialize
- Best provider for each capability
```

---

## Capability Definition

```yaml
Capability:
  id: string                    # cap_generate_api
  name: string                # Generate REST API
  category: string           # Backend
  subcategory: string        # API
  
  description: string        # What this capability does
  
  # Scope
  scope:
    min_complexity: enum      # TRIVIAL, SIMPLE, MODERATE, COMPLEX, EPIC
    max_complexity: enum
    domain: list[string]       # WEB, MOBILE, BACKEND, etc.
    
  # Inputs
  inputs:
    required: list[string]
    optional: list[string]
    
  # Outputs
  outputs:
    artifacts: list[string]
    format: enum
    
  # Quality dimensions
  quality:
    correctness: boolean
    completeness: boolean
    performance: boolean
    security: boolean
    maintainability: boolean
    
  # Benchmark info
  benchmark:
    golden_tasks: integer     # Number of golden tasks
    evaluation_criteria: list[string]
    judge_types: list[string]
    
  # Statistics
  stats:
    total_benchmarks: integer
    provider_count: integer
    avg_success_rate: decimal
    avg_duration: duration
```

---

## Capability Categories (Top Level)

### Coding Capabilities

```yaml
Coding:
  - generate_api
  - generate_crud
  - generate_graphql
  - generate_grpc
  - generate_function
  - generate_class
  - generate_module
  - generate_library
  - generate_sdk
  - generate_cli
  - generate_gui
  - generate_mobile
  - generate_frontend
  - generate_backend
  - generate_fullstack
  - generate_tests
  - generate_migrations
  - generate_schemas
  - generate_dockerfile
  - generate_kubernetes
  - generate_ci_cd
  - generate_terraform
```

### Editing Capabilities

```yaml
Editing:
  - edit_code
  - refactor_code
  - optimize_code
  - fix_bug
  - fix_security
  - fix_performance
  - fix_style
  - add_tests
  - add_docs
  - add_logging
  - add_monitoring
  - add_error_handling
  - add_authentication
  - add_validation
  - add_caching
  - add_optimization
```

### Review Capabilities

```yaml
Review:
  - review_code
  - review_security
  - review_performance
  - review_architecture
  - review_test_coverage
  - review_documentation
  - review_api_design
  - review_database_design
  - review_frontend
  - review_backend
  - review_deployment
```

### Analysis Capabilities

```yaml
Analysis:
  - analyze_codebase
  - analyze_architecture
  - analyze_dependencies
  - analyze_complexity
  - analyze_security
  - analyze_performance
  - analyze_logs
  - analyze_metrics
  - analyze_traces
  - analyze_errors
  - analyze_costs
  - analyze_tech_debt
```

### Database Capabilities

```yaml
Database:
  - design_schema
  - create_migration
  - optimize_query
  - create_index
  - add_constraint
  - migrate_database
  - backup_database
  - restore_database
  - setup_replication
  - configure_connection_pool
```

### DevOps Capabilities

```yaml
DevOps:
  - deploy_container
  - deploy_serverless
  - deploy_kubernetes
  - deploy_aws
  - deploy_gcp
  - deploy_azure
  - setup_monitoring
  - setup_logging
  - setup_alerting
  - setup_ci_cd
  - setup_infrastructure
  - setup_security
```

### Browser Capabilities

```yaml
Browser:
  - browse_website
  - fill_form
  - click_element
  - take_screenshot
  - extract_data
  - automate_workflow
  - test_ui
  - scrape_website
  - monitor_website
```

### Testing Capabilities

```yaml
Testing:
  - write_unit_tests
  - write_integration_tests
  - write_e2e_tests
  - write_performance_tests
  - write_security_tests
  - run_tests
  - debug_tests
  - fix_tests
  - analyze_coverage
  - generate_test_data
```

---

## Example: generate_api Capability

```yaml
capability:
  id: "cap_generate_api"
  name: "Generate REST API"
  category: "Coding"
  subcategory: "Backend"
  
  description: |
    Generate a complete REST API with:
    - Endpoints (CRUD)
    - Models/Schemas
    - Validation
    - Error handling
    - Authentication (optional)
    - Documentation (optional)
    
  scope:
    min_complexity: "SIMPLE"
    max_complexity: "EPIC"
    domain: ["WEB", "MOBILE", "BACKEND"]
    
  inputs:
    required:
      - "language"          # python, javascript, go, etc.
      - "framework"         # express, fastapi, gin, etc.
      - "database"          # postgresql, mongodb, etc.
    optional:
      - "authentication"    # jwt, oauth, etc.
      - "api_style"         # rest, graphql
      - "include_tests"
      - "include_docs"
      
  outputs:
    artifacts:
      - "source_code"
      - "models"
      - "routes"
      - "tests" (optional)
      - "docs" (optional)
    format: "zip"
    
  quality:
    correctness: true
    completeness: true
    performance: true
    security: true
    maintainability: true
    
  benchmark:
    golden_tasks: 100
    evaluation_criteria:
      - "syntax_correctness"
      - "api_completeness"
      - "security"
      - "test_coverage"
      - "documentation"
    judge_types:
      - "static_analysis"
      - "test_execution"
      - "security_scan"
      - "human_review"
      
  stats:
    total_benchmarks: 5000
    provider_count: 15
    avg_success_rate: 0.85
    avg_duration: "5 minutes"
```

---

## Capability Lifecycle

```
DISCOVERED
    │
    ▼
VALIDATED
    │
    ▼
BENCHMARKED
    │
    ▼
CLASSIFIED
    │
    ▼
TRACKED
    │
    ▼
IMPROVED
    │
    ▼
EVOLVED
```

---

## Capability Discovery

```yaml
DiscoverySources:
  # How capabilities are discovered
  
  1. REPOSITORY_ANALYSIS
     - Analyze 100,000 repos
     - Extract common patterns
     - Cluster into capabilities
     
  2. PROVIDER_MAPPING
     - Map provider capabilities
     - Extract common interfaces
     - Standardize names
     
  3. TASK_CATEGORIZATION
     - Analyze 100,000 tasks
     - Group by similarity
     - Define capability boundaries
     
  4. USER_REQUESTS
     - Track user requests
     - Identify common needs
     - Create new capabilities
```

---

## Capability Validation

```yaml
Validation:
  # Before a capability is added
  
  1. UNIQUENESS
     - Is this different from existing capabilities?
     - No overlap?
     
  2. BENCHMARKABILITY
     - Can we benchmark this?
     - Can we define golden tasks?
     
  3. PROVIDABILITY
     - At least one provider can do this?
     - At least one provider passes threshold?
     
  4. DOCUMENTATION
     - Clear description?
     - Clear inputs/outputs?
     - Clear evaluation criteria?
```

---

## Capability Genome

Each capability has a genome:

```yaml
CapabilityGenome:
  capability_id: "cap_generate_api"
  
  dimensions:
    reasoning: 0.0-1.0      # How much reasoning needed
    coding: 0.0-1.0        # How much coding
    testing: 0.0-1.0       # How much testing
    security: 0.0-1.0      # Security awareness needed
    performance: 0.0-1.0    # Performance awareness
    architecture: 0.0-1.0  # Architecture knowledge
    memory: 0.0-1.0         # Memory/context needed
    planning: 0.0-1.0       # Planning complexity
    iteration: 0.0-1.0      # Iterative work
    creativity: 0.0-1.0       # Creative solution
    
  # Example: generate_api
  example_values:
    reasoning: 0.75
    coding: 0.95
    testing: 0.60
    security: 0.80
    performance: 0.50
    architecture: 0.85
    memory: 0.70
    planning: 0.80
    iteration: 0.40
    creativity: 0.30
```

---

## Capability Matching

```python
def match_provider_to_capability(
    capability: Capability,
    providers: list[Provider]
) -> list[Match]:
    """
    Match providers to capability based on genome.
    """
    
    matches = []
    
    # Get capability genome
    cap_genome = capability.genome
    
    for provider in providers:
        # Get provider genome
        prov_genome = provider.genome
        
        # Calculate match score
        score = calculate_genome_similarity(
            cap_genome,
            prov_genome
        )
        
        matches.append({
            "provider": provider,
            "score": score,
            "strengths": get_strengths(cap_genome, prov_genome),
            "weaknesses": get_weaknesses(cap_genome, prov_genome)
        })
        
    # Sort by score
    matches.sort(key=lambda m: m["score"], reverse=True)
    
    return matches
```

---

## Related Documents

- [Golden-Tasks.md](../05-Golden-Tasks/README.md)
- [Benchmark-Schema.md](../02-Benchmark-Schema/README.md)
