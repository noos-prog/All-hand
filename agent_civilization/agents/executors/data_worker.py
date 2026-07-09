#!/usr/bin/env python3
"""
Example Worker Agent - demonstrates a real working agent.
FIXED: Complete implementation with proper message handling.
"""

import asyncio
import logging
from typing import Dict, Any
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('data_worker')


class DataWorkerAgent(BaseAgent):
    """Example agent that processes data tasks.
    FIXED: Complete implementation."""
    
    def __init__(self, name: str, hub: CommunicationHub, 
                 worker_id: int = 0, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.worker_id = worker_id
        self.processed_count = 0
        self.capabilities = ["data_processing", "all"]
        
    async def _execute_work(self, work_item: Dict[str, Any]):
        """Process a data task."""
        task_id = work_item.get("task_id", "unknown")
        data = work_item.get("data", {})
        
        logger.info(f"Worker {self.name} processing task {task_id}")
        
        try:
            # Simulate processing
            result = await self._process_data(data)
            self.processed_count += 1
            self.performance_metrics["tasks_completed"] += 1
            
            # Send result back
            sender = work_item.get("original_sender", "dispatcher")
            result_msg = Message(
                sender=self.name,
                recipient=sender,
                content={
                    "action": "task_complete",
                    "task_id": task_id,
                    "result": result,
                    "worker_id": self.worker_id
                }
            )
            await self.communication_hub.send_message(result_msg)
            
        except Exception as e:
            logger.error(f"Worker {self.name} error: {e}")
            self.performance_metrics["tasks_failed"] += 1
            
    async def _process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data - can be overridden or extended."""
        # Simulate work
        await asyncio.sleep(0.1)
        return {
            "status": "processed",
            "original_data": data,
            "worker": self.name,
            "processed_at": asyncio.get_running_loop().time()
        }
        
    async def _handle_message(self, message: Message):
        """Handle incoming messages."""
        content = message.content
        action = content.get("action")
        
        if action == "status_request":
            status = self.get_status()
            response = Message(
                sender=self.name,
                recipient=message.sender,
                content={"action": "status_response", "status": status}
            )
            await self.communication_hub.send_message(response)
            
        elif action == "register_with_orchestrator":
            # Register with system orchestrator
            msg = Message(
                sender=self.name,
                recipient="orchestrator",
                content={
                    "action": "register",
                    "agent_name": self.name,
                    "metadata": {
                        "capabilities": self.capabilities,
                        "worker_id": self.worker_id
                    }
                }
            )
            await self.communication_hub.send_message(msg)
            
        elif action == "task":
            self.add_work({
                "task_id": content.get("task_id", "unknown"),
                "data": content.get("data", {}),
                "original_sender": message.sender
            })
            
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        base_status = super().get_status()
        return {
            **base_status,
            "worker_id": self.worker_id,
            "processed_count": self.processed_count,
            "capabilities": self.capabilities
        }
