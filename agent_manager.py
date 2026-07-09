# agent_manager.py
"""
Agent Manager for the AI Agent Civilization.
Features:
- Load agent catalogue from agents.yaml
- Fetch/open-source agents via git clone
- Generate stub agents for non-open-source or missing sources
- Self-update capability (placeholder)
- Command-line interface to list, fetch, generate, update agents
"""

import os
import sys
import yaml
import shutil
import subprocess
import argparse
from pathlib import Path

# Optional: GitPython for better git handling; fallback to subprocess
try:
    from git import Repo
    GITPYTHON_AVAILABLE = True
except Exception:  # pragma: no cover
    GITPYTHON_AVAILABLE = False

CATALOGUE_FILE = "agents.yaml"
AGENTS_ROOT = Path("agent_civilization")  # base where agents live


def load_catalogue():
    if not os.path.exists(CATALOGUE_FILE):
        print(f"ERROR: Catalogue file {CATALOGUE_FILE} not found.")
        sys.exit(1)
    with open(CATALOGUE_FILE, "r") as f:
        data = yaml.safe_load(f)
    return data.get("agents", [])


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def run_cmd(cmd, cwd=None):
    """Run a shell command and stream output."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: Command failed: {cmd}")
        print(f"stderr: {result.stderr}")
    return result


def _clone_via_subprocess(repo_url, branch, target_dir):
    if target_dir.exists():
        # pull
        result = run_cmd(f"git -C {target_dir} pull origin {branch}")
        if result.returncode == 0:
            print(f"Pulled latest for {target_dir.name}")
            return True
        else:
            # if pull fails, re-clone
            shutil.rmtree(target_dir, ignore_errors=True)
            result = run_cmd(f"git clone --branch {branch} {repo_url} {target_dir}")
            if result.returncode == 0:
                print(f"Re-cloned {target_dir.name}")
                return True
            return False
    else:
        result = run_cmd(f"git clone --branch {branch} {repo_url} {target_dir}")
        if result.returncode == 0:
            print(f"Cloned {target_dir.name}")
            return True
        return False


def clone_agent(spec):
    """Clone an open-source agent repo into the appropriate location.
    If cloning fails, fall back to generating a stub."""
    name = spec["name"]
    repo_url = spec["source"]
    branch = spec.get("branch", "main")
    target_subdir = spec.get("specialization")
    target_dir = AGENTS_ROOT / target_subdir if target_subdir else AGENTS_ROOT / name
    ensure_dir(target_dir)
    print(f"Attempting to clone {name} from {repo_url} (branch {branch}) into {target_dir}")
    success = False
    if GITPYTHON_AVAILABLE:
        try:
            if target_dir.exists():
                repo = Repo(str(target_dir))
                origin = repo.remotes.origin
                origin.pull()
                print(f"Pulled latest for {name}")
                success = True
            else:
                Repo.clone_from(repo_url, to_path=str(target_dir), branch=branch)
                print(f"Cloned {name}")
                success = True
        except Exception as e:
            print(f"GitPython error ({e}); will try subprocess")
    if not success and not GITPYTHON_AVAILABLE:
        success = _clone_via_subprocess(repo_url, branch, target_dir)
    if not success:
        print(f"Cloning failed for {name}; generating stub instead.")
        generate_stub(spec)
        return


def _get_specialized_methods(specialization: str) -> str:
    """Return specialized processing logic based on agent type."""
    methods = {
        "data_processor": "Process and transform data structures, perform ETL operations, validate data quality.",
        "api_integrator": "Integrate with external APIs, handle authentication, retry failed requests, aggregate responses.",
        "db_manager": "Manage database connections, execute queries, handle transactions, optimize database operations.",
        "code_generator": "Generate code snippets, templates, and complete modules based on specifications.",
        "network_client": "Handle network communications, HTTP requests, WebSocket connections, message brokers.",
        "test_runner": "Execute test suites, report results, handle test retries, generate test reports.",
        "builder": "Build and compile code, container images, deployment packages, artifacts.",
        "designer": "Generate design documents, UI mockups, architecture diagrams, system designs.",
        "monitor": "Monitor system health, collect metrics, alert on anomalies, log system state.",
        "reviewer": "Review code quality, check compliance, suggest improvements, approve changes.",
        "educator": "Provide training materials, evaluate learning progress, adapt curriculum.",
        "modifier": "Modify existing code or configurations while preserving functionality.",
        "surgeon": "Perform precise modifications, extract components, refactor code.",
        "self_developer": "Self-improve through code synthesis and optimization loops.",
        "architect": "Design system architectures, component layouts, integration patterns.",
        "analyst": "Analyze data patterns, extract insights, generate reports.",
        "researcher": "Conduct research, gather information, synthesize findings.",
        "strategist": "Plan long-term strategies, optimize resource allocation.",
        "communicator": "Handle inter-agent communication, translate protocols.",
        "generic": "General purpose agent processing."
    }
    return methods.get(specialization, methods["generic"])


def generate_stub(spec):
    """Generate a comprehensive agent stub when no source is available."""
    name = spec["name"]
    specialization = spec.get("specialization")
    class_name = "".join([p.capitalize() for p in name.split("_")]) + "Agent"
    target_dir = AGENTS_ROOT / specialization if specialization else AGENTS_ROOT / name
    ensure_dir(target_dir)
    init_file = target_dir / "__init__.py"
    agent_file = target_dir / f"{name}.py"
    
    specialization_type = specialization.split("/")[1] if specialization else "generic"
    specialized_methods = _get_specialized_methods(specialization_type)
    
    if not init_file.exists():
        init_file.write_text(f'"""{name} package."""\nfrom .{name} import {class_name}\n')
    
    if agent_file.exists():
        print(f"Agent {name} already exists")
        return
    
    content = f'''#!/usr/bin/env python3
"""
{name.capitalize()} Agent – auto-generated comprehensive stub.
Specialization: {specialization_type}

