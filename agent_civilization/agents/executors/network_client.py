#!/usr/bin/env python3
"""
Network Client Agent - handles network communications and HTTP requests.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import aiohttp
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('network_client')


class NetworkClientAgent(BaseAgent):
    """Agent for handling HTTP requests, WebSocket connections, and network operations."""
    
    def __init__(self, name: str, hub: CommunicationHub, 
                 timeout: int = 30, max_retries: int = 3, **kwargs):
        super().__init__(name, hub, **kwargs)
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _execute_work(self, work_item: dict):
        """Execute network operations."""
        operation = work_item.get("operation")
        
        if operation == "http_get":
            url = work_item.get("url")
            await self._http_get(url, work_item)
            
        elif operation == "http_post":
            url = work_item.get("url")
            data = work_item.get("data", {})
            await self._http_post(url, data, work_item)
            
        elif operation == "check_connectivity":
            host = work_item.get("host")
            await self._check_connectivity(host, work_item)

    async def _handle_message(self, message: Message):
        """Handle incoming messages."""
        content = message.content
        
        if content.get("action") == "http_request":
            await self.add_work({
                "operation": content.get("method", "http_get").lower(),
                "url": content.get("url"),
                "data": content.get("data"),
                "sender": message.sender
            })
            
    async def _http_get(self, url: str, work_item: dict):
        """Perform HTTP GET request."""
        sender = work_item.get("sender", "system")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.timeout) as response:
                    result = {
                        "status": response.status,
                        "body": await response.text(),
                        "headers": dict(response.headers)
                    }
                    response_msg = Message(
                        sender=self.name,
                        recipient=sender,
                        content={"action": "http_response", "result": result},
                        message_id="",
                        timestamp=0
                    )
                    await self.communication_hub.send_message(response_msg)
        except Exception as e:
            logger.error(f"HTTP GET error: {e}")
            error_msg = Message(
                sender=self.name,
                recipient=sender,
                content={"action": "http_error", "error": str(e)},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(error_msg)
            
    async def _http_post(self, url: str, data: dict, work_item: dict):
        """Perform HTTP POST request."""
        sender = work_item.get("sender", "system")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, timeout=self.timeout) as response:
                    result = {
                        "status": response.status,
                        "body": await response.text()
                    }
                    response_msg = Message(
                        sender=self.name,
                        recipient=sender,
                        content={"action": "http_response", "result": result},
                        message_id="",
                        timestamp=0
                    )
                    await self.communication_hub.send_message(response_msg)
        except Exception as e:
            logger.error(f"HTTP POST error: {e}")
            
    async def _check_connectivity(self, host: str, work_item: dict):
        """Check if host is reachable."""
        import socket
        sender = work_item.get("sender", "system")
        try:
            socket.gethostbyname(host)
            result = {"reachable": True, "host": host}
        except socket.gaierror:
            result = {"reachable": False, "host": host}
            
        response_msg = Message(
            sender=self.name,
            recipient=sender,
            content={"action": "connectivity_check", "result": result},
            message_id="",
            timestamp=0
        )
        await self.communication_hub.send_message(response_msg)