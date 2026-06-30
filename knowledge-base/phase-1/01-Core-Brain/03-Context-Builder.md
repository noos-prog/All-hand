# Context Builder

> **Collects all context and creates a Unified Context Object.**

---

## Purpose

The Context Builder aggregates information from multiple sources to create a comprehensive `Unified Context Object` that provides the Core Brain with everything it needs to make decisions.

---

## Context Sources

```
┌─────────────────────────────────────────────────────────────┐
│                    Context Builder                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Conversation │  │ Repository  │  │  Knowledge  │        │
│  │   History   │  │   Context   │  │    Base    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Memory    │  │   Docs     │  │   Files    │        │
│  │             │  │             │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Issues    │  │    Logs     │  │   Config    │        │
│  │             │  │             │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Context Sources Detail

| Source | Description | Access Method |
|--------|-------------|---------------|
| **Conversation** | Current and past messages | Message history |
| **Repository** | Codebase structure, files | Repository API |
| **Knowledge** | Domain knowledge, best practices | Knowledge Base |
| **Memory** | Past interactions, learned patterns | Memory store |
| **Documentation** | Project docs, APIs, specs | Doc index |
| **Files** | Current file contents | File system |
| **Issues** | GitHub issues, bugs | Issue tracker |
| **Logs** | Application logs, errors | Log aggregator |
| **Config** | Environment, settings | Config store |

---

## Unified Context Object

```yaml
UnifiedContext:
  # Identity
  id: string
  goal_id: string
  created_at: datetime
  
  # Conversation Context
  conversation:
    current_messages: list
    previous_sessions: list
    user_preferences: dict
    
  # Repository Context
  repository:
    structure: object      # File tree
    languages: list        # Programming languages
    frameworks: list       # Frameworks used
    dependencies: list     # Package dependencies
    architecture: string   # Current architecture
    
  # Knowledge Context
  knowledge:
    domain: string         # Business domain
    patterns: list         # Known patterns
    best_practices: list   # Domain best practices
    constraints: list      # Known constraints
    
  # Memory Context
  memory:
    past_goals: list       # Previous goals
    successful_patterns: list
    failed_patterns: list
    tool_preferences: dict
    
  # Documentation Context
  documentation:
    project_docs: list
    api_docs: list
    architecture_docs: list
    
  # File Context
  files:
    relevant_files: list   # Files relevant to goal
    recent_changes: list   # Recent modifications
    open_files: list       # Currently open
    
  # Issue Context
  issues:
    related_issues: list   # Linked issues
    blockers: list         # Blocking issues
    context: string        # Issue background
    
  # Log Context
  logs:
    recent_errors: list
    performance_metrics: dict
    usage_patterns: dict
    
  # Config Context
  config:
    environment: string    # dev, staging, prod
    settings: dict         # Environment variables
    secrets: dict          # Secret references
```

---

## Aggregation Process

```
1. Receive Goal Object
        ↓
2. Identify relevant context sources
        ↓
3. Fetch Conversation history
        ↓
4. Fetch Repository context
        ↓
5. Fetch Knowledge Base entries
        ↓
6. Fetch Memory entries
        ↓
7. Fetch Documentation
        ↓
8. Fetch Relevant Files
        ↓
9. Fetch Related Issues
        ↓
10. Fetch Recent Logs
        ↓
11. Fetch Configuration
        ↓
12. Merge all into UnifiedContext
        ↓
13. Validate completeness
        ↓
14. Return UnifiedContext
```

---

## Relevance Scoring

Each context piece is scored for relevance:

```yaml
RelevanceScore:
  goal_alignment: 0.0-1.0  # How aligned with goal
  recency: 0.0-1.0        # How recent
  reliability: 0.0-1.0    # Source reliability
  completeness: 0.0-1.0   # How complete
  overall: 0.0-1.0         # Weighted average
```

---

## Context Freshness

| Type | Freshness | Refresh Rate |
|------|-----------|--------------|
| Conversation | Live | Every message |
| Repository | Real-time | On demand |
| Knowledge | Daily | Weekly update |
| Memory | Persistent | On learning |
| Documentation | Daily | On commit |
| Files | Real-time | On change |
| Issues | Real-time | On update |
| Logs | Real-time | Streaming |
| Config | Cached | On startup |

---

## Context Validation

```yaml
ValidationRules:
  - name: "has_goal"
    check: "Must have goal_id"
    
  - name: "has_conversation"
    check: "Must have conversation context"
    
  - name: "has_repository"
    check: "Must have repo context if goal relates to code"
    
  - name: "has_knowledge"
    check: "Must have knowledge context"
    
  - name: "completeness_threshold"
    check: "Overall completeness >= 0.7"
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Source unavailable | Mark as stale, use cache |
| Partial data | Continue with available |
| Conflicting data | Flag for review |
| Empty context | Request more input |

---

## Related Documents

- [01-Core-Brain-Overview.md](./01-Core-Brain-Overview.md)
- [03-Objects/Universal-Task-Object.md](./03-Objects/01-Universal-Task-Object.md)
