"""
AGOS Environment Manager
======================

Manages environment configurations for different execution contexts.
"""

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class EnvironmentType(Enum):
    """Environment type."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    CUSTOM = "custom"


@dataclass
class EnvironmentConfig:
    """Environment configuration."""
    name: str
    environment_type: EnvironmentType
    variables: Dict[str, str] = field(default_factory=dict)
    secrets: Dict[str, str] = field(default_factory=dict)
    enabled_features: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Environment:
    """An environment."""
    id: str
    name: str
    environment_type: EnvironmentType
    config: EnvironmentConfig
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = False


class EnvironmentManager:
    """
    Environment Manager.
    
    Manages environment configurations and variable injection.
    
    Usage:
        manager = EnvironmentManager()
        
        env = manager.create_environment(
            name="production",
            environment_type=EnvironmentType.PRODUCTION,
            variables={"DEBUG": "false", "LOG_LEVEL": "info"},
        )
        
        with manager.activate(env.id):
            # Code runs with production environment
            pass
    """
    
    def __init__(self):
        """Initialize environment manager."""
        self._environments: Dict[str, Environment] = {}
        self._active_env: Optional[str] = None
        self._original_env: Dict[str, str] = {}
    
    def create_environment(
        self,
        name: str,
        environment_type: EnvironmentType,
        variables: Optional[Dict[str, str]] = None,
        secrets: Optional[Dict[str, str]] = None,
        enabled_features: Optional[List[str]] = None,
    ) -> Environment:
        """Create an environment."""
        config = EnvironmentConfig(
            name=name,
            environment_type=environment_type,
            variables=variables or {},
            secrets=secrets or {},
            enabled_features=enabled_features or [],
        )
        
        env = Environment(
            id=f"env-{uuid.uuid4().hex[:8]}",
            name=name,
            environment_type=environment_type,
            config=config,
        )
        
        self._environments[env.id] = env
        return env
    
    def get_environment(self, env_id: str) -> Optional[Environment]:
        """Get an environment by ID."""
        return self._environments.get(env_id)
    
    def list_environments(self) -> List[Environment]:
        """List all environments."""
        return list(self._environments.values())
    
    def update_environment(
        self,
        env_id: str,
        variables: Optional[Dict[str, str]] = None,
        secrets: Optional[Dict[str, str]] = None,
        enabled_features: Optional[List[str]] = None,
    ) -> Optional[Environment]:
        """Update an environment."""
        env = self._environments.get(env_id)
        if not env:
            return None
        
        if variables:
            env.config.variables.update(variables)
        if secrets:
            env.config.secrets.update(secrets)
        if enabled_features:
            env.config.enabled_features = enabled_features
        
        env.updated_at = datetime.now()
        return env
    
    def delete_environment(self, env_id: str) -> bool:
        """Delete an environment."""
        if env_id in self._environments:
            del self._environments[env_id]
            return True
        return False
    
    def activate(self, env_id: str) -> bool:
        """Activate an environment (inject variables)."""
        env = self._environments.get(env_id)
        if not env:
            return False
        
        # Save original environment
        self._original_env = os.environ.copy()
        
        # Inject environment variables
        for key, value in env.config.variables.items():
            os.environ[key] = value
        
        # Inject secrets (if available)
        for key, value in env.config.secrets.items():
            os.environ[key] = value
        
        env.is_active = True
        self._active_env = env_id
        return True
    
    def deactivate(self) -> bool:
        """Deactivate current environment."""
        if not self._active_env:
            return False
        
        # Restore original environment
        os.environ.clear()
        os.environ.update(self._original_env)
        
        env = self._environments.get(self._active_env)
        if env:
            env.is_active = False
        
        self._active_env = None
        self._original_env = {}
        return True
    
    def get_active(self) -> Optional[Environment]:
        """Get the active environment."""
        if self._active_env:
            return self._environments.get(self._active_env)
        return None
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled in the active environment."""
        active = self.get_active()
        if not active:
            return False
        return feature in active.config.enabled_features
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            "total_environments": len(self._environments),
            "active_environment": self._active_env,
            "by_type": {
                etype.value: len([
                    e for e in self._environments.values()
                    if e.environment_type == etype
                ])
                for etype in EnvironmentType
            },
        }


class EnvironmentContext:
    """Context manager for environment activation."""
    
    def __init__(self, manager: EnvironmentManager, env_id: str):
        """Initialize context."""
        self._manager = manager
        self._env_id = env_id
    
    def __enter__(self) -> None:
        """Activate environment."""
        self._manager.activate(self._env_id)
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Deactivate environment."""
        self._manager.deactivate()


# Global instance
_environment_manager: Optional[EnvironmentManager] = None


def get_environment_manager() -> EnvironmentManager:
    """Get the global environment manager."""
    global _environment_manager
    if _environment_manager is None:
        _environment_manager = EnvironmentManager()
    return _environment_manager
