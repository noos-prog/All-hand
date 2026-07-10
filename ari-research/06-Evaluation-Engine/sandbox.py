#!/usr/bin/env python3
"""
ARI - Sandbox Factory
====================

Sandbox environments for safe code execution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class SandboxType(Enum):
    """Types of sandboxes."""
    DOCKER = "docker"
    VM = "vm"
    CONTAINER = "container"
    WEB = "web"
    BROWSER = "browser"


class SecurityLevel(Enum):
    """Security levels."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class SecurityPolicy:
    """Security policy for a sandbox."""
    security_level: SecurityLevel = SecurityLevel.MEDIUM
    
    # Network
    allow_network: bool = False
    allowed_ports: Tuple[int, ...] = ()
    allowed_hosts: Tuple[str, ...] = ()
    
    # File system
    allow_file_read: bool = True
    allow_file_write: bool = False
    allowed_paths: Tuple[str, ...] = ()
    denied_paths: Tuple[str, ...] = ()
    
    # System
    allow_subprocess: bool = False
    allow_shell: bool = False
    max_memory_mb: int = 512
    max_cpu_seconds: int = 60
    
    # Environment
    env_vars: Tuple[str, ...] = ()  # Allowed env vars
    secrets_allowed: bool = False


@dataclass
class SandboxEnvironment:
    """A sandbox environment."""
    env_id: str
    sandbox_type: SandboxType
    name: str
    
    # Configuration
    image: Optional[str] = None
    command: Optional[str] = None
    working_dir: str = "/workspace"
    
    # Resources
    memory_limit_mb: int = 512
    cpu_limit: float = 1.0
    timeout_seconds: int = 300
    
    # Network
    network_enabled: bool = False
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_used: Optional[str] = None


@dataclass
class ExecutionResult:
    """Result of code execution."""
    result_id: str
    sandbox_id: str
    success: bool
    started_at: str
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    completed_at: Optional[str] = None
    duration_ms: int = 0
    memory_used_mb: float = 0.0
    cpu_time_seconds: float = 0.0
    error: Optional[str] = None
    files_created: Tuple[str, ...] = ()


class Sandbox:
    """
    A sandbox for code execution.
    """
    
    def __init__(self, env: SandboxEnvironment, policy: SecurityPolicy):
        self.env = env
        self.policy = policy
        self._is_running = False
    
    def start(self) -> bool:
        """Start the sandbox."""
        self._is_running = True
        self.env.last_used = datetime.utcnow().isoformat()
        return True
    
    def stop(self) -> bool:
        """Stop the sandbox."""
        self._is_running = False
        return True
    
    def execute(self, code: str, language: str = "python") -> ExecutionResult:
        """Execute code in the sandbox."""
        result_id = f"exec_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        started_at = datetime.utcnow().isoformat()
        
        result = ExecutionResult(
            result_id=result_id,
            sandbox_id=self.env.env_id,
            success=False,
            started_at=started_at,
        )
        
        try:
            # Execute based on language
            if language == "python":
                result = self._execute_python(code)
            elif language == "javascript":
                result = self._execute_javascript(code)
            elif language == "bash":
                result = self._execute_bash(code)
            else:
                raise ValueError(f"Unsupported language: {language}")
            
        except Exception as e:
            result.success = False
            result.error = str(e)
        
        result.completed_at = datetime.utcnow().isoformat()
        result.duration_ms = int(
            (datetime.fromisoformat(result.completed_at) - datetime.fromisoformat(started_at)).total_seconds() * 1000
        )
        
        return result
    
    def _execute_python(self, code: str) -> ExecutionResult:
        """Execute Python code."""
        import io
        import sys
        
        result_id = f"exec_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            exec_globals = {"__name__": "__main__"}
            exec(code, exec_globals)
            
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            
            return ExecutionResult(
                result_id=result_id,
                sandbox_id=self.env.env_id,
                success=True,
                exit_code=0,
                stdout=stdout,
                stderr=stderr,
                started_at=datetime.utcnow().isoformat(),
            )
        except Exception as e:
            return ExecutionResult(
                result_id=result_id,
                sandbox_id=self.env.env_id,
                success=False,
                exit_code=1,
                stdout=sys.stdout.getvalue(),
                stderr=sys.stderr.getvalue(),
                error=str(e),
                started_at=datetime.utcnow().isoformat(),
            )
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _execute_javascript(self, code: str) -> ExecutionResult:
        """Execute JavaScript code."""
        result_id = f"exec_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        return ExecutionResult(
            result_id=result_id,
            sandbox_id=self.env.env_id,
            success=True,
            stdout="JavaScript execution simulated",
            stderr="",
            started_at=datetime.utcnow().isoformat(),
        )
    
    def _execute_bash(self, code: str) -> ExecutionResult:
        """Execute bash code."""
        import subprocess
        
        result_id = f"exec_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        if not self.policy.allow_shell:
            return ExecutionResult(
                result_id=result_id,
                sandbox_id=self.env.env_id,
                success=False,
                error="Shell execution not allowed",
                started_at=datetime.utcnow().isoformat(),
            )
        
        return ExecutionResult(
            result_id=result_id,
            sandbox_id=self.env.env_id,
            success=True,
            stdout="Bash execution simulated",
            stderr="",
            started_at=datetime.utcnow().isoformat(),
        )


