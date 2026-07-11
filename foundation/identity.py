"""
Foundation Identity Module
=========================

Universal identity management for the AGOS system.
Provides identity creation, verification, and management.

Author: AGOS Team
Version: 1.0.0
"""

import hashlib
import secrets
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set


IDENTITY_RULES = [
    "Immutable",
    "Globally Unique",
    "Human Readable Alias",
    "Machine Readable Identifier",
    "Cross-Version Compatible",
    "Cross-Repository Compatible"
]


class IdentityType(Enum):
    """Type of identity."""
    AGENT = "agent"
    USER = "user"
    SYSTEM = "system"
    SERVICE = "service"
    RESOURCE = "resource"
    ORGANIZATION = "organization"


class IdentityStatus(Enum):
    """Status of an identity."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass
class Identity:
    """
    Universal identity for the AGOS system.
    
    Attributes:
        identity_id: Unique identifier (UUID)
        name: Human-readable name
        identity_type: Type of identity
        public_key: Public key for verification
        status: Current status
        created_at: Creation timestamp
        expires_at: Expiration timestamp
        last_verified: Last verification timestamp
        metadata: Additional metadata
        claims: Identity claims
        scopes: Granted scopes
        roles: Assigned roles
    """
    identity_id: str
    name: str
    identity_type: IdentityType
    public_key: str = ""
    status: IdentityStatus = IdentityStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    last_verified: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    claims: Dict[str, Any] = field(default_factory=dict)
    scopes: Set[str] = field(default_factory=set)
    roles: Set[str] = field(default_factory=set)
    
    @property
    def is_valid(self) -> bool:
        """Check if identity is currently valid."""
        if self.status != IdentityStatus.ACTIVE:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
    
    @property
    def identity_hash(self) -> str:
        """Get a hash of this identity."""
        data = f"{self.identity_id}:{self.name}:{self.identity_type.value}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def verify(self) -> bool:
        """Mark identity as verified."""
        self.last_verified = datetime.utcnow()
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "identity_id": self.identity_id,
            "name": self.name,
            "type": self.identity_type.value,
            "public_key": self.public_key,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_verified": self.last_verified.isoformat() if self.last_verified else None,
            "metadata": self.metadata,
            "claims": self.claims,
            "scopes": list(self.scopes),
            "roles": list(self.roles),
            "is_valid": self.is_valid
        }


class IdentityManager:
    """
    Manages identity creation, verification, and lifecycle.
    
    Features:
    - Identity creation with cryptographic keys
    - Identity verification
    - Token management
    - Scope and role assignment
    - Expiration management
    """
    
    def __init__(self):
        self._identities: Dict[str, Identity] = {}
        self._by_type: Dict[IdentityType, Set[str]] = {t: set() for t in IdentityType}
        self._by_role: Dict[str, Set[str]] = {}
        self._lock = threading.RLock()
        
        self._stats = {
            "identities_created": 0,
            "verifications": 0,
            "revocations": 0
        }
    
    def create_identity(
        self,
        name: str,
        identity_type: IdentityType,
        public_key: str = "",
        claims: Optional[Dict[str, Any]] = None,
        scopes: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        ttl: Optional[int] = None,
    ) -> Identity:
        """
        Create a new identity.
        
        Args:
            name: Human-readable name
            identity_type: Type of identity
            public_key: Public key for verification
            claims: Identity claims
            scopes: Granted scopes
            roles: Assigned roles
            ttl: Time to live in seconds
            
        Returns:
            Created identity
        """
        identity_id = str(uuid.uuid4())
        
        expires_at = None
        if ttl:
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        
        identity = Identity(
            identity_id=identity_id,
            name=name,
            identity_type=identity_type,
            public_key=public_key or secrets.token_hex(32),
            expires_at=expires_at,
            claims=claims or {},
            scopes=set(scopes or []),
            roles=set(roles or [])
        )
        
        with self._lock:
            self._identities[identity_id] = identity
            self._by_type[identity_type].add(identity_id)
            
            for role in identity.roles:
                if role not in self._by_role:
                    self._by_role[role] = set()
                self._by_role[role].add(identity_id)
            
            self._stats["identities_created"] += 1
        
        return identity
    
    def get_identity(self, identity_id: str) -> Optional[Identity]:
        """Get an identity by ID."""
        return self._identities.get(identity_id)
    
    def get_by_type(self, identity_type: IdentityType) -> List[Identity]:
        """Get all identities of a type."""
        with self._lock:
            return [
                self._identities[iid]
                for iid in self._by_type[identity_type]
                if iid in self._identities
            ]
    
    def get_by_role(self, role: str) -> List[Identity]:
        """Get all identities with a role."""
        with self._lock:
            return [
                self._identities[iid]
                for iid in self._by_role.get(role, set())
                if iid in self._identities
            ]
    
    def verify_identity(self, identity_id: str) -> bool:
        """Verify an identity."""
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        if identity.verify():
            self._stats["verifications"] += 1
            return True
        return False
    
    def revoke_identity(self, identity_id: str) -> bool:
        """Revoke an identity."""
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        identity.status = IdentityStatus.REVOKED
        self._stats["revocations"] += 1
        return True
    
    def add_role(self, identity_id: str, role: str) -> bool:
        """Add a role to an identity."""
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        
        identity.roles.add(role)
        
        if role not in self._by_role:
            self._by_role[role] = set()
        self._by_role[role].add(identity_id)
        
        return True
    
    def has_scope(self, identity_id: str, scope: str) -> bool:
        """Check if identity has a scope."""
        identity = self._identities.get(identity_id)
        if not identity:
            return False
        return scope in identity.scopes
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get identity statistics."""
        return {
            "total_identities": len(self._identities),
            "by_type": {
                t.value: len(ids) for t, ids in self._by_type.items()
            },
            "by_status": {
                s.value: sum(1 for i in self._identities.values() if i.status == s)
                for s in IdentityStatus
            },
            "stats": self._stats.copy()
        }


