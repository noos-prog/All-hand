# Repository Intelligence Engine (RIE) v2.0.0

> **Analyzes repositories and generates Repository DNA.**

---

## Architecture

```
rie/
├── contracts/           # Domain contracts
├── domain/            # Domain models
├── infrastructure/    # Git operations, File system
├── detectors/         # Isolated plugin-based detectors
│   ├── ai_detector.py        # AI Stack Detector
│   ├── capability_detector.py # Capability Detector
│   └── architecture_detector.py # Architecture Detector
├── application/        # Pipeline, Aggregator, Scoring
│   ├── scoring.py       # Scoring Engine
│   └── dna_generator.py # DNA Generator v2
├── adapters/          # AGOS Kernel adapter
└── pipeline/          # Execution pipeline
```

---

## Pipeline

```
1. Fetch      - Clone repository
2. Normalize - Convert to universal format
3. Discover  - Find files and directories
4. Detect    - Run all detectors
5. Extract   - Extract features
6. Analyze   - Aggregate features
7. Score     - Calculate scores
8. Generate  - Create RepositoryDNA v2
```

---

## Detectors (10 Detectors)

### Basic Detectors
| Detector | Description |
|----------|-------------|
| LanguageDetector | Detects programming languages |
| FrameworkDetector | Detects frameworks |
| ConfigurationDetector | Detects config files |
| LicenseDetector | Detects license type |
| ReadmeDetector | Detects documentation |
| DirectoryDetector | Detects directory structure |
| DependencyDetector | Detects package managers |

### Advanced Detectors
| Detector | Description |
|----------|-------------|
| AIStackDetector | Detects AI/ML stack (LangChain, OpenAI, etc.) |
| CapabilityDetector | Detects capabilities (repo analysis, code gen, etc.) |
| ArchitectureDetector | Detects architecture patterns |

---

## Scoring Engine

| Score | Description |
|-------|-------------|
| Architecture Score | Code organization and structure |
| Quality Score | Configuration and dependencies |
| Maintainability Score | Documentation and licensing |
| Documentation Score | README, license, changelog |
| Plugin Readiness | Extensibility indicators |
| Production Readiness | CI/CD, testing, deployment |
| AI Maturity | AI framework usage |
| Capability Coverage | Feature coverage |

---

## DNA v2

```
RepositoryDNA v2 includes:
✅ Identity
✅ Technology Stack
✅ Architecture
✅ Capabilities (with confidence)
✅ AI Stack
✅ Providers
✅ Dependencies
✅ Quality Scores
✅ Production Readiness
✅ Confidence Scores
✅ Evidence References
```

---

## Serialization

```python
dna.to_json()   # JSON output
dna.to_yaml()   # YAML output
```

---

## Rules

```
✅ Evidence Based
✅ No Guessing
✅ No AI
✅ Deterministic
✅ Repeatable
✅ Independent from Kernel
✅ Isolated detectors
```

---

*RIE v2.0.0 - The intelligence layer for AGOS.*
