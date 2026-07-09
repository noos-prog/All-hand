#!/usr/bin/env python3
"""
Resource Manager Agent - tracks and allocates computational resources.
FIXED: Proper validation, no negative resources.
"""

import asyncio
import logging
from typing import Dict, Any
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('resource_manager')


class ResourceManagerAgent(BaseAgent):
    """Manages physical resources across the system.
    FIXED: Proper validation, no negative resources."""
    
    def __init__(self, name: str, hub: CommunicationHub, 
                 total_cpu: int = 1000, total_memory: int = 16000, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.available_cpu = total_cpu
        self.available_memory = total_memory
        self.allocations: Dict[str, Dict[str, int]] = {}
        self._lock = asyncio.Lock()
        
    async def _handle_message(self, message: Message):
        """Handle messages from agents."""
        content = message.content
        action = content.get("action")
        
        async with self._lock:
            if action == "request_allocation":
                agent_name = message.sender
                cpu_req = max(0, content.get("cpu", 0))
                mem_req = max(0, content.get("memory", 0))
                success = await self._allocate_resources(agent_name, cpu_req, mem_req)
                
                response = Message(
                    sender=self.name,
                    recipient=agent_name,
                    content={"action": "allocation_response", "success": success}
                )
                await self.communication_hub.send_message(response)
                
            elif action == "release_allocation":
                agent_name = message.sender
                await self._release_resources(agent_name)
                
            elif action == "status_request":
                status = self.get_status()
                response = Message(
                    sender=self.name,
                    recipient=message.sender,
                    content={"action": "resource_status", "status": status}
                )
                await self.communication_hub.send_message(response)
                
    async def _allocate_resources(self, agent_name: str, cpu: int, memory: int) -> bool:
        """Allocate resources to an agent if available."""
        if cpu > self.available_cpu or memory > self.available_memory:
            logger.warning(f"Insufficient resources for {agent_name}")
            return False
            
        self.available_cpu -= cpu
        self.available_memory -= memory
        self.allocations[agent_name] = {"cpu": cpu, "memory": memory}
        logger.info(f"Allocated {cpu} CPU, {memory}MB to {agent_name}")
        return True
            
    async def _release_resources(self, agent_name: str):
        """Release previously allocated resources."""
        if agent_name in self.allocations:
            alloc = self.allocations.pop(agent_name)
            self.available_cpu = min(self.total_cpu, self.available_cpu + alloc["cpu"])
            self.available_memory = min(self.total_memory, self.available_memory + alloc["memory"])
            logger.info(f"Released resources from {agent_name}")

    def get_status(self) -> Dict[str, Any]:
        """Get current resource status."""
        return {
            "total_cpu": self.total_cpu,
            "total_memory": self.total_memory,
            "available_cpu": self.available_cpu,
            "available_memory": self.available_memory,
            "used_cpu": self.total_cpu - self.available_cpu,
            "used_memory": self.total_memory - self.available_memory,
            "active_allocations": len(self.allocations)
        }
