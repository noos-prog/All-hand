# Intent Analysis Engine

> **Before execution, answer: What does the user REALLY want?**

---

## Purpose

The Intent Analysis Engine answers critical questions BEFORE execution:

```
What does the user want?
What didn't they say?
What are they assuming?
What's missing?
Are there risks?
Is the goal feasible?
Are there conflicting goals?
Does the goal need decomposition?
```

---

## Analysis Questions

```yaml
IntentQuestions:
  # Primary questions
  
  1. WHAT_DOES_USER_WANT:
     question: "What does the user actually want?"
     analysis:
       - "Extract core request"
       - "Identify the primary goal"
       - "Understand the motivation"
       
  2. WHAT_DID_NOT_SAY:
     question: "What did they NOT say?"
     analysis:
       - "Identify implicit requirements"
       - "Find unspoken needs"
       - "Detect assumptions"
       
  3. WHAT_ARE_THEY_ASSUMING:
     question: "What are they assuming?"
     analysis:
       - "Identify stated assumptions"
       - "Detect unstated assumptions"
       - "Validate assumptions"
       
  4. WHAT_IS_MISSING:
     question: "What information is missing?"
     analysis:
       - "Identify required data"
       - "Detect gaps"
       - "Request clarification"
       
  5. ARE_THERE_RISKS:
     question: "Are there risks?"
     analysis:
       - "Technical risks"
       - "Business risks"
       - "Security risks"
       - "Timeline risks"
       
  6. IS_GOAL_FEASIBLE:
     question: "Is the goal achievable?"
     analysis:
       - "Technical feasibility"
       - "Resource feasibility"
       - "Time feasibility"
       
  7. ARE_THERE_CONFLICTS:
     question: "Are there conflicting goals?"
     analysis:
       - "Conflicting priorities"
       - "Conflicting constraints"
       - "Conflicting requirements"
       
  8. NEEDS_DECOMPOSITION:
     question: "Does the goal need breaking down?"
     analysis:
       - "Is it too complex?"
       - "Is it too large?"
       - "Should it be split?"
```

---

## Analysis Flow

```
1. RECEIVE REQUEST
         ↓
2. EXTRACT CORE REQUEST
         ↓
3. IDENTIFY ASSUMPTIONS
         ↓
4. DETECT MISSING INFO
         ↓
5. ASSESS RISKS
         ↓
6. CHECK FEASIBILITY
         ↓
7. DETECT CONFLICTS
         ↓
8. RECOMMEND DECOMPOSITION
         ↓
9. GENERATE ANALYSIS REPORT
```

---

## Analysis Output

```yaml
IntentAnalysis:
  # Analysis identification
  goal_id: string
  analyzed_at: datetime
  confidence: 0.0-1.0
  
  # Core understanding
  core_request:
    summary: string
    primary_goal: string
    motivation: string
    
  # Assumptions detected
  assumptions:
    stated:
      - text: string
        confidence: 0.0-1.0
        
    unstated:
      - text: string
        confidence: 0.0-1.0
        detection_method: string
        
  # Missing information
  missing_info:
    - item: string
      importance: enum        # CRITICAL, HIGH, MEDIUM, LOW
      source: string         # Where to get it
      can_infer: boolean    # Can we infer it?
      
  # Risks identified
  risks:
    - risk: string
      type: enum            # TECHNICAL, BUSINESS, SECURITY, TIMELINE
      probability: 0.0-1.0
      impact: enum          # LOW, MEDIUM, HIGH, CRITICAL
      
  # Feasibility assessment
  feasibility:
    technical: enum        # FEASIBLE, CHALLENGING, INFEASIBLE
    resource: enum
    timeline: enum
    
    blockers:
      - blocker: string
        severity: enum
        
  # Conflicts detected
  conflicts:
    - conflict: string
      with_requirement: string
      resolution_approach: string
      
  # Recommendations
  recommendations:
    - type: enum            # CLARIFY, DECOMPOSE, ADJUST_SCOPE, etc.
      description: string
      priority: enum
        
  # Decomposition recommendation
  decomposition:
    recommended: boolean
    reasons:
      - reason: string
    sub_goals:
      - goal_id: string
        name: string
        priority: enum
```

