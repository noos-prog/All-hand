# ADR-007: LLM is NOT Brain

> **Architecture Decision Record**

---

## Status

**Proposed**: 2024-01-15  
**Status**: Accepted

---

## Context

There is a common misconception that:
- LLM = Brain
- AI Agent = Thinking entity
- Language Model = Reasoning system

This leads to:
- Architectures tightly coupled to specific LLMs
- Difficulty replacing LLMs
- Confusion about responsibilities
- Blurred lines between inference and reasoning

---

## Decision

> **LLM ≠ Brain**

The LLM is NOT the Brain. It is just an **Inference Engine**.

The Brain is the **Reasoning Kernel (ARK)**.

```
LLM = Inference Engine (replaceable)
ARK = Reasoning Kernel (core)
```

---

## Consequences

### Positive

1. **LLM Agnostic** - Can swap LLMs without changing architecture
2. **Clear Responsibilities** - LLM inference vs reasoning are separate
3. **Testability** - Can test reasoning without LLM
4. **Optimizability** - Can improve reasoning independently
5. **Cost Control** - Can choose LLM based on cost/quality needs

### Negative

1. **Additional Complexity** - Need reasoning layer separately
2. **Two Systems** - LLM + ARK must work together
3. **Integration** - Must coordinate inference and reasoning

### Neutral

1. **LLM Selection** - Still need to select good LLM
2. **Prompt Engineering** - Still need to craft prompts

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Autonomous Reasoning Kernel                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Reasoning Layer                                     │ │
│  │  - Goal Analysis                                    │ │
│  │  - Context Fusion                                  │ │
│  │  - Decision Making                                 │ │
│  │  - Planning                                        │ │
│  │  - Self-Correction                                 │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                             │
│  Uses LLM for:                                             │
│  - Text generation                                         │
│  - Code generation                                        │
│  - Analysis                                               │
│  - Reasoning assistance                                    │
│                                                             │
│  But LLM does NOT control:                                │
│  - Strategy decisions                                     │
│  - Provider selection                                     │
│  - Execution flow                                         │
│  - Verification                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Provider (Inference Engine)                 │
│                                                             │
│  Replaceable:                                             │
│  - Claude                                                 │
│  - GPT-4                                                  │
│  - Gemini                                                 │
│  - Local models                                           │
│                                                             │
│  ARK works the same regardless of which LLM is used       │
└─────────────────────────────────────────────────────────────┘
```

---

## LLM Responsibilities

```yaml
LLM Responsibilities:

  ✅ Generate text
  ✅ Generate code
  ✅ Analyze context
  ✅ Answer questions
  ✅ Summarize information
  ✅ Suggest options
  ✅ Assist reasoning
  
  ❌ Control strategy
  ❌ Select providers
  ❌ Make final decisions
  ❌ Execute plans
  ❌ Verify results
```

---

## ARK Responsibilities

```yaml
ARK Responsibilities:

  ✅ Analyze goals
  ✅ Reason about options
  ✅ Make decisions
  ✅ Select capabilities
  ✅ Verify results
  ✅ Learn from outcomes
  ✅ Self-correct
  ✅ Explain decisions
  
  ❌ Generate text directly
  ❌ Execute code
  ❌ Call providers
```

---

## LLM as a Tool

```python
# ARK uses LLM as a tool, not as the brain

class ReasoningKernel:
    """
    The actual brain - ARK.
    """
    
    async def reason_about_goal(self, goal: Goal):
        """
        Reason about a goal using LLM as a tool.
        """
        
        # ARK makes decisions
        analysis = await self.analyze_intent(goal)
        
        # ARK uses LLM to assist
        context_summary = await self.llm.summarize(context)
        
        # But ARK decides
        decision = await self.make_decision(
            analysis=analysis,
            options=await self.generate_options(goal)
        )
        
        # Not LLM
        return decision
```

---

## Why This Matters

### Before ADR-007

```
User: "Build me a website"

System (with LLM as brain):
1. LLM decides: "Use React"
2. LLM decides: "Use OpenHands"
3. LLM executes
4. LLM verifies

Problem:
- If LLM changes, architecture changes
- Can't swap LLM
- No structured reasoning
```

### After ADR-007

```
User: "Build me a website"

ARK:
1. Analyze intent → "Build a website"
2. Generate options → [React, Vue, Angular]
3. Decision matrix → React selected
4. Select capability → "generate_frontend"
5. Select provider → "openhands"
6. Execute
7. Verify
8. Learn

LLM: Just assists, doesn't control
ARK: Makes all decisions
```

---

## LLM Replacement

```yaml
LLM Replacement Process:

1. New LLM available
   → Evaluate quality
   → Benchmark performance
   → Compare cost
   
2. Update configuration
   → Change LLM provider
   → Update API key
   → Adjust prompts if needed
   
3. ARK continues working
   → No architecture changes
   → No reasoning changes
   → Just different inference engine
```

---

## Implementation

```python
class LLMProvider:
    """
    Pluggable LLM interface.
    """
    
    async def generate(self, prompt: str) -> str:
        """Generate text."""
        pass
        
    async def analyze(self, text: str) -> Analysis:
        """Analyze text."""
        pass

# Can plug in different LLMs

class ClaudeProvider(LLMProvider):
    """Claude implementation."""
    
class GPT4Provider(LLMProvider):
    """GPT-4 implementation."""

class LocalProvider(LLMProvider):
    """Local model implementation."""
```

---

## Related ADRs

| ADR | Title | Relationship |
|-----|-------|--------------|
| ADR-001 | Single Core Brain | Foundation |
| ADR-002 | Agents as Tools | Foundation |
| ADR-006 | Everything is Provider | Foundation |
| **ADR-007** | **LLM is NOT Brain** | **This decision** |

---

## References

- [Autonomous Reasoning Kernel](../README.md)
- [Reasoning-Graph.md](../01-Reasoning-Engine/04-Reasoning-Graph.md)
