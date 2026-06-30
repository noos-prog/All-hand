# Knowledge Engine

> **Searches internal Knowledge Base, not the internet.**

---

## Purpose

The Knowledge Engine provides the Core Brain with relevant knowledge from the internal Knowledge Base, Repository Index, Architecture docs, Memory, Capabilities, Standards, and Research.

---

## What It Is NOT

```
❌ It does NOT search the internet
❌ It does NOT use external APIs
❌ It does NOT scrape websites
❌ It does NOT query external databases

It ONLY searches internal knowledge sources
```

---

## Knowledge Sources

```
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Engine                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Knowledge Base  │  │  Repository     │                  │
│  │   (Internal)    │  │    Index        │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Architecture   │  │    Memory       │                  │
│  │    Documents    │  │   (Learned)     │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Capabilities   │  │   Standards     │                  │
│  │    Registry     │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Research      │  │     ADRs        │                  │
│  │                 │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Knowledge Source Details

### Knowledge Base
- Internal documentation
- Project specifications
- Design documents
- User guides

### Repository Index
- Tool database
- Capability mappings
- Alternative tools
- Usage statistics

### Architecture Documents
- System architecture
- Design patterns
- Integration guides
- ADRs (Architecture Decision Records)

### Memory
- Learned patterns
- Past successes
- Past failures
- User preferences

### Capabilities Registry
- All capabilities
- Tool mappings
- Rankings
- Scores

### Standards
- Coding standards
- Documentation standards
- API standards
- Security standards

### Research
- Technology radar
- Experiment results
- Performance benchmarks
- Case studies

---

## Search Interface

```yaml
KnowledgeQuery:
  query: string           # Natural language query
  sources: list          # Which sources to search
  filters: dict          # Filtering criteria
  limit: integer         # Max results
  
KnowledgeResult:
  results: list          # Matched entries
  sources: list          # Source of each result
  relevance_scores: list # Relevance to query
  metadata: dict         # Additional info
```

---

## Query Types

| Query Type | Example | Sources |
|------------|---------|---------|
| `TOOL_SELECTION` | "Best tool for API generation" | Capability Registry, Repo Index |
| `ARCHITECTURE` | "How to structure microservices" | Architecture docs, ADRs |
| `BEST_PRACTICE` | "Error handling patterns" | Standards, Research |
| `DOMAIN` | "E-commerce patterns" | Knowledge Base |
| `TOOL_ALTERNATIVE` | "Replace LangChain with?" | Repository Index |
| `CAPABILITY` | "What tools can do X?" | Capability Registry |

---

## Search Algorithm

```python
def search(query: KnowledgeQuery) -> KnowledgeResult:
    results = []
    
    for source in query.sources:
        source_results = search_source(source, query)
        scored_results = score_relevance(source_results, query)
        results.extend(scored_results)
    
    # Sort by relevance
    sorted_results = sort_by_relevance(results)
    
    # Limit results
    return KnowledgeResult(
        results=sorted_results[:query.limit],
        sources=[r.source for r in sorted_results],
        relevance_scores=[r.score for r in sorted_results]
    )
```

---

## Relevance Calculation

```yaml
RelevanceScore:
  query_match: 0.0-1.0     # How well it matches query
  recency: 0.0-1.0         # How recent
  usage_count: 0.0-1.0     # How often used
  success_rate: 0.0-1.0    # Historical success
  
  # Weights
  weights:
    query_match: 0.4
    recency: 0.2
    usage_count: 0.2
    success_rate: 0.2
    
  overall_score: calculated
```

---

## Caching Strategy

| Data Type | Cache Duration | Invalidation |
|-----------|----------------|--------------|
| Tool Info | 1 hour | On update |
| Capabilities | 1 hour | On update |
| Architecture | 24 hours | On ADR change |
| Standards | 1 week | On version bump |
| Research | 1 week | Manual refresh |

---

## Example Queries

**Query:** "Best tool for generating REST APIs in Python"

```yaml
Query:
  query: "REST API generation Python"
  sources: [capability_registry, repository_index]
  filters:
    language: Python
    capability: generate_api
  limit: 5

Result:
  - tool: OpenHands
    score: 0.95
    reason: "Best overall for Python APIs"
    
  - tool: Claude Code
    score: 0.88
    reason: "Strong reasoning, good for APIs"
    
  - tool: Aider
    score: 0.82
    reason: "Good CLI option, fast"
```

---

## Knowledge Update Triggers

| Trigger | Action |
|---------|--------|
| New tool added | Update capability mappings |
| Tool deprecation | Update registry |
| ADR created | Update architecture docs |
| Experiment completed | Update research |
| User feedback | Update memory |
| Benchmark update | Update tool scores |

---

## Related Documents

- [02-Components/Capability-Selector.md](./02-Components/05-Capability-Selector.md)
- [02-Components/Learning-Engine.md](./02-Components/10-Learning-Engine.md)