---

## Example Analysis

### Input Request

```
User says: "Build me a web app"
```

### Analysis Output

```yaml
IntentAnalysis:
  goal_id: "goal_analyzed_001"
  analyzed_at: "2024-01-15T10:05:00Z"
  confidence: 0.65
  
  core_request:
    summary: "Build a web application"
    primary_goal: "Create functional web app"
    motivation: "Unspecified"
    
  assumptions:
    stated: []
    unstated:
      - text: "User wants a frontend"
        confidence: 0.8
        detection_method: "Default assumption"
        
      - text: "User expects database"
        confidence: 0.7
        detection_method: "Common pattern"
        
      - text: "User expects deployment"
        confidence: 0.6
        detection_method: "Implied by 'web app'"
        
  missing_info:
    - item: "What type of web app?"
      importance: CRITICAL
      source: "User"
      can_infer: false
      
    - item: "What features?"
      importance: CRITICAL
      source: "User"
      can_infer: false
      
    - item: "What technology stack?"
      importance: HIGH
      source: "User or defaults"
      can_infer: true
      
    - item: "Who are the users?"
      importance: MEDIUM
      source: "User"
      can_infer: false
      
    - item: "What's the budget?"
      importance: MEDIUM
      source: "User"
      can_infer: false
      
    - item: "What's the timeline?"
      importance: MEDIUM
      source: "User"
      can_infer: false
      
  risks:
    - risk: "Unclear requirements may lead to rework"
      type: BUSINESS
      probability: 0.8
      impact: HIGH
      
    - risk: "No technology choice may lead to compatibility issues"
      type: TECHNICAL
      probability: 0.5
      impact: MEDIUM
      
  feasibility:
    technical: CHALLENGING
    resource: FEASIBLE
    timeline: UNKNOWN
    
    blockers:
      - blocker: "Missing critical requirements"
        severity: HIGH
        
  conflicts: []
  
  recommendations:
    - type: CLARIFY
      description: "Request clarification on: app type, features, users"
      priority: CRITICAL
      
    - type: DECOMPOSE
      description: "Break down into frontend, backend, database sub-goals"
      priority: HIGH
      
  decomposition:
    recommended: true
    reasons:
      - "Goal is too broad"
      - "Multiple capabilities needed"
      - "Different expertise areas"
```

---

## Follow-up Questions

Based on analysis, the system may ask:

```yaml
FollowUpQuestions:
  - question: "What type of web application do you need?"
    options:
      - "E-commerce"
      - "SaaS"
      - "Social Network"
      - "Content Management"
      - "Other"
      
  - question: "What are the core features?"
    type: "multi_select"
    options:
      - "User authentication"
      - "Data CRUD"
      - "Real-time updates"
      - "File uploads"
      - "Payments"
      
  - question: "What's your technology preference?"
    options:
      - "No preference"
      - "Python/FastAPI"
      - "JavaScript/Node"
      - "Java/Spring"
      - "Other"
```

---

## Analysis with LLM

```python
async def analyze_intent(
    request: str,
    context: Context
) -> IntentAnalysis:
    """
    Analyze user intent using LLM.
    """
    
    # Build prompt
    prompt = f"""
    Analyze this request: "{request}"
    
    Context:
    - Previous requests: {context.previous_requests}
    - Project: {context.project}
    - User preferences: {context.user_preferences}
    
    Answer:
    1. What does the user really want?
    2. What didn't they say?
    3. What are they assuming?
    4. What's missing?
    5. Are there risks?
    6. Is it feasible?
    7. Are there conflicts?
    8. Should it be decomposed?
    """
    
    # Call LLM
    response = await llm.call(prompt)
    
    # Parse response
    analysis = parse_analysis(response)
    
    return analysis
```

---

## Related Documents

- [Goal-Object.md](./01-Goal-Object.md)
- [Reasoning-Graph.md](./04-Reasoning-Graph.md)
