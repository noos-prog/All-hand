"""
Reasoning Runtime Core
PHASE-02: EXECUTION-000004 - Engineering Reasoning Runtime

Core runtime components for engineering reasoning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict
import uuid

from agos_kernel.civilization.reasoning_runtime.decisions import (
    Decision, ExecutionPlan, DecisionType, DecisionConfidence,
    Alternative, DecisionEvidence, DecisionInput
)


@dataclass
class ReasoningMemory:
    """
    Reasoning Memory - Session Scoped.
    
    Stores reasoning context within a session.
    """
    session_id: str = ""
    decisions: List[Decision] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    traces: List[Dict] = field(default_factory=list)
    
    def add_decision(self, decision: Decision) -> None:
        """Add a decision to memory."""
        self.decisions.append(decision)
    
    def add_trace(self, trace: Dict) -> None:
        """Add a reasoning trace."""
        self.traces.append({
            **trace,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def get_decisions_by_type(self, decision_type: DecisionType) -> List[Decision]:
        """Get decisions by type."""
        return [d for d in self.decisions if d.type == decision_type]
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get context value."""
        return self.context.get(key)
    
    def set_context(self, key: str, value: Any) -> None:
        """Set context value."""
        self.context[key] = value


@dataclass
class ReasoningContext:
    """
    Reasoning Context.
    
    Contains all inputs for a reasoning session.
    """
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Inputs
    mission: Dict = field(default_factory=dict)
    engineering_intelligence: Dict = field(default_factory=dict)
    policies: List[Dict] = field(default_factory=list)
    knowledge_graph: Dict = field(default_factory=dict)
    capability_registry: Dict = field(default_factory=dict)
    provider_registry: Dict = field(default_factory=dict)
    historical_evidence: List[Dict] = field(default_factory=list)
    
    # Session memory
    memory: ReasoningMemory = field(default_factory=ReasoningMemory)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'context_id': self.context_id,
            'timestamp': self.timestamp,
            'mission': self.mission,
            'engineering_intelligence': self.engineering_intelligence,
            'policies': self.policies,
            'knowledge_graph_summary': {
                'nodes': self.knowledge_graph.get('total_nodes', 0),
                'relationships': self.knowledge_graph.get('total_relationships', 0),
            },
            'capability_count': len(self.capability_registry),
            'provider_count': len(self.provider_registry),
            'historical_evidence_count': len(self.historical_evidence),
        }


