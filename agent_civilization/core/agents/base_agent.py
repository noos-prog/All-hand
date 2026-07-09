#!/usr/bin/env python3
"""
Core agent framework for AI civilization system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('base_agent')


@dataclass
class Message:
    """Standard message format for inter-agent communication."""
    sender: str
    recipient: str
    content: Dict[str, Any]
    message_id: str
    timestamp: float
    
    def __post_init__(self):
        """Generate unique message ID if not provided."""
        if not hasattr(self, 'message_id') or not self.message_id:
            import uuid
            self.message_id = str(uuid.uuid4())


class BaseAgent(ABC):
    """Abstract base class for all AI agents in the civilization."""
    
    def __init__(self, 
                 name: str, 
                 communication_hub: 'CommunicationHub',
                 capacity: int = 100,
                 **kwargs):
        """
        Initialize an agent.
        
        Args:
            name: Unique identifier for the agent
            communication_hub: Shared communication hub instance
            capacity: Maximum workload capacity
            **kwargs: Additional configuration parameters
        """
        self.name = name
        self.communication_hub = communication_hub
        self.capacity = capacity
        self.is_active = False
        self.status = "initialized"
        self.workqueue: List[dict] = []
        self.memory: Dict[str, Any] = {}
        logger.info(f"Agent {name} initialized with capacity {capacity}")
        
    def start(self):
        """Start agent execution."""
        if self.is_active:
            logger.warning(f"Agent {self.name} is already running")
            return
            
        self.is_active = True
        self.status = "running"
        logger.info(f"Agent {self.name} started")
        # Start background processing task
        asyncio.create_task(self._run())
        
    async def _run(self):
        """Main agent execution loop."""
        while self.is_active:
            try:
                # Process work queue items
                if self.workqueue:
                    work_item = self.workqueue.pop(0)
                    await self._execute_work(work_item)
                else:
                    # Process pending messages
                    await self._process_incoming_messages()
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.001)
            except Exception as e:
                logger.error(f"Error in agent {self.name}: {e}")
                # Implement retry logic or error handling here
                await asyncio.sleep(0.1)
                
    async def _process_incoming_messages(self):
        """Process messages from communication hub."""
        if self.communication_hub.message_queue:
            # Take first message from queue
            message = self.communication_hub.message_queue[0]
            await self._handle_message(message)
            # Remove processed message
            self.communication_hub.message_queue.pop(0)
            
    @abstractmethod
    async def _execute_work(self, work_item: dict):
        """Execute a unit of work assigned to the agent."""
        pass
        
    @abstractmethod
    async def _handle_message(self, message: Message):
        """Process an incoming message."""
        pass
        
    def add_work(self, work_item: dict):
        """Add work to the agent's queue."""
        self.workqueue.append(work_item)
        logger.debug(f"Added work to agent {self.name}: {work_item}")
        
    def update_capacity(self, new_capacity: int):
        """Update agent capacity."""
        self.capacity = new_capacity
        logger.info(f"Agent {self.name} capacity updated to {new_capacity}")
        
    def shutdown(self):
        """Gracefully shut down the agent."""
        self.is_active = False
        logger.info(f"Agent {self.name} shutting down")
        
    def __repr__(self):
        return f"<BaseAgent name={self.name} status={self.status}>"