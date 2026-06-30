# Decision Graph

> **Not Chain of Thought. Graph of Decision.**

---

## The Problem with Chain of Thought

```
Chain of Thought:
- Linear
- Sequential
- Not storable
- Not auditable
- Not improvable

Decision Graph:
- Branching
- Parallel
- Storable
- Auditable
- Improvable
```

---

## Decision Graph Structure

```yaml
DecisionGraph:
  graph_id: string
  created_at: datetime
  
  # Nodes
  nodes:
    - id: string
      type: enum
      data: object
      
  # Edges
  edges:
    - from: string
      to: string
      type: string
      
  # Metadata
  metadata:
    mission_id: string
    decision_id: string
    version: string
```

---

## Node Types

```yaml
NodeTypes:
  GOAL:
    description: "What we're trying to achieve"
    data:
      - goal: string
      - criteria: list[string]
      - priority: enum
      
  FACT:
    description: "A verified fact"
    data:
      - fact: string
      - source: string
      - confidence: decimal
      - evidence: list[string]
      
  UNKNOWN:
    description: "Something we don't know"
    data:
      - question: string
      - importance: enum
      - can_research: boolean
      
  ASSUMPTION:
    description: "An assumption we're making"
    data:
      - assumption: string
      - confidence: decimal
      - evidence: list[string]
      - can_verify: boolean
      
  EVIDENCE:
    description: "Supporting evidence"
    data:
      - evidence: string
      - type: enum
      - weight: decimal
      - source: string
      
  OPTION:
    description: "A possible option"
    data:
      - option_id: string
      - description: string
      - pros: list[string]
      - cons: list[string]
      - estimated_cost: decimal
      - estimated_time: duration
      
  SIMULATION:
    description: "Simulation result"
    data:
      - scenario: string
      - outcome: string
      - probability: decimal
      - confidence: decimal
      
  RISK:
    description: "A potential risk"
    data:
      - risk: string
      - probability: decimal
      - impact: enum
      - mitigation: string
      
  COST:
    description: "Cost analysis"
    data:
      - cost_type: string
      - amount: decimal
      - unit: string
      - confidence: decimal
      
  DECISION:
    description: "The final decision"
    data:
      - decision: string
      - reasoning: string
      - confidence: decimal
      - alternatives_considered: list[string]
      
  VERIFICATION:
    description: "Verification results"
    data:
      - criteria: string
      - result: enum
      - evidence: list[string]
```

---

## Example Decision Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                     Decision Graph                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GOAL                                                           │
│  "Build E-commerce API"                                        │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────┐                                                    │
│  │  FACT   │                                                    │
│  │ OpenHands│                                                   │
│  │ 95% API │                                                    │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────┐                                                    │
│  │ UNKNOWN │                                                    │
│  │ Budget? │                                                    │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────┐                                                    │
│  │ASSUMPTION│                                                   │
│  │ "< $100" │                                                   │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│  │ OPTION A│  │ OPTION B│  │ OPTION C│                        │
│  │OpenHands│  │  Aider  │  │  Hybrid │                        │
│  │  $50    │  │  $30    │  │   $80   │                        │
│  └────┬────┘  └────┬────┘  └────┬────┘                        │
│       │            │            │                              │
│       ▼            ▼            ▼                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                        │
│  │SIMULATION│  │SIMULATION│  │SIMULATION│                       │
│  │  95%    │  │   85%   │  │   90%   │                        │
│  │  Safe   │  │ Moderate │  │  Safe   │                        │
│  └────┬────┘  └────┬────┘  └────┬────┘                        │
│       │            │            │                              │
│       ▼            ▼            ▼                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    DECISION                              │   │
│  │  "Use OpenHands (Option A)"                             │   │
│  │  Reasoning: "Best success rate, meets budget"            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   VERIFICATION                            │   │
│  │  "Monitor cost, have Aider as backup"                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Graph Construction

```python
class GraphConstructor:
    """
    Build decision graphs.
    """
    
    async def construct_graph(
        self,
        mission: Mission
    ) -> DecisionGraph:
        """
        Construct a decision graph for a mission.
        """
        
        graph = DecisionGraph(
            graph_id=self.generate_id(),
            mission_id=mission.id
        )
        
        # 1. Add Goal node
        goal_node = self.add_goal_node(graph, mission)
        
        # 2. Gather facts
        facts = await self.gather_facts(mission)
        fact_nodes = self.add_fact_nodes(graph, facts)
        
        # 3. Identify unknowns
        unknowns = await self.identify_unknowns(mission)
        unknown_nodes = self.add_unknown_nodes(graph, unknowns)
        
        # 4. Make assumptions
        assumptions = await self.make_assumptions(mission, unknowns)
        assumption_nodes = self.add_assumption_nodes(graph, assumptions)
        
        # 5. Gather evidence
        evidence = await self.gather_evidence(mission)
        evidence_nodes = self.add_evidence_nodes(graph, evidence)
        
        # 6. Generate options
        options = await self.generate_options(mission, facts)
        option_nodes = self.add_option_nodes(graph, options)
        
        # 7. Run simulations
        for option in options:
            simulation = await self.simulate_option(option)
            self.add_simulation_node(graph, option, simulation)
            
        # 8. Analyze risks
        risks = await self.analyze_risks(options)
        risk_nodes = self.add_risk_nodes(graph, risks)
        
        # 9. Calculate costs
        costs = await self.calculate_costs(options)
        cost_nodes = self.add_cost_nodes(graph, costs)
        
        # 10. Make decision
        decision = await self.make_decision(graph, options)
        decision_node = self.add_decision_node(graph, decision)
        
        # 11. Define verification
        verification = self.define_verification(decision)
        verification_node = self.add_verification_node(graph, verification)
        
        return graph
```

