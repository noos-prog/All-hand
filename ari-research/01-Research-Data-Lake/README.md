# Research Data Lake

> **Everything stored. Nothing lost.**

---

## Vision

```
Traditional Data Storage:
- Store what fits
- Delete old data
- Compress everything

ARI Data Lake:
- Store everything
- Never delete
- Always expand
```

---

## Data Categories

### Raw Data

```yaml
RawData:
  Repositories:
    - github_repos
    - gitlab_repos
    - sourceforge
    - HuggingFace
    - Papers With Code
    
  Source Code:
    - All cloned repos
    - All branches
    - All commits
    
  Benchmarks:
    - Raw results
    - Execution logs
    - Error logs
    
  Providers:
    - Provider metadata
    - Provider versions
    - Provider configurations
```

### Processed Data

```yaml
ProcessedData:
  Capabilities:
    - Discovered capabilities
    - Capability mappings
    - Capability scores
    
  Providers:
    - Provider scores
    - Provider rankings
    - Provider comparisons
    
  Models:
    - Model benchmarks
    - Model comparisons
    - Model costs
    
  Tasks:
    - Task definitions
    - Task results
    - Task analyses
```

### Analytics Data

```yaml
AnalyticsData:
  Leaderboards:
    - Provider rankings
    - Capability rankings
    - Model rankings
    
  Trends:
    - Performance trends
    - Cost trends
    - Quality trends
    
  Reports:
    - Weekly reports
    - Monthly reports
    - Quarterly reports
```

---

## Storage Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Lake Storage                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Hot Storage (Recent Data)                              │ │
│  │  - Last 30 days                                      │ │
│  │  - Fast access                                       │ │
│  │  - Full resolution                                  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Warm Storage (Monthly Data)                           │ │
│  │  - Last 12 months                                    │ │
│  │  - Medium access                                    │ │
│  │  - Aggregated                                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Cold Storage (Historical Data)                       │ │
│  │  - All time                                         │ │
│  │  - Slow access                                      │ │
│  │  - Compressed                                       │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Archive Storage (Permanent)                          │ │
│  │  - Critical benchmarks                               │ │
│  │  - Historical comparisons                           │ │
│  │  - Legal/compliance                                │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Schema

### Benchmark Result

```yaml
BenchmarkResult:
  id: string
  timestamp: datetime
  
  # Task Info
  task:
    id: string
    name: string
    capability: string
    difficulty: enum
  
  # Provider Info
  provider:
    id: string
    name: string
    version: string
    type: string
    
  # Model Info
  model:
    id: string
    name: string
    version: string
    
  # Execution
  execution:
    duration: duration
    start_time: datetime
    end_time: datetime
    
  # Resources
  resources:
    cpu_seconds: decimal
    memory_mb_seconds: decimal
    gpu_seconds: decimal
    
  # Costs
  costs:
    model_cost: decimal
    compute_cost: decimal
    api_cost: decimal
    total_cost: decimal
    
  # Results
  results:
    success: boolean
    quality_score: decimal
    correctness: decimal
    artifacts: list[Artifact]
    
  # Evidence
  evidence:
    logs: string
    screenshots: list[string]
    videos: list[string]
    diffs: list[string]
    
  # Judge Results
  judge:
    score: decimal
    details: dict
    judges_used: list[string]
```

---

## Data Collection

### Continuous Collection

```yaml
CollectionSources:
  GitHub:
    frequency: "continuous"
    sources:
      - Trending repos
      - Awesome lists
      - Organization repos
      - Starred repos
      
  GitLab:
    frequency: "daily"
    sources:
      - Popular projects
      - Groups
      
  Papers:
    frequency: "weekly"
    sources:
      - Papers With Code
      - ArXiv
      - HuggingFace
      
  Providers:
    frequency: "on release"
    sources:
      - Provider APIs
      - Provider releases
      - Provider benchmarks
```

---

## Data Retention

```yaml
DataRetention:
  Raw:
    hot: "30 days"
    warm: "12 months"
    cold: "forever"
    
  Processed:
    all: "forever"
    
  Analytics:
    daily: "90 days"
    monthly: "5 years"
    yearly: "forever"
```

---

## Data Access

```python
class DataAccess:
    """
    Access patterns for ARI data.
    """
    
    def get_benchmark(
        benchmark_id: str
    ) -> BenchmarkResult:
        """
        Get specific benchmark result.
        """
        pass
        
    def get_provider_history(
        provider_id: str,
        time_range: TimeRange
    ) -> list[BenchmarkResult]:
        """
        Get provider benchmark history.
        """
        pass
        
    def get_capability_comparison(
        capability_id: str
    ) -> CapabilityComparison:
        """
        Compare providers for capability.
        """
        pass
        
    def get_trend(
        metric: str,
        time_range: TimeRange
    ) -> Trend:
        """
        Get metric trend over time.
        """
        pass
```

---

## Related Documents

- [Capability-Library.md](../04-Capability-Library/README.md)
- [Evaluation-Engine.md](../06-Evaluation-Engine/README.md)
