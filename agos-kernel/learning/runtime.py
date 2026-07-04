"""Universal Learning Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class LearningSource(Enum):
    """Source of learning."""
    MISSION_RESULT = "mission_result"
    BENCHMARK = "benchmark"
    FAILURE = "failure"
    RECOVERY = "recovery"
    ARCHITECTURE_REVIEW = "architecture_review"
    SECURITY_REVIEW = "security_review"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    HUMAN_FEEDBACK = "human_feedback"
    VERIFIED_OUTPUT = "verified_output"


class LearningStatus(Enum):
    """Learning status."""
    PENDING = "pending"
    VALIDATING = "validating"
    VALID = "valid"
    INVALID = "invalid"
    INTEGRATED = "integrated"


class LearningRule(Enum):
    """Learning rules."""
    NO_LEARNING_WITHOUT_VALIDATION = "no_learning_without_validation"
    EVIDENCE_REQUIRED = "evidence_required"
    VALIDATION_REQUIRED = "validation_required"


@dataclass
class LearningItem:
    """A learning item."""
    id: str
    source: LearningSource
    content: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    status: LearningStatus = LearningStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    validated_at: Optional[datetime] = None
    integrated_at: Optional[datetime] = None
    validator: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class LearningReport:
    """Learning report."""
    id: str
    period_start: datetime
    period_end: datetime
    items_count: int = 0
    valid_items: int = 0
    invalid_items: int = 0
    by_source: Dict[str, int] = field(default_factory=dict)
    insights: List[str] = field(default_factory=list)


class LearningRuntime:
    """Universal Learning Runtime."""
    
    def __init__(self):
        """Initialize learning runtime."""
        self.items: Dict[str, LearningItem] = {}
        self.analytics: List[Dict[str, Any]] = []
    
    def learn(
        self,
        source: LearningSource,
        content: str,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> LearningItem:
        """Learn from source."""
        item_id = self._generate_id(f"learn-{source.value}")
        
        item = LearningItem(
            id=item_id,
            source=source,
            content=content,
            evidence=evidence or {},
        )
        
        self.items[item_id] = item
        return item
    
    def validate(self, item_id: str, validator: str) -> bool:
        """Validate a learning item."""
        item = self.items.get(item_id)
        if not item:
            return False
        
        item.status = LearningStatus.VALIDATING
        item.validator = validator
        
        # Rule: NO_LEARNING_WITHOUT_VALIDATION
        if not item.evidence:
            item.errors.append("Evidence required for validation")
            item.status = LearningStatus.INVALID
            return False
        
        # Additional validation
        if len(item.content) < 10:
            item.errors.append("Content too short")
            item.status = LearningStatus.INVALID
            return False
        
        item.status = LearningStatus.VALID
        item.validated_at = datetime.now()
        
        return True
    
    def integrate(self, item_id: str) -> bool:
        """Integrate validated learning."""
        item = self.items.get(item_id)
        if not item:
            return False
        
        if item.status != LearningStatus.VALID:
            return False
        
        item.status = LearningStatus.INTEGRATED
        item.integrated_at = datetime.now()
        
        return True
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics."""
        total = len(self.items)
        by_status = {}
        by_source = {}
        
        for item in self.items.values():
            by_status[item.status.value] = by_status.get(item.status.value, 0) + 1
            by_source[item.source.value] = by_source.get(item.source.value, 0) + 1
        
        return {
            "total_learning_items": total,
            "by_status": by_status,
            "by_source": by_source,
        }
    
    def generate_report(self, period_days: int = 30) -> LearningReport:
        """Generate learning report."""
        end = datetime.now()
        start = datetime.fromtimestamp(end.timestamp() - period_days * 86400)
        
        items = [
            i for i in self.items.values()
            if start <= i.created_at <= end
        ]
        
        report = LearningReport(
            id=self._generate_id("report"),
            period_start=start,
            period_end=end,
            items_count=len(items),
            valid_items=sum(1 for i in items if i.status == LearningStatus.VALID),
            invalid_items=sum(1 for i in items if i.status == LearningStatus.INVALID),
        )
        
        for item in items:
            src = item.source.value
            report.by_source[src] = report.by_source.get(src, 0) + 1
        
        return report
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
