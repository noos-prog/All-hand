#!/usr/bin/env python3
"""
AIE - Decision Packet
====================

A complete packet containing all decision information.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class PacketStatus(Enum):
    """Status of a decision packet."""
    CREATED = "created"
    PROCESSING = "processing"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PacketPriority(Enum):
    """Priority levels."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class DecisionContext:
    """
    Context information for a decision.
    """
    request_id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Input
    input_data: Dict[str, Any] = field(default_factory=dict)
    
    # Constraints
    constraints: Dict[str, Any] = field(default_factory=dict)
    budget: Optional[float] = None
    max_duration_ms: Optional[int] = None
    
    # Preferences
    preferences: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_priority_weight(self) -> float:
        """Calculate priority weight based on constraints."""
        weight = 1.0
        
        if self.budget and self.budget > 0:
            weight *= 1.2
        
        if self.max_duration_ms and self.max_duration_ms < 60000:
            weight *= 1.1
        
        return weight


@dataclass
class DecisionMetadata:
    """
    Metadata about the decision process.
    """
    # Knowledge
    knowledge_used: Tuple[str, ...] = ()
    evidence_ids: Tuple[str, ...] = ()
    
    # Reasoning
    reasoning_chain_id: Optional[str] = None
    reasoning_type: Optional[str] = None
    
    # Simulation
    simulation_result_id: Optional[str] = None
    scenarios_tested: int = 0
    
    # Optimization
    optimization_result_id: Optional[str] = None
    alternatives_considered: int = 0
    
    # Verification
    verification_result_id: Optional[str] = None
    checks_passed: int = 0
    checks_failed: int = 0
    
    # Timing
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    processing_started_at: Optional[str] = None
    decided_at: Optional[str] = None
    executed_at: Optional[str] = None
    
    # Performance
    processing_duration_ms: int = 0
    total_cost: float = 0.0


@dataclass
class DecisionOption:
    """
    A possible decision option.
    """
    option_id: str
    name: str
    description: str
    
    # Values
    value: float = 0.0
    cost: float = 0.0
    probability: float = 1.0
    
    # Evidence
    supporting_evidence: Tuple[str, ...] = ()
    contradicting_evidence: Tuple[str, ...] = ()
    
    # Requirements
    requirements: Tuple[str, ...] = ()
    prerequisites: Tuple[str, ...] = ()
    
    # Metadata
    confidence: float = 0.0
    risk_level: str = "medium"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_score(self) -> float:
        """Calculate option score."""
        return (self.value * self.confidence) / max(self.cost, 0.01)


@dataclass
class DecisionPacket:
    """
    A complete decision packet.
    """
    packet_id: str
    context: DecisionContext
    decision_type: str
    decision_goal: str
    status: PacketStatus = PacketStatus.CREATED
    priority: PacketPriority = PacketPriority.NORMAL
    options: Tuple[DecisionOption, ...] = ()
    selected_option_id: Optional[str] = None
    recommended_option_id: Optional[str] = None
    reasoning_summary: str = ""
    execution_plan: Dict[str, Any] = field(default_factory=dict)
    metadata: DecisionMetadata = field(default_factory=DecisionMetadata)
    approval_required: bool = False
    approved_by: Optional[str] = None
    approval_notes: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def select_best_option(self) -> Optional[DecisionOption]:
        """Select the best option based on score."""
        if not self.options:
            return None
        
        scored_options = [
            (opt, opt.get_score()) for opt in self.options
        ]
        scored_options.sort(key=lambda x: x[1], reverse=True)
        
        return scored_options[0][0] if scored_options else None
    
    def get_option_by_id(self, option_id: str) -> Optional[DecisionOption]:
        """Get an option by ID."""
        for option in self.options:
            if option.option_id == option_id:
                return option
        return None
    
    def approve(self, approver: str, notes: str = "") -> None:
        """Approve the decision."""
        self.status = PacketStatus.APPROVED
        self.approved_by = approver
        self.approval_notes = notes
    
    def reject(self, reason: str) -> None:
        """Reject the decision."""
        self.status = PacketStatus.REJECTED
        self.error = reason
    
    def mark_executing(self) -> None:
        """Mark as executing."""
        self.status = PacketStatus.EXECUTING
        self.metadata.executed_at = datetime.utcnow().isoformat()
    
    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Mark as completed."""
        self.status = PacketStatus.COMPLETED
        self.execution_result = result
        self.metadata.processing_duration_ms = (
            datetime.utcnow() - datetime.fromisoformat(self.metadata.created_at)
        ).total_seconds() * 1000
    
    def mark_failed(self, error: str) -> None:
        """Mark as failed."""
        self.status = PacketStatus.FAILED
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "packet_id": self.packet_id,
            "status": self.status.value,
            "priority": self.priority.value,
            "decision_type": self.decision_type,
            "decision_goal": self.decision_goal,
            "options_count": len(self.options),
            "selected_option": self.selected_option_id,
            "recommended_option": self.recommended_option_id,
            "approved_by": self.approved_by,
            "created_at": self.metadata.created_at,
        }


class PacketProcessor:
    """
    Processes decision packets through the AIE pipeline.
    """
    
    def __init__(self):
        self._processors = []
        self._initialized = True
    
    def add_processor(
        self,
        name: str,
        processor: Callable[[DecisionPacket], DecisionPacket]
    ) -> None:
        """Add a processor to the pipeline."""
        self._processors.append((name, processor))
    
    def process(self, packet: DecisionPacket) -> DecisionPacket:
        """Process a packet through all processors."""
        current_packet = packet
        
        for name, processor in self._processors:
            try:
                current_packet = processor(current_packet)
            except Exception as e:
                current_packet.mark_failed(f"Processor '{name}' failed: {e}")
                break
        
        return current_packet


def create_decision_packet(
    packet_id: str,
    decision_type: str,
    decision_goal: str,
    context_data: Dict[str, Any],
    options: List[Dict[str, Any]]
) -> DecisionPacket:
    """Create a new decision packet."""
    # Create context
    context = DecisionContext(
        request_id=context_data.get("request_id", packet_id),
        user_id=context_data.get("user_id"),
        session_id=context_data.get("session_id"),
        input_data=context_data.get("input_data", {}),
        constraints=context_data.get("constraints", {}),
        budget=context_data.get("budget"),
        max_duration_ms=context_data.get("max_duration_ms"),
        preferences=context_data.get("preferences", {}),
    )
    
    # Create options
    decision_options = [
        DecisionOption(
            option_id=opt.get("id", f"opt_{i}"),
            name=opt.get("name", f"Option {i+1}"),
            description=opt.get("description", ""),
            value=opt.get("value", 0.0),
            cost=opt.get("cost", 0.0),
            probability=opt.get("probability", 1.0),
            supporting_evidence=tuple(opt.get("evidence", [])),
            confidence=opt.get("confidence", 0.5),
            risk_level=opt.get("risk_level", "medium"),
        )
        for i, opt in enumerate(options)
    ]
    
    # Create metadata
    metadata = DecisionMetadata()
    
    # Create packet
    packet = DecisionPacket(
        packet_id=packet_id,
        context=context,
        decision_type=decision_type,
        decision_goal=decision_goal,
        options=tuple(decision_options),
        metadata=metadata,
    )
    
    # Auto-select best option
    best_option = packet.select_best_option()
    if best_option:
        packet.recommended_option_id = best_option.option_id
    
    return packet
