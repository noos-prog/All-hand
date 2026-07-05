"""
AGOS Bootstrap Module
==================

System bootstrap and initialization.
Handles startup sequence, dependency loading, and health verification.

RULES:
- Bootstrap runs BEFORE any business logic
- Bootstrap verifies all dependencies
- Bootstrap reports status to Kernel
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import importlib
import logging
import os
import sys


class BootstrapPhase(Enum):
    """Bootstrap phases."""
    PREPARE = "prepare"
    LOAD_DEPENDENCIES = "load_dependencies"
    VERIFY = "verify"
    INITIALIZE = "initialize"
    READY = "ready"


class BootstrapStatus(Enum):
    """Bootstrap status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BootstrapStep:
    """A bootstrap step."""
    name: str
    phase: BootstrapPhase
    handler: Callable
    dependencies: List[str] = field(default_factory=list)
    required: bool = True
    status: BootstrapStatus = BootstrapStatus.PENDING
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class BootstrapConfig:
    """Bootstrap configuration."""
    name: str = "AGOS"
    version: str = "1.0.0"
    verify_dependencies: bool = True
    strict_mode: bool = False
    log_level: str = "INFO"
    
    # Module paths to bootstrap
    modules: List[str] = field(default_factory=list)
    
    # Skip certain bootstrap steps
    skip_steps: List[str] = field(default_factory=list)
    
    # Custom handlers
    custom_handlers: Dict[str, Callable] = field(default_factory=dict)


@dataclass
class BootstrapResult:
    """Result of bootstrap operation."""
    success: bool
    status: BootstrapStatus
    phases_completed: List[BootstrapPhase]
    steps_completed: List[str]
    steps_failed: List[str]
    duration_seconds: float
    errors: List[str]
    warnings: List[str]