This agent provides a realistic implementation structure for the {specialization_type} domain.
Replace or extend the logic below with actual behavior when needed.
"""

from agent_civilization.core.agents.base_agent import BaseAgent, Message, CommunicationHub
import logging
import asyncio
from typing import Dict, Any, List, Optional
import uuid
import json

logger = logging.getLogger("{name}")


class {class_name}(BaseAgent):
    """Agent specialized in {specialization_type} tasks."""
    
    def __init__(self, name: str, communication_hub: CommunicationHub, **kwargs):
        """Initialize the {specialization_type} agent."""
        super().__init__(name, communication_hub, **kwargs)
        
        # Specialization-specific configuration
        self.{specialization_type}_config = {{
            "max_concurrent_tasks": kwargs.get("max_concurrent_tasks", 5),
            "timeout_seconds": kwargs.get("timeout_seconds", 30),
            "retry_attempts": kwargs.get("retry_attempts", 3),
        }}
        
        # State tracking
        self.task_history: List[Dict[str, Any]] = []
        self.performance_metrics = {{
            "tasks_completed": 0,
            "errors": 0,
            "avg_processing_time": 0.0
        }}
        
        logger.info(f"{{self.name}} initialized as {{self.__class__.__name__}}")

    async def _execute_work(self, work_item: Dict[str, Any]):
        """Execute a unit of work specific to {specialization_type} tasks."""
        task_id = work_item.get("task_id", str(uuid.uuid4()))
        task_type = work_item.get("type", "generic")
        
        logger.info(f"{{self.name}} executing task {{task_id}} (type: {{task_type}})")
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Dispatch to specialized handler
            result = await self._{specialization_type}_process(work_item)
            
            end_time = asyncio.get_event_loop().time()
            
            # Track performance
            elapsed = end_time - start_time
            self.task_history.append({{
                "task_id": task_id,
                "type": task_type,
                "duration": elapsed,
                "success": True
            }})
            self.performance_metrics["tasks_completed"] += 1
            self.performance_metrics["avg_processing_time"] = (
                self.performance_metrics["avg_processing_time"] * (self.performance_metrics["tasks_completed"] - 1) + elapsed
            ) / self.performance_metrics["tasks_completed"]
            
            # Notify sender
            response = Message(
                sender=self.name,
                recipient=work_item.get("sender", "unknown"),
                content={{"task_id": task_id, "result": result, "status": "completed"}},
                message_id="",
                timestamp=end_time
            )
            await self.communication_hub.send_message(response)
            
        except Exception as e:
            logger.error(f"{{self.name}} error executing task {{task_id}}: {{e}}")
            self.performance_metrics["errors"] += 1
            
            error_response = Message(
                sender=self.name,
                recipient=work_item.get("sender", "unknown"),
                content={{"task_id": task_id, "error": str(e), "status": "failed"}},
                message_id="",
                timestamp=asyncio.get_event_loop().time()
            )
            await self.communication_hub.send_message(error_response)

    async def _{specialization_type}_process(self, work_item: Dict[str, Any]) -> Dict[str, Any]:
        """{specialized_methods}"""
        return {{"status": "processed", "data": work_item.get("data", {{}})}}

    async def _handle_message(self, message: Message):
        """Handle incoming messages from other agents or systems."""
        msg_type = message.content.get("type", "generic")
        logger.debug(f"{{self.name}} handling message of type {{msg_type}} from {{message.sender}}")
        
        if msg_type == "status_request":
            status_response = Message(
                sender=self.name,
                recipient=message.sender,
                content={{"status": self.status, "metrics": self.performance_metrics}},
                message_id="",
                timestamp=asyncio.get_event_loop().time()
            )
            await self.communication_hub.send_message(status_response)
            
        elif msg_type == "config_update":
            new_config = message.content.get("config", {{}})
            self.{specialization_type}_config.update(new_config)
            logger.info(f"{{self.name}} updated config: {{new_config}}")
            
        elif msg_type == "task":
            self.add_work(message.content)
            
        else:
            logger.warning(f"{{self.name}} unknown message type: {{msg_type}}")

    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent supports."""
        return ["{specialization_type}_processing", "message_handling", "task_execution"]


