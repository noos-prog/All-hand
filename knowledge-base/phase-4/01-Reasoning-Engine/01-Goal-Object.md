# Universal Goal Object

> **Every request transforms into this comprehensive Goal Object.**

---

## Goal Object Schema

```yaml
Goal:
  # ========== Identification ==========
  id: string                    # Unique identifier (e.g., "goal_2024_001")
  version: string              # Schema version
  created_at: datetime
  updated_at: datetime
  
  # ========== Core Information ==========
  type: enum                  # BUILD, FIX, REFACTOR, REVIEW, ANALYZE, DEPLOY, etc.
  mission: string              # Natural language description
  expected_outcome: string    # What success looks like
  
  # ========== Classification ==========
  category: enum              # FEATURE, BUG, INFRA, SECURITY, RESEARCH, etc.
  priority: enum              # CRITICAL, HIGH, MEDIUM, LOW
  complexity: enum            # TRIVIAL, SIMPLE, MODERATE, COMPLEX, EPIC
  
  # ========== Success Criteria ==========
  success_criteria:
    - criterion: string
      type: enum              # functional, performance, security, etc.
      measurable: boolean
      target: string          # e.g., "99.9% uptime", "<100ms latency"
      
  # ========== Constraints ==========
  constraints:
    budget:
      type: "budget"
      value: string          # "$500/month"
      currency: string
      is_hard: boolean
        
    deadline:
      type: "deadline"
      value: datetime
      is_hard: boolean
        
    security:
      type: "security"
      level: enum            # NONE, LOW, MEDIUM, HIGH, CRITICAL
      requirements: list[string]
        
    language:
      type: "language"
      required: list[string]
      forbidden: list[string]
        
    framework:
      type: "framework"
      required: list[string]
      forbidden: list[string]
        
    license:
      type: "license"
      allowed: list[string]  # MIT, Apache, etc.
      forbidden: list[string]
        
    performance:
      type: "performance"
      targets: dict          # latency, throughput, etc.
        
    cloud:
      type: "cloud"
      provider: enum         # AWS, GCP, AZURE, SELF_HOSTED
      constraints: list[string]
        
    compliance:
      type: "compliance"
      standards: list[string]  # SOC2, HIPAA, GDPR, etc.
      
  # ========== Risk & Security ==========
  risk_level: enum            # VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH
  security_level: enum        # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
  
  # ========== Value ==========
  business_value: string      # Why does this matter?
  impact: string              # What happens if we don't do this?
  
  # ========== Technical ==========
  technical_complexity: enum   # TRIVIAL, LOW, MEDIUM, HIGH, VERY_HIGH
  technical_debt: enum        # NONE, LOW, MEDIUM, HIGH
  
  # ========== Requirements ==========
  required_capabilities: list[CapabilityID]
  nice_to_have: list[CapabilityID]
  
  # ========== Context ==========
  context_references:
    repository: string
    documentation: list[string]
    related_goals: list[GoalID]
    blocking_goals: list[GoalID]
    
  # ========== Assumptions ==========
  assumptions:
    - assumption: string
      confidence: 0.0-1.0
      evidence: string
      verification_required: boolean
      verified: boolean
      
  # ========== Unknowns ==========
  unknowns:
    - unknown: string
      impact: string          # How does this affect the goal?
      investigation_required: boolean
      priority: enum
      
  # ========== Dependencies ==========
  dependencies:
    external: list[string]    # External systems, APIs, etc.
    internal: list[GoalID]     # Goals this depends on
    
  # ========== Conflicts ==========
  conflicts:
    - with_goal: GoalID
      type: string
      resolution: string
      
  # ========== State ==========
  state: enum                 # DRAFT, ANALYZED, PLANNED, IN_PROGRESS, VERIFIED, COMPLETED, ABORTED
  blockers: list[string]
  
  # ========== Meta ==========
  created_by: string          # User or system
  approved_by: string
  tags: list[string]
```

---

## Goal Types

