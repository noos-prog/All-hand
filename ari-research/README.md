# AGOS Research Infrastructure (ARI)

> **The World's Largest Automated Research Laboratory**

---

## Implementation

```
ari-research/
├── __init__.py                    # Module exports
├── test_ari.py                    # Test suite
│
├── 01-Research-Data-Lake/
│   ├── __init__.py
│   ├── repository.py               # Repository data
│   ├── provider.py                 # Provider registry
│   ├── benchmark.py                # Benchmark definitions
│   └── model.py                    # Model registry
│
├── 06-Evaluation-Engine/
│   ├── __init__.py
│   ├── engine.py                  # Evaluation engine
│   ├── sandbox.py                 # Sandbox factory
│   ├── judge.py                   # Judge engine
│   └── genome.py                  # Genome engine
│
├── 10-Dashboards/
│   ├── __init__.py
│   ├── leaderboard.py             # Leaderboards
│   └── reports.py                 # Report generation
│
└── README.md
```

---

## Quick Start

```python
from ari_research import (
    # Data Lake
    RepositoryDataLake,
    ProviderRegistry,
    BenchmarkRunner,
    ModelRegistry,
    # Evaluation
    EvaluationEngine,
    SandboxFactory,
    JudgeEngine,
    GenomeEngine,
    # Analytics
    RankingEngine,
    ReportGenerator,
)

# 1. Repository Data Lake
lake = RepositoryDataLake()
repo = Repository(...)
lake.add_repository(repo)

# 2. Provider Registry
registry = ProviderRegistry()
registry.register(provider)

# 3. Evaluation Engine
engine = EvaluationEngine()
result = engine.evaluate(task, provider_id)

# 4. Sandbox
factory = SandboxFactory()
sandbox = factory.create_isolated_sandbox("python")
result = sandbox.execute("print('Hello')", "python")

# 5. Leaderboard
ranking = RankingEngine()
leaderboard = ranking.rank_providers(providers)

# 6. Reports
generator = ReportGenerator()
report = generator.generate_provider_report(provider_id, data, results)
```

---

## Core Components

### Data Lake
- **Repository**: Repository discovery, analysis, metrics
- **Provider**: Provider registry, capability mapping
- **Benchmark**: Benchmark definitions, suites, runners
- **Model**: Model registry, comparison

### Evaluation Engine
- **Engine**: Task evaluation, result aggregation
- **Sandbox**: Isolated code execution
- **Judge**: Output judgement and scoring
- **Genome**: Agent genome analysis

### Analytics
- **Leaderboard**: Provider/model rankings
- **Reports**: Report generation and publishing

---

## Running Tests

```bash
cd ari-research
python test_ari.py
```

---

## Implementation Files

| File | Lines | Description |
|------|-------|-------------|
| `repository.py` | 300+ | Repository data lake |
| `provider.py` | 350+ | Provider registry |
| `benchmark.py` | 300+ | Benchmark system |
| `model.py` | 300+ | Model registry |
| `engine.py` | 300+ | Evaluation engine |
| `sandbox.py` | 300+ | Sandbox factory |
| `judge.py` | 300+ | Judge engine |
| `genome.py` | 350+ | Genome engine |
| `leaderboard.py` | 350+ | Rankings |
| `reports.py` | 350+ | Report generation |

**Total: 3,200+ lines of production code**

---

*We don't believe. We measure.*
