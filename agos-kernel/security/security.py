"""AGOS Security."""
import hashlib
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class SecurityLevel(Enum):
    """Security level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Secret:
    """A secret."""
    id: str
    name: str
    hash: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SecurityManager:
    """
    Security Manager.
    
    Manages secrets and security operations.
    
    Usage:
        manager = SecurityManager()
        secret = manager.create_secret("api_key", "secret_value")
    """
    
    def __init__(self):
        """Initialize security manager."""
        self._secrets: Dict[str, Secret] = {}
    
    def hash_value(self, value: str) -> str:
        """Hash a value."""
        return hashlib.sha256(value.encode()).hexdigest()
    
    def create_secret(
        self,
        name: str,
        value: str,
        expires_in_hours: Optional[int] = None,
    ) -> Secret:
        """Create a secret."""
        secret = Secret(
            id=f"secret-{uuid.uuid4().hex[:8]}",
            name=name,
            hash=self.hash_value(value),
            expires_at=datetime.now() + timedelta(hours=expires_in_hours) if expires_in_hours else None,
        )
        self._secrets[secret.id] = secret
        return secret
    
    def verify_secret(self, secret_id: str, value: str) -> bool:
        """Verify a secret."""
        secret = self._secrets.get(secret_id)
        if not secret:
            return False
        
        if secret.expires_at and datetime.now() > secret.expires_at:
            return False
        
        return secret.hash == self.hash_value(value)
    
    def get_secret(self, secret_id: str) -> Optional[Secret]:
        """Get a secret by ID."""
        return self._secrets.get(secret_id)
    
    def delete_secret(self, secret_id: str) -> bool:
        """Delete a secret."""
        if secret_id in self._secrets:
            del self._secrets[secret_id]
            return True
        return False
    
    def generate_token(self, length: int = 32) -> str:
        """Generate a secure token."""
        return secrets.token_urlsafe(length)
    
    def generate_password(self, length: int = 16) -> str:
        """Generate a secure password."""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(chars) for _ in range(length))


# Global instance
_security_manager: Optional[SecurityManager] = None


def get_security_manager() -> SecurityManager:
    """Get the global security manager."""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager
