# Capability Marketplace Overview

> **Not a store. A database of capability providers.**

---

## Marketplace Concept

```
┌─────────────────────────────────────────────────────────────┐
│                   Capability Marketplace                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Capability                                                  │
│       ↓                                                     │
│  Generate Tests                                              │
│       ↓                                                     │
│  Available Providers                                        │
│       ↓                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │OpenHands │ │  Goose  │ │  Aider  │ │ Claude  │       │
│  │  0.95   │ │  0.85   │ │  0.82   │ │  0.90   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│       ↓                                                     │
│  Scores & Metrics                                           │
│       ↓                                                     │
│  Choose (by score)                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Provider Database Schema

```yaml
ProviderDatabase:
  # Provider Information
  provider_id: string
  name: string
  description: string
  
  # Technical
  adapter_type: enum        # cli, api, sdk, docker
  endpoint: string           # For API type
  image: string             # For Docker type
  
  # Capabilities
  capabilities: list[CapabilityID]
  
  # Scoring
  scores:
    overall: 0.0-1.0
    by_capability:
      cap_id: score
      
  # Metrics
  metrics:
    total_executions: integer
    success_rate: percentage
    avg_cost: decimal
    avg_duration: duration
    uptime: percentage
    
  # Status
  status: enum              # active, inactive, experimental
  health: enum              # healthy, degraded, unhealthy
  
  # Costs
  pricing:
    model: enum             # free, per_use, subscription
    per_use_cost: decimal
    monthly_cost: decimal
    
  # Limits
  limits:
    max_concurrent: integer
    rate_limit: integer     # per minute
    quota: integer           # per day/month
```

---

## Capability Provider Matrix

```yaml
CapabilityMatrix:
  # Rows: Capabilities
  # Cols: Providers
  # Values: Score (0.0-1.0)
  
  capabilities:
    - cap_generate_code
    - cap_edit_code
    - cap_generate_api
    - cap_deploy
    - cap_run_tests
    - cap_fix_bugs
    - cap_review_code
    
  providers:
    - openhands
    - cline
    - aider
    - goose
    - claude
    - cursor
    
  matrix:
    # Format: [provider_id][capability_id] = score
    
    openhands:
      cap_generate_code: 0.95
      cap_edit_code: 0.92
      cap_generate_api: 0.94
      cap_deploy: 0.88
      cap_run_tests: 0.90
      cap_fix_bugs: 0.85
      cap_review_code: 0.88
      
    cline:
      cap_generate_code: 0.88
      cap_edit_code: 0.92
      cap_generate_api: 0.85
      cap_deploy: 0.80
      cap_run_tests: 0.85
      cap_fix_bugs: 0.82
      cap_review_code: 0.80
      
    aider:
      cap_generate_code: 0.85
      cap_edit_code: 0.90
      cap_generate_api: 0.88
      cap_deploy: 0.75
      cap_run_tests: 0.88
      cap_fix_bugs: 0.88
      cap_review_code: 0.82
      
    goose:
      cap_generate_code: 0.82
      cap_edit_code: 0.88
      cap_generate_api: 0.80
      cap_deploy: 0.78
      cap_run_tests: 0.82
      cap_fix_bugs: 0.80
      cap_review_code: 0.78
      
    claude:
      cap_generate_code: 0.92
      cap_edit_code: 0.88
      cap_generate_api: 0.90
      cap_deploy: 0.85
      cap_run_tests: 0.92
      cap_fix_bugs: 0.90
      cap_review_code: 0.95
```

---

## Provider Comparison

```yaml
ProviderComparison:
  # Compare providers side by side
  
  columns:
    - name
    - capabilities_count
    - avg_score
    - cost_per_use
    - uptime
    - latency
    
  providers:
    - id: openhands
      name: "OpenHands"
      capabilities_count: 45
      avg_score: 0.91
      cost_per_use: 0.05
      uptime: 99.9%
      latency: "3 min"
      
    - id: cline
      name: "Cline"
      capabilities_count: 35
      avg_score: 0.85
      cost_per_use: 0.02
      uptime: 99.5%
      latency: "2 min"
      
    - id: aider
      name: "Aider"
      capabilities_count: 30
      avg_score: 0.84
      cost_per_use: 0.01
      uptime: 99.7%
      latency: "1 min"
```

---

## Metrics Dashboard

```yaml
MetricsDashboard:
  # Per Capability
  cap_generate_code:
    total_executions: 5000
    success_rate: 92%
    avg_duration: "3m 30s"
    avg_cost: 0.04
    
    by_provider:
      openhands:
        executions: 3000
        success_rate: 95%
      cline:
        executions: 1200
        success_rate: 88%
      aider:
        executions: 800
        success_rate: 85%
        
    trends:
      - week: "2024-W01"
        executions: 500
        success_rate: 91%
      - week: "2024-W02"
        executions: 550
        success_rate: 92%
```

---

## Provider Selection Guide

```yaml
SelectionGuide:
  # When to use which provider
  
  by_priority:
    speed:
      1. aider (fastest)
      2. cline
      3. openhands
      
    quality:
      1. openhands
      2. claude
      3. cline
      
    cost:
      1. aider (cheapest)
      2. cline
      3. openhands
      
    reliability:
      1. openhands (highest uptime)
      2. claude
      3. aider
      
  by_use_case:
    small_changes:
      - aider
      - cline
      
    new_features:
      - openhands
      - claude
      
    bug_fixes:
      - aider
      - cline
      - openhands
      
    code_review:
      - claude
      - openhands
```

---

## Related Documents

- [Registry-Structure.md](../02-Capability-Registry/01-Registry-Structure.md)
- [Provider-Mapping.md](../02-Capability-Registry/02-Provider-Mapping.md)
