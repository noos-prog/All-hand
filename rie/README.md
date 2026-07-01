# Repository Intelligence Engine (RIE) v1.0.0

> **Analyzes repositories and generates Repository DNA.**

---

## Architecture

```
rie/
├── contracts/        # Domain contracts (RepositoryDNA, DetectorResult)
├── domain/          # Domain models (Repository, FileNode, Feature)
├── infrastructure/  # Git operations, File system
├── detectors/       # Isolated plugin-based detectors
├── application/     # Pipeline, Feature Aggregator
├── adapters/       # AGOS Kernel adapter
└── pipeline/       # Execution pipeline
```

---

## Pipeline

```
1. Fetch      - Clone repository
2. Normalize - Convert to universal format
3. Discover  - Find files and directories
4. Detect    - Run detectors
5. Extract   - Extract features
6. Analyze   - Aggregate features
7. Validate  - Validate results
8. Generate  - Create RepositoryDNA
```

---

## Detectors

| Detector | Description |
|----------|-------------|
| LanguageDetector | Detects programming languages |
| FrameworkDetector | Detects frameworks |
| ConfigurationDetector | Detects config files |
| LicenseDetector | Detects license type |
| ReadmeDetector | Detects documentation |
| DirectoryDetector | Detects directory structure |
| DependencyDetector | Detects package managers |

---

## Rules

```
✅ Independent from Kernel
✅ No direct Kernel access
✅ Isolated detectors
✅ No detector communication
✅ No shared mutable state
✅ Deterministic
✅ Repeatable
✅ No AI
```

---

## Output

RepositoryDNA:
- Languages
- Frameworks
- Dependencies
- Config files
- Directory structure
- License
- Documentation status

---

*RIE - The intelligence layer for AGOS.*
