"""Universal Recovery Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Recovery, RecoveryType, RecoveryStatus, Checkpoint, RecoveryPlan, FailureAnalysis
)


class RecoveryRuntime:
    """Universal Recovery Runtime."""
    
    def __init__(self):
        """Initialize recovery runtime."""
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.recoveries: Dict[str, Recovery] = {}
    
    def create_checkpoint(
        self,
        entity_type: str,
        entity_id: str,
        data: Dict[str, Any],
        state: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Checkpoint:
        """Create a checkpoint."""
        checkpoint_id = self._generate_id(f"checkpoint-{entity_id}")
        
        checkpoint = Checkpoint(
            id=checkpoint_id,
            entity_type=entity_type,
            entity_id=entity_id,
            created_at=datetime.now(),
            data=data,
            state=state or {},
            metadata=metadata or {},
        )
        
        self.checkpoints[checkpoint_id] = checkpoint
        return checkpoint
    
    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Get checkpoint by ID."""
        return self.checkpoints.get(checkpoint_id)
    
    def list_checkpoints(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> List[Checkpoint]:
        """List checkpoints with optional filtering."""
        checkpoints = list(self.checkpoints.values())
        
        if entity_type:
            checkpoints = [c for c in checkpoints if c.entity_type == entity_type]
        
        if entity_id:
            checkpoints = [c for c in checkpoints if c.entity_id == entity_id]
        
        # Sort by date descending
        checkpoints.sort(key=lambda x: x.created_at, reverse=True)
        
        return checkpoints
    
    def create_recovery(
        self,
        recovery_type: RecoveryType,
        entity_id: str,
        entity_type: str,
    ) -> Recovery:
        """Create a recovery operation."""
        recovery_id = self._generate_id(f"recovery-{entity_id}")
        
        recovery = Recovery(
            id=recovery_id,
            recovery_type=recovery_type,
            entity_id=entity_id,
            entity_type=entity_type,
        )
        
        self.recoveries[recovery_id] = recovery
        return recovery
    
    def start_recovery(self, recovery_id: str) -> bool:
        """Start a recovery operation."""
        recovery = self.recoveries.get(recovery_id)
        if not recovery:
            return False
        
        recovery.status = RecoveryStatus.IN_PROGRESS
        recovery.started_at = datetime.now()
        return True
    
    def complete_recovery(self, recovery_id: str, success: bool = True, error: Optional[str] = None) -> bool:
        """Complete a recovery operation."""
        recovery = self.recoveries.get(recovery_id)
        if not recovery:
            return False
        
        recovery.status = RecoveryStatus.COMPLETED if success else RecoveryStatus.FAILED
        recovery.completed_at = datetime.now()
        recovery.success = success
        recovery.error = error
        
        if recovery.started_at:
            recovery.duration_seconds = (recovery.completed_at - recovery.started_at).total_seconds()
        
        return True
    
    def analyze_failure(self, entity_id: str, error_type: str, error_message: str) -> FailureAnalysis:
        """Analyze a failure."""
        analysis_id = self._generate_id(f"analysis-{entity_id}")
        
        analysis = FailureAnalysis(
            id=analysis_id,
            entity_id=entity_id,
            error_type=error_type,
            error_message=error_message,
        )
        
        # Simple analysis - in production would use ML/patterns
        if "timeout" in error_message.lower():
            analysis.root_cause = "Timeout - resource exhaustion or network issue"
            analysis.suggestions.append("Increase timeout or check resource availability")
        elif "connection" in error_message.lower():
            analysis.root_cause = "Connection failure"
            analysis.suggestions.append("Check network connectivity and service availability")
        elif "memory" in error_message.lower():
            analysis.root_cause = "Memory exhaustion"
            analysis.suggestions.append("Increase memory allocation or optimize usage")
        else:
            analysis.root_cause = "Unknown - requires manual investigation"
        
        return analysis
    
    def create_recovery_plan(
        self,
        entity_id: str,
        recovery_type: RecoveryType,
    ) -> RecoveryPlan:
        """Create a recovery plan."""
        plan_id = self._generate_id(f"plan-{entity_id}")
        
        plan = RecoveryPlan(
            id=plan_id,
            entity_id=entity_id,
            steps=self._generate_recovery_steps(entity_id, recovery_type),
            created_at=datetime.now(),
        )
        
        return plan
    
    def validate_recovery(self, recovery_id: str) -> bool:
        """Validate a recovery operation."""
        recovery = self.recoveries.get(recovery_id)
        if not recovery:
            return False
        
        # Check if checkpoint exists for rollback
        if recovery.recovery_type == RecoveryType.ROLLBACK:
            checkpoints = self.list_checkpoints(entity_id=recovery.entity_id)
            if not checkpoints:
                return False
        
        return True
    
    def restore_from_checkpoint(self, entity_id: str, checkpoint_id: Optional[str] = None) -> Optional[Checkpoint]:
        """Restore from a checkpoint."""
        if checkpoint_id:
            return self.checkpoints.get(checkpoint_id)
        
        # Get latest checkpoint
        checkpoints = self.list_checkpoints(entity_id=entity_id)
        return checkpoints[0] if checkpoints else None
    
    def rollback_entity(self, entity_id: str) -> bool:
        """Rollback an entity to its last checkpoint."""
        checkpoint = self.restore_from_checkpoint(entity_id)
        if not checkpoint:
            return False
        
        # In production, would restore actual entity state
        return True
    
    def replay_entity(self, entity_id: str, from_checkpoint_id: str) -> bool:
        """Replay an entity from a checkpoint."""
        checkpoint = self.checkpoints.get(from_checkpoint_id)
        if not checkpoint:
            return False
        
        # In production, would replay entity operations
        return True
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """Get recovery statistics."""
        total = len(self.recoveries)
        completed = sum(1 for r in self.recoveries.values() if r.status == RecoveryStatus.COMPLETED)
        failed = sum(1 for r in self.recoveries.values() if r.status == RecoveryStatus.FAILED)
        
        avg_duration = 0.0
        completed_recoveries = [r for r in self.recoveries.values() if r.status == RecoveryStatus.COMPLETED]
        if completed_recoveries:
            avg_duration = sum(r.duration_seconds for r in completed_recoveries) / len(completed_recoveries)
        
        return {
            "total_recoveries": total,
            "completed": completed,
            "failed": failed,
            "success_rate": (completed / total * 100) if total > 0 else 0,
            "avg_duration_seconds": avg_duration,
            "total_checkpoints": len(self.checkpoints),
        }
    
    def _generate_recovery_steps(self, entity_id: str, recovery_type: RecoveryType) -> List[Dict[str, Any]]:
        """Generate recovery steps."""
        steps = [
            {"step": 1, "action": "analyze_failure", "description": "Analyze failure cause"},
            {"step": 2, "action": "validate_checkpoint", "description": "Validate checkpoint availability"},
            {"step": 3, "action": "prepare_recovery", "description": "Prepare recovery environment"},
            {"step": 4, "action": "execute_recovery", "description": "Execute recovery operation"},
            {"step": 5, "action": "validate_recovery", "description": "Validate recovery success"},
        ]
        
        if recovery_type == RecoveryType.ROLLBACK:
            steps.insert(3, {"step": 3, "action": "rollback_state", "description": "Rollback to checkpoint"})
        
        return steps
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
