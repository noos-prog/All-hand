#!/usr/bin/env python3
"""
Communication hub for inter-agent messaging in the AI civilization system.
"""

from typing import Dict, List, TYPE_CHECKING
import asyncio
import logging

if TYPE_CHECKING:
    from agent_civilization.core.agents.base_agent import BaseAgent, Message

logger = logging.getLogger('communication_hub')


class CommunicationHub:
    """Central communication hub for agent message routing."""
    
    def __init__(self):
        """Initialize communication hub."""
        self.agents: Dict[str, 'BaseAgent'] = {}
        self.message_queue: List['Message'] = []
        self.running = False
        
    def register_agent(self, agent: 'BaseAgent', name: str):
        """Register an agent with the communication hub."""
        self.agents[name] = agent
        logger.info(f"Agent {name} registered with communication hub")
        
    async def send_message(self, message: 'Message'):
        """Send message to target agent or broadcast."""
        message.timestamp = asyncio.get_event_loop().time()
        self.message_queue.append(message)
        logger.debug(f"Message received from {message.sender}: {message.content}")
        
    async def broadcast(self, message: 'Message'):
        """Broadcast message to all registered agents."""
        self.message_queue.append(message)
        logger.debug(f"Broadcast message from {message.sender}: {message.content}")
        
    async def process_messages(self):
        """Process messages from the queue."""
        while self.message_queue:
            message = self.message_queue.pop(0)
            await self._deliver_message(message)
            
    async def _deliver_message(self, message: 'Message'):
        """Deliver message to appropriate recipient."""
        if message.recipient == 'broadcast':
            for agent_name, agent in self.agents.items():
                await self._deliver_to_agent(agent, message)
        elif message.recipient in self.agents:
            await self._deliver_to_agent(self.agents[message.recipient], message)
        else:
            logger.warning(f"Message targeted at unregistered agent: {message.recipient}")
            
    async def _deliver_to_agent(self, agent: 'BaseAgent', message: 'Message'):
        """Deliver message to specific agent."""
        await self._handle_message(agent, message)
        
    async def _handle_message(self, agent: 'BaseAgent', message: 'Message'):
        """Process an incoming message."""
        logger.debug(f"Message from {message.sender} to {agent.name}: {message.content}")