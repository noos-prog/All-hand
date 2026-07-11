"""
Policy Engine Module
====================

Universal policy engine for rule-based governance.
Evaluates policies against contexts and generates decisions.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class PolicyDecision(Enum):
    """Policy decision outcomes."""
    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"
    UNKNOWN = "unknown"


@dataclass
class PolicyRule:
    """A single policy rule."""
    rule_id: str
    name: str
    description: str
    condition: Callable[[PolicyContext], bool]
    decision: PolicyDecision
    priority: int = 0
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def evaluate(self, context: PolicyContext) -> bool:
        """Evaluate the rule condition against context."""
        try:
            return self.condition(context)
        except:
            return False


@dataclass
class PolicyContext:
    """Context for policy evaluation."""
    subject: str
    action: str
    resource: str
    environment: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def has_attribute(self, key: str) -> bool:
        return key in self.attributes or key in self.environment
    
    def get_attribute(self, key: str, default: Any = None) -> Any:
        if key in self.attributes:
            return self.attributes[key]
        if key in self.environment:
            return self.environment[key]
        return default


@dataclass
class PolicyResult:
    """Result of policy evaluation."""
    decision: PolicyDecision
    matched_rules: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    conditions_met: Dict[str, bool] = field(default_factory=dict)
    evaluated_at: datetime = field(default_factory=datetime.utcnow)
    evaluation_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_allowed(self) -> bool:
        return self.decision == PolicyDecision.ALLOW
    
    @property
    def is_denied(self) -> bool:
        return self.decision == PolicyDecision.DENY
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "is_allowed": self.is_allowed,
            "is_denied": self.is_denied,
            "matched_rules": self.matched_rules,
            "reasons": self.reasons,
            "evaluated_at": self.evaluated_at.isoformat(),
            "evaluation_time_ms": self.evaluation_time_ms,
        }


@dataclass
class PolicySet:
    """A collection of related policies."""
    policy_set_id: str
    name: str
    description: str
    rules: List[PolicyRule] = field(default_factory=list)
    is_active: bool = True
    combining_algorithm: str = "first_match"
    
    def add_rule(self, rule: PolicyRule) -> None:
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_id: str) -> bool:
        for i, rule in enumerate(self.rules):
            if rule.rule_id == rule_id:
                self.rules.pop(i)
                return True
        return False


class PolicyEngine:
    """
    Universal Policy Engine.
    
    Evaluates policies against contexts and generates
    decisions for authorization, access control, and governance.
    """
    
    def __init__(self):
        self.policy_sets: Dict[str, PolicySet] = {}
        self.default_decision: PolicyDecision = PolicyDecision.UNKNOWN
        self._setup_default_policies()
    
    def _setup_default_policies(self) -> None:
        """Set up default policies."""
        # Create default policy set
        default_set = PolicySet(
            policy_set_id="default",
            name="Default Policies",
            description="Default policy set for the platform",
        )
        
        # Add a default allow rule for authenticated users
        default_set.add_rule(PolicyRule(
            rule_id="auth_user_access",
            name="Authenticated User Access",
            description="Allow access for authenticated users",
            condition=lambda ctx: ctx.attributes.get("authenticated", False),
            decision=PolicyDecision.ALLOW,
            priority=50,
        ))
        
        self.policy_sets["default"] = default_set
    
    def create_policy_set(
        self,
        name: str,
        description: str,
        combining_algorithm: str = "first_match",
    ) -> PolicySet:
        """Create a new policy set."""
        policy_set = PolicySet(
            policy_set_id=str(uuid.uuid4()),
            name=name,
            description=description,
            combining_algorithm=combining_algorithm,
        )
        self.policy_sets[policy_set.policy_set_id] = policy_set
        return policy_set
    
    def get_policy_set(self, policy_set_id: str) -> Optional[PolicySet]:
        """Get a policy set by ID."""
        return self.policy_sets.get(policy_set_id)
    
    def add_rule_to_set(
        self,
        policy_set_id: str,
        rule: PolicyRule,
    ) -> bool:
        """Add a rule to a policy set."""
        policy_set = self.policy_sets.get(policy_set_id)
        if policy_set:
            policy_set.add_rule(rule)
            return True
        return False
    
    def evaluate(self, context: PolicyContext) -> PolicyResult:
        """Evaluate all policies against a context."""
        import time
        start_time = time.time()
        
        matched_rules: List[str] = []
        reasons: List[str] = []
        conditions_met: Dict[str, bool] = {}
        final_decision = self.default_decision
        
        for policy_set in self.policy_sets.values():
            if not policy_set.is_active:
                continue
            
            for rule in policy_set.rules:
                if not rule.is_active:
                    continue
                
                try:
                    condition_met = rule.evaluate(context)
                    conditions_met[rule.rule_id] = condition_met
                    
                    if condition_met:
                        matched_rules.append(rule.rule_id)
                        reasons.append(f"{rule.name}: {rule.description}")
                        
                        if policy_set.combining_algorithm == "first_match":
                            final_decision = rule.decision
                            break
                        elif rule.decision == PolicyDecision.DENY:
                            final_decision = PolicyDecision.DENY
                        elif rule.decision == PolicyDecision.ALLOW and final_decision != PolicyDecision.DENY:
                            final_decision = PolicyDecision.ALLOW
                        elif rule.decision == PolicyDecision.CONDITIONAL:
                            final_decision = PolicyDecision.CONDITIONAL
                
                except Exception:
                    conditions_met[rule.rule_id] = False
        
        evaluation_time = (time.time() - start_time) * 1000
        
        return PolicyResult(
            decision=final_decision,
            matched_rules=matched_rules,
            reasons=reasons,
            conditions_met=conditions_met,
            evaluation_time_ms=evaluation_time,
        )
    
    def authorize(
        self,
        subject: str,
        action: str,
        resource: str,
        **attributes,
    ) -> PolicyResult:
        """Authorize a request."""
        context = PolicyContext(
            subject=subject,
            action=action,
            resource=resource,
            attributes=attributes,
        )
        return self.evaluate(context)
    
    def batch_evaluate(
        self,
        contexts: List[PolicyContext],
    ) -> List[PolicyResult]:
        """Evaluate multiple contexts."""
        return [self.evaluate(ctx) for ctx in contexts]
