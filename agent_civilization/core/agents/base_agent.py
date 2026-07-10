#!/usr/bin/env python3
"""
Core agent framework for AI civilization system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional
import asyncio
import logging
import uuid

if TYPE_CHECKING:
    from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('base_agent')


@dataclass
class Message:
    """Standard message format for inter-agent communication."""
    sender: str
    recipient: str
    content: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: 0.0)
    reply_to: Optional[str] = None

    def __post_init__(self):
        if self.timestamp == 0.0:
            try:
                loop = asyncio.get_running_loop()
                self.timestamp = loop.time()
            except RuntimeError:
                self.timestamp = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "reply_to": self.reply_to,
        }


class BaseAgent(ABC):
    """Abstract base class for all AI agents."""

    def __init__(
        self,
        name: str,
        communication_hub: 'CommunicationHub',
        capacity: int = 100,
        **kwargs
    ):
        self.name = name
        self.communication_hub = communication_hub
        self.capacity = capacity
        self.is_active = False
        self.status = "initialized"
        self.workqueue: asyncio.Queue = asyncio.Queue()
        self._inbox: asyncio.Queue = asyncio.Queue()
        self.memory: Dict[str, Any] = {}
        self._run_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self.start_time = datetime.now()
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "messages_processed": 0,
            "errors": []
        }
        logger.info(f"Agent {name} initialized with capacity {capacity}")

    def start(self):
        """Start agent execution."""
        if self.is_active:
            logger.warning(f"Agent {self.name} is already running")
            return
        self.is_active = True
        self.status = "running"
        logger.info(f"Agent {self.name} started")
        self._run_task = asyncio.create_task(self._run())

    async def _run(self):
        """Main agent execution loop."""
        logger.info(f"Agent {self.name} _run loop started")
        while self.is_active:
            try:
                try:
                    message = await asyncio.wait_for(self._inbox.get(), timeout=0.1)
                    await self._handle_message(message)
                    self._inbox.task_done()
                    self.performance_metrics["messages_processed"] += 1
                except asyncio.TimeoutError:
                    pass

                try:
                    work_item = await asyncio.wait_for(self.workqueue.get(), timeout=0.05)
                    await self._execute_work(work_item)
                    self.workqueue.task_done()
                except asyncio.TimeoutError:
                    pass

            except asyncio.CancelledError:
                logger.info(f"Agent {self.name} cancelled")
                break
            except Exception as e:
                logger.error(f"Error in agent {self.name}: {e}")
                self.performance_metrics["errors"].append(str(e))
                await asyncio.sleep(0.1)

        logger.info(f"Agent {self.name} _run loop ended")

    async def _execute_work(self, work_item: Dict[str, Any]):
        """Execute a unit of work. Override in subclasses."""
        try:
            logger.debug(f"Agent {self.name} executing work: {work_item.get('type', 'unknown')}")
            self.performance_metrics["tasks_completed"] += 1
        except Exception as e:
            logger.error(f"Work execution error in {self.name}: {e}")
            self.performance_metrics["tasks_failed"] += 1
            raise

    async def _handle_message(self, message: Message):
        """Process an incoming message. Override in subclasses."""
        logger.debug(f"Agent {self.name} handling message from {message.sender}")

    def add_work(self, work_item: Dict[str, Any]):
        """Add work to the agent's queue."""
        if not self.is_active:
            logger.warning(f"Cannot add work to inactive agent {self.name}")
            return
        self.workqueue.put_nowait(work_item)

    def deliver_message(self, message: Message):
        """Deliver a message to this agent's inbox."""
        if self.is_active:
            self._inbox.put_nowait(message)
        else:
            logger.warning(f"Message dropped for inactive agent {self.name}")

    async def send_to(self, recipient: str, content: Dict[str, Any],
                      reply_to: Optional[str] = None) -> Message:
        """Send a message to another agent."""
        msg = Message(sender=self.name, recipient=recipient, content=content, reply_to=reply_to)
        await self.communication_hub.send_message(msg)
        return msg

    async def broadcast(self, content: Dict[str, Any]):
        """Broadcast to all agents."""
        msg = Message(sender=self.name, recipient="broadcast", content=content)
        await self.communication_hub.broadcast(msg)

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "name": self.name,
            "status": self.status,
            "is_active": self.is_active,
            "queue_size": self.workqueue.qsize(),
            "inbox_size": self._inbox.qsize(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "performance": self.performance_metrics.copy(),
        }

    async def shutdown_async(self):
        """Async shutdown."""
        logger.info(f"Agent {self.name} shutting down")
        self.is_active = False
        if self._run_task:
            self._run_task.cancel()
            try:
                await self._run_task
            except asyncio.CancelledError:
                pass

    def shutdown(self):
        """Synchronous shutdown trigger."""
        if self.is_active:
            asyncio.create_task(self.shutdown_async())

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} status={self.status}>"
