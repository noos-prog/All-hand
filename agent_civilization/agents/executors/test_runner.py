#!/usr/bin/env python3
"""
Test Runner Agent - executes test suites and reports results.
"""

import asyncio
import logging
import subprocess
from typing import Dict, Any, List
from agent_civilization.core.agents.base_agent import BaseAgent, Message
from agent_civilization.core.agents.communication_hub import CommunicationHub

logger = logging.getLogger('test_runner')


class TestRunnerAgent(BaseAgent):
    """Agent for executing test suites and generating reports."""
    
    def __init__(self, name: str, hub: CommunicationHub, 
                 test_dir: str = "tests", **kwargs):
        super().__init__(name, hub, **kwargs)
        self.test_dir = test_dir
        self.test_history: List[Dict[str, Any]] = []
        
    async def _execute_work(self, work_item: dict):
        """Execute test operations."""
        operation = work_item.get("operation")
        
        if operation == "run_tests":
            test_path = work_item.get("path", self.test_dir)
            await self._run_tests(test_path, work_item)
            
        elif operation == "run_specific":
            test_file = work_item.get("file")
            await self._run_specific_test(test_file, work_item)
            
        elif operation == "generate_report":
            await self._generate_report(work_item)

    async def _handle_message(self, message: Message):
        """Handle incoming messages."""
        content = message.content
        
        if content.get("action") == "run_test":
            await self.add_work({
                "operation": "run_tests",
                "path": content.get("path", self.test_dir),
                "sender": message.sender
            })
            
    async def _run_tests(self, test_path: str, work_item: dict):
        """Run test suite."""
        sender = work_item.get("sender", "system")
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", test_path, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            test_result = {
                "passed": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "test_path": test_path
            }
            
            self.test_history.append(test_result)
            
            response_msg = Message(
                sender=self.name,
                recipient=sender,
                content={"action": "test_results", "result": test_result},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(response_msg)
            
        except subprocess.TimeoutExpired:
            logger.error(f"Test timeout for {test_path}")
            error_msg = Message(
                sender=self.name,
                recipient=sender,
                content={"action": "test_error", "error": "Test timeout"},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(error_msg)
            
        except Exception as e:
            logger.error(f"Test error: {e}")
            
    async def _run_specific_test(self, test_file: str, work_item: dict):
        """Run a specific test file."""
        sender = work_item.get("sender", "system")
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", test_file, "-v"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            test_result = {
                "passed": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "test_file": test_file
            }
            
            response_msg = Message(
                sender=self.name,
                recipient=sender,
                content={"action": "test_results", "result": test_result},
                message_id="",
                timestamp=0
            )
            await self.communication_hub.send_message(response_msg)
            
        except Exception as e:
            logger.error(f"Specific test error: {e}")
            
    async def _generate_report(self, work_item: dict):
        """Generate test execution report."""
        sender = work_item.get("sender", "system")
        
        total = len(self.test_history)
        passed = sum(1 for t in self.test_history if t.get("passed"))
        failed = total - passed
        
        report = {
            "total_runs": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "history": self.test_history[-10:]  # Last 10 tests
        }
        
        response_msg = Message(
            sender=self.name,
            recipient=sender,
            content={"action": "test_report", "report": report},
            message_id="",
            timestamp=0
        )
        await self.communication_hub.send_message(response_msg)