class SandboxFactory:
    """
    Factory for creating sandboxes.
    """
    
    def __init__(self):
        self._templates: Dict[str, SandboxEnvironment] = {}
        self._sandboxes: Dict[str, Sandbox] = {}
        self._default_policy = SecurityPolicy()
        
        # Register default templates
        self._register_default_templates()
    
    def _register_default_templates(self) -> None:
        """Register default sandbox templates."""
        self.register_template("python", SandboxEnvironment(
            env_id="python",
            sandbox_type=SandboxType.CONTAINER,
            name="Python Sandbox",
            image="python:3.11-slim",
            command="python",
            working_dir="/workspace",
            memory_limit_mb=512,
            timeout_seconds=300,
        ))
        
        self.register_template("javascript", SandboxEnvironment(
            env_id="javascript",
            sandbox_type=SandboxType.CONTAINER,
            name="JavaScript Sandbox",
            image="node:20-slim",
            command="node",
            working_dir="/workspace",
            memory_limit_mb=512,
            timeout_seconds=300,
        ))
        
        self.register_template("web", SandboxEnvironment(
            env_id="web",
            sandbox_type=SandboxType.WEB,
            name="Web Sandbox",
            working_dir="/workspace",
            memory_limit_mb=1024,
            timeout_seconds=600,
            network_enabled=True,
        ))
    
    def register_template(
        self,
        name: str,
        env: SandboxEnvironment
    ) -> None:
        """Register a sandbox template."""
        self._templates[name] = env
    
    def create_sandbox(
        self,
        template: str = "python",
        policy: SecurityPolicy = None
    ) -> Sandbox:
        """Create a sandbox from a template."""
        if template not in self._templates:
            raise ValueError(f"Unknown template: {template}")
        
        env = self._templates[template]
        policy = policy or self._default_policy
        
        sandbox = Sandbox(env, policy)
        self._sandboxes[sandbox.env.env_id] = sandbox
        
        return sandbox
    
    def create_isolated_sandbox(
        self,
        language: str = "python"
    ) -> Sandbox:
        """Create an isolated sandbox for a single execution."""
        env = SandboxEnvironment(
            env_id=f"isolated_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            sandbox_type=SandboxType.CONTAINER,
            name=f"Isolated {language} Sandbox",
            working_dir="/tmp",
            memory_limit_mb=256,
            timeout_seconds=60,
        )
        
        policy = SecurityPolicy(
            security_level=SecurityLevel.HIGH,
            allow_network=False,
            allow_file_write=False,
            allow_subprocess=False,
            allow_shell=False,
        )
        
        sandbox = Sandbox(env, policy)
        return sandbox
    
    def get_sandbox(self, sandbox_id: str) -> Optional[Sandbox]:
        """Get a sandbox by ID."""
        return self._sandboxes.get(sandbox_id)
    
    def cleanup(self, sandbox_id: str) -> bool:
        """Clean up a sandbox."""
        if sandbox_id in self._sandboxes:
            sandbox = self._sandboxes[sandbox_id]
            sandbox.stop()
            del self._sandboxes[sandbox_id]
            return True
        return False
    
    def cleanup_all(self) -> int:
        """Clean up all sandboxes."""
        count = len(self._sandboxes)
        for sandbox in self._sandboxes.values():
            sandbox.stop()
        self._sandboxes.clear()
        return count
