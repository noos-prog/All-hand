"""Universal Human Collaboration Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class CollaborationAction(Enum):
    """Human collaboration action."""
    REVIEW = "review"
    APPROVAL = "approval"
    FEEDBACK = "feedback"
    CORRECTION = "correction"
    ANNOTATION = "annotation"
    KNOWLEDGE_CONTRIBUTION = "knowledge_contribution"
    DECISION_OVERRIDE = "decision_override"
    POLICY_PROPOSAL = "policy_proposal"


class ReviewStatus(Enum):
    """Review status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass
class HumanContribution:
    """Human contribution to AGOS."""
    id: str
    action: CollaborationAction
    contributor_id: str
    content: str
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution: str = ""


@dataclass
class Review:
    """Human review."""
    id: str
    target_id: str
    target_type: str
    reviewer_id: str
    status: ReviewStatus = ReviewStatus.PENDING
    comments: List[str] = field(default_factory=list)
    annotations: Dict[str, Any] = field(default_factory=dict)
    decision: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class Feedback:
    """Human feedback."""
    id: str
    source_id: str
    content: str
    rating: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ConsensusDecision:
    """Consensus decision."""
    id: str
    topic: str
    participants: List[str] = field(default_factory=list)
    votes: Dict[str, str] = field(default_factory=dict)  # participant -> vote
    decision: str = ""
    reached: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class HumanRuntime:
    """Universal Human Collaboration Runtime."""
    
    def __init__(self):
        """Initialize human runtime."""
        self.contributions: Dict[str, HumanContribution] = {}
        self.reviews: Dict[str, Review] = {}
        self.feedback: Dict[str, Feedback] = {}
        self.consensus: Dict[str, ConsensusDecision] = {}
    
    # Contributions
    def add_contribution(
        self,
        action: CollaborationAction,
        contributor_id: str,
        content: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> HumanContribution:
        """Add a human contribution."""
        contribution = HumanContribution(
            id=self._generate_id("contrib"),
            action=action,
            contributor_id=contributor_id,
            content=content,
            context=context or {},
        )
        
        self.contributions[contribution.id] = contribution
        return contribution
    
    def resolve_contribution(self, contribution_id: str, resolution: str) -> bool:
        """Resolve a contribution."""
        contribution = self.contributions.get(contribution_id)
        if not contribution:
            return False
        
        contribution.resolved = True
        contribution.resolution = resolution
        return True
    
    # Reviews
    def create_review(
        self,
        target_id: str,
        target_type: str,
        reviewer_id: str,
    ) -> Review:
        """Create a review."""
        review = Review(
            id=self._generate_id("review"),
            target_id=target_id,
            target_type=target_type,
            reviewer_id=reviewer_id,
        )
        
        self.reviews[review.id] = review
        return review
    
    def add_comment(self, review_id: str, comment: str) -> bool:
        """Add a comment to a review."""
        review = self.reviews.get(review_id)
        if not review:
            return False
        
        review.comments.append(comment)
        review.status = ReviewStatus.IN_PROGRESS
        return True
    
    def complete_review(self, review_id: str, decision: str) -> bool:
        """Complete a review."""
        review = self.reviews.get(review_id)
        if not review:
            return False
        
        review.status = ReviewStatus.COMPLETED
        review.decision = decision
        review.completed_at = datetime.now()
        return True
    
    # Feedback
    def add_feedback(
        self,
        source_id: str,
        content: str,
        rating: int = 0,
        tags: Optional[List[str]] = None,
    ) -> Feedback:
        """Add feedback."""
        feedback = Feedback(
            id=self._generate_id("feedback"),
            source_id=source_id,
            content=content,
            rating=rating,
            tags=tags or [],
        )
        
        self.feedback[feedback.id] = feedback
        return feedback
    
    # Consensus
    def create_consensus(
        self,
        topic: str,
        participants: Optional[List[str]] = None,
    ) -> ConsensusDecision:
        """Create a consensus decision."""
        consensus = ConsensusDecision(
            id=self._generate_id("consensus"),
            topic=topic,
            participants=participants or [],
        )
        
        self.consensus[consensus.id] = consensus
        return consensus
    
    def vote(self, consensus_id: str, participant: str, vote: str) -> bool:
        """Vote on a consensus."""
        consensus = self.consensus.get(consensus_id)
        if not consensus:
            return False
        
        consensus.votes[participant] = vote
        
        # Check if consensus reached
        if len(consensus.votes) >= len(consensus.participants):
            all_same = len(set(consensus.votes.values())) == 1
            if all_same:
                consensus.reached = True
                consensus.decision = list(consensus.votes.values())[0]
        
        return True
    
    # Analytics
    def get_stats(self) -> Dict[str, Any]:
        """Get collaboration statistics."""
        return {
            "contributions": len(self.contributions),
            "pending_contributions": sum(1 for c in self.contributions.values() if not c.resolved),
            "reviews": len(self.reviews),
            "completed_reviews": sum(1 for r in self.reviews.values() if r.status == ReviewStatus.COMPLETED),
            "feedback": len(self.feedback),
            "avg_feedback_rating": sum(f.rating for f in self.feedback.values()) / len(self.feedback) if self.feedback else 0,
            "consensus_decisions": len(self.consensus),
            "reached_consensus": sum(1 for c in self.consensus.values() if c.reached),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
