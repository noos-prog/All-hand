# Capability Object

> **Every Capability transforms into this standardized Object.**

---

## Capability Object Schema

```yaml
Capability:
  # ========== Identification ==========
  id: string                    # Unique identifier
  version: string              # Semantic version
  name: string                 # Human-readable name
  slug: string                 # URL-safe identifier
  
  # ========== Classification ==========
  category: enum               # Main category
  subcategory: string          # Sub-category
  tags: list[string]          # Searchable tags
  
  # ========== Description ==========
  description: string          # What it does
  long_description: string     # Detailed description
  use_cases: list[string]     # When to use
  examples: list[Example]      # Usage examples
  
  # ========== Interface ==========
  inputs:
    schema: object             # JSON Schema for inputs
    required: list[string]     # Required input fields
    optional: list[string]     # Optional input fields
    validation: object         # Validation rules
    
  outputs:
    schema: object             # JSON Schema for outputs
    artifacts: list[Artifact]  # Expected artifacts
    artifacts_schema: object   # Schema for artifacts
    
  # ========== Constraints ==========
  constraints:
    timeout:
      min: duration           # Minimum execution time
      max: duration           # Maximum execution time
      default: duration       # Default timeout
      
    cost:
      min: decimal            # Minimum cost
      max: decimal           # Maximum cost
      default: decimal       # Default cost
      
    resources:
      memory_mb: integer
      cpu_cores: decimal
      gpu: boolean
      
  # ========== Requirements ==========
  requirements:
    permissions: list[string]  # Required permissions
    environment: list[string]  # Required environment
    dependencies: list[string]  # Required dependencies
    
  # ========== Security ==========
  security:
    level: enum               # public, internal, restricted
    data_classification: enum  # none, low, medium, high
    audit_required: boolean   # Requires audit logging
    
  # ========== Policies ==========
  policies:
    verification_required: boolean
    verification_types: list[enum]
    retry_policy: object
    fallback_policy: object
    
  # ========== Contracts ==========
  contracts:
    input_contract: Contract
    output_contract: Contract
    error_contract: Contract
    
  # ========== Metrics ==========
  metrics:
    success_rate: 0.0-1.0
    avg_duration: duration
    avg_cost: decimal
    total_executions: integer
    
  # ========== Dependencies ==========
  dependencies:
    depends_on: list[CapabilityID]  # Required capabilities
    enables: list[CapabilityID]    # Capabilities this enables
    conflicts_with: list[CapabilityID]  # Cannot run with
    
  # ========== Providers ==========
  providers:
    available: list[ProviderID]  # All providers
    recommended: list[ProviderID] # Recommended providers
    blocked: list[ProviderID]    # Blocked providers
    
  # ========== Lifecycle ==========
  status: enum                  # active, deprecated, experimental
  deprecated_at: datetime
  sunset_date: datetime
  replacement: CapabilityID     # If deprecated, what's the replacement
```

---

## Example: Generate Code Capability

```yaml
Capability:
  id: "cap_generate_code"
  version: "1.0.0"
  name: "Generate Code"
  slug: "generate-code"
  
  category: "coding"
  subcategory: "generation"
  tags: ["code", "generation", "ai", "llm"]
  
  description: "Generate code from natural language requirements"
  long_description: |
    This capability generates code based on natural language 
    requirements. It understands context, follows best practices,
    and produces production-ready code.
  use_cases:
    - "Generate new features"
    - "Create boilerplate code"
    - "Implement algorithms"
  examples:
    - "Generate a REST API endpoint"
    - "Create a user authentication module"
    - "Implement a sorting algorithm"
    
  inputs:
    schema:
      type: "object"
      properties:
        requirements:
          type: "string"
          description: "Natural language requirements"
        language:
          type: "string"
          enum: ["python", "javascript", "typescript", "go", "rust", "java"]
        framework:
          type: "string"
        context:
          type: "object"
      required: ["requirements", "language"]
      
  outputs:
    schema:
      type: "object"
      properties:
        code:
          type: "string"
        files:
          type: "array"
          items:
            type: "object"
            properties:
              path: "string"
              content: "string"
        tests:
          type: "array"
    artifacts:
      - type: "source_code"
        extensions: [".py", ".js", ".ts", ".go"]
      - type: "test_code"
        extensions: ["_test.py", ".test.js", ".spec.ts"]
        
  constraints:
    timeout:
      min: "30s"
      max: "10m"
      default: "5m"
    cost:
      min: 0.01
      max: 1.00
      default: 0.05
      
  security:
    level: "internal"
    data_classification: "low"
    audit_required: true
    
  policies:
    verification_required: true
    verification_types: ["syntax", "lint", "tests"]
    retry_policy:
      max_retries: 2
      backoff: "exponential"
    fallback_policy:
      action: "try_alternative_provider"
      
  dependencies:
    depends_on: []
    enables: ["cap_edit_code", "cap_review_code", "cap_test"]
    conflicts_with: []
    
  metrics:
    success_rate: 0.92
    avg_duration: "3m 30s"
    avg_cost: 0.04
    total_executions: 1500
```

