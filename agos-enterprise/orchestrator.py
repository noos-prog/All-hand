#!/usr/bin/env python3
"""
AGOS Enterprise - Enterprise Orchestrator Module
=================================================

The Enterprise Orchestrator connects all components:
- Core Brain (CEO) - Makes strategic decisions
- Hierarchy - Provides structure
- Providers - Execute work
- Marketplace - Discovers capabilities

The orchestrator implements the canonical flow:
1. INTENT → User/system expresses intent
2. PARSE → Brain parses and validates intent
3. PLAN → Brain creates execution plan
4. VALIDATE → Governance validates plan
5. ROUTE → Brain routes to department
6. EXECUTE → Providers execute
7. OBSERVE → All actions produce events
8. LOG → All results logged
9. RESULT → Brain returns result
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import hashlib
import json
import uuid


class ExecutionState(Enum):
    """State of execution flow."""
    IDLE = "idle"
    PARSING = "parsing"
    PLANNING = "planning"
    VALIDATING = "validating"
    ROUTING = "routing"
    EXECUTING = "executing"
    OBSERVING = "observing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionPriority(Enum):
    """Priority levels for execution."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class ExecutionEvent:
    """An event in the execution flow."""
    event_id: str
    event_type: str
    state: ExecutionState
    timestamp: str
    data: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "state": self.state.value,
            "timestamp": self.timestamp,
            "data": self.data,
        }


@dataclass
class ExecutionRequest:
    """A request for execution."""
    request_id: str
    intent: str                          # Natural language intent
    context: Dict[str, Any]             # Additional context
    priority: ExecutionPriority = ExecutionPriority.NORMAL
    deadline: Optional[datetime] = None
    user_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = str(uuid.uuid4())


@dataclass
class ExecutionPlan:
    """A plan for executing a request."""
    plan_id: str
    request_id: str
    department_id: Optional[str] = None
    service_id: Optional[str] = None
    capability_id: Optional[str] = None
    steps: Tuple[Dict[str, Any], ...] = ()
    estimated_duration_ms: int = 0
    estimated_cost: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ExecutionResult:
    """Result of an execution."""
    execution_id: str
    request_id: str
    success: bool
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    events: Tuple[ExecutionEvent, ...] = ()
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: int = 0
    cost: float = 0.0


