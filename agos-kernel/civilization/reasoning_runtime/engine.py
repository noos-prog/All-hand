"""
Reasoning Engine
PHASE-02: EXECUTION-000004 - Engineering Reasoning Runtime

Main orchestration engine for engineering reasoning.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from agos_kernel.civilization.reasoning_runtime.decisions import (
    Decision, ExecutionPlan, DecisionType, DecisionConfidence,
    Alternative, DecisionEvidence, DecisionInput
)
from agos_kernel.civilization.reasoning_runtime.runtime import (
    ReasoningSession, ReasoningContext,
    ReasoningPlanner, ReasoningAnalyzer, ReasoningEvaluator,
    ReasoningComparator, ReasoningValidator,
    EvidenceCollector, TraceRecorder
)


class ReasoningEngine:
    """
    Reasoning Engine.
    
    Main orchestrator for engineering reasoning.
    
    Reasoning Rules:
    - Reasoning never performs execution
    - Reasoning never modifies repositories
    - Reasoning never invokes Providers directly
    - Reasoning produces Decisions only
    - Execution consumes Decisions
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.planner = ReasoningPlanner()
        self.analyzer = ReasoningAnalyzer()
        self.evaluator = ReasoningEvaluator()
        self.comparator = ReasoningComparator()
        self.validator = ReasoningValidator()
        self.evidence_collector = EvidenceCollector()
        self.trace_recorder = TraceRecorder()
        
        # Active sessions
        self.sessions: Dict[str, ReasoningSession] = {}
    
    def create_session(
        self,
        mission: Dict,
        engineering_intelligence: Dict,
        policies: List[Dict],
        knowledge_graph: Optional[Dict] = None,
        capability_registry: Optional[Dict] = None,
        provider_registry: Optional[Dict] = None,
        historical_evidence: Optional[List[Dict]] = None,
    ) -> ReasoningSession:
        """Create a new reasoning session."""
        session = ReasoningSession()
        session.initialize(mission, engineering_intelligence, policies)
        
        # Set additional context
        if knowledge_graph:
            session.context.knowledge_graph = knowledge_graph
        if capability_registry:
            session.context.capability_registry = capability_registry
        if provider_registry:
            session.context.provider_registry = provider_registry
        if historical_evidence:
            session.context.historical_evidence = historical_evidence
        
        # Store session
        self.sessions[session.session_id] = session
        
        return session
    
    def reason(self, session: ReasoningSession) -> ExecutionPlan:
        """
        Execute reasoning process.
        
        Takes Engineering Intelligence Package and produces Execution Plan.
        """
        print("=" * 60)
        print("ENGINEERING REASONING ENGINE")
        print("=" * 60)
        print(f"Session: {session.session_id}")
        print(f"Mission: {session.context.mission.get('objective', 'N/A')}")
        print()
        
        # Step 1: Analyze inputs
        print("[1/6] Analyzing inputs...")
        intel_analysis = self.analyzer.analyze_intelligence(
            session.context.engineering_intelligence
        )
        mission_analysis = self.analyzer.analyze_mission(
            session.context.mission
        )
        session.context.memory.set_context('intel_analysis', intel_analysis)
        session.context.memory.set_context('mission_analysis', mission_analysis)
        print(f"  OK Language: {intel_analysis['language']}")
        print(f"  OK Architecture: {intel_analysis['architecture']}")
        
        # Step 2: Select capabilities
        print("[2/6] Selecting capabilities...")
        capability_decision = self._select_capabilities(session)
        session.add_decision(capability_decision)
        print(f"  OK Selected: {capability_decision.selected_alternative}")
        
        # Step 3: Select providers
        print("[3/6] Selecting providers...")
        provider_decision = self._select_providers(session)
        session.add_decision(provider_decision)
        print(f"  OK Selected: {provider_decision.selected_alternative}")
        
        # Step 4: Plan workflow
        print("[4/6] Planning workflow...")
        workflow_decision = self._plan_workflow(session)
        session.add_decision(workflow_decision)
        print(f"  OK Planned: {workflow_decision.selected_alternative}")
        
        # Step 5: Assess risk
        print("[5/6] Assessing risk...")
        risk_decision = self._assess_risk(session)
        session.add_decision(risk_decision)
        print(f"  OK Risk: {risk_decision.selected_alternative}")
        
        # Step 6: Generate execution plan
        print("[6/6] Generating execution plan...")
        execution_plan = self.planner.create_plan(
            session.decisions,
            session.context
        )
        session.complete(execution_plan)
        
        print()
        print("=" * 60)
        print("REASONING COMPLETE")
        print("=" * 60)
        print(f"Decisions made: {len(session.decisions)}")
        print(f"Plan steps: {len(execution_plan.steps)}")
        print(f"Capabilities: {', '.join(execution_plan.capabilities)}")
        print(f"Confidence: {risk_decision.confidence_score:.1f}%")
        print()
        
        return execution_plan
    
    def _select_capabilities(self, session: ReasoningSession) -> Decision:
        """Select appropriate capabilities."""
        decision = Decision(
            type=DecisionType.CAPABILITY_SELECTION,
            title="Select Engineering Capabilities",
            description="Selecting capabilities based on mission and intelligence",
        )
        
        # Get available capabilities
        available = session.context.capability_registry.get('capabilities', [
            {'name': 'RepositoryAnalysis', 'score': 80},
            {'name': 'ArchitectureAnalysis', 'score': 75},
            {'name': 'CodeQualityAnalysis', 'score': 70},
            {'name': 'SecurityAnalysis', 'score': 65},
        ])
        
        # Analyze mission
        mission = session.context.mission
        objective = mission.get('objective', '').lower()
        
        # Create alternatives
        alternatives = []
        for cap in available:
            alt = Alternative(
                id=str(len(alternatives) + 1),
                name=cap['name'],
                description=f"Use {cap['name']} capability",
                score=cap.get('score', 50),
            )
            
            # Add pros/cons based on mission
            if any(kw in objective for kw in ['analyze', 'understand', 'review']):
                if 'analysis' in cap['name'].lower():
                    alt.pros.append("Matches analysis objective")
                    alt.score += 20
            
            alternatives.append(alt)
        
        # Evaluate and select
        alternatives = self.evaluator.evaluate_alternatives(alternatives, {})
        best = self.comparator.select_best(alternatives)
        
        if best:
            decision.selected_alternative = best.name
            decision.selection_reason = f"Highest score ({best.score}) matching mission"
            best.selected = True
        
        decision.alternatives = alternatives
        
        # Calculate confidence
        decision.confidence_score = best.score if best else 50
        decision.confidence_level = self.evaluator.assess_confidence(decision)
        
        # Collect evidence
        decision.evidence = self.evidence_collector.collect_evidence(
            {
                'intelligence': session.context.engineering_intelligence,
                'knowledge_graph': session.context.knowledge_graph,
            },
            DecisionType.CAPABILITY_SELECTION
        )
        
        # Add to decision
        decision.inputs.append(DecisionInput(
            source='mission',
            type='objective',
            data={'objective': mission.get('objective')}
        ))
        
        return decision
    
    def _select_providers(self, session: ReasoningSession) -> Decision:
        """Select appropriate providers."""
        decision = Decision(
            type=DecisionType.PROVIDER_SELECTION,
            title="Select Providers",
            description="Selecting providers based on available capabilities",
        )
        
        # Get available providers
        available = session.context.provider_registry.get('providers', [
            {'name': 'FilesystemProvider', 'score': 90},
            {'name': 'GitProvider', 'score': 85},
            {'name': 'GitHubProvider', 'score': 80},
        ])
        
        # Create alternatives
        alternatives = []
        for prov in available:
            alt = Alternative(
                id=str(len(alternatives) + 1),
                name=prov['name'],
                description=f"Use {prov['name']}",
                score=prov.get('score', 50),
            )
            alternatives.append(alt)
        
        # Select best
        alternatives = self.evaluator.evaluate_alternatives(alternatives, {})
        best = self.comparator.select_best(alternatives)
        
        if best:
            decision.selected_alternative = best.name
            decision.selection_reason = f"Highest score ({best.score})"
            best.selected = True
        
        decision.alternatives = alternatives
        decision.confidence_score = best.score if best else 50
        decision.confidence_level = self.evaluator.assess_confidence(decision)
        
        decision.evidence = self.evidence_collector.collect_evidence(
            {'intelligence': session.context.engineering_intelligence},
            DecisionType.PROVIDER_SELECTION
        )
        
        return decision
    
    def _plan_workflow(self, session: ReasoningSession) -> Decision:
        """Plan the execution workflow."""
        decision = Decision(
            type=DecisionType.WORKFLOW_SELECTION,
            title="Plan Execution Workflow",
            description="Creating workflow based on selected capabilities",
        )
        
        # Analyze what is needed
        intel = session.context.engineering_intelligence
        quality = intel.get('quality_profile', {})
        complexity = quality.get('complexity_score', 50)
        
        # Create workflow alternatives
        alternatives = [
            Alternative(
                id='1',
                name='SequentialWorkflow',
                description='Execute steps sequentially',
                pros=['Simple', 'Easy to debug'],
                cons=['May be slow'],
                score=60 if complexity < 70 else 40,
            ),
            Alternative(
                id='2',
                name='ParallelWorkflow',
                description='Execute independent steps in parallel',
                pros=['Fast', 'Efficient'],
                cons=['More complex'],
                score=70 if complexity < 70 else 50,
            ),
            Alternative(
                id='3',
                name='AdaptiveWorkflow',
                description='Adapt workflow based on results',
                pros=['Flexible', 'Robust'],
                cons=['Most complex'],
                score=80 if complexity >= 70 else 60,
            ),
        ]
        
        # Evaluate
        alternatives = self.evaluator.evaluate_alternatives(alternatives, {})
        best = self.comparator.select_best(alternatives)
        
        if best:
            decision.selected_alternative = best.name
            decision.selection_reason = f"Best match for complexity ({complexity})"
            best.selected = True
        
        decision.alternatives = alternatives
        decision.confidence_score = best.score if best else 50
        decision.confidence_level = self.evaluator.assess_confidence(decision)
        
        return decision
    
    def _assess_risk(self, session: ReasoningSession) -> Decision:
        """Assess execution risk."""
        decision = Decision(
            type=DecisionType.RISK_ASSESSMENT,
            title="Assess Execution Risk",
            description="Evaluating risk factors",
        )
        
        intel = session.context.engineering_intelligence
        security = intel.get('security_profile', {})
        risk_level = security.get('risk_level', 'unknown')
        
        # Map risk levels
        risk_map = {
            'minimal': (10, 'Very Low'),
            'low': (25, 'Low'),
            'medium': (50, 'Medium'),
            'high': (75, 'High'),
            'critical': (90, 'Very High'),
        }
        
        score, level = risk_map.get(risk_level, (50, 'Medium'))
        
        alternatives = [
            Alternative(
                id='1',
                name=f'{level}Risk',
                description=f'Risk level: {risk_level}',
                pros=['Risk assessed'],
                score=100 - score,
            )
        ]
        
        decision.selected_alternative = level
        decision.alternatives = alternatives
        decision.confidence_score = 100 - score
        decision.confidence_level = self.evaluator.assess_confidence(decision)
        
        # Add risk evidence
        decision.evidence.append(DecisionEvidence(
            type='risk_assessment',
            source='security_profile',
            content=f"Risk level: {risk_level}",
            weight=0.9,
        ))
        
        return decision
    
    def validate_plan(self, plan: ExecutionPlan, policies: List[Dict]) -> Dict:
        """Validate execution plan against policies."""
        all_valid = True
        violations = []
        
        for decision in plan.decisions:
            result = self.validator.validate_decision(decision, policies)
            if not result['valid']:
                all_valid = False
                violations.extend(result['violations'])
        
        return {
            'valid': all_valid,
            'violations': violations,
            'validated_decisions': len(plan.decisions),
        }
    
    def export_reasoning_graph(self, session: ReasoningSession) -> Dict:
        """Export reasoning graph."""
        return {
            'session_id': session.session_id,
            'decisions': [d.to_dict() for d in session.decisions],
            'traces': self.trace_recorder.get_traces(session.session_id),
        }
    
    def export_decision_timeline(self, session: ReasoningSession) -> List[Dict]:
        """Export decision timeline."""
        return self.trace_recorder.export_timeline(session.session_id)
    
    def export_decision_evidence(self, session: ReasoningSession) -> Dict:
        """Export decision evidence package."""
        all_evidence = []
        
        for decision in session.decisions:
            all_evidence.extend(decision.evidence)
        
        return {
            'session_id': session.session_id,
            'evidence_count': len(all_evidence),
            'evidence': [e.__dict__ for e in all_evidence],
        }
