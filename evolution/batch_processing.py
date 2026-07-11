"""
Batch Processing Module
======================

Large-scale batch processing for evolution operations.
Handles parallel processing of evolution tasks.

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


class BatchStatus(Enum):
    """Status of a batch job."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class BatchPriority(Enum):
    """Priority levels for batch jobs."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class BatchJob:
    """
    A single job within a batch processing operation.
    """
    job_id: str
    batch_id: str
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    status: BatchStatus = BatchStatus.PENDING
    priority: BatchPriority = BatchPriority.NORMAL
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
    retry_count: int = 0
    max_retries: int = 3
    
    def can_execute(self, completed_jobs: Set[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return all(dep in completed_jobs for dep in self.dependencies)
    
    def mark_running(self) -> None:
        """Mark job as running."""
        self.status = BatchStatus.RUNNING
        self.started_at = datetime.utcnow()
    
    def mark_completed(self, result: Any) -> None:
        """Mark job as completed."""
        self.status = BatchStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.result = result
        self.progress = 1.0
    
    def mark_failed(self, error: str) -> None:
        """Mark job as failed."""
        self.status = BatchStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error = error
    
    def retry(self) -> bool:
        """Attempt to retry the job."""
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.status = BatchStatus.PENDING
            self.error = None
            return True
        return False


@dataclass
class BatchMetrics:
    """Metrics for batch processing operations."""
    total_jobs: int = 0
    completed_jobs: int = 0
    failed_jobs: int = 0
    running_jobs: int = 0
    pending_jobs: int = 0
    total_processing_time: float = 0.0
    average_job_time: float = 0.0
    throughput: float = 0.0  # jobs per second
    
    def update(self, jobs: List[BatchJob]) -> None:
        """Update metrics from job list."""
        self.total_jobs = len(jobs)
        self.completed_jobs = sum(1 for j in jobs if j.status == BatchStatus.COMPLETED)
        self.failed_jobs = sum(1 for j in jobs if j.status == BatchStatus.FAILED)
        self.running_jobs = sum(1 for j in jobs if j.status == BatchStatus.RUNNING)
        self.pending_jobs = sum(1 for j in jobs if j.status == BatchStatus.PENDING)
        
        completed = [j for j in jobs if j.completed_at and j.started_at]
        if completed:
            times = [(j.completed_at - j.started_at).total_seconds() for j in completed]
            self.total_processing_time = sum(times)
            self.average_job_time = sum(times) / len(times) if times else 0
        
        # Calculate throughput
        if self.total_processing_time > 0:
            self.throughput = self.completed_jobs / self.total_processing_time


@dataclass
class BatchProgress:
    """Progress tracking for batch operations."""
    total: int
    completed: int = 0
    failed: int = 0
    running: int = 0
    pending: int = 0
    
    @property
    def percentage(self) -> float:
        """Get completion percentage."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "running": self.running,
            "pending": self.pending,
            "percentage": self.percentage,
        }