@dataclass
class ReasoningSession:
    """
    Reasoning Session.
    
    Manages a complete reasoning session from input to decision output.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "initialized"
    
    # Context
    context: Optional[ReasoningContext] = None
    
    # Decisions
    decisions: List[Decision] = field(default_factory=list)
    
    # Output
    execution_plan: Optional[ExecutionPlan] = None
    
    def initialize(self, mission: Dict, intelligence: Dict, policies: List[Dict]) -> None:
        """Initialize session with inputs."""
        self.context = ReasoningContext(
            mission=mission,
            engineering_intelligence=intelligence,
            policies=policies,
            memory=ReasoningMemory(session_id=self.session_id)
        )
        self.status = "ready"
    
    def add_decision(self, decision: Decision) -> None:
        """Add decision to session."""
        decision.reasoning_session_id = self.session_id
        decision.reasoning_context_id = self.context.context_id if self.context else ""
        self.decisions.append(decision)
        
        if self.context:
            self.context.memory.add_decision(decision)
    
    def complete(self, plan: ExecutionPlan) -> None:
        """Complete session with execution plan."""
        self.execution_plan = plan
        self.status = "completed"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'session_id': self.session_id,
            'created_at': self.created_at,
            'status': self.status,
            'context': self.context.to_dict() if self.context else None,
            'decisions_count': len(self.decisions),
            'has_execution_plan': self.execution_plan is not None,
        }


class ReasoningPlanner:
    """
    Reasoning Planner.
    
    Creates execution plans based on decisions.
    """
    
    def create_plan(self, decisions: List[Decision], context: ReasoningContext) -> ExecutionPlan:
        """Create execution plan from decisions."""
        plan = ExecutionPlan()
        
        # Sort decisions by type priority
        priority_order = [
            DecisionType.CAPABILITY_SELECTION,
            DecisionType.PROVIDER_SELECTION,
            DecisionType.WORKFLOW_SELECTION,
            DecisionType.EXECUTION_PLAN,
        ]
        
        sorted_decisions = sorted(
            decisions,
            key=lambda d: priority_order.index(d.type) if d.type in priority_order else 999
        )
        
        # Extract plan components
        for decision in sorted_decisions:
            if decision.selected_alternative:
                # Add step
                plan.steps.append({
                    'decision_id': decision.id,
                    'action': decision.title,
                    'description': decision.description,
                    'selected': decision.selected_alternative,
                    'confidence': decision.confidence_score,
                })
            
            # Extract capabilities
            for alt in decision.alternatives:
                if alt.selected:
                    if 'capability' in alt.name.lower():
                        plan.capabilities.append(alt.name)
                    if 'provider' in alt.name.lower():
                        plan.providers.append(alt.name)
        
        # Add decisions to plan
        plan.decisions = decisions
        
        # Define constraints
        plan.constraints = self._extract_constraints(context)
        
        # Define fallback
        plan.fallback_strategy = "rollback_and_report"
        plan.fallback_steps = [
            {'action': 'rollback', 'description': 'Rollback changes'},
            {'action': 'report', 'description': 'Report failure'},
        ]
        
        # Define success criteria
        plan.success_criteria = self._extract_success_criteria(context)
        
        return plan
    
    def _extract_constraints(self, context: ReasoningContext) -> List[str]:
        """Extract constraints from context."""
        constraints = []
        
        # From policies
        for policy in context.policies:
            if 'constraint' in policy:
                constraints.append(policy['constraint'])
        
        # From intelligence
        intel = context.engineering_intelligence
        if intel.get('security_profile', {}).get('risk_level') == 'high':
            constraints.append("require_security_review")
        
        return constraints
    
    def _extract_success_criteria(self, context: ReasoningContext) -> List[str]:
        """Extract success criteria from context."""
        criteria = []
        
        mission = context.mission
        if mission.get('objective'):
            criteria.append(f"achieve_{mission['objective']}")
        
        criteria.append("all_tests_pass")
        criteria.append("no_policy_violations")
        
        return criteria


class ReasoningAnalyzer:
    """
    Reasoning Analyzer.
    
    Analyzes inputs and extracts insights.
    """
    
    def analyze_intelligence(self, intelligence: Dict) -> Dict:
        """Analyze engineering intelligence."""
        analysis = {
            'language': intelligence.get('identity', {}).get('language', 'Unknown'),
            'architecture': intelligence.get('architecture_summary', {}).get('pattern', 'Unknown'),
            'complexity': intelligence.get('quality_profile', {}).get('complexity_score', 0),
            'security_risk': intelligence.get('security_profile', {}).get('risk_level', 'unknown'),
            'recommendations_count': len(intelligence.get('recommendations', [])),
        }
        
        return analysis
    
    def analyze_mission(self, mission: Dict) -> Dict:
        """Analyze mission."""
        return {
            'objective': mission.get('objective', ''),
            'constraints': mission.get('constraints', []),
            'priority': mission.get('priority', 'medium'),
            'deadline': mission.get('deadline'),
        }


class ReasoningEvaluator:
    """
    Reasoning Evaluator.
    
    Evaluates alternatives and assigns scores.
    """
    
    def evaluate_alternatives(
        self,
        alternatives: List[Alternative],
        criteria: Dict
    ) -> List[Alternative]:
        """Evaluate and score alternatives."""
        for alt in alternatives:
            score = 0.0
            weights = criteria.get('weights', {})
            
            # Score based on pros
            score += len(alt.pros) * weights.get('pros', 1.0)
            
            # Penalty for cons
            score -= len(alt.cons) * weights.get('cons', 0.5)
            
            # Factor in criteria scores
            for key, value in criteria.items():
                if key in alt.name.lower() or key in alt.description.lower():
                    score += value * 0.1
            
            alt.score = min(100, max(0, score))
        
        # Sort by score
        alternatives.sort(key=lambda a: a.score, reverse=True)
        
        # Mark best as selected
        if alternatives:
            alternatives[0].selected = True
        
        return alternatives
    
    def assess_confidence(self, decision: Decision) -> DecisionConfidence:
        """Assess decision confidence."""
        score = decision.confidence_score
        
        if score >= 90:
            return DecisionConfidence.VERY_HIGH
        elif score >= 75:
            return DecisionConfidence.HIGH
        elif score >= 50:
            return DecisionConfidence.MEDIUM
        elif score >= 25:
            return DecisionConfidence.LOW
        else:
            return DecisionConfidence.VERY_LOW


class ReasoningComparator:
    """
    Reasoning Comparator.
    
    Compares options and selects best alternatives.
    """
    
    def select_best(
        self,
        alternatives: List[Alternative],
        criteria: str = "score"
    ) -> Optional[Alternative]:
        """Select best alternative."""
        if not alternatives:
            return None
        
        if criteria == "score":
            return max(alternatives, key=lambda a: a.score)
        elif criteria == "pros":
            return max(alternatives, key=lambda a: len(a.pros) - len(a.cons))
        
        return alternatives[0]


class ReasoningValidator:
    """
    Reasoning Validator.
    
    Validates decisions against policies and constraints.
    """
    
    def validate_decision(
        self,
        decision: Decision,
        policies: List[Dict]
    ) -> Dict:
        """Validate a decision against policies."""
        violations = []
        
        for policy in policies:
            policy_name = policy.get('name', '')
            policy_rules = policy.get('rules', [])
            
            for rule in policy_rules:
                if self._violates_rule(decision, rule):
                    violations.append({
                        'policy': policy_name,
                        'rule': rule,
                        'decision_id': decision.id,
                    })
        
        return {
            'valid': len(violations) == 0,
            'violations': violations,
        }
    
    def _violates_rule(self, decision: Decision, rule: Dict) -> bool:
        """Check if decision violates a rule."""
        rule_type = rule.get('type', '')
        
        if rule_type == 'constraint':
            constraint = rule.get('constraint', '')
            if constraint in decision.description:
                return True
        
        return False


class EvidenceCollector:
    """
    Evidence Collector.
    
    Collects evidence to support decisions.
    """
    
    def collect_evidence(
        self,
        sources: Dict[str, Any],
        decision_type: DecisionType
    ) -> List[DecisionEvidence]:
        """Collect evidence from sources."""
        evidence = []
        
        # From engineering intelligence
        if 'intelligence' in sources:
            intel = sources['intelligence']
            
            if intel.get('dna'):
                evidence.append(DecisionEvidence(
                    type='repository_dna',
                    source='engineering_intelligence',
                    content=str(intel['dna']),
                    weight=0.9,
                ))
            
            if intel.get('trust_score'):
                evidence.append(DecisionEvidence(
                    type='trust_score',
                    source='engineering_intelligence',
                    content=f"Trust Score: {intel['trust_score']}",
                    weight=0.8,
                ))
        
        # From knowledge graph
        if 'knowledge_graph' in sources:
            kg = sources['knowledge_graph']
            
            evidence.append(DecisionEvidence(
                type='graph_statistics',
                source='knowledge_graph',
                content=f"Nodes: {kg.get('total_nodes', 0)}, Edges: {kg.get('total_relationships', 0)}",
                weight=0.7,
            ))
        
        # From historical evidence
        if 'historical' in sources:
            historical = sources['historical']
            
            for item in historical[:5]:  # Limit to 5 most recent
                evidence.append(DecisionEvidence(
                    type='historical',
                    source='history',
                    content=item.get('description', ''),
                    weight=0.5,
                ))
        
        return evidence


class TraceRecorder:
    """
    Trace Recorder.
    
    Records reasoning traces for audit and analysis.
    """
    
    def __init__(self):
        self.traces: List[Dict] = []
    
    def record_step(
        self,
        session_id: str,
        step: str,
        data: Dict
    ) -> None:
        """Record a reasoning step."""
        trace = {
            'session_id': session_id,
            'step': step,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
        }
        self.traces.append(trace)
    
    def get_traces(self, session_id: str) -> List[Dict]:
        """Get traces for a session."""
        return [t for t in self.traces if t.get('session_id') == session_id]
    
    def export_timeline(self, session_id: str) -> List[Dict]:
        """Export reasoning timeline."""
        traces = self.get_traces(session_id)
        
        timeline = []
        for i, trace in enumerate(traces):
            timeline.append({
                'step': i + 1,
                'timestamp': trace['timestamp'],
                'action': trace['step'],
                'summary': self._summarize(trace['data']),
            })
        
        return timeline
    
    def _summarize(self, data: Dict) -> str:
        """Create summary of trace data."""
        if 'decision' in data:
            return f"Decision: {data['decision'].get('title', 'Unknown')}"
        if 'plan' in data:
            return f"Plan created with {len(data['plan'].get('steps', []))} steps"
        return str(data)[:100]


from typing import Optional