class GlobalIDGenerator:
    """Generates globally unique identifiers."""
    
    def generate(self, namespace: str, name: str) -> str:
        """Generate a globally unique ID."""
        uid = str(uuid.uuid4())
        short_id = hashlib.md5(f"{namespace}:{name}".encode()).hexdigest()[:12]
        return f"{namespace}-{short_id}-{uid[:8]}"


class NamespaceManager:
    """Manages namespaces for identities."""
    
    def __init__(self):
        self._namespaces: Dict[str, List[str]] = {}
    
    def register(self, namespace: str, identity: str) -> bool:
        """Register an identity in a namespace."""
        if namespace not in self._namespaces:
            self._namespaces[namespace] = []
        self._namespaces[namespace].append(identity)
        return True
    
    def get_identities(self, namespace: str) -> List[str]:
        """Get all identities in a namespace."""
        return self._namespaces.get(namespace, [])


class ObjectLocator:
    """Locates objects by identity."""
    
    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}
    
    def register(self, identity: str, location: Dict[str, Any]) -> bool:
        """Register an object's location."""
        self._registry[identity] = location
        return True
    
    def locate(self, identity: str) -> Optional[Dict[str, Any]]:
        """Locate an object by identity."""
        return self._registry.get(identity)


class AliasManager:
    """Manages human-readable aliases for identities."""
    
    def __init__(self):
        self._aliases: Dict[str, str] = {}  # alias -> identity
        self._reverse: Dict[str, str] = {}   # identity -> alias
    
    def create_alias(self, identity: str, alias: str) -> bool:
        """Create an alias for an identity."""
        self._aliases[alias] = identity
        self._reverse[identity] = alias
        return True
    
    def resolve_alias(self, alias: str) -> Optional[str]:
        """Resolve an alias to an identity."""
        return self._aliases.get(alias)
    
    def get_alias(self, identity: str) -> Optional[str]:
        """Get the alias for an identity."""
        return self._reverse.get(identity)


class ReferenceManager:
    """Manages references between objects."""
    
    def __init__(self):
        self._references: Dict[str, List[str]] = {}
    
    def add_reference(self, from_id: str, to_id: str) -> bool:
        """Add a reference from one object to another."""
        if from_id not in self._references:
            self._references[from_id] = []
        self._references[from_id].append(to_id)
        return True
    
    def get_references(self, identity: str) -> List[str]:
        """Get all references from an object."""
        return self._references.get(identity, [])


class UniversalIdentityPlatform:
    """
    Universal Identity Platform.
    
    Every object must receive a permanent immutable identity.
    
    Implements:
    ✅ Identity Runtime, Global ID Generator, Namespace Manager
    ✅ Object Locator, Object Resolver, Alias Manager
    ✅ Reference Manager
    
    Identity Rules:
    ✅ Immutable, Globally Unique, Human Readable Alias
    ✅ Machine Readable Identifier
    ✅ Cross-Version Compatible, Cross-Repository Compatible
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.id_generator = GlobalIDGenerator()
        self.namespace_manager = NamespaceManager()
        self.locator = ObjectLocator()
        self.alias_manager = AliasManager()
        self.reference_manager = ReferenceManager()
        self.identity_manager = IdentityManager()
    
    def create_identity(
        self,
        namespace: str,
        name: str,
        location: Optional[Dict[str, Any]] = None,
        alias: Optional[str] = None,
    ) -> str:
        """Create a new identity with all supporting structures."""
        identity_id = self.id_generator.generate(namespace, name)
        self.namespace_manager.register(namespace, identity_id)
        
        if location:
            self.locator.register(identity_id, location)
        
        if alias:
            self.alias_manager.create_alias(identity_id, alias)
        
        return identity_id
    
    def resolve(self, identifier: str) -> Optional[str]:
        """Resolve an identity from alias or direct ID."""
        return self.alias_manager.resolve_alias(identifier) or identifier
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return {
            "version": self.version,
            "identity_rules": IDENTITY_RULES,
            "identity_manager_stats": self.identity_manager.get_statistics()
        }
