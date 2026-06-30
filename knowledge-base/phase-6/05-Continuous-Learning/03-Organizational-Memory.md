# Organizational Memory

> **Not just technical memory, but organizational memory.**

---

## Concept

```
Technical Memory (OLD):
  - Code patterns
  - Architecture rules
  - API definitions

Organizational Memory (NEW):
  - Best decisions
  - Failed decisions
  - Most successful tools
  - Failed tools
  - Reasons for replacement
  - Best patterns
  - Worst patterns
  - Best strategies
  - Statistics from 1000s of projects
```

---

## Memory Structure

```yaml
OrganizationalMemory:
  # ========== Decision Memory ==========
  decision_memory:
    successful_decisions:
      - decision: string
        success_rate: decimal
        contexts: list[string]
        evidence: list[string]
        project_count: integer
        
    failed_decisions:
      - decision: string
        failure_rate: decimal
        reasons: list[string]
        lessons: list[string]
        project_count: integer
        
  # ========== Tool Memory ==========
  tool_memory:
    successful_tools:
      - tool: string
        success_rate: decimal
        use_cases: list[string]
        avg_quality: decimal
        avg_cost: decimal
        project_count: integer
        
    failed_tools:
      - tool: string
        failure_rate: decimal
        failure_reasons: list[string]
        projects_affected: integer
        replacements: list[string]
        
  # ========== Pattern Memory ==========
  pattern_memory:
    best_patterns:
      - pattern: string
        success_rate: decimal
        domains: list[string]
        context_fit: dict
        project_count: integer
        
    worst_patterns:
      - pattern: string
        failure_rate: decimal
        reasons: list[string]
        anti_pattern: boolean
        
  # ========== Strategy Memory ==========
  strategy_memory:
    best_strategies:
      - strategy: string
        success_rate: decimal
        context: string
        project_types: list[string]
        avg_outcome: decimal
        
    failed_strategies:
      - strategy: string
        failure_rate: decimal
        reasons: list[string]
        
  # ========== Statistics ==========
  statistics:
    total_projects: integer
    successful_projects: integer
    failed_projects: integer
    
    avg_quality_score: decimal
    avg_cost_per_project: decimal
    avg_time_per_project: decimal
    
    top_technologies: list[string]
    top_patterns: list[string]
    top_providers: list[string]
    
  # ========== Recommendations ==========
  recommendations:
    for_domain:
      - domain: string
        recommendations: list[string]
        confidence: decimal
        
    for_context:
      - context: string
        recommendations: list[string]
        confidence: decimal
        
    for_technology:
      - technology: string
        recommendations: list[string]
        confidence: decimal
```

---

## Learning Sources

```yaml
LearningSources:
  # Where organizational memory learns from
  
  1. Completed Missions
     - Extract decisions
     - Extract outcomes
     - Extract patterns
     
  2. Failed Missions
     - Extract failure reasons
     - Extract what went wrong
     - Extract lessons learned
     
  3. Provider Performance
     - Track provider success rates
     - Track provider failure modes
     - Track provider quality scores
     
  4. Architecture Decisions
     - Track ADR outcomes
     - Track what worked
     - Track what didn't
     
  5. Technology Selection
     - Track technology success
     - Track technology failures
     - Track replacement decisions
```

---

## Learning Process

```python
async def learn_from_mission(mission: Mission):
    """
    Extract learning from completed mission.
    """
    
    memory = OrganizationalMemory.get_instance()
    
    # 1. Extract decisions
    for decision in mission.decisions:
        await memory.record_decision(decision)
        
    # 2. Extract tool performance
    for provider_usage in mission.provider_usage:
        await memory.record_tool_performance(provider_usage)
        
    # 3. Extract patterns
    for pattern in mission.patterns:
        await memory.record_pattern(pattern)
        
    # 4. Extract strategies
    for strategy in mission.strategies:
        await memory.record_strategy(strategy)
        
    # 5. Update statistics
    await memory.update_statistics(mission)
    
    # 6. Generate recommendations
    await memory.generate_recommendations()


async def learn_from_failure(failure: MissionFailure):
    """
    Extract learning from failed mission.
    """
    
    memory = OrganizationalMemory.get_instance()
    
    # 1. Record failure
    await memory.record_failure(failure)
    
    # 2. Analyze reasons
    reasons = await analyze_failure(failure)
    
    for reason in reasons:
        await memory.record_failed_pattern(reason)
        
    # 3. Generate lessons
    lessons = await generate_lessons(failure)
    
    for lesson in lessons:
        await memory.record_lesson(lesson)
        
    # 4. Update recommendations
    await memory.update_recommendations()
```

---

## Example: Learning from 1000 Projects

