#!/usr/bin/env python3
"""
ARI - Evaluation Engine
====================

Main evaluation engine for ARI.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import random


class EvaluationStatus(Enum):
    """Evaluation status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    """Task types."""
    CODE_GENERATION = "code_generation"
    CODE_REFACTOR = "code_refactor"
    BUG_FIX = "bug_fix"
    TEST_WRITE = "test_write"
    DOCUMENTATION = "documentation"
    CODE_REVIEW = "code_review"
    ARCHITECTURE_DESIGN = "architecture_design"
    DEPLOYMENT = "deployment"


@dataclass
class EvaluationTask:
    """A task to evaluate."""
    task_id: str
    name: str
    description: str
    task_type: TaskType
    
    # Input
    prompt: str
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Expected output
    expected_output: Optional[Dict[str, Any]] = None
    reference_solution: Optional[str] = None
    
    # Configuration
    timeout_seconds: int = 300
    max_retries: int = 3
    difficulty: str = "medium"
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Tuple[str, ...] = ()
    
    # Capabilities required
    required_capabilities: Tuple[str, ...] = ()


@dataclass
class EvaluationResult:
    """Result of an evaluation."""
    result_id: str
    task_id: str
    provider_id: str
    status: EvaluationStatus
    success: bool
    started_at: str
    output: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: int = 0
    accuracy_score: float = 0.0
    quality_score: float = 0.0
    efficiency_score: float = 0.0
    overall_score: float = 0.0
    tokens_used: int = 0
    cost: float = 0.0
    retries: int = 0
    judgement: Optional[Dict[str, Any]] = None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get result summary."""
        return {
            "result_id": self.result_id,
            "task_id": self.task_id,
            "success": self.success,
            "score": f"{self.overall_score:.1%}",
            "duration": f"{self.duration_ms/1000:.1f}s",
            "cost": f"${self.cost:.4f}",
        }


@dataclass
class EvaluationReport:
    """Report of evaluation run."""
    report_id: str
    provider_id: str
    task_count: int
    passed_count: int
    failed_count: int
    success_rate: float
    avg_score: float
    avg_duration_ms: float
    avg_cost: float
    results: Tuple[EvaluationResult, ...]
    created_at: str


class TaskGenerator:
    """
    Generates evaluation tasks.
    """
    
    def __init__(self):
        self._generators: Dict[TaskType, Callable] = {}
        self._templates: Dict[str, Dict] = {}
    
    def register_generator(
        self,
        task_type: TaskType,
        generator: Callable[[Dict], EvaluationTask]
    ) -> None:
        """Register a task generator."""
        self._generators[task_type] = generator
    
    def generate_task(
        self,
        task_type: TaskType,
        parameters: Dict[str, Any]
    ) -> EvaluationTask:
        """Generate a task."""
        if task_type in self._generators:
            return self._generators[task_type](parameters)
        
        # Default generator
        task_id = f"task_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        return EvaluationTask(
            task_id=task_id,
            name=parameters.get("name", f"Task {task_type.value}"),
            description=parameters.get("description", ""),
            task_type=task_type,
            prompt=parameters.get("prompt", ""),
            context=parameters.get("context", {}),
            difficulty=parameters.get("difficulty", "medium"),
        )
    
    def generate_batch(
        self,
        task_type: TaskType,
        count: int,
        parameters: Dict[str, Any] = None
    ) -> List[EvaluationTask]:
        """Generate a batch of tasks."""
        parameters = parameters or {}
        return [
            self.generate_task(task_type, {**parameters, "index": i})
            for i in range(count)
        ]


class EvaluationEngine:
    """
    Main evaluation engine.
    """
    
    def __init__(self):
        self._executors: Dict[str, Callable] = {}
        self._judges: Dict[str, Callable] = {}
        self._results: Dict[str, EvaluationResult] = {}
        self._task_generator = TaskGenerator()
        self._aggregator = ResultAggregator()
    
    def register_executor(
        self,
        name: str,
        executor: Callable[[EvaluationTask, str], EvaluationResult]
    ) -> None:
        """Register an executor."""
        self._executors[name] = executor
    
    def register_judge(
        self,
        name: str,
        judge: Callable[[EvaluationTask, EvaluationResult], Dict]
    ) -> None:
        """Register a judge."""
        self._judges[name] = judge
    
    def evaluate(
        self,
        task: EvaluationTask,
        provider_id: str,
        executor_name: str = "default",
        judge_name: str = "default"
    ) -> EvaluationResult:
        """Evaluate a provider on a task."""
        result_id = f"eval_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        started_at = datetime.utcnow().isoformat()
        
        result = EvaluationResult(
            result_id=result_id,
            task_id=task.task_id,
            provider_id=provider_id,
            status=EvaluationStatus.RUNNING,
            success=False,
            started_at=started_at,
        )
        
        try:
            # Execute
            if executor_name not in self._executors:
                raise ValueError(f"Unknown executor: {executor_name}")
            
            result = self._executors[executor_name](task, provider_id)
            
            # Judge
            if judge_name in self._judges:
                result.judgement = self._judges[judge_name](task, result)
                if result.judgement:
                    result.overall_score = result.judgement.get("score", 0)
            
            result.status = EvaluationStatus.COMPLETED
            result.success = True
            
        except Exception as e:
            result.status = EvaluationStatus.FAILED
            result.error = str(e)
        
        result.completed_at = datetime.utcnow().isoformat()
        result.duration_ms = int(
            (datetime.fromisoformat(result.completed_at) - datetime.fromisoformat(started_at)).total_seconds() * 1000
        )
        
        self._results[result_id] = result
        return result
    
    def evaluate_batch(
        self,
        tasks: List[EvaluationTask],
        provider_id: str,
        executor_name: str = "default"
    ) -> EvaluationReport:
        """Evaluate a provider on multiple tasks."""
        results = []
        
        for task in tasks:
            result = self.evaluate(task, provider_id, executor_name)
            results.append(result)
        
        passed = sum(1 for r in results if r.success)
        failed = len(results) - passed
        
        report = EvaluationReport(
            report_id=f"report_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            provider_id=provider_id,
            task_count=len(tasks),
            passed_count=passed,
            failed_count=failed,
            success_rate=passed / len(tasks) if tasks else 0,
            avg_score=sum(r.overall_score for r in results) / len(results) if results else 0,
            avg_duration_ms=sum(r.duration_ms for r in results) / len(results) if results else 0,
            avg_cost=sum(r.cost for r in results) / len(results) if results else 0,
            results=tuple(results),
            created_at=datetime.utcnow().isoformat(),
        )
        
        return report
    
    def get_result(self, result_id: str) -> Optional[EvaluationResult]:
        """Get a result by ID."""
        return self._results.get(result_id)
    
    def get_results_by_provider(self, provider_id: str) -> List[EvaluationResult]:
        """Get all results for a provider."""
        return [r for r in self._results.values() if r.provider_id == provider_id]


class ResultAggregator:
    """
    Aggregates evaluation results.
    """
    
    def __init__(self):
        self._reports: Dict[str, EvaluationReport] = {}
    
    def add_report(self, report: EvaluationReport) -> str:
        """Add a report."""
        self._reports[report.report_id] = report
        return report.report_id
    
    def get_report(self, report_id: str) -> Optional[EvaluationReport]:
        """Get a report by ID."""
        return self._reports.get(report_id)
    
    def get_provider_summary(self, provider_id: str) -> Dict[str, Any]:
        """Get summary for a provider."""
        reports = [r for r in self._reports.values() if r.provider_id == provider_id]
        
        if not reports:
            return {"error": "No reports found"}
        
        total_tasks = sum(r.task_count for r in reports)
        total_passed = sum(r.passed_count for r in reports)
        
        return {
            "provider_id": provider_id,
            "report_count": len(reports),
            "total_tasks": total_tasks,
            "total_passed": total_passed,
            "overall_success_rate": total_passed / total_tasks if total_tasks > 0 else 0,
            "avg_score": sum(r.avg_score for r in reports) / len(reports),
            "avg_cost": sum(r.avg_cost for r in reports) / len(reports),
        }
    
    def compare_providers(
        self,
        provider_ids: List[str]
    ) -> Dict[str, Any]:
        """Compare multiple providers."""
        comparison = {}
        
        for pid in provider_ids:
            summary = self.get_provider_summary(pid)
            if "error" not in summary:
                comparison[pid] = summary
        
        # Rank by success rate
        ranked = sorted(
            comparison.items(),
            key=lambda x: x[1]["overall_success_rate"],
            reverse=True
        )
        
        return {
            "rankings": [
                {"provider_id": pid, "success_rate": s["overall_success_rate"]}
                for pid, s in ranked
            ],
            "details": comparison,
        }
