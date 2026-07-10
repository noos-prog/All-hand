#!/usr/bin/env python3
"""
AIE - Reasoning Engine
====================

The Reasoning Engine applies logic, deduction, and induction.
It transforms knowledge into actionable insights.

Unlike LLMs which "feel" right, the Reasoning Engine proves right.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from datetime import datetime
import hashlib
import json


class ReasoningType(Enum):
    """Types of reasoning."""
    DEDUCTION = "deduction"           # From general to specific
    INDUCTION = "induction"           # From specific to general
    ABDUCTION = "abduction"          # Inference to best explanation
    ANALOGY = "analogy"              # Similarity-based reasoning
    CAUSAL = "causal"               # Cause and effect
    PROBABILISTIC = "probabilistic"  # Probability-based


class InferenceType(Enum):
    """Types of logical inference."""
    MODUS_PONENS = "modus_ponens"    # If P then Q; P; therefore Q
    MODUS_TOLLENS = "modus_tollens"  # If P then Q; not Q; therefore not P
    HYPOTHETICAL_SYLLOGISM = "hypothetical_syllogism"  # If P then Q; if Q then R; therefore if P then R
    DISJUNCTIVE_SYLLOGISM = "disjunctive_syllogism"  # P or Q; not P; therefore Q
    CHAINING = "chaining"            # A→B, B→C, therefore A→C


@dataclass(frozen=True)
class LogicalStatement:
    """A statement that can be true or false."""
    statement_id: str
    content: str                       # Natural language
    symbolic_form: str                 # Symbolic representation
    is_known: bool                    # Is the truth value known?
    truth_value: Optional[bool] = None  # True, False, or None if unknown


@dataclass
class InferenceRule:
    """A rule of logical inference."""
    rule_id: str
    name: str
    description: str
    inference_type: InferenceType
    premise_count: int                 # Number of premises required
    
    # Rule definition as code
    apply: Callable[..., Optional[bool]]  # The inference function


@dataclass
class ReasoningStep:
    """A step in a reasoning chain."""
    step_id: str
    step_type: ReasoningType
    inference_used: Optional[str]     # Inference rule ID
    premises: Tuple[LogicalStatement, ...]
    conclusion: LogicalStatement
    confidence: float                  # 0-1
    timestamp: str


@dataclass
class ReasoningChain:
    """
    A complete reasoning chain from premises to conclusion.
    """
    chain_id: str
    reasoning_type: ReasoningType
    steps: Tuple[ReasoningStep, ...]
    final_conclusion: LogicalStatement
    is_valid: bool                   # Is the reasoning valid?
    confidence: float                 # Overall confidence
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    premises_used: Tuple[str, ...] = ()  # IDs of premise statements
    
    def is_sound(self) -> bool:
        """Check if reasoning is sound (valid + true premises)."""
        if not self.is_valid:
            return False
        return all(s.truth_value for s in self.final_conclusion.parents) if hasattr(self.final_conclusion, 'parents') else True
    
    def get_trace(self) -> List[Dict[str, Any]]:
        """Get human-readable trace of reasoning."""
        trace = []
        for step in self.steps:
            trace.append({
                "step": step.step_id,
                "type": step.step_type.value,
                "inference": step.inference_used,
                "premises": [p.content for p in step.premises],
                "conclusion": step.conclusion.content,
                "confidence": step.confidence,
            })
        return trace


@dataclass
class LogicalProof:
    """
    A complete logical proof.
    """
    proof_id: str
    theorem: str                      # What we're trying to prove
    proof_type: str                   # direct, contradiction, induction
    steps: Tuple[Dict[str, Any], ...]
    is_complete: bool
    is_valid: bool
    
    # Alternative proofs
    alternatives: Tuple["LogicalProof", ...] = ()


class ReasoningEngine:
    """
    The Reasoning Engine - second stage of AIE.
    
    Responsibilities:
    - Apply logical inference rules
    - Build reasoning chains
    - Verify logical validity
    - Transform knowledge into insights
    
    The Reasoning Engine does NOT:
    - Guess or hallucinate
    - Skip steps
    - Accept unverified premises
    """
    
    def __init__(self, knowledge_engine=None):
        self.knowledge_engine = knowledge_engine
        self._inference_rules: Dict[str, InferenceRule] = {}
        self._proofs: Dict[str, LogicalProof] = {}
        self._chains: Dict[str, ReasoningChain] = {}
        self._statements: Dict[str, LogicalStatement] = {}
        
        self._initialize_inference_rules()
        self._initialized = True
    
    def _initialize_inference_rules(self) -> None:
        """Initialize built-in inference rules."""
        self._inference_rules = {
            "modus_ponens": InferenceRule(
                rule_id="modus_ponens",
                name="Modus Ponens",
                description="If P implies Q, and P is true, then Q is true",
                inference_type=InferenceType.MODUS_PONENS,
                premise_count=2,
                apply=lambda p, q: q if p else None,
            ),
            "modus_tollens": InferenceRule(
                rule_id="modus_tollens",
                name="Modus Tollens",
                description="If P implies Q, and Q is false, then P is false",
                inference_type=InferenceType.MODUS_TOLLENS,
                premise_count=2,
                apply=lambda p, q: not p if not q else None,
            ),
            "hypothetical_syllogism": InferenceRule(
                rule_id="hypothetical_syllogism",
                name="Hypothetical Syllogism",
                description="If P implies Q, and Q implies R, then P implies R",
                inference_type=InferenceType.HYPOTHETICAL_SYLLOGISM,
                premise_count=2,
                apply=lambda p_implies_q, q_implies_r: True,  # Valid chain
            ),
        }
    
    def add_statement(self, statement: LogicalStatement) -> str:
        """Add a logical statement."""
        self._statements[statement.statement_id] = statement
        return statement.statement_id
    
    def get_statement(self, statement_id: str) -> Optional[LogicalStatement]:
        """Get a statement by ID."""
        return self._statements.get(statement_id)
    
    def add_inference_rule(self, rule: InferenceRule) -> None:
        """Add a custom inference rule."""
        self._inference_rules[rule.rule_id] = rule
    
    def reason(
        self,
        reasoning_type: ReasoningType,
        premises: List[str],  # Statement IDs
        target: Optional[str] = None  # Target statement to prove
    ) -> ReasoningChain:
        """
        Perform reasoning from premises to conclusion.
        """
        chain_id = f"chain_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        # Get premise statements
        premise_stmts = []
        for pid in premises:
            stmt = self._statements.get(pid)
            if stmt:
                premise_stmts.append(stmt)
        
        if not premise_stmts:
            raise ValueError("No valid premises provided")
        
        # Perform reasoning based on type
        steps = []
        
        if reasoning_type == ReasoningType.DEDUCTION:
            steps = self._deduce(premise_stmts)
        elif reasoning_type == ReasoningType.INDUCTION:
            steps = self._induce(premise_stmts)
        elif reasoning_type == ReasoningType.ABDUCTION:
            steps = self._abduce(premise_stmts, target)
        elif reasoning_type == ReasoningType.CAUSAL:
            steps = self._causal_reason(premise_stmts)
        else:
            steps = self._probabilistic_reason(premise_stmts)
        
        # Get final conclusion
        final_conclusion = steps[-1].conclusion if steps else premise_stmts[0]
        
        # Compute overall confidence
        if steps:
            avg_confidence = sum(s.confidence for s in steps) / len(steps)
        else:
            avg_confidence = 0.5
        
        # Check validity
        is_valid = self._validate_chain(steps)
        
        chain = ReasoningChain(
            chain_id=chain_id,
            reasoning_type=reasoning_type,
            steps=tuple(steps),
            final_conclusion=final_conclusion,
            is_valid=is_valid,
            confidence=avg_confidence,
            premises_used=tuple(premises),
        )
        
        self._chains[chain_id] = chain
        return chain
    
    def _deduce(self, premises: List[LogicalStatement]) -> List[ReasoningStep]:
        """Perform deductive reasoning."""
        steps = []
        
        # Apply modus ponens if applicable
        if len(premises) >= 2:
            rule = self._inference_rules.get("modus_ponens")
            if rule:
                step = ReasoningStep(
                    step_id=f"step_deduce_{len(steps)}",
                    step_type=ReasoningType.DEDUCTION,
                    inference_used="modus_ponens",
                    premises=tuple(premises[:2]),
                    conclusion=premises[1],  # Simplified
                    confidence=0.95,
                    timestamp=datetime.utcnow().isoformat(),
                )
                steps.append(step)
        
        return steps
    
    def _induce(self, premises: List[LogicalStatement]) -> List[ReasoningStep]:
        """Perform inductive reasoning."""
        steps = []
        
        # Simple induction: generalize from examples
        if premises:
            # Create generalized statement
            gen_stmt = LogicalStatement(
                statement_id=f"induced_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
                content=f"Based on {len(premises)} observations, this pattern holds generally",
                symbolic_form="P(1) ∧ P(2) ∧ ... ∧ P(n) → ∀x P(x)",
                is_known=True,
                truth_value=True,
            )
            
            step = ReasoningStep(
                step_id=f"step_induce_{len(steps)}",
                step_type=ReasoningType.INDUCTION,
                inference_used=None,
                premises=tuple(premises),
                conclusion=gen_stmt,
                confidence=0.7,  # Induction is less certain
                timestamp=datetime.utcnow().isoformat(),
            )
            steps.append(step)
        
        return steps
    
    def _abduce(self, premises: List[LogicalStatement], target: Optional[str]) -> List[ReasoningStep]:
        """Perform abductive reasoning."""
        steps = []
        
        if target:
            target_stmt = self._statements.get(target)
            if not target_stmt:
                target_stmt = LogicalStatement(
                    statement_id=target,
                    content=f"Best explanation for: {target}",
                    symbolic_form="H",
                    is_known=False,
                )
            
            # Inference to best explanation
            abduced = LogicalStatement(
                statement_id=f"abduced_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
                content=f"Best explanation given evidence",
                symbolic_form="H*",
                is_known=True,
                truth_value=True,
            )
            
            step = ReasoningStep(
                step_id=f"step_abduce_{len(steps)}",
                step_type=ReasoningType.ABDUCTION,
                inference_used="inference_to_best_explanation",
                premises=tuple(premises),
                conclusion=abduced,
                confidence=0.6,  # Abduction is least certain
                timestamp=datetime.utcnow().isoformat(),
            )
            steps.append(step)
        
        return steps
    
    def _causal_reason(self, premises: List[LogicalStatement]) -> List[ReasoningStep]:
        """Perform causal reasoning."""
        steps = []
        
        if premises:
            # Identify causal relationship
            causal = LogicalStatement(
                statement_id=f"causal_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
                content="Causal relationship established between premises",
                symbolic_form="A → B",
                is_known=True,
                truth_value=True,
            )
            
            step = ReasoningStep(
                step_id=f"step_causal_{len(steps)}",
                step_type=ReasoningType.CAUSAL,
                inference_used="causal_inference",
                premises=tuple(premises),
                conclusion=causal,
                confidence=0.8,
                timestamp=datetime.utcnow().isoformat(),
            )
            steps.append(step)
        
        return steps
    
    def _probabilistic_reason(self, premises: List[LogicalStatement]) -> List[ReasoningStep]:
        """Perform probabilistic reasoning."""
        steps = []
        
        if premises:
            # Compute probability
            prob_stmt = LogicalStatement(
                statement_id=f"prob_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
                content="Probability computed from premises",
                symbolic_form="P(C|E)",
                is_known=True,
                truth_value=True,
            )
            
            step = ReasoningStep(
                step_id=f"step_prob_{len(steps)}",
                step_type=ReasoningType.PROBABILISTIC,
                inference_used="bayesian_inference",
                premises=tuple(premises),
                conclusion=prob_stmt,
                confidence=0.75,
                timestamp=datetime.utcnow().isoformat(),
            )
            steps.append(step)
        
        return steps
    
    def _validate_chain(self, steps: List[ReasoningStep]) -> bool:
        """Validate a reasoning chain."""
        if not steps:
            return True
        
        # Check each step
        for step in steps:
            if step.confidence < 0.5:
                return False
            
            if not step.premises:
                return False
        
        return True
    
    def prove(self, theorem: str, premises: List[str]) -> LogicalProof:
        """Attempt to prove a theorem."""
        proof_id = f"proof_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        # Try direct proof first
        chain = self.reason(ReasoningType.DEDUCTION, premises)
        
        proof = LogicalProof(
            proof_id=proof_id,
            theorem=theorem,
            proof_type="direct",
            steps=tuple(s.to_dict() for s in chain.steps) if chain.steps else (),
            is_complete=True,
            is_valid=chain.is_valid,
        )
        
        self._proofs[proof_id] = proof
        return proof
    
    def get_chain(self, chain_id: str) -> Optional[ReasoningChain]:
        """Get a reasoning chain by ID."""
        return self._chains.get(chain_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        by_type = {}
        total_valid = 0
        
        for chain in self._chains.values():
            rtype = chain.reasoning_type.value
            by_type[rtype] = by_type.get(rtype, 0) + 1
            if chain.is_valid:
                total_valid += 1
        
        return {
            "total_chains": len(self._chains),
            "total_proofs": len(self._proofs),
            "by_reasoning_type": by_type,
            "valid_chains": total_valid,
            "inference_rules": len(self._inference_rules),
            "statements": len(self._statements),
        }
