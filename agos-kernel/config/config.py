"""
AGOS Configuration Management
===========================

Configuration management for AGOS.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AGOSConfig:
    """AGOS configuration."""
    version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    max_workers: int = 4
    timeout_seconds: int = 300
    storage_path: str = "/tmp/agos"
    enable_telemetry: bool = True
    providers: Dict[str, Any] = field(default_factory=dict)
    capabilities: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AGOSConfig":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "debug": self.debug,
            "log_level": self.log_level,
            "max_workers": self.max_workers,
            "timeout_seconds": self.timeout_seconds,
            "storage_path": self.storage_path,
            "enable_telemetry": self.enable_telemetry,
            "providers": self.providers,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }


class ConfigManager:
    """
    Configuration Manager.
    
    Manages AGOS configuration with file persistence.
    
    Usage:
        manager = ConfigManager()
        config = manager.load_config()
        config.debug = True
        manager.save_config(config)
    """
    
    def __init__(self, config_path: str = None):
        """Initialize config manager."""
        self.config_path = config_path or os.environ.get("AGOS_CONFIG", "~/.agos/config.json")
        self.config_path = Path(self.config_path).expanduser()
        self._config: Optional[AGOSConfig] = None
    
    def load_config(self) -> AGOSConfig:
        """Load configuration from file."""
        if self._config:
            return self._config
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                self._config = AGOSConfig.from_dict(data)
            except Exception:
                self._config = AGOSConfig()
        else:
            self._config = AGOSConfig()
        
        return self._config
    
    def save_config(self, config: AGOSConfig) -> bool:
        """Save configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
            self._config = config
            return True
        except Exception:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        config = self.load_config()
        return getattr(config, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        config = self.load_config()
        if hasattr(config, key):
            setattr(config, key, value)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get config statistics."""
        config = self.load_config()
        return {
            "config_path": str(self.config_path),
            "exists": self.config_path.exists(),
            "version": config.version,
            "debug": config.debug,
            "log_level": config.log_level,
        }


# Global instance
_config_manager: Optional[ConfigManager] = None


def get_config() -> AGOSConfig:
    """Get the global configuration."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.load_config()


def get_config_manager() -> ConfigManager:
    """Get the global config manager."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
