#!/usr/bin/env python3
"""
System Orchestrator Agent - Central orchestrator managing agent lifecycle and system health.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('orchestrator')


class SystemOrchestratorAgent(BaseAgent):
    """Central orchestrator managing agent lifecycle and system health."""
    
    def __init__(self, name: str, hub: CommunicationHub, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.registry: Dict[str, BaseAgent] = {}
        self.agent_health: Dict[str, str] = {}
        self.start_time = asyncio.get_event_loop().time()
        
    async def _execute_work(self, work_item: dict):
        """Execute orchestration tasks."""
        command = work_item.get("command")
        target = work_item.get("agent")
        
        if command == "register":
            await self._register_agent(target, work_item.get("agent_instance"))
        elif command == "unregister":
            await self._unregister_agent(target)
        elif command == "health_check":
            await self._health_check(target)
        elif command == "status":
            await self._report_status(work_item.get("sender"))
            
    async def _handle_message(self, message: Message):
        """Handle messages from other agents."""
        content = message.content
        
        if content.get("action") == "register":
            agent_name = content.get("agent_name")
            self.registry[agent_name] = message.sender
            self.agent_health[agent_name] = "healthy"
            logger.info(f"Registered agent: {agent_name}")
            
        elif content.get("action") == "status_request":
            status = self._get_system_status()
            response = Message(
                sender=self.name,
                recipient=message.sender,
                content={"action": "status_response", "status": status},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(response)
            
        elif content.get("action") == "health_ping":
            agent_name = message.sender
            if agent_name in self.agent_health:
                response = Message(
                    sender=self.name,
                    recipient=agent_name,
                    content={"action": "health_pong"},
                    message_id="",
                    timestamp=0
                )
                await self.communication_hub.send_message(response)
                
    async def _register_agent(self, agent_name: str, agent_instance: BaseAgent):
        """Register a new agent."""
        self.registry[agent_name] = agent_instance
        self.agent_health[agent_name] = "healthy"
        logger.info(f"Agent registered: {agent_name}")
        
    async def _unregister_agent(self, agent_name: str):
        """Unregister an agent."""
        if agent_name in self.registry:
            del self.registry[agent_name]
            del self.agent_health[agent_name]
            logger.info(f"Agent unregistered: {agent_name}")
            
    async def _health_check(self, agent_name: str):
        """Perform health check on an agent."""
        if agent_name in self.agent_health:
            self.agent_health[agent_name] = "checked"
            logger.info(f"Health check performed on: {agent_name}")
            
    async def _report_status(self, requester: str):
        """Report overall system status."""
        status = self._get_system_status()
        response = Message(
            sender=self.name,
            recipient=requester,
            content={"action": "status_report", "status": status},
            message_id="",
            timestamp=0
        )
        await self.communication_hub.send_message(response)
        
    def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        uptime = asyncio.get_event_loop().time() - self.start_time
        return {
            "uptime_seconds": uptime,
            "registered_agents": len(self.registry),
            "healthy_agents": sum(1 for h in self.agent_health.values() if h == "healthy"),
            "agents": list(self.registry.keys())
        }