---

## Graph Storage

```yaml
GraphStorage:
  # Decision graphs are stored forever
  
  storage:
    - graph_id: string
      mission_id: string
      created_at: datetime
      version: string
      status: enum
      
  retrieval:
    by_mission: list[Graph]
    by_time_range: list[Graph]
    by_decision_type: list[Graph]
    
  comparison:
    - graph_a: string
      graph_b: string
      similarity: decimal
      
  replay:
    - graph_id: string
      replay_available: boolean
      replay_count: integer
```

---

## Graph Improvement

```python
class GraphImprover:
    """
    Improve decision graphs over time.
    """
    
    async def improve_graph(
        self,
        graph: DecisionGraph
    ) -> ImprovedGraph:
        """
        Improve a decision graph.
        """
        
        # 1. Identify improvement areas
        areas = await self.identify_improvements(graph)
        
        # 2. Add missing facts
        if areas.missing_facts:
            new_facts = await self.gather_missing_facts(areas.missing_facts)
            self.add_facts(graph, new_facts)
            
        # 3. Verify assumptions
        if areas.unverified_assumptions:
            verifications = await self.verify_assumptions(
                areas.unverified_assumptions
            )
            self.update_assumptions(graph, verifications)
            
        # 4. Add more options
        if areas.limited_options:
            new_options = await self.generate_alternatives(
                areas.limited_options
            )
            self.add_options(graph, new_options)
            
        # 5. Update confidence scores
        await self.update_confidence_scores(graph)
        
        return graph
        
    async def learn_from_outcome(
        self,
        graph: DecisionGraph,
        outcome: Outcome
    ):
        """
        Learn from the outcome of a decision.
        """
        
        # Compare predicted vs actual
        comparison = self.compare_prediction_vs_actual(
            graph.decision,
            outcome
        )
        
        # Store learning
        await self.store_learning(
            decision_type=graph.decision.type,
            prediction_accuracy=comparison.accuracy,
            factors=comparison.factors
        )
```

---

## Graph Analytics

```python
class GraphAnalytics:
    """
    Analyze decision graphs for insights.
    """
    
    async def analyze_decision_patterns(
        self,
        graphs: list[DecisionGraph]
    ) -> AnalysisResult:
        """
        Find patterns in decisions.
        """
        
        patterns = {
            "common_facts": self.find_common_facts(graphs),
            "common_assumptions": self.find_common_assumptions(graphs),
            "common_risks": self.find_common_risks(graphs),
            "successful_patterns": self.find_successful_patterns(graphs),
            "failed_patterns": self.find_failed_patterns(graphs),
        }
        
        return AnalysisResult(
            patterns=patterns,
            recommendations=self.generate_recommendations(patterns)
        )
```

---

## Graph Visualization

```yaml
GraphVisualization:
  # Decision graphs can be visualized
  
  formats:
    - mermaid: "For documentation"
    - d3: "For interactive"
    - graphviz: "For static"
    
  views:
    - full: "Show all nodes and edges"
    - summary: "Show only key nodes"
    - timeline: "Show decision sequence"
    - comparison: "Compare two graphs"
```

---

## Comparison: Chain of Thought vs Decision Graph

```
Chain of Thought:
─────────────────────────────────────────────
Think step by step
1. Goal: Build API
2. I need a provider
3. OpenHands is good
4. Let me use OpenHands

Problems:
- Linear
- Can't store
- Can't review
- Can't improve
─────────────────────────────────────────────

Decision Graph:
─────────────────────────────────────────────
GOAL: Build API
  │
  ├── FACT: OpenHands 95% success
  ├── UNKNOWN: Budget?
  ├── ASSUMPTION: < $100
  │
  ├── OPTION A: OpenHands ($50)
  │     └── SIMULATION: 95% success
  │
  ├── OPTION B: Aider ($30)
  │     └── SIMULATION: 85% success
  │
  ├── OPTION C: Hybrid ($80)
  │     └── SIMULATION: 90% success
  │
  └── DECISION: OpenHands
        └── REASONING: Best success rate, within budget

Benefits:
- Stored forever
- Fully auditable
- Can improve over time
- Can compare decisions
─────────────────────────────────────────────
```

---

## Related Documents

- [Core-Engines.md](../01-Core-Engines/README.md)
- [Decision-Packet.md](../03-Decision-Packet/README.md)
