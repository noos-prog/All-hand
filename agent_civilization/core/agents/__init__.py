"""
Core agents package for AI civilization system.
"""

from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

__all__ = ["BaseAgent", "Message", "CommunicationHub"]
