"""Universal Organization Runtime."""
import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class OrganizationType(Enum):
    """Organization type."""
    BUSINESS_UNIT = "business_unit"
    DEPARTMENT = "department"
    TEAM = "team"
    PROJECT = "project"


@dataclass
class Role:
    """Organization role."""
    id: str
    name: str
    permissions: List[str] = field(default_factory=list)


@dataclass
class User:
    """Organization user."""
    id: str
    name: str
    email: str
    roles: List[str] = field(default_factory=list)


@dataclass
class Policy:
    """Organization policy."""
    id: str
    name: str
    description: str
    rules: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Organization:
    """Universal Organization."""
    id: str
    name: str
    org_type: OrganizationType
    description: str = ""
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    users: List[str] = field(default_factory=list)
    roles: List[Role] = field(default_factory=list)
    policies: List[Policy] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    budgets: Dict[str, float] = field(default_factory=dict)
    knowledge_base: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class OrganizationRuntime:
    """Universal Organization Runtime."""
    
    def __init__(self):
        """Initialize organization runtime."""
        self.organizations: Dict[str, Organization] = {}
        self.users: Dict[str, User] = {}
    
    def create_organization(
        self,
        name: str,
        org_type: OrganizationType,
        description: str = "",
        parent_id: Optional[str] = None,
    ) -> Organization:
        """Create an organization."""
        org_id = self._generate_id(name)
        
        org = Organization(
            id=org_id,
            name=name,
            org_type=org_type,
            description=description,
            parent_id=parent_id,
        )
        
        self.organizations[org_id] = org
        
        # Add to parent's children
        if parent_id and parent_id in self.organizations:
            self.organizations[parent_id].children.append(org_id)
        
        return org
    
    def add_user(self, org_id: str, user: User) -> bool:
        """Add a user to organization."""
        org = self.organizations.get(org_id)
        if not org:
            return False
        
        self.users[user.id] = user
        org.users.append(user.id)
        return True
    
    def add_role(self, org_id: str, role: Role) -> bool:
        """Add a role to organization."""
        org = self.organizations.get(org_id)
        if not org:
            return False
        
        org.roles.append(role)
        return True
    
    def add_policy(self, org_id: str, policy: Policy) -> bool:
        """Add a policy to organization."""
        org = self.organizations.get(org_id)
        if not org:
            return False
        
        org.policies.append(policy)
        return True
    
    def get_organization(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID."""
        return self.organizations.get(org_id)
    
    def list_organizations(
        self,
        org_type: Optional[OrganizationType] = None,
    ) -> List[Organization]:
        """List organizations."""
        orgs = list(self.organizations.values())
        
        if org_type:
            orgs = [o for o in orgs if o.org_type == org_type]
        
        return orgs
    
    def get_organization_graph(self, org_id: str) -> Dict[str, Any]:
        """Get organization hierarchy graph."""
        org = self.organizations.get(org_id)
        if not org:
            return {}
        
        children = []
        for child_id in org.children:
            child = self.organizations.get(child_id)
            if child:
                children.append(self.get_organization_graph(child_id))
        
        return {
            "id": org.id,
            "name": org.name,
            "type": org.org_type.value,
            "children": children,
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get organization statistics."""
        by_type = {}
        for org in self.organizations.values():
            type_name = org.org_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        return {
            "total_organizations": len(self.organizations),
            "by_type": by_type,
            "total_users": len(self.users),
        }
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