```yaml
GoalTypes:
  BUILD:
    description: "Build something new"
    required_fields: ["mission", "success_criteria"]
    typical_constraints: ["budget", "deadline", "technology"]
    
  FIX:
    description: "Fix existing issue"
    required_fields: ["mission", "success_criteria"]
    typical_constraints: ["budget", "deadline"]
    additional_fields: ["affected_systems", "severity"]
    
  REFACTOR:
    description: "Improve existing system"
    required_fields: ["mission", "success_criteria"]
    typical_constraints: ["compatibility", "performance"]
    
  REVIEW:
    description: "Review code/docs/architecture"
    required_fields: ["mission"]
    typical_constraints: ["scope", "depth"]
    
  ANALYZE:
    description: "Analyze system or data"
    required_fields: ["mission"]
    typical_constraints: ["scope", "tools"]
    
  DEPLOY:
    description: "Deploy to environment"
    required_fields: ["mission", "environment"]
    typical_constraints: ["downtime", "rollback"]
    
  MIGRATE:
    description: "Migrate data or system"
    required_fields: ["mission", "source", "target"]
    typical_constraints: ["downtime", "data_integrity"]
    
  SECURITY:
    description: "Security audit or fix"
    required_fields: ["mission", "scope"]
    typical_constraints: ["timeline", "compliance"]
```

---

## Goal State Machine

```
DRAFT
   ↓ (submitted)
ANALYZED
   ↓ (plan created)
PLANNED
   ↓ (execution starts)
IN_PROGRESS
   ↓ (verification passed)
VERIFIED
   ↓ (all criteria met)
COMPLETED
   ↓ (any time)
ABORTED
   ↓ (blocker resolved)
DRAFT (restart)
```

---

## Example: Build E-commerce Platform

```yaml
Goal:
  id: "goal_2024_001"
  version: "1.0"
  created_at: "2024-01-15T10:00:00Z"
  
  type: "BUILD"
  mission: "Build multi-tenant SaaS e-commerce platform"
  expected_outcome: "Production-ready e-commerce platform with multi-tenancy"
  
  category: "FEATURE"
  priority: "HIGH"
  complexity: "EPIC"
  
  success_criteria:
    - criterion: "User registration and authentication"
      type: "functional"
      measurable: true
      target: "100% of users can register and login"
      
    - criterion: "Product management"
      type: "functional"
      measurable: true
      target: "CRUD operations for products"
      
    - criterion: "Order processing"
      type: "functional"
      measurable: true
      target: "Complete order flow"
      
    - criterion: "Performance"
      type: "performance"
      measurable: true
      target: "< 200ms API response time"
      
  constraints:
    budget:
      type: "budget"
      value: "$500/month"
      is_hard: false
      
    deadline:
      type: "deadline"
      value: "2024-02-15T00:00:00Z"
      is_hard: true
      
    security:
      type: "security"
      level: "HIGH"
      requirements:
        - "OAuth2 authentication"
        - "PCI-DSS compliance for payments"
        
    language:
      type: "language"
      required: ["Python", "TypeScript"]
      forbidden: []
      
    framework:
      type: "framework"
      required: ["FastAPI", "React"]
      forbidden: []
      
  risk_level: "MEDIUM"
  security_level: "CONFIDENTIAL"
  
  business_value: "Enable B2B e-commerce sales channel"
  impact: "Revenue opportunity of $100K/month"
  
  technical_complexity: "HIGH"
  technical_debt: "LOW"
  
  required_capabilities:
    - "cap_generate_backend"
    - "cap_generate_frontend"
    - "cap_design_database"
    - "cap_setup_infra"
    - "cap_deploy"
    
  assumptions:
    - assumption: "User authentication via OAuth2 is acceptable"
      confidence: 0.9
      evidence: "Stakeholder discussion"
      verification_required: true
      verified: false
      
    - assumption: "PostgreSQL is acceptable for database"
      confidence: 1.0
      evidence: "Infrastructure preference"
      verification_required: false
      verified: true
      
  unknowns:
    - unknown: "Payment processor integration details"
      impact: "May affect timeline"
      investigation_required: true
      priority: "HIGH"
```

---

## Related Documents

- [Intent-Analysis.md](./02-Intent-Analysis.md)
- [Reasoning-Graph.md](./04-Reasoning-Graph.md)
