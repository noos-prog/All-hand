"""Universal Self-Healing Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable


class FailureType(Enum):
    """Type of failure."""
    PROVIDER = "provider"
    CAPABILITY = "capability"
    STRATEGY = "strategy"
    RESOURCE = "resource"
    EXTERNAL = "external"


class RecoveryAction(Enum):
    """Recovery action."""
    ROLLBACK = "rollback"
    RETRY = "retry"
    SWITCH_PROVIDER = "switch_provider"
    SWITCH_CAPABILITY = "switch_capability"
    SWITCH_STRATEGY = "switch_strategy"
    REALLOCATE = "reallocate"
    ESCALATE = "escalate"


class RecoveryStatus(Enum):
    """Recovery status."""
    PLANNED = "planned"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Failure:
    """A detected failure."""
    id: str
    failure_type: FailureType
    description: str
    detected_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution: str = ""


@dataclass
class RecoveryPlan:
    """Recovery plan."""
    id: str
    failure_id: str
    actions: List[Dict[str, Any]] = field(default_factory=list)
    status: RecoveryStatus = RecoveryStatus.PLANNED
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None


class SelfHealingRuntime:
    """Universal Self-Healing Runtime."""
    
    def __init__(self):
        """Initialize runtime."""
        self.failures: List[Failure] = []
        self.recovery_plans: Dict[str, RecoveryPlan] = {}
        
        # Alternative selection
        self.alternative_providers: Dict[str, List[str]] = {}
        self.alternative_capabilities: Dict[str, List[str]] = {}
        self.alternative_strategies: Dict[str, List[str]] = {}
    
    def detect_failure(
        self,
        failure_type: FailureType,
        description: str,
    ) -> Failure:
        """Detect a failure."""
        failure = Failure(
            id=self._generate_id("failure"),
            failure_type=failure_type,
            description=description,
        )
        
        self.failures.append(failure)
        return failure
    
    def plan_recovery(self, failure_id: str) -> RecoveryPlan:
        """Plan recovery for a failure."""
        failure = None
        for f in self.failures:
            if f.id == failure_id:
                failure = f
                break
        
        if not failure:
            raise ValueError(f"Failure {failure_id} not found")
        
        # Create recovery plan based on failure type
        plan = RecoveryPlan(
            id=self._generate_id("recovery"),
            failure_id=failure_id,
        )
        
        if failure.failure_type == FailureType.PROVIDER:
            plan.actions = [
                {"action": RecoveryAction.SWITCH_PROVIDER.value, "alternative": "provider-2"},
                {"action": "verify", "check": "health"},
            ]
        elif failure.failure_type == FailureType.CAPABILITY:
            plan.actions = [
                {"action": RecoveryAction.SWITCH_CAPABILITY.value, "alternative": "capability-2"},
                {"action": "verify", "check": "functionality"},
            ]
        elif failure.failure_type == FailureType.RESOURCE:
            plan.actions = [
                {"action": RecoveryAction.REALLOCATE.value, "resources": "additional"},
                {"action": "verify", "check": "capacity"},
            ]
        else:
            plan.actions = [
                {"action": RecoveryAction.ROLLBACK.value, "checkpoint": "last"},
                {"action": "verify", "check": "state"},
            ]
        
        self.recovery_plans[plan.id] = plan
        return plan
    
    def execute_recovery(self, plan_id: str) -> bool:
        """Execute a recovery plan."""
        plan = self.recovery_plans.get(plan_id)
        if not plan:
            return False
        
        plan.status = RecoveryStatus.EXECUTING
        
        # Execute actions
        for action in plan.actions:
            # In real implementation, would execute each action
            pass
        
        # Mark as success
        plan.status = RecoveryStatus.SUCCESS
        plan.executed_at = datetime.now()
        
        # Resolve failure
        for f in self.failures:
            if f.id == plan.failure_id:
                f.resolved = True
                f.resolution = f"Recovery plan {plan_id} executed successfully"
                break
        
        return True
    
    def rollback(self, entity_id: str, checkpoint_id: str) -> bool:
        """Rollback to checkpoint."""
        # In real implementation, would restore state
        return True
    
    def retry(self, operation_id: str, max_attempts: int = 3) -> bool:
        """Retry an operation."""
        # In real implementation, would retry operation
        return True
    
    def switch_provider(self, from_provider: str, to_provider: str) -> bool:
        """Switch to alternative provider."""
        return True
    
    def switch_capability(self, from_capability: str, to_capability: str) -> bool:
        """Switch to alternative capability."""
        return True
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """Get recovery statistics."""
        total = len(self.failures)
        resolved = sum(1 for f in self.failures if f.resolved)
        
        return {
            "total_failures": total,
            "resolved": resolved,
            "pending": total - resolved,
            "recovery_plans": len(self.recovery_plans),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
