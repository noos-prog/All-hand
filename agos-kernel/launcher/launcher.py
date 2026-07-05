"""
AGOS Launcher
============

Application launcher for AGOS.
"""

import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class LaunchMode(Enum):
    """Launch mode."""
    STANDALONE = "standalone"
    SERVER = "server"
    AGENT = "agent"
    WORKER = "worker"


class LaunchStatus(Enum):
    """Launch status."""
    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class LaunchConfig:
    """Launch configuration."""
    mode: LaunchMode = LaunchMode.STANDALONE
    host: str = "localhost"
    port: int = 8080
    workers: int = 1
    debug: bool = False
    config_file: str = ""


@dataclass
class LaunchResult:
    """Launch result."""
    success: bool
    pid: Optional[int] = None
    status: LaunchStatus = LaunchStatus.PENDING
    message: str = ""
    started_at: datetime = field(default_factory=datetime.now)


class Launcher:
    """
    AGOS Application Launcher.
    
    Launches AGOS in different modes.
    
    Usage:
        launcher = Launcher()
        result = launcher.launch(mode=LaunchMode.SERVER)
    """
    
    def __init__(self):
        """Initialize launcher."""
        self._apps: Dict[str, Callable] = {}
        self._current_launch: Optional[LaunchResult] = None
    
    def register_app(self, name: str, app: Callable) -> None:
        """Register an application."""
        self._apps[name] = app
    
    def launch(
        self,
        mode: LaunchMode = LaunchMode.STANDALONE,
        config: Optional[LaunchConfig] = None,
    ) -> LaunchResult:
        """Launch AGOS."""
        config = config or LaunchConfig(mode=mode)
        
        self._current_launch = LaunchResult(
            success=False,
            status=LaunchStatus.STARTING,
            message=f"Launching in {mode.value} mode",
        )
        
        try:
            if mode == LaunchMode.STANDALONE:
                return self._launch_standalone(config)
            elif mode == LaunchMode.SERVER:
                return self._launch_server(config)
            elif mode == LaunchMode.AGENT:
                return self._launch_agent(config)
            elif mode == LaunchMode.WORKER:
                return self._launch_worker(config)
            else:
                self._current_launch.message = f"Unknown mode: {mode}"
                return self._current_launch
        
        except Exception as e:
            self._current_launch.success = False
            self._current_launch.status = LaunchStatus.FAILED
            self._current_launch.message = str(e)
            return self._current_launch
    
    def _launch_standalone(self, config: LaunchConfig) -> LaunchResult:
        """Launch in standalone mode."""
        self._current_launch.success = True
        self._current_launch.status = LaunchStatus.RUNNING
        self._current_launch.message = "Running in standalone mode"
        return self._current_launch
    
    def _launch_server(self, config: LaunchConfig) -> LaunchResult:
        """Launch in server mode."""
        self._current_launch.success = True
        self._current_launch.status = LaunchStatus.RUNNING
        self._current_launch.message = f"Server starting on {config.host}:{config.port}"
        return self._current_launch
    
    def _launch_agent(self, config: LaunchConfig) -> LaunchResult:
        """Launch in agent mode."""
        self._current_launch.success = True
        self._current_launch.status = LaunchStatus.RUNNING
        self._current_launch.message = "Agent started"
        return self._current_launch
    
    def _launch_worker(self, config: LaunchConfig) -> LaunchResult:
        """Launch in worker mode."""
        self._current_launch.success = True
        self._current_launch.status = LaunchStatus.RUNNING
        self._current_launch.message = f"Worker pool started with {config.workers} workers"
        return self._current_launch
    
    def stop(self) -> bool:
        """Stop the current launch."""
        if self._current_launch:
            self._current_launch.status = LaunchStatus.STOPPED
            self._current_launch.success = False
            self._current_launch.message = "Stopped"
            return True
        return False
    
    def get_status(self) -> Optional[LaunchResult]:
        """Get current launch status."""
        return self._current_launch


# Global instance
_launcher: Optional[Launcher] = None


def get_launcher() -> Launcher:
    """Get the global launcher."""
    global _launcher
    if _launcher is None:
        _launcher = Launcher()
    return _launcher