---

## Example: Deploy Capability

```yaml
Capability:
  id: "cap_deploy"
  version: "1.0.0"
  name: "Deploy"
  slug: "deploy"
  
  category: "deployment"
  subcategory: "execution"
  tags: ["deploy", "ci", "cd", "infrastructure"]
  
  description: "Deploy application to target environment"
  
  inputs:
    schema:
      type: "object"
      properties:
        environment:
          type: "string"
          enum: ["development", "staging", "production"]
        artifacts:
          type: "array"
        config:
          type: "object"
      required: ["environment", "artifacts"]
      
  outputs:
    schema:
      type: "object"
      properties:
        deployment_id: "string"
        url: "string"
        status: "string"
        health_check: "object"
        
  constraints:
    timeout:
      min: "1m"
      max: "30m"
      default: "15m"
    cost:
      min: 0.10
      max: 5.00
      default: 0.50
      
  security:
    level: "restricted"
    data_classification: "high"
    audit_required: true
    
  policies:
    verification_required: true
    verification_types: ["security", "health_check", "rollback"]
    retry_policy:
      max_retries: 1
      backoff: "linear"
    fallback_policy:
      action: "rollback"
      
  dependencies:
    depends_on: ["cap_build", "cap_run_tests"]
    enables: []
```

---

## Input Schema Example

```yaml
inputs:
  schema:
    type: "object"
    properties:
      requirements:
        type: "string"
        description: "What to generate"
        min_length: 10
        max_length: 10000
        
      language:
        type: "string"
        description: "Programming language"
        enum: ["python", "javascript", "typescript"]
        
      framework:
        type: "string"
        description: "Framework to use (optional)"
        
      context:
        type: "object"
        description: "Additional context"
        properties:
          existing_files:
            type: "array"
          project_structure:
            type: "object"
          coding_standards:
            type: "string"
            
      output_format:
        type: "string"
        enum: ["files", "inline", "both"]
        default: "files"
        
    required: ["requirements", "language"]
    additional_properties: false
    
  validation:
    - field: "requirements"
      rule: "min_length_10"
      message: "Requirements must be at least 10 characters"
      
    - field: "language"
      rule: "enum"
      message: "Language must be one of the supported options"
```

---

## Output Schema Example

```yaml
outputs:
  schema:
    type: "object"
    properties:
      success:
        type: "boolean"
        
      code:
        type: "string"
        description: "Generated code (if inline)"
        
      files:
        type: "array"
        items:
          type: "object"
          properties:
            path:
              type: "string"
            content:
              type: "string"
            language:
              type: "string"
            lines:
              type: "integer"
            hash:
              type: "string"
              
      metadata:
        type: "object"
        properties:
          generation_time:
            type: "duration"
          token_usage:
            type: "integer"
          cost:
            type: "decimal"
            
      quality:
        type: "object"
        properties:
          syntax_valid: "boolean"
          lint_passed: "boolean"
          estimated_quality: "0.0-1.0"
          
  artifacts:
    - type: "source_code"
      required: true
      extensions: [".py", ".js", ".ts"]
    - type: "tests"
      required: false
      extensions: ["_test.py", ".test.js"]
```

---

## Related Documents

- [Capability-Overview.md](./01-Capability-Overview.md)
- [Capability-Categories.md](./03-Capability-Categories.md)
- [Capability-Contracts.md](../05-Capability-Contracts/01-Contracts-Overview.md)
