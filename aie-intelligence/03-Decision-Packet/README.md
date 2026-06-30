# Decision Packet System

> **Models become Sensors, not Brains.**

---

## The Transformation

```
Traditional Approach:
Claude → Decision
GPT → Decision
Gemini → Decision
Core Brain → Votes

AGOS Approach:
Claude → Evidence
GPT → Evidence
Gemini → Evidence
DeepSeek → Evidence
Core Brain → Compares, Simulates, Calculates, Decides
```

---

## Decision Packet

A Decision Packet is a structured package sent to multiple models.

### Decision Packet Structure

```yaml
DecisionPacket:
  # Metadata
  packet_id: string
  created_at: datetime
  expires_at: datetime
  priority: enum
  
  # Context
  context:
    mission: Mission Object
    history: list[Event]
    current_state: State Object
    
  # Knowledge
  knowledge:
    relevant_facts: list[Fact]
    patterns: list[Pattern]
    evidence: list[Evidence]
    
  # Options
  options:
    - option_id: string
      description: string
      approach: string
      expected_outcome: string
      
  # Constraints
  constraints:
    hard: list[Constraint]
    soft: list[Constraint]
    
  # Risks
  risks:
    identified: list[Risk]
    probabilities: dict[string, float]
    impacts: dict[string, Impact]
    
  # Verification
  verification:
    criteria: list[Criterion]
    expected_metrics: dict[string, Metric]
    
  # Models to query
  models:
    - model_id: "claude"
      prompt: string
    - model_id: "gpt4"
      prompt: string
    - model_id: "gemini"
      prompt: string
    - model_id: "deepseek"
      prompt: string
```

---

## Example Decision Packet

```yaml
DecisionPacket:
  packet_id: "dp_001"
  
  context:
    mission:
      type: "BUILD_API"
      domain: "E-commerce"
      requirements:
        - "REST API"
        - "PostgreSQL"
        - "Authentication"
        
  knowledge:
    relevant_facts:
      - "OpenHands: 95% success rate for APIs"
      - "Aider: 85% success rate for APIs"
      - "Cline: 80% success rate for APIs"
      
  options:
    - option_id: "A"
      description: "Use OpenHands"
      approach: "Single provider"
      
    - option_id: "B"
      description: "Use Aider"
      approach: "Single provider"
      
    - option_id: "C"
      description: "Use OpenHands + Aider"
      approach: "Hybrid"
      
  constraints:
    hard:
      - "Budget < $100"
      - "Time < 1 day"
    soft:
      - "Prefer open-source"
      
  risks:
    identified:
      - "Provider failure"
      - "Quality issues"
      - "Time overrun"
```

---

## Multi-Model Query

```python
class MultiModelQuery:
    """
    Query multiple models and collect evidence.
    """
    
    async def query_models(
        self,
        packet: DecisionPacket
    ) -> list[ModelEvidence]:
        """
        Send packet to multiple models.
        """
        
        results = []
        
        # Query all models in parallel
        tasks = [
            self.query_model(model_id, packet)
            for model_id in packet.models
        ]
        
        raw_results = await asyncio.gather(*tasks)
        
        # Convert to evidence
        for model_id, raw_result in raw_results:
            evidence = self.convert_to_evidence(
                model_id=model_id,
                raw_result=raw_result
            )
            results.append(evidence)
            
        return results
        
    async def query_model(
        self,
        model_id: str,
        packet: DecisionPacket
    ) -> ModelResult:
        """
        Query a specific model.
        """
        
        # Get model configuration
        model_config = self.get_model_config(model_id)
        
        # Build prompt from packet
        prompt = self.build_prompt(packet, model_config)
        
        # Query model
        result = await self.llm.query(
            model=model_config.name,
            prompt=prompt,
            temperature=0.3  # Lower for more consistent results
        )
        
        return ModelResult(
            model_id=model_id,
            raw_response=result,
            latency=result.latency,
            tokens=result.tokens
        )
```

---

## Evidence Collection

