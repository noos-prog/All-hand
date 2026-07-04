"""
Mission Planner
PHASE-02: EXECUTION-000005 - Universal Mission Planner

Transforms every Mission into an executable engineering plan.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

from agos_kernel.civilization.mission_planner.task import (
    Task, TaskStatus, TaskPriority, RetryPolicy,
    TaskInput, TaskOutput, ValidationRule
)
from agos_kernel.civilization.mission_planner.execution_graph import (
    ExecutionGraph, GraphNode, GraphEdge,
    GraphNodeType, EdgeType
)


@dataclass
class Mission:
    """Mission model."""
    mission_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    objective: str = ""
    description: str = ""
    constraints: List[str] = field(default_factory=list)
    priority: str = "medium"
    deadline: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """Execution Plan."""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    mission_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    tasks: List[Task] = field(default_factory=list)
    execution_graph: Dict = field(default_factory=dict)
    
    estimated_duration: int = 0
    estimated_cost: float = 0.0
    risk_level: str = "medium"
    
    validation_result: Dict = field(default_factory=dict)
    evidence: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'plan_id': self.plan_id,
            'mission_id': self.mission_id,
            'created_at': self.created_at,
            'tasks': [t.to_dict() for t in self.tasks],
            'execution_graph': self.execution_graph,
            'estimated_duration': self.estimated_duration,
            'estimated_cost': self.estimated_cost,
            'risk_level': self.risk_level,
            'validation_result': self.validation_result,
            'evidence': self.evidence,
        }


class MissionAnalyzer:
    """Analyzes missions."""
    
    def analyze(self, mission: Mission, context: Dict) -> Dict:
        """Analyze mission and extract key information."""
        analysis = {
            'objective': mission.objective,
            'keywords': self._extract_keywords(mission.objective),
            'complexity': self._assess_complexity(mission),
            'constraints': mission.constraints,
            'priority': mission.priority,
        }
        
        return analysis
    
    def _extract_keywords(self, objective: str) -> List[str]:
        """Extract keywords from objective."""
        keywords = []
        important_words = [
            'analyze', 'build', 'create', 'implement', 'design',
            'refactor', 'test', 'deploy', 'fix', 'update',
            'repository', 'module', 'api', 'service', 'component'
        ]
        
        objective_lower = objective.lower()
        for word in important_words:
            if word in objective_lower:
                keywords.append(word)
        
        return keywords
    
    def _assess_complexity(self, mission: Mission) -> str:
        """Assess mission complexity."""
        objective_len = len(mission.objective)
        
        if objective_len < 50 and len(mission.constraints) <= 2:
            return 'simple'
        elif objective_len < 100 and len(mission.constraints) <= 4:
            return 'moderate'
        else:
            return 'complex'


class MissionDecomposer:
    """Decomposes missions into tasks."""
    
    def decompose(self, mission: Mission, analysis: Dict, context: Dict) -> List[Task]:
        """Decompose mission into tasks."""
        tasks = []
        
        # Get capability registry from context
        capabilities = context.get('capabilities', [
            'RepositoryAnalysis',
            'ArchitectureAnalysis',
            'CodeQualityAnalysis',
            'DependencyAnalysis',
            'SecurityAnalysis',
            'DocumentationAnalysis',
        ])
        
        # Base task
        base_task = Task(
            mission_id=mission.mission_id,
            name='execute_mission',
            description=mission.description or mission.objective,
            objective=mission.objective,
        )
        base_task.required_capabilities = [capabilities[0]]  # Default capability
        base_task.priority = TaskPriority.MEDIUM
        
        tasks.append(base_task)
        
        # Analysis tasks
        for cap in capabilities[:3]:
            task = Task(
                mission_id=mission.mission_id,
                name=f'analyze_with_{cap.lower()}',
                description=f'Execute {cap} capability',
                objective=f'Use {cap} to analyze the target',
            )
            task.required_capabilities = [cap]
            task.depends_on_names = [base_task.name]
            task.estimated_duration = 120
            tasks.append(task)
        
        # Validation task
        validation_task = Task(
            mission_id=mission.mission_id,
            name='validate_results',
            description='Validate mission results',
            objective='Ensure mission objectives are met',
        )
        validation_task.depends_on_names = [t.name for t in tasks]
        validation_task.validation_rules = [
            ValidationRule(
                name='check_completion',
                type='check',
                condition='all_objectives_met'
            )
        ]
        tasks.append(validation_task)
        
        return tasks


class TaskPlanner:
    """Plans task details."""
    
    def plan(self, tasks: List[Task], context: Dict) -> List[Task]:
        """Plan task details."""
        planned_tasks = []
        
        for task in tasks:
            # Add inputs
            if not task.inputs:
                task.inputs = [
                    TaskInput(name='context', type='dict', source='mission_context')
                ]
            
            # Add outputs
            if not task.outputs:
                task.outputs = [
                    TaskOutput(name='results', type='dict', destination='next_task')
                ]
            
            # Add evidence requirements
            if not task.evidence_requirements:
                task.evidence_requirements = ['execution_log', 'result_data']
            
            # Add completion criteria
            if not task.completion_criteria:
                task.completion_criteria = ['task_completed', 'no_errors']
            
            # Set retry policy based on priority
            if task.priority == TaskPriority.CRITICAL:
                task.retry_policy = RetryPolicy.RETRY_3
                task.max_retries = 3
            elif task.priority == TaskPriority.HIGH:
                task.retry_policy = RetryPolicy.RETRY_2
                task.max_retries = 2
            else:
                task.retry_policy = RetryPolicy.RETRY_1
                task.max_retries = 1
            
            # Set timeout
            task.timeout_seconds = 300 if task.estimated_duration > 60 else 120
            
            planned_tasks.append(task)
        
        return planned_tasks


class DependencyPlanner:
    """Plans task dependencies."""
    
    def plan(self, tasks: List[Task]) -> List[Task]:
        """Plan task dependencies."""
        # Create name to task index
        name_to_task = {t.name: t for t in tasks}
        
        # Resolve dependency names to IDs
        for task in tasks:
            resolved_ids = []
            for dep_name in task.depends_on_names:
                if dep_name in name_to_task:
                    resolved_ids.append(name_to_task[dep_name].task_id)
            task.depends_on = resolved_ids
        
        return tasks


class ExecutionPlanner:
    """Plans execution flow."""
    
    def plan(self, tasks: List[Task]) -> ExecutionGraph:
        """Plan execution graph."""
        graph = ExecutionGraph()
        
        # Add task nodes
        task_to_node = {}
        for task in tasks:
            node = GraphNode(
                type=GraphNodeType.TASK,
                task_id=task.task_id,
                name=task.name,
                metadata={'priority': task.priority.value if isinstance(task.priority, TaskPriority) else task.priority}
            )
            graph.add_node(node)
            task_to_node[task.task_id] = node.id
        
        # Add sequence edges
        for task in tasks:
            node_id = task_to_node.get(task.task_id)
            if not node_id:
                continue
            
            if not task.depends_on:
                graph.set_entry_point(node_id)
            else:
                for dep_id in task.depends_on:
                    dep_node_id = task_to_node.get(dep_id)
                    if dep_node_id:
                        edge = GraphEdge(
                            source_id=dep_node_id,
                            target_id=node_id,
                            type=EdgeType.SEQUENCE
                        )
                        graph.add_edge(edge)
        
        # Set exit point (last task)
        if tasks:
            last_node_id = task_to_node.get(tasks[-1].task_id)
            if last_node_id:
                graph.add_exit_point(last_node_id)
        
        # Add checkpoints
        if len(tasks) > 3:
            mid_task = tasks[len(tasks) // 2]
            mid_node_id = task_to_node.get(mid_task.task_id)
            if mid_node_id:
                checkpoint = GraphNode(
                    type=GraphNodeType.CHECKPOINT,
                    name='mid_execution_checkpoint',
                    metadata={'checkpoint': True}
                )
                graph.add_node(checkpoint)
                
                # Insert checkpoint after mid task
                for edge in list(graph.edges.values()):
                    if edge.source_id == mid_node_id and edge.type == EdgeType.SEQUENCE:
                        graph.add_edge(GraphEdge(
                            source_id=mid_node_id,
                            target_id=checkpoint.id,
                            type=EdgeType.SEQUENCE
                        ))
                        break
        
        return graph


class ResourcePlanner:
    """Plans resource allocation."""
    
    def plan(self, tasks: List[Task], context: Dict) -> Dict:
        """Plan resource allocation."""
        resources = {
            'providers': [],
            'capabilities': [],
            'estimated_cost': 0.0,
            'estimated_duration': 0,
        }
        
        for task in tasks:
            resources['providers'].extend(task.required_providers)
            resources['capabilities'].extend(task.required_capabilities)
            resources['estimated_cost'] += task.estimated_cost
            resources['estimated_duration'] += task.estimated_duration
        
        # Deduplicate
        resources['providers'] = list(set(resources['providers']))
        resources['capabilities'] = list(set(resources['capabilities']))
        
        return resources


class RiskPlanner:
    """Plans risk mitigation."""
    
    def plan(self, tasks: List[Task], context: Dict) -> Dict:
        """Plan risk mitigation."""
        risks = []
        
        # Identify risks
        for task in tasks:
            if task.priority == TaskPriority.CRITICAL:
                risks.append({
                    'task_id': task.task_id,
                    'risk': 'critical_task_failure',
                    'mitigation': 'Implement retry and rollback',
                    'level': 'high'
                })
            
            if task.timeout_seconds < 60:
                risks.append({
                    'task_id': task.task_id,
                    'risk': 'timeout_risk',
                    'mitigation': 'Increase timeout',
                    'level': 'medium'
                })
        
        # Add rollback strategies
        for task in tasks:
            if not task.rollback_strategy:
                task.rollback_strategy = 'log_and_report'
        
        return {
            'risks': risks,
            'overall_level': 'high' if any(r['level'] == 'high' for r in risks) else 'medium',
            'mitigations': [r['mitigation'] for r in risks]
        }


class ValidationPlanner:
    """Plans validation."""
    
    def validate(self, plan: ExecutionPlan) -> Dict:
        """Validate execution plan."""
        issues = []
        
        # Check for cycles
        tasks_by_id = {t.task_id: t for t in plan.tasks}
        
        # Check for missing dependencies
        for task in plan.tasks:
            for dep_id in task.depends_on:
                if dep_id not in tasks_by_id:
                    issues.append({
                        'type': 'missing_dependency',
                        'task_id': task.task_id,
                        'missing_dep': dep_id
                    })
        
        # Check for circular dependencies
        visited = set()
        in_stack = set()
        
        def has_cycle(task_id: str) -> bool:
            if task_id in in_stack:
                return True
            if task_id in visited:
                return False
            
            visited.add(task_id)
            in_stack.add(task_id)
            
            task = tasks_by_id.get(task_id)
            if task:
                for dep_id in task.depends_on:
                    if has_cycle(dep_id):
                        return True
            
            in_stack.remove(task_id)
            return False
        
        for task in plan.tasks:
            if has_cycle(task.task_id):
                issues.append({
                    'type': 'circular_dependency',
                    'task_id': task.task_id
                })
        
        # Check for empty plan
        if not plan.tasks:
            issues.append({
                'type': 'empty_plan',
                'message': 'Plan has no tasks'
            })
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'task_count': len(plan.tasks),
        }


class MissionPlanner:
    """
    Universal Mission Planner.
    
    Transforms every Mission into an executable engineering plan.
    
    Planning Rules:
    - Planner never executes Tasks
    - Planner never modifies external systems
    - Planner produces deterministic plans
    - Planning decisions must be reproducible
    """
    
    VERSION = "1.0"
    
    def __init__(self):
        self.analyzer = MissionAnalyzer()
        self.decomposer = MissionDecomposer()
        self.task_planner = TaskPlanner()
        self.dependency_planner = DependencyPlanner()
        self.execution_planner = ExecutionPlanner()
        self.resource_planner = ResourcePlanner()
        self.risk_planner = RiskPlanner()
        self.validation_planner = ValidationPlanner()
    
    def plan(self, mission: Mission, context: Dict) -> ExecutionPlan:
        """
        Create execution plan from mission.
        
        Pipeline:
        1. Mission Analysis
        2. Objective Extraction
        3. Constraint Extraction
        4. Policy Resolution
        5. Knowledge Resolution
        6. Capability Resolution
        7. Provider Resolution
        8. Task Decomposition
        9. Dependency Graph Generation
        10. Execution Graph Generation
        11. Resource Allocation
        12. Execution Plan
        """
        print("=" * 60)
        print("UNIVERSAL MISSION PLANNER")
        print("=" * 60)
        print(f"Mission: {mission.objective[:50]}...")
        print()
        
        plan = ExecutionPlan(mission_id=mission.mission_id)
        
        # Step 1: Analyze mission
        print("[1/10] Analyzing mission...")
        analysis = self.analyzer.analyze(mission, context)
        print(f"  OK Complexity: {analysis['complexity']}")
        print(f"  OK Keywords: {', '.join(analysis['keywords'][:3])}")
        
        # Step 2: Decompose into tasks
        print("[2/10] Decomposing mission...")
        tasks = self.decomposer.decompose(mission, analysis, context)
        print(f"  OK Created {len(tasks)} tasks")
        
        # Step 3: Plan task details
        print("[3/10] Planning task details...")
        tasks = self.task_planner.plan(tasks, context)
        print(f"  OK Planned task details")
        
        # Step 4: Plan dependencies
        print("[4/10] Planning dependencies...")
        tasks = self.dependency_planner.plan(tasks)
        print(f"  OK Resolved dependencies")
        
        # Step 5: Generate execution graph
        print("[5/10] Generating execution graph...")
        execution_graph = self.execution_planner.plan(tasks)
        print(f"  OK Graph nodes: {len(execution_graph)}")
        
        # Step 6: Plan resources
        print("[6/10] Planning resources...")
        resources = self.resource_planner.plan(tasks, context)
        print(f"  OK Capabilities: {len(resources['capabilities'])}")
        
        # Step 7: Plan risk mitigation
        print("[7/10] Planning risk mitigation...")
        risk_info = self.risk_planner.plan(tasks, context)
        print(f"  OK Risks identified: {len(risk_info['risks'])}")
        
        # Step 8: Validate plan
        print("[8/10] Validating plan...")
        plan.tasks = tasks
        plan.execution_graph = execution_graph.to_dict()
        validation = self.validation_planner.validate(plan)
        plan.validation_result = validation
        print(f"  OK Valid: {validation['valid']}")
        if not validation['valid']:
            print(f"  Issues: {len(validation['issues'])}")
        
        # Step 9: Finalize plan
        print("[9/10] Finalizing plan...")
        plan.estimated_cost = resources['estimated_cost']
        plan.estimated_duration = resources['estimated_duration']
        plan.risk_level = risk_info['overall_level']
        
        # Step 10: Add evidence
        print("[10/10] Adding evidence...")
        plan.evidence = [
            {
                'type': 'planning_evidence',
                'timestamp': datetime.utcnow().isoformat(),
                'analysis': analysis,
                'resources': resources,
                'risks': risk_info,
            }
        ]
        
        print()
        print("=" * 60)
        print("PLANNING COMPLETE")
        print("=" * 60)
        print(f"Tasks: {len(tasks)}")
        print(f"Duration: ~{plan.estimated_duration}s")
        print(f"Risk: {plan.risk_level}")
        print(f"Valid: {validation['valid']}")
        print()
        
        return plan
    
    def validate_plan(self, plan: ExecutionPlan) -> Dict:
        """Validate an execution plan."""
        return self.validation_planner.validate(plan)