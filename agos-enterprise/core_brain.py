#!/usr/bin/env python3
"""
AGOS Enterprise - Core Brain Module
===================================

The Core Brain acts as the CEO of the enterprise.
It sets strategy, allocates budget, decides priorities,
approves decisions, reviews results, and assigns to departments.

The Core Brain NEVER writes code.
Providers (employees) execute.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json


class BrainDecisionType(Enum):
    """Types of decisions the brain can make."""
    ROUTING = "routing"                 # Route request to department
    PRIORITY = "priority"               # Set execution priority
    RESOURCE = "resource"                # Allocate resources
    STRATEGY = "strategy"               # Strategic decisions
    APPROVAL = "approval"               # Approve or reject


class BrainStrategy(Enum):
    """Strategic approaches."""
    COST_OPTIMIZED = "cost_optimized"
    SPEED_OPTIMIZED = "speed_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    BALANCED = "balanced"


class DecisionConfidence(Enum):
    """Confidence levels for decisions."""
    HIGH = "high"      # > 90%
    MEDIUM = "medium"  # 70-90%
    LOW = "low"        # < 70%


@dataclass(frozen=True)
class BrainDecision:
    """
    Immutable record of a brain decision.
    Every decision is traceable, explainable, and auditable.
    """
    decision_id: str                    # Unique identifier
    decision_type: BrainDecisionType    # Type of decision
    input_data: Tuple[Any, ...]        # What was considered
    output: Any                        # The decision made
    reasoning: str                      # Why this decision was made
    confidence: DecisionConfidence      # Confidence level
    strategy_used: BrainStrategy       # Strategy that guided decision
    timestamp: str                     # When decision was made
    department_id: Optional[str] = None  # Assigned department (if routing)
    priority: int = 1                 # Assigned priority
    estimated_cost: float = 0.0       # Estimated cost
    estimated_duration_ms: int = 0     # Estimated duration
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "decision_type": self.decision_type.value,
            "input_data": self.input_data,
            "output": self.output,
            "reasoning": self.reasoning,
            "confidence": self.confidence.value,
            "strategy_used": self.strategy_used.value,
            "timestamp": self.timestamp,
            "department_id": self.department_id,
            "priority": self.priority,
            "estimated_cost": self.estimated_cost,
            "estimated_duration_ms": self.estimated_duration_ms,
        }


@dataclass
class Strategy:
    """
    Strategic configuration for the core brain.
    """
    strategy_id: str
    name: str
    description: str
    priorities: Dict[str, float]  # Factor -> weight
    cost_weight: float = 0.3
    speed_weight: float = 0.3
    quality_weight: float = 0.4
    max_budget: float = 10000.0
    max_duration_ms: int = 3600000  # 1 hour
    fallback_strategy: Optional[str] = None


class CoreBrain:
    """
    The Core Brain - CEO of the enterprise.
    
    Responsibilities:
    ✓ Sets Strategy
    ✓ Allocates Budget
    ✓ Decides Priorities
    ✓ Approves Decisions
    ✓ Reviews Results
    ✓ Assigns to Departments
    
    NOT Responsible For:
    ✗ Writing Code
    ✗ Running Tests
    ✗ Deploying Systems
    ✗ Writing Documentation
    """
    
    def __init__(self, brain_id: str = "ceo_001"):
        self.brain_id = brain_id
        self.name = "Core Brain"
        self.version = "1.0"
        self._decision_history: List[BrainDecision] = []
        self._strategy = self._default_strategy()
        self._budget_allocations: Dict[str, float] = {}
        self._initialized = True
    
    def _default_strategy(self) -> Strategy:
        """Create default strategy."""
        return Strategy(
            strategy_id="default",
            name="Balanced Default",
            description="Default balanced strategy",
            priorities={"cost": 0.3, "speed": 0.3, "quality": 0.4},
            cost_weight=0.3,
            speed_weight=0.3,
            quality_weight=0.4,
        )
    
    def set_strategy(self, strategy: Strategy) -> None:
        """Set the brain's operating strategy."""
        self._strategy = strategy
        self._record_decision(
            decision_type=BrainDecisionType.STRATEGY,
            input_data=(strategy.strategy_id,),
            output=strategy.name,
            reasoning=f"Strategy changed to {strategy.name}",
            confidence=DecisionConfidence.HIGH,
        )
    
    def route_request(self, request: Dict[str, Any], hierarchy_info: Dict[str, Any]) -> BrainDecision:
        """
        Route a request to the appropriate department.
        
        The brain analyzes the request and decides which department
        should handle it based on:
        - Request type
        - Required capabilities
        - Department availability
        - Budget constraints
        """
        request_type = request.get("type", "unknown")
        required_capability = request.get("capability", "unknown")
        priority_level = request.get("priority", 1)
        
        # Find best matching department
        best_dept = None
        best_score = 0.0
        
        for dept_id, dept_info in hierarchy_info.get("departments", {}).items():
            score = self._calculate_department_score(
                dept_id=dept_id,
                dept_info=dept_info,
                required_capability=required_capability,
            )
            if score > best_score:
                best_score = score
                best_dept = dept_id
        
        # Calculate confidence based on score
        confidence = DecisionConfidence.HIGH if best_score > 0.9 else (
            DecisionConfidence.MEDIUM if best_score > 0.7 else DecisionConfidence.LOW
        )
        
        decision = BrainDecision(
            decision_id=self._generate_id("dec"),
            decision_type=BrainDecisionType.ROUTING,
            input_data=(request_type, required_capability, priority_level),
            output=best_dept or "no_department",
            reasoning=f"Routed to {best_dept} based on capability match and availability",
            confidence=confidence,
            strategy_used=self._strategy.strategy_id,
            timestamp=datetime.utcnow().isoformat(),
            department_id=best_dept,
            priority=priority_level,
        )
        
        self._record_decision(decision)
        return decision
    
    def _calculate_department_score(
        self,
        dept_id: str,
        dept_info: Dict[str, Any],
        required_capability: str,
    ) -> float:
        """Calculate how well a department matches requirements."""
        capabilities = dept_info.get("capabilities", [])
        
        # Check if department has required capability
        if required_capability in capabilities:
            capability_score = 1.0
        else:
            capability_score = 0.3  # Partial match
        
        # Check availability
        availability_score = dept_info.get("availability", 1.0)
        
        # Check budget
        budget_score = 1.0
        if self._budget_allocations.get(dept_id, 0) >= self._strategy.max_budget:
            budget_score = 0.0
        
        # Weighted score
        score = (
            capability_score * 0.5 +
            availability_score * 0.3 +
            budget_score * 0.2
        )
        
        return score
    
    def allocate_budget(self, department_id: str, amount: float) -> BrainDecision:
        """
        Allocate budget to a department.
        
        The brain decides how much budget each department gets
        based on:
        - Strategic priorities
        - Historical usage
        - Current workload
        """
        if amount > self._strategy.max_budget:
            amount = self._strategy.max_budget
        
        previous_budget = self._budget_allocations.get(department_id, 0.0)
        self._budget_allocations[department_id] = amount
        
        decision = BrainDecision(
            decision_id=self._generate_id("dec"),
            decision_type=BrainDecisionType.RESOURCE,
            input_data=(department_id, previous_budget, amount),
            output={"allocated": amount, "previous": previous_budget},
            reasoning=f"Allocated ${amount} to department {department_id}",
            confidence=DecisionConfidence.HIGH,
            strategy_used=self._strategy.strategy_id,
            timestamp=datetime.utcnow().isoformat(),
            department_id=department_id,
            estimated_cost=amount,
        )
        
        self._record_decision(decision)
        return decision
    
    def set_priority(self, task_id: str, priority: int, reason: str) -> BrainDecision:
        """
        Set the priority of a task.
        
        Priority is 1-10, where 1 is highest.
        The brain decides based on:
        - Urgency
        - Importance
        - Dependencies
        """
        priority = max(1, min(10, priority))  # Clamp to 1-10
        
        decision = BrainDecision(
            decision_id=self._generate_id("dec"),
            decision_type=BrainDecisionType.PRIORITY,
            input_data=(task_id, priority),
            output=priority,
            reasoning=reason,
            confidence=DecisionConfidence.MEDIUM,
            strategy_used=self._strategy.strategy_id,
            timestamp=datetime.utcnow().isoformat(),
            priority=priority,
        )
        
        self._record_decision(decision)
        return decision
    
    def approve_request(self, request: Dict[str, Any]) -> Tuple[bool, BrainDecision]:
        """
        Approve or reject a request.
        
        The brain reviews the request and decides whether to approve
        based on:
        - Budget availability
        - Resource availability
        - Strategic alignment
        """
        estimated_cost = request.get("estimated_cost", 0.0)
        department_id = request.get("department_id", "unknown")
        
        # Check budget
        available_budget = self._budget_allocations.get(department_id, 0.0)
        budget_ok = available_budget >= estimated_cost
        
        # Check strategy alignment
        strategy_ok = True  # Simplified
        
        approved = budget_ok and strategy_ok
        
        decision = BrainDecision(
            decision_id=self._generate_id("dec"),
            decision_type=BrainDecisionType.APPROVAL,
            input_data=(request.get("request_id"), estimated_cost),
            output=approved,
            reasoning=(
                f"{'Approved' if approved else 'Rejected'}: "
                f"{'Budget OK' if budget_ok else 'Insufficient budget'}"
            ),
            confidence=DecisionConfidence.HIGH if approved else DecisionConfidence.MEDIUM,
            strategy_used=self._strategy.strategy_id,
            timestamp=datetime.utcnow().isoformat(),
            department_id=department_id,
            estimated_cost=estimated_cost,
        )
        
        self._record_decision(decision)
        return approved, decision
    
    def review_results(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review execution results and provide feedback.
        
        The brain analyzes what happened and decides:
        - If results meet expectations
        - If any follow-up is needed
        - If strategy needs adjustment
        """
        success = execution_result.get("success", False)
        expected_outcome = execution_result.get("expected")
        actual_outcome = execution_result.get("actual")
        
        # Simple review logic
        if success:
            review = {
                "status": "success",
                "outcome": "Results meet expectations",
                "follow_up_required": False,
                "strategy_adjustment": None,
            }
        else:
            review = {
                "status": "failure",
                "outcome": "Results did not meet expectations",
                "follow_up_required": True,
                "strategy_adjustment": "Review allocation strategy",
            }
        
        return review
    
    def _record_decision(
        self,
        decision: BrainDecision = None,
        decision_type: BrainDecisionType = None,
        input_data: Tuple[Any, ...] = None,
        output: Any = None,
        reasoning: str = "",
        confidence: DecisionConfidence = None,
    ) -> None:
        """Record a decision in history."""
        if decision is not None:
            d = decision
        else:
            d = BrainDecision(
                decision_id=self._generate_id("dec"),
                decision_type=decision_type,
                input_data=input_data or (),
                output=output,
                reasoning=reasoning,
                confidence=confidence or DecisionConfidence.MEDIUM,
                strategy_used=self._strategy.strategy_id,
                timestamp=datetime.utcnow().isoformat(),
            )
        
        self._decision_history.append(d)
        
        # Keep only last 1000 decisions
        if len(self._decision_history) > 1000:
            self._decision_history = self._decision_history[-1000:]
    
    def get_decision_history(
        self,
        decision_type: Optional[BrainDecisionType] = None,
        limit: int = 100,
    ) -> List[BrainDecision]:
        """Get decision history with optional filtering."""
        history = self._decision_history
        
        if decision_type:
            history = [d for d in history if d.decision_type == decision_type]
        
        return history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get brain statistics."""
        total_decisions = len(self._decision_history)
        
        by_type = {}
        for decision in self._decision_history:
            dtype = decision.decision_type.value
            by_type[dtype] = by_type.get(dtype, 0) + 1
        
        by_confidence = {}
        for decision in self._decision_history:
            conf = decision.confidence.value
            by_confidence[conf] = by_confidence.get(conf, 0) + 1
        
        return {
            "brain_id": self.brain_id,
            "name": self.name,
            "version": self.version,
            "strategy": self._strategy.name,
            "total_decisions": total_decisions,
            "decisions_by_type": by_type,
            "decisions_by_confidence": by_confidence,
            "budget_allocations": dict(self._budget_allocations),
            "total_budget_allocated": sum(self._budget_allocations.values()),
        }
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"
    
    def compute_hash(self) -> str:
        """Compute deterministic hash."""
        data = {
            "brain_id": self.brain_id,
            "version": self.version,
            "strategy": self._strategy.strategy_id,
            "decisions_count": len(self._decision_history),
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:16]
