# Goal Interpreter

> **Transforms user input into structured Goal Objects.**

---

## Purpose

The Goal Interpreter converts natural language from users into a structured `Goal Object` that can be processed by the Core Brain.

---

## Input → Output

```
User: "ابنِ لي متجر إلكتروني"

      ↓
Goal Interpreter

      ↓
Goal Object
```

---

## Goal Object Schema

```yaml
Goal:
  # Identification
  id: string              # Unique goal identifier
  version: string        # Schema version
  
  # Core Information
  type: enum             # Type of goal
  description: string    # Natural language description
  original_text: string  # Raw user input
  
  # Priority & Constraints
  priority: enum         # Critical, High, Medium, Low
  budget: string         # Budget constraints
  deadline: datetime     # Time constraints
  
  # Functional
  constraints: list      # Hard constraints
  preferences: list      # Soft constraints
  
  # Success Criteria
  success_criteria: list
  acceptance_tests: list
  
  # Output
  output: enum           # Expected output type
  output_format: enum    # JSON, Files, API, etc.
  
  # Metadata
  created_at: datetime
  expires_at: datetime
  parent_goal: string    # For sub-goals
```

---

## Goal Types

| Type | Description | Example |
|------|-------------|---------|
| `BUILD` | Build something new | "Build an e-commerce store" |
| `FIX` | Fix existing issue | "Fix the login bug" |
| `REFACTOR` | Improve existing | "Refactor the API" |
| `REVIEW` | Review code/docs | "Review the PR" |
| `ANALYZE` | Analyze something | "Analyze performance" |
| `DEPLOY` | Deploy to environment | "Deploy to production" |
| `MIGRATE` | Migrate data/system | "Migrate to PostgreSQL" |
| `SECURITY` | Security audit | "Audit for vulnerabilities" |
| `TEST` | Create/run tests | "Add unit tests" |
| `DOCUMENT` | Create documentation | "Document the API" |

---

## Priority Levels

| Level | Description | SLA |
|-------|-------------|-----|
| `CRITICAL` | Production down | 1 hour |
| `HIGH` | Major feature blocked | 4 hours |
| `MEDIUM` | Feature enhancement | 24 hours |
| `LOW` | Nice to have | 72 hours |

---

## Constraint Types

```yaml
Constraints:
  - name: "language"
    type: "required"
    value: "Python"
    
  - name: "framework"
    type: "forbidden"
    value: "Django"
    
  - name: "budget"
    type: "limit"
    value: "$100/month"
    
  - name: "performance"
    type: "requirement"
    value: "<100ms latency"
```

---

## Success Criteria Examples

```yaml
Success Criteria:
  - "User can browse products"
  - "User can add to cart"
  - "User can checkout"
  - "Payment processing works"
  - "Admin can manage inventory"
  
Acceptance Tests:
  - "Load time < 2 seconds"
  - "99.9% uptime"
  - "Zero security vulnerabilities"
```

---

## Processing Flow

```
1. Receive raw input
        ↓
2. Extract entities (nouns, verbs, constraints)
        ↓
3. Classify goal type
        ↓
4. Extract priorities
        ↓
5. Identify constraints
        ↓
6. Define success criteria
        ↓
7. Generate Goal Object
        ↓
8. Validate completeness
        ↓
9. Return Goal Object or ask for clarification
```

---

## Example Transformation

**Input:**
```
"ابنِ لي متجر إلكتروني بسيط بـ Python و FastAPI، 
يحتوي على تسجيل دخول وإدارة منتجات وسلة مشتريات. 
أريده جاهز خلال أسبوع وبميزانية 500 دولار شهرياً."
```

**Output Goal Object:**
```yaml
Goal:
  id: "goal_2024_001"
  type: "BUILD"
  description: "E-commerce platform with auth, products, cart"
  
  priority: "MEDIUM"
  budget: "$500/month"
  deadline: "7 days"
  
  constraints:
    - name: "language"
      type: "required"
      value: "Python"
    - name: "framework"
      type: "required"
      value: "FastAPI"
      
  preferences:
    - "Simple design"
    - "Quick to build"
    
  success_criteria:
    - "User authentication"
    - "Product management"
    - "Shopping cart"
    
  output:
    type: "WEB_APPLICATION"
    format: "DEPLOYED"
```

---

## Validation Rules

| Rule | Description |
|------|-------------|
| `has_id` | Must have unique ID |
| `has_type` | Must have goal type |
| `has_description` | Must have description |
| `has_priority` | Must have priority |
| `has_success_criteria` | Must have at least one criteria |
| `is_feasible` | Must be technically possible |

---

## Error Handling

| Error | Action |
|-------|--------|
| Ambiguous input | Ask clarifying questions |
| Missing constraints | Use defaults |
| Conflicting constraints | Flag for review |
| Invalid goal | Reject with explanation |

---

## Related Documents

- [03-Objects/Universal-Task-Object.md](./03-Objects/01-Universal-Task-Object.md)
- [04-Policies/Decision-Policies.md](./04-Policies/01-Decision-Policies.md)
