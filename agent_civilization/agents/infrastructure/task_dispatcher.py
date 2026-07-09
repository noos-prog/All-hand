#!/usr/bin/env python3
"""
Task Dispatcher Agent - distributes work based on agent capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Any
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('task_dispatcher')


class TaskDispatcherAgent(BaseAgent):
    """Dispatches tasks to agents based on their capabilities and load."""
    
    def __init__(self, name: str, hub: CommunicationHub, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.agent_capabilities: Dict[str, List[str]] = {}
        self.agent_load: Dict[str, int] = {}
        self.pending_tasks: List[Dict[str, Any]] = []
        
    async def _execute_work(self, work_item: dict):
        """Execute task dispatch."""
        task_type = work_item.get("type")
        task_data = work_item.get("data", {})
        task_id = work_item.get("task_id", "unknown")
        
        eligible_agents = self._find_eligible_agents(task_type)
        if not eligible_agents:
            logger.warning(f"No agent found for task: {task_type}")
            self.pending_tasks.append(work_item)
            return
            
        selected_agent = self._select_least_loaded(eligible_agents)
        logger.info(f"Dispatching task {task_id} ({task_type}) to {selected_agent}")
        
        # Update load
        self.agent_load[selected_agent] = self.agent_load.get(selected_agent, 0) + 1
        
        task_msg = Message(
            sender=self.name,
            recipient=selected_agent,
            content={
                "task_id": task_id,
                "type": task_type,
                "data": task_data,
                "original_sender": work_item.get("sender", "system")
            },
            message_id="",
            timestamp=0
        )
        await self.communication_hub.send_message(task_msg)

    async def _handle_message(self, message: Message):
        """Handle messages from agents."""
        content = message.content
        
        if content.get("action") == "register":
            agent_name = message.sender
            capabilities = content.get("capabilities", [])
            self.agent_capabilities[agent_name] = capabilities
            self.agent_load[agent_name] = 0
            logger.info(f"Registered agent {agent_name} with capabilities: {capabilities}")
            
        elif content.get("action") == "load_update":
            agent_name = message.sender
            load = content.get("load", 0)
            self.agent_load[agent_name] = load
            
        elif content.get("action") == "task_complete":
            agent_name = message.sender
            if agent_name in self.agent_load:
                self.agent_load[agent_name] = max(0, self.agent_load[agent_name] - 1)
            logger.info(f"Task completed by {agent_name}")
            
        elif content.get("action") == "dispatch_task":
            self.add_work({
                "type": content.get("task_type"),
                "data": content.get("data", {}),
                "task_id": content.get("task_id", "unknown"),
                "sender": message.sender
            })

    def _find_eligible_agents(self, task_type: str) -> List[str]:
        """Find all agents that can handle a given task type."""
        return [name for name, caps in self.agent_capabilities.items() 
                if task_type in caps or "all" in caps]

    def _select_least_loaded(self, candidates: List[str]) -> str:
        """Select the agent with the lowest current load."""
        if not candidates:
            return ""
        return min(candidates, key=lambda a: self.agent_load.get(a, 0))
        
    def get_stats(self) -> Dict[str, Any]:
        """Get dispatcher statistics."""
        return {
            "total_agents": len(self.agent_capabilities),
            "pending_tasks": len(self.pending_tasks),
            "total_load": sum(self.agent_load.values())
        }