class BatchProcessor:
    """
    Batch processor for handling large-scale evolution operations.
    Supports parallel processing, job dependencies, and retry logic.
    """
    
    def __init__(
        self,
        batch_id: Optional[str] = None,
        max_concurrent: int = 10,
        enable_retry: bool = True,
    ):
        self.batch_id = batch_id or f"batch_{uuid.uuid4().hex[:8]}"
        self.max_concurrent = max_concurrent
        self.enable_retry = enable_retry
        self.jobs: Dict[str, BatchJob] = {}
        self.running_jobs: Set[str] = set()
        self.completed_jobs: Set[str] = set()
        self.failed_jobs: Set[str] = set()
        self._callbacks: Dict[str, List[Callable]] = {
            "job_start": [],
            "job_complete": [],
            "job_fail": [],
            "batch_complete": [],
            "progress": [],
        }
        self._handlers: Dict[str, Callable] = {}
        self._metrics = BatchMetrics()
        self._semaphore: Optional[asyncio.Semaphore] = None
    
    def add_job(
        self,
        name: str,
        data: Dict[str, Any],
        handler: Optional[Callable] = None,
        priority: BatchPriority = BatchPriority.NORMAL,
        dependencies: Optional[Set[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BatchJob:
        """Add a new job to the batch."""
        job = BatchJob(
            job_id=f"{self.batch_id}_{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:4]}",
            batch_id=self.batch_id,
            name=name,
            data=data,
            priority=priority,
            dependencies=dependencies or set(),
            metadata=metadata or {},
        )
        self.jobs[job.job_id] = job
        if handler:
            self._handlers[job.job_id] = handler
        return job
    
    def set_handler(self, job_id: str, handler: Callable) -> None:
        """Set the handler function for a job."""
        self._handlers[job_id] = handler
    
    def on(self, event: str, callback: Callable) -> None:
        """Register a callback for batch events."""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
    
    def _emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event to all registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception:
                pass
    
    def get_next_job(self) -> Optional[BatchJob]:
        """Get the next job ready to execute."""
        pending = [
            job for job in self.jobs.values()
            if job.status == BatchStatus.PENDING
            and job.can_execute(self.completed_jobs)
            and len(self.running_jobs) < self.max_concurrent
        ]
        
        if not pending:
            return None
        
        # Sort by priority (higher first) and age (older first)
        pending.sort(key=lambda j: (-j.priority.value, j.job_id))
        return pending[0]
    
    def get_progress(self) -> BatchProgress:
        """Get current batch progress."""
        progress = BatchProgress(total=len(self.jobs))
        for job in self.jobs.values():
            if job.status == BatchStatus.COMPLETED:
                progress.completed += 1
            elif job.status == BatchStatus.FAILED:
                progress.failed += 1
            elif job.status == BatchStatus.RUNNING:
                progress.running += 1
            elif job.status == BatchStatus.PENDING:
                progress.pending += 1
        return progress
    
    async def process_job(self, job: BatchJob) -> Any:
        """Process a single job."""
        job.mark_running()
        self.running_jobs.add(job.job_id)
        self._emit("job_start", job)
        
        handler = self._handlers.get(job.job_id)
        if not handler:
            raise ValueError(f"No handler for job {job.job_id}")
        
        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(job.data)
            else:
                result = handler(job.data)
            
            job.mark_completed(result)
            self.completed_jobs.add(job.job_id)
            self._emit("job_complete", job, result)
            return result
            
        except Exception as e:
            job.mark_failed(str(e))
            self._emit("job_fail", job, str(e))
            
            if self.enable_retry and job.retry():
                self._emit("job_start", job)  # Emit restart event
                return await self.process_job(job)
            
            self.failed_jobs.add(job.job_id)
            raise
    
    async def execute(self) -> Dict[str, Any]:
        """Execute all jobs in the batch."""
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        while True:
            job = self.get_next_job()
            if not job:
                break
            
            if len(self.running_jobs) >= self.max_concurrent:
                await asyncio.sleep(0.1)
                continue
            
            asyncio.create_task(self._process_with_semaphore(job))
        
        # Wait for all running jobs to complete
        while self.running_jobs:
            await asyncio.sleep(0.1)
        
        self._update_metrics()
        self._emit("batch_complete", self)
        
        return {
            "batch_id": self.batch_id,
            "total_jobs": len(self.jobs),
            "completed": len(self.completed_jobs),
            "failed": len(self.failed_jobs),
            "metrics": self._metrics.__dict__,
        }
    
    async def _process_with_semaphore(self, job: BatchJob) -> None:
        """Process job with semaphore for concurrency control."""
        if self._semaphore:
            async with self._semaphore:
                await self.process_job(job)
        else:
            await self.process_job(job)
        self.running_jobs.discard(job.job_id)
        
        # Emit progress
        progress = self.get_progress()
        self._emit("progress", progress)
    
    def _update_metrics(self) -> None:
        """Update batch metrics."""
        self._metrics.update(list(self.jobs.values()))
    
    def cancel(self) -> int:
        """Cancel all pending jobs."""
        cancelled = 0
        for job in self.jobs.values():
            if job.status == BatchStatus.PENDING:
                job.status = BatchStatus.CANCELLED
                cancelled += 1
        return cancelled
    
    def get_status(self) -> Dict[str, Any]:
        """Get current batch status."""
        progress = self.get_progress()
        return {
            "batch_id": self.batch_id,
            "total_jobs": len(self.jobs),
            "max_concurrent": self.max_concurrent,
            "running_jobs": len(self.running_jobs),
            "completed_jobs": len(self.completed_jobs),
            "failed_jobs": len(self.failed_jobs),
            "progress": progress.to_dict(),
            "metrics": self._metrics.__dict__,
        }


def create_batch_processor(
    name: str = "Evolution Batch",
    max_concurrent: int = 10,
) -> BatchProcessor:
    """Factory function to create a standard batch processor."""
    return BatchProcessor(
        batch_id=f"batch_{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:4]}",
        max_concurrent=max_concurrent,
    )
