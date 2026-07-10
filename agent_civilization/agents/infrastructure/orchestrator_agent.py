#!/usr/bin/env python3
"""
System Orchestrator Agent - manages agent lifecycle and system health.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict

from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('orchestrator')


class SystemOrchestratorAgent(BaseAgent):
    """Central orchestrator managing agent lifecycle and system health."""

    def __init__(self, name: str, hub: CommunicationHub, **kwargs):
        super().__init__(name, hub, **kwargs)
        self._agent_registry: Dict[str, Dict[str, Any]] = {}
        self._health_status: Dict[str, str] = {}
        self._lock = asyncio.Lock()
        self._start_time = datetime.now()

    async def _handle_message(self, message: Message):
        content = message.content
        action = content.get("action")

        async with self._lock:
            if action == "register":
                agent_name = content.get("agent_name", message.sender)
                metadata = content.get("metadata", {})
                self._agent_registry[agent_name] = {
                    "registered_at": datetime.now(),
                    "metadata": metadata,
                    "status": "active"
                }
                self._health_status[agent_name] = "healthy"
                logger.info(f"Registered: {agent_name}")

            elif action == "unregister":
                agent_name = content.get("agent_name", message.sender)
                self._agent_registry.pop(agent_name, None)
                self._health_status.pop(agent_name, None)
                logger.info(f"Unregistered: {agent_name}")

            elif action == "status_request":
                status = self.get_system_status()
                msg = Message(
                    sender=self.name,
                    recipient=message.sender,
                    content={"action": "status_response", "status": status}
                )
                await self.communication_hub.send_message(msg)

            elif action == "health_ping":
                msg = Message(
                    sender=self.name,
                    recipient=message.sender,
                    content={"action": "health_pong"}
                )
                await self.communication_hub.send_message(msg)

    def get_system_status(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self._start_time).total_seconds()
        return {
            "uptime_seconds": uptime,
            "registered_agents": len(self._agent_registry),
            "healthy_agents": sum(1 for s in self._health_status.values() if s == "healthy"),
            "agents": list(self._agent_registry.keys())
        }
