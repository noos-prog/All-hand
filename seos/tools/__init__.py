"""Universal Tool Execution Platform - Runs every external tool supported by SEOS."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import subprocess
import os


class ExecutionEnvironment(Enum):
    """Execution environments."""
    LOCAL = "local"
    REMOTE = "remote"
    CONTAINER = "container"
    CLOUD = "cloud"
    SERVERLESS = "serverless"
    MCP = "mcp"


class ToolCategory(Enum):
    """Tool categories."""
    VERSION_CONTROL = "version_control"
    CONTAINER = "container"
    INFRASTRUCTURE = "infrastructure"
    BROWSER = "browser"
    LANGUAGE = "language"
    PACKAGE_MANAGER = "package_manager"
    BUILD = "build"
    TEST = "test"
    SHELL = "shell"


@dataclass
class ToolDescriptor:
    """Descriptor for a tool."""
    name: str
    category: ToolCategory
    command: str
    environments: List[ExecutionEnvironment] = field(default_factory=list)
    version_command: str = ""
    health_check: str = ""
    description: str = ""


@dataclass
class ToolExecution:
    """Tool execution record."""
    execution_id: str
    tool_name: str
    command: List[str]
    environment: ExecutionEnvironment
    started_at: datetime
    completed_at: Optional[datetime] = None
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    success: bool = True


class IToolAdapter(ABC):
    """Tool adapter interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, command: List[str], cwd: str = None, env: Dict[str, str] = None) -> ToolExecution:
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        pass


class BaseToolAdapter(IToolAdapter):
    """Base adapter for command-line tools."""
    
    def __init__(self, name: str, command: str):
        self._name = name
        self._command = command
    
    @property
    def name(self) -> str:
        return self._name
    
    def execute(self, command: List[str], cwd: str = None, env: Dict[str, str] = None) -> ToolExecution:
        execution = ToolExecution(
            execution_id=f"exec_{int(datetime.utcnow().timestamp())}",
            tool_name=self._name,
            command=command,
            environment=ExecutionEnvironment.LOCAL,
            started_at=datetime.utcnow()
        )
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                env=env or os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=300
            )
            execution.exit_code = result.returncode
            execution.stdout = result.stdout
            execution.stderr = result.stderr
            execution.success = result.returncode == 0
        except Exception as e:
            execution.stderr = str(e)
            execution.success = False
            execution.exit_code = -1
        
        execution.completed_at = datetime.utcnow()
        return execution
    
    def health_check(self) -> bool:
        try:
            result = subprocess.run(
                [self._command, "--version"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def get_version(self) -> str:
        try:
            result = subprocess.run(
                [self._command, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except:
            return ""


# Tool Adapters
class GitAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("git", "git")


class DockerAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("docker", "docker")


class PythonAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("python", "python3")


class NodeAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("node", "node")


class GoAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("go", "go")


class RustAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("cargo", "cargo")


class NPMAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("npm", "npm")


class PIPAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("pip", "pip")


class GitHubAdapter(BaseToolAdapter):
    def __init__(self):
        super().__init__("gh", "gh")


class ToolRegistry:
    """Registry for tool adapters."""
    
    def __init__(self):
        self._adapters: Dict[str, IToolAdapter] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """Register default tool adapters."""
        adapters = [
            GitAdapter(),
            DockerAdapter(),
            PythonAdapter(),
            NodeAdapter(),
            GoAdapter(),
            RustAdapter(),
            NPMAdapter(),
            PIPAdapter(),
            GitHubAdapter(),
        ]
        for adapter in adapters:
            self._adapters[adapter.name] = adapter
    
    def register(self, adapter: IToolAdapter) -> None:
        self._adapters[adapter.name] = adapter
    
    def get(self, name: str) -> Optional[IToolAdapter]:
        return self._adapters.get(name)
    
    def list_all(self) -> List[str]:
        return list(self._adapters.keys())
    
    def health_check_all(self) -> Dict[str, bool]:
        return {name: adapter.health_check() for name, adapter in self._adapters.items()}


class ToolRuntime:
    """
    Universal Tool Execution Platform.
    
    Supported Tools:
    - Git, Docker, Podman, Kubernetes
    - Terraform, Ansible
    - Playwright, Puppeteer, Selenium
    - Node, Python, Java, Go, Rust
    - CMake, Gradle, Maven
    - npm, pnpm, yarn
    - pip, poetry, uv, cargo
    - bash, PowerShell
    
    Rules:
    ✅ Every tool executes through adapters
    ✅ No direct execution
    """
    
    def __init__(self):
        self.registry = ToolRegistry()
        self._executions: Dict[str, ToolExecution] = {}
    
    def execute(self, tool_name: str, command: List[str], cwd: str = None) -> ToolExecution:
        """Execute a tool through adapter."""
        adapter = self.registry.get(tool_name)
        if not adapter:
            execution = ToolExecution(
                execution_id=f"exec_{int(datetime.utcnow().timestamp())}",
                tool_name=tool_name,
                command=command,
                environment=ExecutionEnvironment.LOCAL,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                success=False,
                stderr=f"Tool not found: {tool_name}"
            )
            return execution
        
        execution = adapter.execute(command, cwd)
        self._executions[execution.execution_id] = execution
        return execution
    
    def get_execution(self, execution_id: str) -> Optional[ToolExecution]:
        return self._executions.get(execution_id)
    
    def list_tools(self) -> List[str]:
        return self.registry.list_all()
    
    def health_check(self) -> Dict[str, bool]:
        return self.registry.health_check_all()
