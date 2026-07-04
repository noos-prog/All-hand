"""
Universal Policy Runtime
PHASE-02: EXECUTION-000013 - Universal Policy Runtime
Every execution is governed by Policies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class PolicyType(Enum):
    EXECUTION = "execution"
    SECURITY = "security"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"


@dataclass
class Policy:
    policy_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    policy_type: PolicyType = PolicyType.EXECUTION
    version: str = "1.0.0"
    rules: List[Dict] = field(default_factory=list)
    priority: int = 0
    enabled: bool = True
    parent_id: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'policy_id': self.policy_id,
            'name': self.name,
            'description': self.description,
            'policy_type': self.policy_type.value if isinstance(self.policy_type, PolicyType) else self.policy_type,
            'version': self.version,
            'rules': self.rules,
            'priority': self.priority,
            'enabled': self.enabled,
            'parent_id': self.parent_id,
        }


class PolicyRegistry:
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
    
    def register(self, policy: Policy) -> None:
        self.policies[policy.policy_id] = policy
    
    def get(self, policy_id: str) -> Optional[Policy]:
        return self.policies.get(policy_id)
    
    def get_by_type(self, ptype: PolicyType) -> List[Policy]:
        return [p for p in self.policies.values() if p.policy_type == ptype and p.enabled]


class PolicyEvaluator:
    def evaluate(self, policy: Policy, context: Dict) -> Dict:
        results = []
        for rule in policy.rules:
            results.append({'rule': rule.get('name'), 'passed': True})
        return {'policy_id': policy.policy_id, 'passed': True, 'results': results}


class PolicyRuntime:
    VERSION = "1.0"
    
    def __init__(self):
        self.registry = PolicyRegistry()
        self.evaluator = PolicyEvaluator()
    
    def create_policy(self, name: str, ptype: PolicyType, rules: List[Dict]) -> Policy:
        policy = Policy(name=name, policy_type=ptype, rules=rules)
        self.registry.register(policy)
        return policy
    
    def evaluate_policies(self, ptype: PolicyType, context: Dict) -> List[Dict]:
        policies = self.registry.get_by_type(ptype)
        return [self.evaluator.evaluate(p, context) for p in policies]
    
    def get_governance_report(self) -> Dict:
        return {
            'total_policies': len(self.registry.policies),
            'by_type': {t.value: len(self.registry.get_by_type(t)) for t in PolicyType}
        }