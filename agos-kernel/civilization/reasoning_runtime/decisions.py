"""
Engineering Reasoning Runtime
PHASE-02: EXECUTION-000004 - Engineering Reasoning Runtime

Separates engineering reasoning from engineering execution.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid


class DecisionType(Enum):
    """Types of reasoning decisions."""
    CAPABILITY_SELECTION = "capability_selection"
    PROVIDER_SELECTION = "provider_selection"
    WORKFLOW_SELECTION = "workflow_selection"
    RISK_ASSESSMENT = "risk_assessment"
    CONFIDENCE_ASSESSMENT = "confidence_assessment"
    EXECUTION_PLAN = "execution_plan"
    CONSTRAINT_DEFINITION = "constraint_definition"
    FALLBACK_STRATEGY = "fallback_strategy"
    SUCCESS_CRITERIA = "success_criteria"


class DecisionConfidence(Enum):
    """Decision confidence levels."""
    VERY_HIGH = "very_high"  # 90-100%
    HIGH = "high"            # 75-89%
    MEDIUM = "medium"        # 50-74%
    LOW = "low"             # 25-49%
    VERY_LOW = "very_low"   # 0-24%


@dataclass
class DecisionInput:
    """Input used in a decision."""
    source: str = ""  # engineering_intelligence, mission, policies, etc.
    type: str = ""
    data: Dict = field(default_factory=dict)


@dataclass
class Alternative:
    """Alternative considered in a decision."""
    id: str = ""
    name: str = ""
    description: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    score: float = 0.0
    selected: bool = False


@dataclass
class DecisionEvidence:
    """Evidence supporting a decision."""
    type: str = ""
    source: str = ""
    content: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    weight: float = 1.0  # 0.0 to 1.0


@dataclass
class Decision:
    """
    Engineering Decision.
    
    Every decision must include:
    - Decision Identifier
    - Timestamp
    - Inputs
    - Knowledge Used
    - Policies Applied
    - Alternatives Considered
    - Selected Alternative
    - Confidence
    - Evidence
    - Expected Outcome
    """
    
    # Identification
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: DecisionType = DecisionType.EXECUTION_PLAN
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Description
    title: str = ""
    description: str = ""
    
    # Inputs
    inputs: List[DecisionInput] = field(default_factory=list)
    
    # Reasoning
    knowledge_used: List[str] = field(default_factory=list)
    policies_applied: List[str] = field(default_factory=list)
    
    # Alternatives
    alternatives: List[Alternative] = field(default_factory=list)
    
    # Selection
    selected_alternative: str = ""
    selection_reason: str = ""
    
    # Confidence
    confidence_score: float = 0.0
    confidence_level: DecisionConfidence = DecisionConfidence.MEDIUM
    
    # Evidence
    evidence: List[DecisionEvidence] = field(default_factory=list)
    
    # Outcome
    expected_outcome: str = ""
    
    # Metadata
    reasoning_session_id: str = ""
    reasoning_context_id: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value if isinstance(self.type, DecisionType) else self.type,
            'timestamp': self.timestamp,
            'title': self.title,
            'description': self.description,
            'inputs': [
                {'source': i.source, 'type': i.type, 'data': i.data}
                for i in self.inputs
            ],
            'knowledge_used': self.knowledge_used,
            'policies_applied': self.policies_applied,
            'alternatives': [
                {
                    'id': a.id,
                    'name': a.name,
                    'description': a.description,
                    'pros': a.pros,
                    'cons': a.cons,
                    'score': a.score,
                    'selected': a.selected,
                }
                for a in self.alternatives
            ],
            'selected_alternative': self.selected_alternative,
            'selection_reason': self.selection_reason,
            'confidence_score': self.confidence_score,
            'confidence_level': self.confidence_level.value if isinstance(self.confidence_level, DecisionConfidence) else self.confidence_level,
            'evidence': [
                {
                    'type': e.type,
                    'source': e.source,
                    'content': e.content,
                    'timestamp': e.timestamp,
                    'weight': e.weight,
                }
                for e in self.evidence
            ],
            'expected_outcome': self.expected_outcome,
            'reasoning_session_id': self.reasoning_session_id,
            'reasoning_context_id': self.reasoning_context_id,
        }


@dataclass
class ExecutionPlan:
    """Execution plan generated from decisions."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Plan content
    steps: List[Dict] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    providers: List[str] = field(default_factory=list)
    
    # Constraints
    constraints: List[str] = field(default_factory=list)
    timeout_seconds: int = 300
    
    # Fallback
    fallback_strategy: str = ""
    fallback_steps: List[Dict] = field(default_factory=list)
    
    # Success criteria
    success_criteria: List[str] = field(default_factory=list)
    
    # Decisions
    decisions: List[Decision] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'plan_id': self.plan_id,
            'timestamp': self.timestamp,
            'steps': self.steps,
            'capabilities': self.capabilities,
            'providers': self.providers,
            'constraints': self.constraints,
            'timeout_seconds': self.timeout_seconds,
            'fallback_strategy': self.fallback_strategy,
            'fallback_steps': self.fallback_steps,
            'success_criteria': self.success_criteria,
            'decisions': [d.to_dict() for d in self.decisions],
        }
