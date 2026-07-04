"""Universal Environment Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Environment, EnvironmentType, EnvironmentStatus, EnvironmentConfig, EnvironmentHealth
)


class EnvironmentRuntime:
    """Universal Environment Runtime."""
    
    def __init__(self):
        """Initialize environment runtime."""
        self.environments: Dict[str, Environment] = {}
        self.templates: Dict[str, EnvironmentConfig] = {}
    
    def create_environment(
        self,
        name: str,
        environment_type: EnvironmentType,
        config: Optional[EnvironmentConfig] = None,
        workspace_id: Optional[str] = None,
    ) -> Environment:
        """Create a new environment."""
        env_id = self._generate_id(name)
        
        environment = Environment(
            id=env_id,
            name=name,
            environment_type=environment_type,
            status=EnvironmentStatus.INITIALIZING,
            config=config or EnvironmentConfig(),
            workspace_id=workspace_id,
        )
        
        # Set default endpoint based on type
        if environment_type == EnvironmentType.LOCAL:
            environment.endpoint = "local://default"
        elif environment_type == EnvironmentType.CONTAINER:
            environment.endpoint = f"container://{env_id}"
        elif environment_type == EnvironmentType.CLOUD:
            environment.endpoint = f"cloud://{env_id}"
        
        environment.status = EnvironmentStatus.READY
        environment.created_at = datetime.now()
        environment.updated_at = datetime.now()
        
        self.environments[env_id] = environment
        return environment
    
    def get_environment(self, env_id: str) -> Optional[Environment]:
        """Get environment by ID."""
        return self.environments.get(env_id)
    
    def list_environments(
        self,
        environment_type: Optional[EnvironmentType] = None,
        status: Optional[EnvironmentStatus] = None,
        workspace_id: Optional[str] = None,
    ) -> List[Environment]:
        """List environments with optional filtering."""
        envs = list(self.environments.values())
        
        if environment_type:
            envs = [e for e in envs if e.environment_type == environment_type]
        
        if status:
            envs = [e for e in envs if e.status == status]
        
        if workspace_id:
            envs = [e for e in envs if e.workspace_id == workspace_id]
        
        return envs
    
    def update_environment(self, env_id: str, **kwargs) -> Optional[Environment]:
        """Update environment attributes."""
        env = self.environments.get(env_id)
        if not env:
            return None
        
        for key, value in kwargs.items():
            if hasattr(env, key):
                setattr(env, key, value)
        
        env.updated_at = datetime.now()
        return env
    
    def check_health(self, env_id: str) -> bool:
        """Check environment health."""
        env = self.environments.get(env_id)
        if not env:
            return False
        
        env.health.last_check = datetime.now()
        
        # Simulate health check
        if env.status == EnvironmentStatus.READY:
            env.health.status = EnvironmentStatus.HEALTHY
            env.health.checks["connection"] = True
            env.health.checks["resources"] = True
            return True
        
        env.health.status = EnvironmentStatus.UNHEALTHY
        return False
    
    def discover_environments(self) -> List[Environment]:
        """Discover available environments."""
        discovered = []
        
        # This would typically scan for actual environments
        # For now, return all registered environments
        for env in self.environments.values():
            if self.check_health(env.id):
                discovered.append(env)
        
        return discovered
    
    def start_environment(self, env_id: str) -> bool:
        """Start an environment."""
        env = self.environments.get(env_id)
        if not env:
            return False
        
        env.status = EnvironmentStatus.INITIALIZING
        env.updated_at = datetime.now()
        
        # Simulate startup
        env.status = EnvironmentStatus.READY
        env.health.status = EnvironmentStatus.HEALTHY
        env.last_used = datetime.now()
        
        return True
    
    def stop_environment(self, env_id: str) -> bool:
        """Stop an environment."""
        env = self.environments.get(env_id)
        if not env:
            return False
        
        env.status = EnvironmentStatus.STOPPING
        env.updated_at = datetime.now()
        
        env.status = EnvironmentStatus.STOPPED
        return True
    
    def delete_environment(self, env_id: str) -> bool:
        """Delete an environment."""
        if env_id in self.environments:
            del self.environments[env_id]
            return True
        return False
    
    def create_template(
        self,
        name: str,
        config: EnvironmentConfig,
    ) -> EnvironmentConfig:
        """Create an environment template."""
        self.templates[name] = config
        return config
    
    def get_template(self, name: str) -> Optional[EnvironmentConfig]:
        """Get environment template."""
        return self.templates.get(name)
    
    def check_compatibility(self, env_id: str, requirements: Dict[str, Any]) -> bool:
        """Check if environment is compatible with requirements."""
        env = self.environments.get(env_id)
        if not env:
            return False
        
        # Check environment type compatibility
        if "environment_types" in requirements:
            if env.environment_type.value not in requirements["environment_types"]:
                return False
        
        # Check resources compatibility
        if "resources" in requirements:
            # Simple compatibility check
            pass
        
        return True
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