class EnterpriseOrchestrator:
    """
    The Enterprise Orchestrator.
    
    Implements the canonical execution flow:
    1. Receives intent from user/system
    2. Parses intent using Core Brain
    3. Creates execution plan
    4. Validates plan with governance
    5. Routes to appropriate department
    6. Coordinates provider execution
    7. Observes and logs all actions
    8. Returns results
    
    The orchestrator NEVER executes skills directly.
    Providers execute.
    """
    
    def __init__(self, core_brain=None, hierarchy=None, provider_pool=None, marketplace=None):
        self.core_brain = core_brain
        self.hierarchy = hierarchy
        self.provider_pool = provider_pool
        self.marketplace = marketplace
        
        self._executions: Dict[str, Dict[str, Any]] = {}
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._metrics: Dict[str, int] = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
        }
    
    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """
        Execute a request through the canonical flow.
        """
        self._metrics["total_requests"] += 1
        execution_id = f"exec_{request.request_id}"
        
        events = []
        result = ExecutionResult(
            execution_id=execution_id,
            request_id=request.request_id,
            success=False,
            started_at=datetime.utcnow().isoformat(),
        )
        
        try:
            # STEP 1: PARSING
            events.append(self._emit_event(
                execution_id, "parse_start", ExecutionState.PARSING,
                {"intent": request.intent}
            ))
            
            parsed = self._parse_intent(request)
            events.append(self._emit_event(
                execution_id, "parse_complete", ExecutionState.PARSING,
                {"parsed": parsed}
            ))
            
            # STEP 2: PLANNING
            events.append(self._emit_event(
                execution_id, "plan_start", ExecutionState.PLANNING,
                {}
            ))
            
            plan = self._create_plan(request, parsed)
            events.append(self._emit_event(
                execution_id, "plan_complete", ExecutionState.PLANNING,
                {"plan_id": plan.plan_id}
            ))
            
            # STEP 3: VALIDATION
            events.append(self._emit_event(
                execution_id, "validate_start", ExecutionState.VALIDATING,
                {}
            ))
            
            valid, validation_error = self._validate_plan(plan)
            if not valid:
                raise ValueError(f"Plan validation failed: {validation_error}")
            
            events.append(self._emit_event(
                execution_id, "validate_complete", ExecutionState.VALIDATING,
                {}
            ))
            
            # STEP 4: ROUTING
            events.append(self._emit_event(
                execution_id, "route_start", ExecutionState.ROUTING,
                {"department": plan.department_id}
            ))
            
            self._route_to_department(plan)
            events.append(self._emit_event(
                execution_id, "route_complete", ExecutionState.ROUTING,
                {}
            ))
            
            # STEP 5: EXECUTION
            events.append(self._emit_event(
                execution_id, "execute_start", ExecutionState.EXECUTING,
                {}
            ))
            
            output = self._execute_plan(plan)
            events.append(self._emit_event(
                execution_id, "execute_complete", ExecutionState.EXECUTING,
                {"success": True}
            ))
            
            # STEP 6-7: OBSERVATION & LOGGING
            events.append(self._emit_event(
                execution_id, "observe", ExecutionState.OBSERVING,
                {"events": [e.to_dict() for e in events]}
            ))
            
            # STEP 8: RESULT
            result.success = True
            result.output = output
            self._metrics["successful"] += 1
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            events.append(self._emit_event(
                execution_id, "error", ExecutionState.FAILED,
                {"error": str(e)}
            ))
            self._metrics["failed"] += 1
        
        finally:
            result.completed_at = datetime.utcnow().isoformat()
            result.duration_ms = self._calculate_duration(result)
            result.events = tuple(events)
        
        return result
    
    def _parse_intent(self, request: ExecutionRequest) -> Dict[str, Any]:
        """Parse user intent into structured request."""
        # Simple parsing - in production would use NLP
        intent = request.intent.lower()
        
        parsed = {
            "action": "unknown",
            "target": "unknown",
            "parameters": {},
        }
        
        # Simple keyword detection
        if "review" in intent or "check" in intent:
            parsed["action"] = "review"
        elif "fix" in intent or "resolve" in intent:
            parsed["action"] = "fix"
        elif "create" in intent or "generate" in intent:
            parsed["action"] = "create"
        elif "deploy" in intent:
            parsed["action"] = "deploy"
        elif "test" in intent:
            parsed["action"] = "test"
        
        # Use brain for decision if available
        if self.core_brain and self.hierarchy:
            decision = self.core_brain.route_request(
                {"type": parsed["action"], "intent": request.intent},
                self.hierarchy.get_statistics()
            )
            parsed["department"] = decision.department_id
            parsed["confidence"] = decision.confidence.value
        
        return parsed
    
    def _create_plan(self, request: ExecutionRequest, parsed: Dict[str, Any]) -> ExecutionPlan:
        """Create an execution plan."""
        plan = ExecutionPlan(
            plan_id=f"plan_{request.request_id}",
            request_id=request.request_id,
            department_id=parsed.get("department"),
            steps=(
                {"step": 1, "action": "validate_input"},
                {"step": 2, "action": parsed.get("action", "unknown")},
                {"step": 3, "action": "validate_output"},
            ),
            estimated_duration_ms=60000,  # 1 minute estimate
            estimated_cost=10.0,  # $10 estimate
        )
        
        return plan
    
    def _validate_plan(self, plan: ExecutionPlan) -> Tuple[bool, Optional[str]]:
        """Validate execution plan."""
        # Basic validation
        if not plan.steps:
            return False, "Plan has no steps"
        
        if plan.department_id is None:
            return False, "No department assigned"
        
        return True, None
    
    def _route_to_department(self, plan: ExecutionPlan) -> None:
        """Route plan to appropriate department."""
        # Placeholder - would coordinate with hierarchy
        pass
    
    def _execute_plan(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute the plan using providers."""
        output = {
            "plan_id": plan.plan_id,
            "executed_steps": len(plan.steps),
            "success": True,
        }
        
        # Execute each step using providers
        for step in plan.steps:
            # Find provider for this step
            if self.provider_pool:
                provider = self.provider_pool.find_available_provider_for_skill(
                    step.get("skill_id", "")
                )
                if provider:
                    result = provider.execute(
                        step.get("skill_id", ""),
                        step.get("input", {}),
                    )
                    step["result"] = result
        
        return output
    
    def _emit_event(
        self,
        execution_id: str,
        event_type: str,
        state: ExecutionState,
        data: Dict[str, Any],
    ) -> ExecutionEvent:
        """Emit an execution event."""
        event = ExecutionEvent(
            event_id=f"{execution_id}_{event_type}",
            event_type=event_type,
            state=state,
            timestamp=datetime.utcnow().isoformat(),
            data=data,
        )
        
        # Call registered handlers
        handlers = self._event_handlers.get(event_type, [])
        handlers.extend(self._event_handlers.get("*", []))
        
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass  # Don't let handler errors break execution
        
        return event
    
    def on_event(self, event_type: str, handler: Callable) -> None:
        """Register an event handler."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def _calculate_duration(self, result: ExecutionResult) -> int:
        """Calculate execution duration."""
        if result.started_at and result.completed_at:
            start = datetime.fromisoformat(result.started_at)
            end = datetime.fromisoformat(result.completed_at)
            return int((end - start).total_seconds() * 1000)
        return 0
    
    def get_execution(self, execution_id: str) -> Optional[ExecutionResult]:
        """Get an execution by ID."""
        return self._executions.get(execution_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get orchestrator metrics."""
        total = self._metrics["total_requests"]
        success_rate = (
            self._metrics["successful"] / total if total > 0 else 0
        )
        
        return {
            "total_requests": total,
            "successful": self._metrics["successful"],
            "failed": self._metrics["failed"],
            "success_rate": round(success_rate, 3),
            "active_executions": len(self._executions),
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            "orchestrator": self.get_metrics(),
            "core_brain": self.core_brain.get_statistics() if self.core_brain else None,
            "hierarchy": self.hierarchy.get_statistics() if self.hierarchy else None,
            "providers": self.provider_pool.get_statistics() if self.provider_pool else None,
            "marketplace": self.marketplace.get_statistics() if self.marketplace else None,
        }
