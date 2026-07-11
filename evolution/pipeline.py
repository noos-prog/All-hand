"""
Evolution Pipeline Module
========================

Multi-stage evolution pipeline for AGOS self-improvement.
Orchestrates the continuous evolution process across multiple stages.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


class PipelineStageType(Enum):
    """Types of stages in the evolution pipeline."""
    DISCOVERY = "discovery"
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class StageStatus(Enum):
    """Status of a pipeline stage."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    PAUSED = "paused"


@dataclass
class PipelineStage:
    """A single stage in the evolution pipeline."""
    stage_id: str
    name: str
    stage_type: PipelineStageType
    status: StageStatus = StageStatus.PENDING
    dependencies: Set[str] = field(default_factory=set)
    handlers: List[Callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def can_execute(self, completed_stages: Set[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return all(dep in completed_stages for dep in self.dependencies)
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the stage with given context."""
        self.status = StageStatus.RUNNING
        self.started_at = datetime.utcnow()
        
        try:
            result = {"stage_id": self.stage_id, "status": "executed"}
            for handler in self.handlers:
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(context, result)
                else:
                    result = handler(context, result)
            
            self.status = StageStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            return result
        except Exception as e:
            self.status = StageStatus.FAILED
            self.error = str(e)
            raise


@dataclass
class EvolutionResult:
    """Result of an evolution pipeline execution."""
    result_id: str
    pipeline_id: str
    stages_completed: int
    stages_failed: int
    duration_seconds: float
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


class EvolutionPipeline:
    """
    Multi-stage evolution pipeline that orchestrates the self-improvement process.
    
    The pipeline executes stages in dependency order, handling failures
    and providing comprehensive tracking of the evolution process.
    """
    
    def __init__(self, pipeline_id: Optional[str] = None, name: str = "Evolution Pipeline"):
        self.pipeline_id = pipeline_id or f"pipeline_{uuid.uuid4().hex[:8]}"
        self.name = name
        self.stages: Dict[str, PipelineStage] = {}
        self.execution_order: List[str] = []
        self.results: List[EvolutionResult] = []
        self._callbacks: Dict[str, List[Callable]] = {
            "stage_start": [],
            "stage_complete": [],
            "stage_fail": [],
            "pipeline_complete": [],
        }
    
    def add_stage(
        self,
        name: str,
        stage_type: PipelineStageType,
        dependencies: Optional[Set[str]] = None,
        handlers: Optional[List[Callable]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> PipelineStage:
        """Add a new stage to the pipeline."""
        stage = PipelineStage(
            stage_id=f"{self.pipeline_id}_{name.lower().replace(' ', '_')}",
            name=name,
            stage_type=stage_type,
            dependencies=dependencies or set(),
            handlers=handlers or [],
            metadata=metadata or {},
        )
        self.stages[stage.stage_id] = stage
        self._update_execution_order()
        return stage
    
    def _update_execution_order(self) -> None:
        """Topologically sort stages by dependencies."""
        visited = set()
        order = []
        
        def visit(stage_id: str):
            if stage_id in visited:
                return
            visited.add(stage_id)
            stage = self.stages[stage_id]
            for dep in stage.dependencies:
                if dep in self.stages:
                    visit(dep)
            order.append(stage_id)
        
        for stage_id in self.stages:
            visit(stage_id)
        
        self.execution_order = order
    
    def on(self, event: str, callback: Callable) -> None:
        """Register a callback for pipeline events."""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event to all registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception:
                pass
    
    async def execute(self, initial_context: Dict[str, Any]) -> EvolutionResult:
        """Execute the complete pipeline with given context."""
        start_time = datetime.utcnow()
        completed_stages = set()
        stage_results = {}
        errors = []
        
        for stage_id in self.execution_order:
            stage = self.stages[stage_id]
            
            # Wait for dependencies
            if not stage.can_execute(completed_stages):
                stage.status = StageStatus.SKIPPED
                continue
            
            self._emit("stage_start", stage)
            
            try:
                result = await stage.execute(initial_context)
                stage_results[stage_id] = result
                completed_stages.add(stage_id)
                self._emit("stage_complete", stage, result)
            except Exception as e:
                errors.append(f"{stage.name}: {str(e)}")
                self._emit("stage_fail", stage, str(e))
                if not stage.metadata.get("optional", False):
                    break
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        result = EvolutionResult(
            result_id=f"result_{uuid.uuid4().hex[:8]}",
            pipeline_id=self.pipeline_id,
            stages_completed=len([s for s in self.stages.values() if s.status == StageStatus.COMPLETED]),
            stages_failed=len([s for s in self.stages.values() if s.status == StageStatus.FAILED]),
            duration_seconds=duration,
            success=len(errors) == 0,
            data={"stage_results": stage_results, "context": initial_context},
            errors=errors,
        )
        
        self.results.append(result)
        self._emit("pipeline_complete", result)
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "pipeline_id": self.pipeline_id,
            "name": self.name,
            "total_stages": len(self.stages),
            "stages": {
                stage_id: {
                    "name": stage.name,
                    "type": stage.stage_type.value,
                    "status": stage.status.value,
                }
                for stage_id, stage in self.stages.items()
            },
            "execution_order": self.execution_order,
        }


def create_evolution_pipeline(name: str = "Default Evolution") -> EvolutionPipeline:
    """Factory function to create a standard evolution pipeline."""
    pipeline = EvolutionPipeline(name=name)
    
    # Discovery stage
    pipeline.add_stage(
        name="Discovery",
        stage_type=PipelineStageType.DISCOVERY,
        handlers=[lambda ctx, r: {**r, "discovered": True}],
    )
    
    # Analysis stage
    pipeline.add_stage(
        name="Analysis",
        stage_type=PipelineStageType.ANALYSIS,
        dependencies={f"{pipeline.pipeline_id}_discovery"},
        handlers=[lambda ctx, r: {**r, "analyzed": True}],
    )
    
    # Design stage
    pipeline.add_stage(
        name="Design",
        stage_type=PipelineStageType.DESIGN,
        dependencies={f"{pipeline.pipeline_id}_analysis"},
        handlers=[lambda ctx, r: {**r, "designed": True}],
    )
    
    # Implementation stage
    pipeline.add_stage(
        name="Implementation",
        stage_type=PipelineStageType.IMPLEMENTATION,
        dependencies={f"{pipeline.pipeline_id}_design"},
        handlers=[lambda ctx, r: {**r, "implemented": True}],
    )
    
    # Testing stage
    pipeline.add_stage(
        name="Testing",
        stage_type=PipelineStageType.TESTING,
        dependencies={f"{pipeline.pipeline_id}_implementation"},
        handlers=[lambda ctx, r: {**r, "tested": True}],
    )
    
    # Validation stage
    pipeline.add_stage(
        name="Validation",
        stage_type=PipelineStageType.VALIDATION,
        dependencies={f"{pipeline.pipeline_id}_testing"},
        handlers=[lambda ctx, r: {**r, "validated": True}],
    )
    
    # Deployment stage
    pipeline.add_stage(
        name="Deployment",
        stage_type=PipelineStageType.DEPLOYMENT,
        dependencies={f"{pipeline.pipeline_id}_validation"},
        handlers=[lambda ctx, r: {**r, "deployed": True}],
    )
    
    return pipeline
