"""
AGOS Agent Civilization Framework
A real, working system of AI agents serving the user and the civilization.
"""

__version__ = "3.0.0"
__author__ = "AGOS Civilization Team"

from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

__all__ = ["BaseAgent", "Message", "CommunicationHub", "__version__"]