```yaml
OrganizationalMemory:
  statistics:
    total_projects: 1000
    successful_projects: 850
    failed_projects: 150
    
    avg_quality_score: 0.87
    avg_cost_per_project: "$5,000"
    avg_time_per_project: "3 weeks"
    
  successful_decisions:
    - decision: "Use microservices for SaaS"
      success_rate: 0.92
      contexts: ["SaaS", "Multi-tenant", "High scale"]
      evidence: ["85 successful projects"]
      
    - decision: "Use PostgreSQL for transactional"
      success_rate: 0.95
      contexts: ["E-commerce", "Finance", "CRM"]
      
  failed_decisions:
    - decision: "Use MongoDB for financial data"
      failure_rate: 0.85
      reasons:
        - "ACID compliance issues"
        - "Transaction complexity"
      lessons:
        - "Use relational for financial"
        
  best_tools:
    - tool: "OpenHands"
      success_rate: 0.88
      use_cases: ["Complex features", "Large projects"]
      avg_quality: 0.92
      avg_cost: "$0.05/execution"
      
    - tool: "Semgrep"
      success_rate: 0.95
      use_cases: ["Security analysis", "Static analysis"]
      
  worst_tools:
    - tool: "Tool X"
      failure_rate: 0.75
      failure_reasons:
        - "Inconsistent output"
        - "High cost"
      replacements: ["OpenHands", "Aider"]
      
  best_patterns:
    - pattern: "Test-driven development"
      success_rate: 0.90
      domains: ["Backend", "API", "Database"]
      
  worst_patterns:
    - pattern: "Big bang integration"
      failure_rate: 0.80
      anti_pattern: true
```

---

## Querying Organizational Memory

```python
async def query_memory(query: MemoryQuery) -> MemoryResult:
    """
    Query organizational memory.
    """
    
    memory = OrganizationalMemory.get_instance()
    
    # Find best tools for this context
    if query.type == "tool_recommendation":
        tools = await memory.find_tools(
            domain=query.domain,
            use_case=query.use_case,
            requirements=query.requirements
        )
        
        return sorted(tools, key=lambda t: t.success_rate, reverse=True)
        
    # Find best patterns for this domain
    if query.type == "pattern_recommendation":
        patterns = await memory.find_patterns(
            domain=query.domain,
            context=query.context
        )
        
        return sorted(patterns, key=lambda p: p.success_rate, reverse=True)
        
    # Find best decisions for this context
    if query.type == "decision_guidance":
        decisions = await memory.find_decisions(
            context=query.context
        )
        
        return [d for d in decisions if d.success_rate > 0.8]
```

---

## Usage Examples

### Example 1: New E-commerce Project

```
Query: "Best patterns for e-commerce platform"

Result:
1. Microservices: 92% success rate
2. PostgreSQL: 95% success rate
3. Test-driven: 90% success rate
4. Blue-green deployment: 88% success rate

Recommendation:
- "Use microservices for scalability"
- "Use PostgreSQL for transactions"
- "Use TDD for quality"
```

### Example 2: Security-Critical Project

```
Query: "Best tools for security analysis"

Result:
1. Semgrep: 95% success rate
2. SonarQube: 88% success rate
3. Snyk: 85% success rate

Recommendation:
- "Use Semgrep for static analysis"
- "Use Snyk for dependency scanning"
```

### Example 3: Low-Budget Project

```
Query: "Best approach for low budget"

Result:
1. Use simpler architecture: 85% success
2. Use open-source tools: 90% success
3. Reduce testing: 30% success (NOT recommended)

Recommendation:
- "Keep architecture simple"
- "Use open-source stack"
- "Don't skip testing"
```

---

## Knowledge Hierarchy

```yaml
KnowledgeHierarchy:
  LEVEL 1: RAW DATA
    - Mission logs
    - Execution metrics
    - Provider performance
    - Code patterns
    
  LEVEL 2: EXTRACTED KNOWLEDGE
    - Success rates
    - Failure patterns
    - Recommendations
    - Lessons learned
    
  LEVEL 3: STRATEGIC INSIGHTS
    - Best practices
    - Anti-patterns
    - Context-aware guidance
    - Trend analysis
    
  LEVEL 4: AUTONOMOUS DECISIONS
    - Automated recommendations
    - Pre-approved patterns
    - Trusted tools
    - Proven strategies
```

---

## Comparison with Individual Memory

```yaml
Comparison:

INDIVIDUAL MEMORY:
  - Learns from ONE project
  - Limited experience
  - Personal biases
  - Limited scope
  
ORGANIZATIONAL MEMORY:
  - Learns from 1000s of projects
  - Massive experience
  - Data-driven insights
  - Universal patterns
```

---

## Privacy & Security

```yaml
Privacy:
  # What can be learned from
  
  CAN_LEARN:
    - Patterns and anti-patterns
    - Success rates
    - Average costs
    - Best practices
    - Recommended tools
    
  CANNOT_LEARN:
    - Proprietary code
    - User credentials
    - API keys
    - Business secrets
    - Personal information
```

---

## Related Documents

- [Knowledge-Mining.md](./01-Knowledge-Mining.md)
- [Capability-Optimization.md](./02-Capability-Optimization.md)
