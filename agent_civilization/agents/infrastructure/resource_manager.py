#!/usr/bin/env python3
"""
Resource Manager Agent - tracks and allocates computational resources.
"""

import asyncio
import logging
from typing import Dict, Any
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('resource_manager')


class ResourceManagerAgent(BaseAgent):
    """Manages physical resources (CPU, memory, network) across the system."""
    
    def __init__(self, name: str, hub: CommunicationHub, 
                 total_cpu: int = 1000, total_memory: int = 16000, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.available_cpu = total_cpu
        self.available_memory = total_memory
        self.allocations: Dict[str, Dict[str, int]] = {}
        
    async def _execute_work(self, work_item: dict):
        """Execute resource management tasks."""
        action = work_item.get("action")
        
        if action == "allocate":
            agent_name = work_item.get("agent")
            cpu_req = work_item.get("cpu", 0)
            mem_req = work_item.get("memory", 0)
            await self._allocate_resources(agent_name, cpu_req, mem_req)
            
        elif action == "release":
            agent_name = work_item.get("agent")
            await self._release_resources(agent_name)
            
        elif action == "status":
            status = self.get_status()
            response = Message(
                sender=self.name,
                recipient=work_item.get("requester", "system"),
                content={"action": "resource_status", "status": status},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(response)

    async def _handle_message(self, message: Message):
        """Handle messages from agents."""
        content = message.content
        
        if content.get("action") == "request_allocation":
            agent_name = message.sender
            cpu_req = content.get("cpu", 0)
            mem_req = content.get("memory", 0)
            await self._allocate_resources(agent_name, cpu_req, mem_req)
            
        elif content.get("action") == "release_allocation":
            agent_name = message.sender
            await self._release_resources(agent_name)
            
        elif content.get("action") == "status_request":
            status = self.get_status()
            response = Message(
                sender=self.name,
                recipient=message.sender,
                content={"action": "resource_status", "status": status},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(response)

    async def _allocate_resources(self, agent_name: str, cpu: int, memory: int) -> bool:
        """Allocate resources to an agent if available."""
        if cpu <= self.available_cpu and memory <= self.available_memory:
            self.available_cpu -= cpu
            self.available_memory -= memory
            self.allocations[agent_name] = {"cpu": cpu, "memory": memory}
            logger.info(f"Allocated {cpu} CPU, {memory}MB to {agent_name}")
            return True
        else:
            logger.warning(f"Insufficient resources for {agent_name}")
            return False
            
    async def _release_resources(self, agent_name: str):
        """Release previously allocated resources."""
        if agent_name in self.allocations:
            alloc = self.allocations.pop(agent_name)
            self.available_cpu += alloc["cpu"]
            self.available_memory += alloc["memory"]
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
            "active_allocations": len(self.allocations),
            "allocations": self.allocations
        }