def register_agent(hub: CommunicationHub, name: Optional[str] = None) -> {class_name}:
    """Factory function for dynamic registration."""
    agent_name = name or "{name}"
    agent = {class_name}(name=agent_name, communication_hub=hub)
    hub.register_agent(agent, agent_name)
    logger.info(f"Registered agent {{agent_name}}")
    return agent
'''
    agent_file.write_text(content)
    print(f"Generated comprehensive stub for {name} at {agent_file}")


def fetch_agent(spec):
    """Dispatch to clone or stub based on presence of source."""
    if spec.get("source"):
        clone_agent(spec)
    else:
        generate_stub(spec)


def self_update():
    """Placeholder for self-update – pull latest version of this script/repo."""
    print("Self-update: pulling latest from origin (if this repo is a git checkout)...")
    result = run_cmd("git pull origin main")
    if result.returncode == 0:
        print("Self-update successful")
    else:
        print("Self-update failed or not a git repo")


def list_agents():
    agents = load_catalogue()
    print(f"Known agents ({len(agents)}):")
    for a in agents:
        src = a.get("source", "[GENERATED]")
        spec = a.get("specialization", "-")
        print(f" - {a['name']:20} | source: {src:50} | specialization: {spec}")


def main():
    parser = argparse.ArgumentParser(description="Agent Manager for AI Civilization")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all known agents")

    # fetch
    fetch_p = subparsers.add_parser("fetch", help="Fetch (clone) all agents from catalogue")
    fetch_p.add_argument("--name", help="Fetch only this agent by name", default=None)

    # generate
    gen_p = subparsers.add_parser("generate", help="Generate stubs for all agents")
    gen_p.add_argument("--name", help="Generate only this agent by name", default=None)

    # update (self)
    subparsers.add_parser("update-self", help="Update the agent manager script itself")

    args = parser.parse_args()

    if args.command == "list":
        list_agents()
    elif args.command == "fetch":
        agents = load_catalogue()
        for spec in agents:
            if args.name and spec["name"] != args.name:
                continue
            fetch_agent(spec)
    elif args.command == "generate":
        agents = load_catalogue()
        for spec in agents:
            if args.name and spec["name"] != args.name:
                continue
            generate_stub(spec)
    elif args.command == "update-self":
        self_update()
    else:
        parser.print_help()


if __name__ == "__main__":
    # Ensure we are in the repo root (where agents.yaml lives)
    if not os.path.exists(CATALOGUE_FILE):
        print(f"ERROR: Please run this script from the repository root (missing {CATALOGUE_FILE})")
        sys.exit(1)
    main()