```python
class EvidenceCollector:
    """
    Collect and structure evidence from models.
    """
    
    def convert_to_evidence(
        self,
        model_id: str,
        raw_result: ModelResult
    ) -> ModelEvidence:
        """
        Convert model response to structured evidence.
        """
        
        # Parse response
        parsed = self.parse_response(raw_result.raw_response)
        
        # Structure as evidence
        return ModelEvidence(
            model_id=model_id,
            timestamp=raw_result.timestamp,
            
            # What the model said
            recommendation: parsed.recommendation,
            confidence: parsed.confidence,
            
            # Reasoning
            reasoning: parsed.reasoning,
            
            # Options considered
            options_considered: parsed.options,
            
            # Evidence used
            evidence_used: parsed.evidence,
            
            # Risks identified
            risks_identified: parsed.risks,
            
            # Metadata
            latency=raw_result.latency,
            tokens=raw_result.tokens,
            cost=raw_result.cost
        )
```

---

## Evidence Fusion

```python
class EvidenceFusion:
    """
    Fuse evidence from multiple models.
    """
    
    def fuse_evidence(
        self,
        evidence_list: list[ModelEvidence]
    ) -> FusedEvidence:
        """
        Fuse evidence into consensus.
        """
        
        # 1. Extract facts from each model
        all_facts = []
        for evidence in evidence_list:
            facts = self.extract_facts(evidence)
            all_facts.extend(facts)
            
        # 2. Cluster similar facts
        fact_clusters = self.cluster_facts(all_facts)
        
        # 3. Weight by model reliability
        weighted_clusters = self.weight_by_reliability(fact_clusters)
        
        # 4. Build consensus
        consensus_facts = self.build_consensus(weighted_clusters)
        
        # 5. Build conflict list
        conflicts = self.find_conflicts(evidence_list)
        
        return FusedEvidence(
            consensus_facts=consensus_facts,
            conflicts=conflicts,
            confidence=self.calculate_confidence(weighted_clusters),
            model_count=len(evidence_list)
        )
        
    def extract_facts(self, evidence: ModelEvidence) -> list[Fact]:
        """
        Extract factual claims from evidence.
        """
        
        # Use LLM to extract facts
        prompt = f"""
        Extract factual claims from this evidence:
        
        Evidence: {evidence.reasoning}
        
        Return as structured facts.
        """
        
        facts = self.llm.extract(prompt)
        return facts
```

---

## Example: Evidence from 4 Models

```
=== Model Responses ===

Claude:
  "I recommend Option A (OpenHands) because:
   - 95% success rate for APIs
   - Best code quality
   Evidence: 500+ benchmarks"

GPT:
  "I recommend Option C (Hybrid) because:
   - Redundancy is important
   - Better risk management
   Evidence: Industry best practices"

Gemini:
  "I recommend Option A (OpenHands) because:
   - Highest success rate
   - Best for large projects
   Evidence: Internal benchmarks"

DeepSeek:
  "I recommend Option B (Aider) because:
   - Lower cost
   - Good for quick iterations
   Evidence: Cost analysis"

=== Fused Evidence ===

Consensus Facts:
1. "OpenHands has 95% success rate" (3/4 models)
2. "OpenHands has best code quality" (2/4 models)
3. "Aider is cheaper" (2/4 models)
4. "Hybrid provides redundancy" (1/4 models)

Confidence: 0.85

Conflicts:
1. "Which is better for cost?" (Models disagree)

Core Brain Decision:
→ Use OpenHands (evidence-based)
→ But monitor cost closely
→ Have Aider as backup
```

---

## Decision Graph Integration

```
Decision Packet
      │
      ▼
┌─────────────────┐
│  Query Models   │
│  Claude, GPT,   │
│  Gemini, DeepSeek│
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Collect Evidence│
│  Structured     │
│  Responses      │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Fuse Evidence  │
│  Consensus      │
│  Conflicts      │
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Decision Graph │
│  Facts → Decision│
└─────────────────┘
      │
      ▼
┌─────────────────┐
│  Core Brain     │
│  Decide         │
└─────────────────┘
```

---

## Model Roles

```yaml
ModelRoles:
  claude:
    role: "Primary Analyst"
    strength: "Detailed reasoning, code quality"
    
  gpt4:
    role: "Completeness Checker"
    strength: "Thoroughness, edge cases"
    
  gemini:
    role: "Speed Evaluator"
    strength: "Performance, efficiency"
    
  deepseek:
    role: "Cost Analyst"
    strength: "Cost-effectiveness, optimization"
    
  llama:
    role: "Alternative Perspective"
    strength: "Different approaches"
```

---

## Related Documents

- [Multi-Model.md](../05-Multi-Model/README.md)
- [Decision-Graph.md](../02-Decision-Graph/README.md)