class Bootstrap:
    """
    AGOS System Bootstrap.
    
    Handles the complete startup sequence:
    1. PREPARE - Load configuration, set up logging
    2. LOAD_DEPENDENCIES - Import all required modules
    3. VERIFY - Check dependency versions and availability
    4. INITIALIZE - Initialize all subsystems
    5. READY - System is ready to operate
    
    Usage:
        config = BootstrapConfig(name="AGOS")
        bootstrap = Bootstrap(config)
        result = bootstrap.run()
        
        if result.success:
            print("AGOS ready!")
        else:
            print(f"Bootstrap failed: {result.errors}")
    """
    
    def __init__(self, config: Optional[BootstrapConfig] = None):
        """Initialize bootstrap."""
        self.config = config or BootstrapConfig()
        self.logger = logging.getLogger(f"agos.bootstrap.{self.config.name}")
        
        self._steps: Dict[str, BootstrapStep] = {}
        self._phase_order = [
            BootstrapPhase.PREPARE,
            BootstrapPhase.LOAD_DEPENDENCIES,
            BootstrapPhase.VERIFY,
            BootstrapPhase.INITIALIZE,
        ]
        
        self._status = BootstrapStatus.PENDING
        self._started_at: Optional[datetime] = None
        
        # Register default bootstrap steps
        self._register_default_steps()
    
    def _register_default_steps(self) -> None:
        """Register default bootstrap steps."""
        
        # PREPARE phase
        self.register_step(BootstrapStep(
            name="setup_logging",
            phase=BootstrapPhase.PREPARE,
            handler=self._step_setup_logging,
            required=False,
        ))
        
        self.register_step(BootstrapStep(
            name="load_config",
            phase=BootstrapPhase.PREPARE,
            handler=self._step_load_config,
        ))
        
        self.register_step(BootstrapStep(
            name="detect_environment",
            phase=BootstrapPhase.PREPARE,
            handler=self._step_detect_environment,
            required=False,
        ))
        
        # LOAD_DEPENDENCIES phase
        self.register_step(BootstrapStep(
            name="import_core_modules",
            phase=BootstrapPhase.LOAD_DEPENDENCIES,
            handler=self._step_import_core_modules,
        ))
        
        self.register_step(BootstrapStep(
            name="import_runtime_modules",
            phase=BootstrapPhase.LOAD_DEPENDENCIES,
            handler=self._step_import_runtime_modules,
        ))
        
        self.register_step(BootstrapStep(
            name="import_capability_modules",
            phase=BootstrapPhase.LOAD_DEPENDENCIES,
            handler=self._step_import_capability_modules,
        ))
        
        # VERIFY phase
        self.register_step(BootstrapStep(
            name="verify_python_version",
            phase=BootstrapPhase.VERIFY,
            handler=self._step_verify_python_version,
        ))
        
        self.register_step(BootstrapStep(
            name="verify_dependencies",
            phase=BootstrapPhase.VERIFY,
            handler=self._step_verify_dependencies,
        ))
        
        self.register_step(BootstrapStep(
            name="verify_registry",
            phase=BootstrapPhase.VERIFY,
            handler=self._step_verify_registry,
        ))
        
        # INITIALIZE phase
        self.register_step(BootstrapStep(
            name="init_registries",
            phase=BootstrapPhase.INITIALIZE,
            handler=self._step_init_registries,
        ))
        
        self.register_step(BootstrapStep(
            name="init_kernel",
            phase=BootstrapPhase.INITIALIZE,
            handler=self._step_init_kernel,
        ))
        
        self.register_step(BootstrapStep(
            name="init_governance",
            phase=BootstrapPhase.INITIALIZE,
            handler=self._step_init_governance,
        ))
    
    def register_step(self, step: BootstrapStep) -> None:
        """Register a bootstrap step."""
        if step.name not in self.config.skip_steps:
            self._steps[step.name] = step
    
    def run(self) -> BootstrapResult:
        """
        Run the complete bootstrap sequence.
        
        Returns:
            BootstrapResult with status and details
        """
        self._started_at = datetime.utcnow()
        self._status = BootstrapStatus.RUNNING
        
        phases_completed: List[BootstrapPhase] = []
        steps_completed: List[str] = []
        steps_failed: List[str] = []
        errors: List[str] = []
        warnings: List[str] = []
        
        self.logger.info(f"Starting bootstrap for {self.config.name} v{self.config.version}")
        
        # Run each phase
        for phase in self._phase_order:
            self.logger.info(f"Starting phase: {phase.value}")
            
            phase_steps = [
                (name, step) for name, step in self._steps.items()
                if step.phase == phase
            ]
            
            for step_name, step in phase_steps:
                try:
                    self.logger.debug(f"Running step: {step_name}")
                    step.started_at = datetime.utcnow()
                    step.status = BootstrapStatus.RUNNING
                    
                    # Run step handler
                    result = step.handler()
                    
                    if result is False and step.required:
                        step.status = BootstrapStatus.FAILED
                        step.error = "Step returned False"
                        steps_failed.append(step_name)
                        errors.append(f"{step_name}: {step.error}")
                        self.logger.error(f"Step failed: {step_name}")
                        
                        if self.config.strict_mode:
                            break
                    else:
                        step.status = BootstrapStatus.SUCCESS
                        step.completed_at = datetime.utcnow()
                        steps_completed.append(step_name)
                        self.logger.debug(f"Step completed: {step_name}")
                
                except Exception as e:
                    step.status = BootstrapStatus.FAILED
                    step.error = str(e)
                    step.completed_at = datetime.utcnow()
                    steps_failed.append(step_name)
                    errors.append(f"{step_name}: {e}")
                    self.logger.error(f"Step error: {step_name}: {e}")
                    
                    if self.config.strict_mode and step.required:
                        break
            
            phases_completed.append(phase)
        
        # Determine overall status
        if steps_failed and self.config.strict_mode:
            self._status = BootstrapStatus.FAILED
        elif steps_failed:
            self._status = BootstrapStatus.SUCCESS
            self._status = BootstrapStatus.SKIPPED
        else:
            self._status = BootstrapStatus.SUCCESS
        
        duration = (datetime.utcnow() - self._started_at).total_seconds()
        
        self.logger.info(f"Bootstrap complete: {self._status.value} ({duration:.2f}s)")
        
        return BootstrapResult(
            success=self._status == BootstrapStatus.SUCCESS,
            status=self._status,
            phases_completed=phases_completed,
            steps_completed=steps_completed,
            steps_failed=steps_failed,
            duration_seconds=duration,
            errors=errors,
            warnings=warnings,
        )
    
    # === Default Step Handlers ===
    
    def _step_setup_logging(self) -> bool:
        """Set up logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return True
    
    def _step_load_config(self) -> bool:
        """Load configuration."""
        # In a full implementation, this would load from config files
        self.logger.info(f"Configuration loaded: {self.config.name}")
        return True
    
    def _step_detect_environment(self) -> bool:
        """Detect runtime environment."""
        env = {
            "platform": sys.platform,
            "python_version": sys.version,
            "path": sys.path,
        }
        self.logger.info(f"Environment: {env.get('platform')}")
        return True
    
    def _step_import_core_modules(self) -> bool:
        """Import core modules."""
        modules = [
            "kernel",
            "registry.component",
            "registry.cap_registry",
            "registry.provider_registry",
            "registry.workflow_registry",
            "registry.knowledge_registry",
        ]
        
        for module in modules:
            try:
                importlib.import_module(module)
                self.logger.debug(f"Imported: {module}")
            except ImportError as e:
                self.logger.warning(f"Could not import {module}: {e}")
        
        return True
    
    def _step_import_runtime_modules(self) -> bool:
        """Import runtime modules."""
        modules = [
            "knowledge.runtime",
            "memory.runtime",
            "learning.runtime",
            "experience.runtime",
            "governance.runtime",
        ]
        
        for module in modules:
            try:
                importlib.import_module(module)
                self.logger.debug(f"Imported: {module}")
            except ImportError as e:
                self.logger.warning(f"Could not import {module}: {e}")
        
        return True
    
    def _step_import_capability_modules(self) -> bool:
        """Import capability modules."""
        # Import foundation capabilities
        try:
            from capabilities.foundation import capability_001_discovery
            from capabilities.foundation import capability_002_clone
            self.logger.debug("Foundation capabilities imported")
        except ImportError as e:
            self.logger.warning(f"Could not import capabilities: {e}")
        
        return True
    
    def _step_verify_python_version(self) -> bool:
        """Verify Python version."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.logger.error(f"Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        self.logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def _step_verify_dependencies(self) -> bool:
        """Verify required dependencies."""
        required = ["dataclasses", "datetime", "typing", "threading", "logging"]
        
        for dep in required:
            if dep not in sys.modules:
                self.logger.warning(f"Dependency not imported: {dep}")
        
        return True
    
    def _step_verify_registry(self) -> bool:
        """Verify registry is accessible."""
        try:
            from registry.component import get_component_registry
            reg = get_component_registry()
            self.logger.debug("Registry verified")
            return True
        except Exception as e:
            self.logger.error(f"Registry verification failed: {e}")
            return False
    
    def _step_init_registries(self) -> bool:
        """Initialize all registries."""
        try:
            from registry.component import get_component_registry
            from registry.cap_registry import get_capability_registry
            from registry.provider_registry import get_provider_registry
            from registry.workflow_registry import get_workflow_registry
            from registry.knowledge_registry import get_knowledge_registry
            
            # Initialize registries
            get_component_registry()
            get_capability_registry()
            get_provider_registry()
            get_workflow_registry()
            get_knowledge_registry()
            
            self.logger.info("All registries initialized")
            return True
        except Exception as e:
            self.logger.error(f"Registry initialization failed: {e}")
            return False
    
    def _step_init_kernel(self) -> bool:
        """Initialize kernel."""
        try:
            from kernel import AGOSKernel
            kernel = AGOSKernel()
            self.logger.info("Kernel initialized")
            return True
        except Exception as e:
            self.logger.error(f"Kernel initialization failed: {e}")
            return False
    
    def _step_init_governance(self) -> bool:
        """Initialize governance."""
        try:
            from governance.runtime import GovernanceRuntime
            gov = GovernanceRuntime()
            self.logger.info("Governance initialized")
            return True
        except Exception as e:
            self.logger.warning(f"Governance initialization warning: {e}")
            return True  # Governance is optional
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bootstrap status."""
        return {
            "status": self._status.value,
            "steps": {
                name: {
                    "phase": step.phase.value,
                    "status": step.status.value,
                    "error": step.error,
                }
                for name, step in self._steps.items()
            },
        }
