"""Universal Experience Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ExperienceType(Enum):
    """Experience type."""
    PLAYBOOK = "playbook"
    RUNBOOK = "runbook"
    RECIPE = "recipe"
    STRATEGY = "strategy"
    TEMPLATE = "template"


class ExperienceStatus(Enum):
    """Experience status."""
    DRAFT = "draft"
    VALIDATED = "validated"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Experience:
    """Universal Experience."""
    id: str
    name: str
    experience_type: ExperienceType
    content: str
    status: ExperienceStatus = ExperienceStatus.DRAFT
    rank: float = 0.5
    usage_count: int = 0
    success_rate: float = 0.0
    tags: List[str] = field(default_factory=list)
    related_experiences: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    validated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExperienceRuntime:
    """Universal Experience Engine."""
    
    def __init__(self):
        """Initialize experience runtime."""
        self.experiences: Dict[str, Experience] = {}
        self.index: Dict[str, set] = {}
    
    def create_experience(
        self,
        name: str,
        experience_type: ExperienceType,
        content: str,
        tags: Optional[List[str]] = None,
    ) -> Experience:
        """Create new experience."""
        exp_id = self._generate_id(name)
        
        exp = Experience(
            id=exp_id,
            name=name,
            experience_type=experience_type,
            content=content,
            tags=tags or [],
        )
        
        self.experiences[exp_id] = exp
        self._index_experience(exp)
        
        return exp
    
    def get_experience(self, exp_id: str) -> Optional[Experience]:
        """Get experience by ID."""
        return self.experiences.get(exp_id)
    
    def search_experiences(self, query: str, limit: int = 10) -> List[Experience]:
        """Search experiences."""
        query_lower = query.lower()
        words = query_lower.split()
        
        candidate_ids = set()
        for word in words:
            if word in self.index:
                candidate_ids.update(self.index[word])
        
        results = []
        for cid in candidate_ids:
            e = self.experiences.get(cid)
            if e:
                results.append(e)
        
        # Sort by rank
        results.sort(key=lambda x: x.rank, reverse=True)
        
        return results[:limit]
    
    def rank_experience(self, exp_id: str, success: bool) -> bool:
        """Update experience rank based on success."""
        exp = self.experiences.get(exp_id)
        if not exp:
            return False
        
        exp.usage_count += 1
        
        # Bayesian average
        prior = 0.5
        weight = min(exp.usage_count, 100)
        new_rate = 1.0 if success else 0.0
        exp.success_rate = (prior * weight + new_rate) / (weight + 1)
        exp.rank = (exp.success_rate * 0.7) + (exp.usage_count / 100 * 0.3)
        
        exp.updated_at = datetime.now()
        return True
    
    def validate_experience(self, exp_id: str) -> bool:
        """Validate experience."""
        exp = self.experiences.get(exp_id)
        if not exp:
            return False
        
        if len(exp.content) < 50:
            return False
        
        exp.status = ExperienceStatus.VALIDATED
        exp.validated_at = datetime.now()
        exp.updated_at = datetime.now()
        
        return True
    
    def _index_experience(self, exp: Experience) -> None:
        """Index experience for search."""
        words = exp.name.lower().split()
        words.extend([t.lower() for t in exp.tags])
        
        for word in words:
            if len(word) > 2:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(exp.id)
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
