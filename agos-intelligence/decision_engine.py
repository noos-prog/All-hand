#!/usr/bin/env python3
"""
AGOS Intelligence - Decision Engine
================================

The core decision engine for AGOS Intelligence.
Rules → Knowledge → Evidence → AI → Decision

Every decision is:
- Explainable
- Traceable
- Repeatable
- Auditable
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json


class DecisionType(Enum):
    """Types of decisions."""
    ROUTING = "routing"           # Route to capability/department
    PROVIDER_SELECTION = "provider_selection"  # Select provider
    PRIORITY = "priority"         # Set priority
    APPROVAL = "approval"         # Approve/reject
    RESOURCE_ALLOCATION = "resource_allocation"  # Allocate resources
    STRATEGY = "strategy"         # Strategic decisions


class DecisionConfidence(Enum):
    """Confidence levels."""
    HIGH = "high"      # > 90%
    MEDIUM = "medium"  # 70-90%
    LOW = "low"        # < 70%
    UNCERTAIN = "uncertain"  # < 50%


class DecisionStatus(Enum):
    """Status of a decision."""
    PENDING = "pending"
    DECIDED = "decided"
    EXECUTED = "executed"
    REVERSED = "reversed"
    EXPIRED = "expired"


@dataclass(frozen=True)
class Decision:
    """
    Immutable decision record.
    
    Every decision contains:
    - What was decided
    - Why it was decided
    - What was considered
    - Who made it (human/AI/kernel)
    """
    decision_id: str
    decision_type: DecisionType
    input_data: Tuple[Any, ...]        # What was considered
    output: Any                         # The decision
    reasoning: str                      # Why this decision
    confidence: DecisionConfidence
    timestamp: str
    made_by: str                        # "human", "kernel", "ai"
    status: DecisionStatus
    
    # Evidence chain
    evidence_ids: Tuple[str, ...] = ()
    
    # Alternative options considered
    alternatives_considered: Tuple[str, ...] = ()
    why_not_alternatives: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type.value,
            "input_data": list(self.input_data),
            "output": self.output,
            "reasoning": self.reasoning,
            "confidence": self.confidence.value,
            "timestamp": self.timestamp,
            "made_by": self.made_by,
            "status": self.status.value,
            "evidence_ids": list(self.evidence_ids),
            "alternatives_considered": list(self.alternatives_considered),
            "why_not_alternatives": self.why_not_alternatives,
        }


@dataclass
class DecisionRule:
    """
    A rule that guides decisions.
    
    Rules are the foundation of the decision engine.
    They define how inputs map to outputs.
    """
    rule_id: str
    name: str
    description: str
    decision_type: DecisionType
    
    # Condition function (as string for serialization)
    condition: str  # e.g., "complexity > 5"
    
    # Priority (higher = evaluated first)
    priority: int = 100
    
    # Whether rule is active
    active: bool = True
    
    # Version for tracking changes
    version: str = "1.0"
    
    # Tags for categorization
    tags: Tuple[str, ...] = ()


@dataclass
class Evidence:
    """
    Evidence supporting a decision.
    
    Evidence is immutable once created.
    """
    evidence_id: str
    source: str                          # Where evidence came from
    content: Dict[str, Any]            # The evidence content
    confidence: float                  # Evidence confidence (0-1)
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source": self.source,
            "content": self.content,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class DecisionEngine:
    """
    The core decision engine.
    
    Process:
    1. Collect evidence from knowledge base
    2. Apply rules
    3. Generate decision candidates
    4. Select best decision
    5. Record decision with full trace
    
    Key Principles:
    - Rules come first, AI is last resort
    - Every decision is explainable
    - Every decision is traceable
    - Confidence is always stated
    """
    
    def __init__(self, knowledge_base=None):
        self._knowledge_base = knowledge_base
        self._rules: Dict[str, DecisionRule] = {}
        self._decision_history: Dict[str, Decision] = {}
        self._evidence_store: Dict[str, Evidence] = {}
        self._initialized = False
        
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default decision rules."""
        default_rules = [
            DecisionRule(
                rule_id="rule_priority_high",
                name="High Priority Tasks",
                description="Tasks with high priority get routed first",
                decision_type=DecisionType.ROUTING,
                condition="priority >= 8",
                priority=200,
            ),
            DecisionRule(
                rule_id="rule_simple_task",
                name="Simple Task Routing",
                description="Simple tasks go to instant mode",
                decision_type=DecisionType.ROUTING,
                condition="complexity == 'simple'",
                priority=150,
            ),
            DecisionRule(
                rule_id="rule_production_task",
                name="Production Task Routing",
                description="Production tasks go to engineer mode",
                decision_type=DecisionType.ROUTING,
                condition="complexity == 'complex'",
                priority=180,
            ),
            DecisionRule(
                rule_id="rule_research_task",
                name="Research Task Routing",
                description="Research tasks go to research mode",
                decision_type=DecisionType.ROUTING,
                condition="intent contains 'research'",
                priority=190,
            ),
        ]
        
        for rule in default_rules:
            self._rules[rule.rule_id] = rule
    
    def add_rule(self, rule: DecisionRule) -> None:
        """Add a decision rule."""
        self._rules[rule.rule_id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a decision rule."""
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[DecisionRule]:
        """Get a specific rule."""
        return self._rules.get(rule_id)
    
    def list_rules(self, decision_type: Optional[DecisionType] = None) -> List[DecisionRule]:
        """List all rules, optionally filtered by type."""
        rules = list(self._rules.values())
        
        if decision_type:
            rules = [r for r in rules if r.decision_type == decision_type]
        
        # Sort by priority (higher first)
        rules.sort(key=lambda r: r.priority, reverse=True)
        
        return rules
    
    def add_evidence(self, evidence: Evidence) -> str:
        """Add evidence to the store."""
        self._evidence_store[evidence.evidence_id] = evidence
        return evidence.evidence_id
    
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """Get evidence by ID."""
        return self._evidence_store.get(evidence_id)
    
    def decide(
        self,
        decision_type: DecisionType,
        input_data: Tuple[Any, ...],
        context: Dict[str, Any],
        made_by: str = "kernel"
    ) -> Decision:
        """
        Make a decision.
        
        Args:
            decision_type: Type of decision to make
            input_data: Data to consider
            context: Additional context
            made_by: Who is making the decision
        
        Returns:
            Decision with full trace
        """
        decision_id = self._generate_id("dec")
        
        # STEP 1: Collect evidence
        relevant_evidence = self._collect_evidence(decision_type, input_data, context)
        
        # STEP 2: Apply rules
        rule_matches = self._apply_rules(decision_type, input_data, context)
        
        # STEP 3: Generate candidates
        candidates = self._generate_candidates(
            decision_type, input_data, context, rule_matches, relevant_evidence
        )
        
        # STEP 4: Select best decision
        selected, reasoning, confidence = self._select_best(
            candidates, relevant_evidence
        )
        
        # STEP 5: Create decision record
        decision = Decision(
            decision_id=decision_id,
            decision_type=decision_type,
            input_data=input_data,
            output=selected,
            reasoning=reasoning,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat(),
            made_by=made_by,
            status=DecisionStatus.DECIDED,
            evidence_ids=tuple(e.evidence_id for e in relevant_evidence),
            alternatives_considered=tuple(c.get("reason", "") for c in candidates if c != selected),
        )
        
        # Record decision
        self._decision_history[decision_id] = decision
        
        return decision
    
    def _collect_evidence(
        self,
        decision_type: DecisionType,
        input_data: Tuple[Any, ...],
        context: Dict[str, Any]
    ) -> List[Evidence]:
        """Collect relevant evidence from knowledge base."""
        evidence_list = []
        
        # Query knowledge base if available
        if self._knowledge_base:
            kb_evidence = self._knowledge_base.query(
                topic=context.get("topic", ""),
                limit=5,
            )
            for e in kb_evidence:
                evidence_list.append(e)
        
        # Add contextual evidence
        if context.get("historical_success_rate"):
            evidence = Evidence(
                evidence_id=self._generate_id("ev"),
                source="historical_analysis",
                content={"success_rate": context["historical_success_rate"]},
                confidence=0.85,
                timestamp=datetime.utcnow().isoformat(),
            )
            evidence_list.append(evidence)
        
        return evidence_list
    
    def _apply_rules(
        self,
        decision_type: DecisionType,
        input_data: Tuple[Any, ...],
        context: Dict[str, Any]
    ) -> List[DecisionRule]:
        """Apply rules to get decision candidates."""
        matching_rules = []
        
        rules = self.list_rules(decision_type)
        
        for rule in rules:
            if not rule.active:
                continue
            
            if self._evaluate_condition(rule.condition, input_data, context):
                matching_rules.append(rule)
        
        return matching_rules
    
    def _evaluate_condition(
        self,
        condition: str,
        input_data: Tuple[Any, ...],
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate a rule condition."""
        # Simple condition evaluation
        # In production would use proper expression parser
        
        try:
            # Build evaluation context
            eval_context = {
                "priority": context.get("priority", 0),
                "complexity": context.get("complexity", ""),
                "intent": context.get("intent", ""),
                "input_data": input_data,
            }
            
            # Check for simple conditions
            if "priority >=" in condition:
                threshold = int(condition.split(">=")[1].strip())
                return eval_context.get("priority", 0) >= threshold
            
            if "priority >" in condition:
                threshold = int(condition.split(">")[1].strip())
                return eval_context.get("priority", 0) > threshold
            
            if "complexity ==" in condition:
                value = condition.split("==")[1].strip().strip("'\"")
                return eval_context.get("complexity") == value
            
            if "contains" in condition:
                parts = condition.split("contains")
                field_name = parts[0].strip().replace(".", "")
                value = parts[1].strip().strip("'\"")
                field_value = eval_context.get(field_name, "")
                return value in field_value
            
            return False
            
        except Exception:
            return False
    
    def _generate_candidates(
        self,
        decision_type: DecisionType,
        input_data: Tuple[Any, ...],
        context: Dict[str, Any],
        rule_matches: List[DecisionRule],
        evidence: List[Evidence]
    ) -> List[Dict[str, Any]]:
        """Generate decision candidates from rules and evidence."""
        candidates = []
        
        # Generate from rules
        for rule in rule_matches:
            candidates.append({
                "rule": rule.rule_id,
                "reason": f"Matches rule: {rule.name}",
                "confidence": 0.9,
                "output": self._apply_rule_output(rule, context),
            })
        
        # If no rule candidates, use evidence-based reasoning
        if not candidates and evidence:
            for e in evidence:
                candidates.append({
                    "evidence": e.evidence_id,
                    "reason": f"Based on evidence from {e.source}",
                    "confidence": e.confidence,
                    "output": e.content.get("recommendation", context.get("default")),
                })
        
        # Fallback default
        if not candidates:
            candidates.append({
                "default": True,
                "reason": "Default fallback",
                "confidence": 0.5,
                "output": context.get("default", "instant"),
            })
        
        return candidates
    
    def _apply_rule_output(self, rule: DecisionRule, context: Dict[str, Any]) -> Any:
        """Get output from a matched rule."""
        # Simple output extraction based on rule type
        if rule.decision_type == DecisionType.ROUTING:
            if "simple" in rule.rule_id:
                return "instant"
            elif "complex" in rule.rule_id or "production" in rule.rule_id:
                return "engineer"
            elif "research" in rule.rule_id:
                return "research"
        return context.get("default")
    
    def _select_best(
        self,
        candidates: List[Dict[str, Any]],
        evidence: List[Evidence]
    ) -> Tuple[Any, str, DecisionConfidence]:
        """Select the best candidate based on confidence."""
        if not candidates:
            return None, "No candidates available", DecisionConfidence.UNCERTAIN
        
        # Sort by confidence
        candidates.sort(key=lambda c: c.get("confidence", 0), reverse=True)
        
        best = candidates[0]
        confidence_value = best.get("confidence", 0.5)
        
        # Map confidence value to enum
        if confidence_value >= 0.9:
            confidence = DecisionConfidence.HIGH
        elif confidence_value >= 0.7:
            confidence = DecisionConfidence.MEDIUM
        elif confidence_value >= 0.5:
            confidence = DecisionConfidence.LOW
        else:
            confidence = DecisionConfidence.UNCERTAIN
        
        return best.get("output"), best.get("reason", ""), confidence
    
    def get_decision(self, decision_id: str) -> Optional[Decision]:
        """Get a decision by ID."""
        return self._decision_history.get(decision_id)
    
    def get_decision_history(
        self,
        decision_type: Optional[DecisionType] = None,
        limit: int = 100
    ) -> List[Decision]:
        """Get decision history with optional filtering."""
        history = list(self._decision_history.values())
        
        if decision_type:
            history = [d for d in history if d.decision_type == decision_type]
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda d: d.timestamp, reverse=True)
        
        return history[:limit]
    
    def explain_decision(self, decision_id: str) -> Dict[str, Any]:
        """Get detailed explanation of a decision."""
        decision = self._decision_history.get(decision_id)
        if not decision:
            return {"error": "Decision not found"}
        
        # Build explanation
        explanation = {
            "decision_id": decision.decision_id,
            "what_was_decided": decision.output,
            "why": decision.reasoning,
            "confidence": {
                "level": decision.confidence.value,
                "factors": self._explain_confidence(decision),
            },
            "evidence_used": [
                self._evidence_store.get(eid).__dict__ if self._evidence_store.get(eid) else {"id": eid}
                for eid in decision.evidence_ids
            ],
            "alternatives_considered": list(decision.alternatives_considered),
            "why_not_alternatives": decision.why_not_alternatives,
            "who_decided": decision.made_by,
            "when": decision.timestamp,
        }
        
        return explanation
    
    def _explain_confidence(self, decision: Decision) -> List[str]:
        """Explain factors affecting confidence."""
        factors = []
        
        if len(decision.evidence_ids) > 3:
            factors.append("Multiple evidence sources supported decision")
        
        if len(decision.alternatives_considered) > 0:
            factors.append("Alternatives were compared")
        
        if decision.confidence == DecisionConfidence.HIGH:
            factors.append("High confidence based on rules and evidence")
        elif decision.confidence == DecisionConfidence.MEDIUM:
            factors.append("Moderate confidence - some uncertainty")
        
        return factors
    
    def reverse_decision(self, decision_id: str, reason: str) -> bool:
        """Reverse a previous decision."""
        decision = self._decision_history.get(decision_id)
        if not decision:
            return False
        
        # Create new decision as reversed version
        reversed_decision = Decision(
            decision_id=self._generate_id("dec"),
            decision_type=decision.decision_type,
            input_data=decision.input_data,
            output=None,
            reasoning=f"Reversed: {reason}",
            confidence=DecisionConfidence.UNCERTAIN,
            timestamp=datetime.utcnow().isoformat(),
            made_by="human",
            status=DecisionStatus.REVERSED,
            evidence_ids=decision.evidence_ids,
        )
        
        self._decision_history[reversed_decision.decision_id] = reversed_decision
        return True
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        total_decisions = len(self._decision_history)
        
        by_type = {}
        by_confidence = {}
        by_status = {}
        
        for decision in self._decision_history.values():
            # By type
            dtype = decision.decision_type.value
            by_type[dtype] = by_type.get(dtype, 0) + 1
            
            # By confidence
            conf = decision.confidence.value
            by_confidence[conf] = by_confidence.get(conf, 0) + 1
            
            # By status
            status = decision.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_decisions": total_decisions,
            "total_evidence": len(self._evidence_store),
            "total_rules": len(self._rules),
            "by_type": by_type,
            "by_confidence": by_confidence,
            "by_status": by_status,
        }
