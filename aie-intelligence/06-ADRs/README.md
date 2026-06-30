# Architecture Decision Records

---

## ADR-AIE-001: LLMs are Sensors, not Brains

**Status**: ACCEPTED

**Context**: Current AI systems treat LLMs as the brain.

**Decision**: LLMs are sensors that provide evidence. The brain is the mathematical engine that processes evidence and decides.

**Consequences**:
- LLM responses become evidence, not decisions
- Multiple LLMs queried for multiple perspectives
- Core Brain processes evidence mathematically
- Models can be swapped without changing decision logic

---

## ADR-AIE-002: No Single Brain

**Status**: ACCEPTED

**Context**: Traditional systems have one monolithic brain.

**Decision**: Core Brain contains 10+ independent engines, all as libraries, none as agents.

**Engines**:
1. Logic Engine - Formal reasoning
2. Planning Engine - Goal decomposition
3. Optimization Engine - Find best solutions
4. Risk Engine - Risk assessment
5. Economics Engine - Cost-benefit analysis
6. Knowledge Engine - Fact management
7. Policy Engine - Rule enforcement
8. Simulation Engine - What-if analysis
9. Verification Engine - Validation
10. Learning Engine - Continuous improvement

---

## ADR-AIE-003: Decision Graphs over Chain of Thought

**Status**: ACCEPTED

**Context**: Chain of Thought is linear and not storable.

**Decision**: All reasoning is stored as Decision Graphs with nodes and edges.

**Benefits**:
- Stored forever
- Fully auditable
- Can compare decisions
- Can improve over time
- Can replay decisions

---

## ADR-AIE-004: Everything is an Object

**Status**: ACCEPTED

**Context**: Systems use natural language internally.

**Decision**: Inside the system, almost everything is an Object, not text.

**Objects**:
- Mission Object
- Capability Object
- Provider Object
- Verification Object
- Decision Object
- Evidence Object
- Graph Object

---

## ADR-AIE-005: Decision Packets

**Status**: ACCEPTED

**Context**: Models are queried individually with simple prompts.

**Decision**: Models are queried with structured Decision Packets containing context, knowledge, options, constraints, risks, and verification criteria.

**Benefits**:
- Consistent queries across models
- Structured evidence collection
- Easier to compare responses
- Better prompt engineering

---

## ADR-AIE-006: Evidence Fusion

**Status**: ACCEPTED

**Context**: Models make decisions independently.

**Decision**: Model responses are converted to evidence and fused into consensus.

**Process**:
1. Query multiple models
2. Convert responses to evidence
3. Fuse evidence into consensus
4. Core Brain decides based on consensus

---

## ADR-AIE-007: Multi-Engine Consensus

**Status**: ACCEPTED

**Context**: Single engine makes all decisions.

**Decision**: Multiple engines analyze questions and consensus mechanism aggregates results.

**Engines**:
- Each engine specializes in one domain
- Each engine contributes perspective
- Consensus mechanism determines final decision
- No single engine dominates

---

## ADR-AIE-008: Verification Before Execution

**Status**: ACCEPTED

**Context**: Systems execute and hope for the best.

**Decision**: Every execution is verified against criteria before, during, and after.

**Verification Stages**:
- Pre-execution: Simulation
- During execution: Monitoring
- Post-execution: Validation

---

## ADR-AIE-009: Math Over Language

**Status**: ACCEPTED

**Context**: Systems rely on LLM reasoning.

**Decision**: Mathematical engines (optimization, simulation, statistics) are primary. LLMs are secondary.

**Priority**:
1. Mathematical calculation
2. Simulation
3. Statistics
4. Knowledge graph
5. LLM reasoning (only for ambiguity)

---

## ADR-AIE-010: Permanent Audit Trail

**Status**: ACCEPTED

**Context**: Decisions are not stored or audited.

**Decision**: Every decision, with full context and reasoning, is stored forever.

**Stored**:
- Decision graphs
- Evidence from models
- Engine results
- Outcomes
- Comparisons

---

## ADR-AIE-011: Self-Improving Architecture

**Status**: ACCEPTED

**Context**: Systems don't learn from decisions.

**Decision**: System continuously learns from decisions and improves.

**Learning Loop**:
1. Make decision
2. Execute
3. Observe outcome
4. Compare prediction vs actual
5. Update models
6. Improve decision process
