# CGP: Capability Genome Project

> **From Repository DNA to Capability DNA**

---

## Implementation

```
cgp-genome/
├── __init__.py                    # Main exports
├── test_cgp.py                    # Test suite
│
├── S1_Skills/
│   ├── __init__.py
│   └── primitive.py               # Primitive skills (34 skills)
│
├── S2_Capabilities/
│   ├── __init__.py
│   └── composer.py                # Capability composer
│
├── S3_Services/
│   ├── __init__.py
│   └── aggregator.py              # Service aggregator
│
├── S4_Departments/
│   ├── __init__.py
│   └── organizer.py               # Department organizer
│
├── S5_Missions/
│   ├── __init__.py
│   └── builder.py                # Mission builder
│
├── S6_Capability_Graph/
│   ├── __init__.py
│   └── analyzer.py               # Genome analyzer
│
├── S7_Reuse/
│   ├── __init__.py
│   └── engine.py                 # Reuse engine
│
├── S8_Overlap/
│   ├── __init__.py
│   └── overlap_analyzer.py       # Overlap analyzer
│
├── S9_Evolution/
│   ├── __init__.py
│   └── tracker.py                # Evolution tracker
│
├── S10_Marketplace/
│   ├── __init__.py
│   └── marketplace.py            # Capability marketplace
│
└── README.md
```

---

## Quick Start

```python
# Skills
from cgp_genome import SkillRegistry, Skill
registry = SkillRegistry()
skill = registry.get("read_file")

# Capabilities
from cgp_genome import CapabilityComposer, CapabilityRegistry
composer = CapabilityComposer()
capability = composer.compose("code_gen", "Code Generation", ...)

# Services
from cgp_genome import ServiceAggregator
service = aggregator.aggregate("backend", "Backend Dev", ...)

# Departments
from cgp_genome import DepartmentOrganizer
dept = organizer.organize("qa", "QA Department", ...)

# Missions
from cgp_genome import MissionBuilder
mission = builder.build("build_saas", "Build SaaS", ...)

# Genome
from cgp_genome import GenomeGenerator
genome = generator.generate(project_id, name, skills, caps)

# Reuse
from cgp_genome import ReuseEngine
engine = ReuseEngine()
engine.record_usage("openhands", "code_generation")

# Overlap
from cgp_genome import OverlapAnalyzer
analyzer = OverlapAnalyzer()
overlap = analyzer.analyze_pair("openhands", "goose")

# Evolution
from cgp_genome import EvolutionTracker
tracker = EvolutionTracker()
tracker.record_event(event)

# Marketplace
from cgp_genome import Marketplace
marketplace = Marketplace()
marketplace.publish(listing)
```

---

## Hierarchy

```
MISSION
   │
   ▼
DEPARTMENT
   │
   ▼
SERVICE
   │
   ▼
CAPABILITY
   │
   ▼
SKILL
   │
   ▼
PRIMITIVE
```

---

## Core Components

| Component | Module | Description |
|-----------|--------|-------------|
| Skills | S1_Skills | 34 primitive skills |
| Capabilities | S2_Capabilities | Composed from skills |
| Services | S3_Services | Aggregated capabilities |
| Departments | S4_Departments | Organized services |
| Missions | S5_Missions | Full projects |
| Genome | S6_Capability_Graph | Complete analysis |
| Reuse | S7_Reuse | Reuse analysis |
| Overlap | S8_Overlap | Project overlap |
| Evolution | S9_Evolution | Trend tracking |
| Marketplace | S10_Marketplace | Capability marketplace |

---

## Running Tests

```bash
cd cgp-genome
python test_cgp.py
```

---

## Implementation Files

| File | Lines | Description |
|------|-------|-------------|
| `primitive.py` | 300+ | 34 primitive skills |
| `composer.py` | 300+ | Capability composer |
| `aggregator.py` | 200+ | Service aggregator |
| `organizer.py` | 200+ | Department organizer |
| `builder.py` | 200+ | Mission builder |
| `analyzer.py` | 250+ | Genome analyzer |
| `engine.py` | 200+ | Reuse engine |
| `overlap_analyzer.py` | 200+ | Overlap analyzer |
| `tracker.py` | 200+ | Evolution tracker |
| `marketplace.py` | 200+ | Marketplace |

**Total: 2,000+ lines of production code**

---

*From Repository DNA to Capability DNA.*
*From Features to Capabilities.*
*From Analysis to Intelligence.*
