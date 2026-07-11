"""Resource Scheduler - Schedule resource requests over time."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class SchedulePolicy(Enum):
    """Scheduling policies."""
    FIFO = "fifo"
    PRIORITY = "priority"
    FAIR = "fair"
    Earliest_Deadline_First = "edf"


@dataclass
class TimeSlot:
    """A time slot for scheduling."""
    slot_id: str
    start_time: datetime
    end_time: datetime
    resource_type: str
    available: float = 0.0


@dataclass
class ResourceRequest:
    """A resource scheduling request."""
    request_id: str
    requester: str
    resource_type: str
    amount: float
    start_time: datetime
    duration_minutes: int
    priority: int = 5
    status: str = "pending"
    scheduled_slot: Optional[str] = None


@dataclass
class ScheduleResult:
    """Result of a scheduling operation."""
    success: bool
    request_id: Optional[str] = None
    slot_id: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    error: Optional[str] = None


class ResourceScheduler:
    """Schedule resource requests over time."""
    
    def __init__(self):
        self.time_slots: Dict[str, TimeSlot] = {}
        self.requests: Dict[str, ResourceRequest] = {}
        self.policy: SchedulePolicy = SchedulePolicy.FIFO
    
    def create_time_slots(
        self,
        resource_type: str,
        start_time: datetime,
        hours: int = 24,
        slot_duration_minutes: int = 60,
    ) -> List[TimeSlot]:
        slots = []
        current = start_time
        
        for i in range(hours * 60 // slot_duration_minutes):
            slot = TimeSlot(
                slot_id=str(uuid.uuid4()),
                start_time=current,
                end_time=current + timedelta(minutes=slot_duration_minutes),
                resource_type=resource_type,
                available=100.0,
            )
            self.time_slots[slot.slot_id] = slot
            slots.append(slot)
            current = slot.end_time
        
        return slots
    
    def submit_request(
        self,
        requester: str,
        resource_type: str,
        amount: float,
        start_time: datetime,
        duration_minutes: int,
        priority: int = 5,
    ) -> ResourceRequest:
        request = ResourceRequest(
            request_id=str(uuid.uuid4()),
            requester=requester,
            resource_type=resource_type,
            amount=amount,
            start_time=start_time,
            duration_minutes=duration_minutes,
            priority=priority,
        )
        self.requests[request.request_id] = request
        return request
    
    def schedule(self, request_id: str) -> ScheduleResult:
        request = self.requests.get(request_id)
        if not request:
            return ScheduleResult(success=False, error="Request not found")
        
        if request.status != "pending":
            return ScheduleResult(success=False, error="Request already scheduled")
        
        # Find available slot
        end_time = request.start_time + timedelta(minutes=request.duration_minutes)
        
        for slot in self.time_slots.values():
            if (slot.resource_type == request.resource_type and
                slot.start_time >= request.start_time and
                slot.end_time <= end_time and
                slot.available >= request.amount):
                
                request.status = "scheduled"
                request.scheduled_slot = slot.slot_id
                slot.available -= request.amount
                
                return ScheduleResult(
                    success=True,
                    request_id=request_id,
                    slot_id=slot.slot_id,
                    scheduled_start=slot.start_time,
                )
        
        return ScheduleResult(success=False, error="No suitable slot found")
    
    def cancel(self, request_id: str) -> bool:
        request = self.requests.get(request_id)
        if not request:
            return False
        
        if request.scheduled_slot:
            slot = self.time_slots.get(request.scheduled_slot)
            if slot:
                slot.available += request.amount
        
        request.status = "cancelled"
        return True
    
    def get_pending_requests(self) -> List[ResourceRequest]:
        return [r for r in self.requests.values() if r.status == "pending"]
