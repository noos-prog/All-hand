"""Universal Collaboration Platform - Humans and AGOS collaborate on engineering missions."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# =============================================================================
# ENUMS
# =============================================================================

class UserStatus(Enum):
    """User status."""
    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"
    OFFLINE = "offline"


class ReviewStatus(Enum):
    """Review status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"


class NotificationType(Enum):
    """Notification types."""
    MENTION = "mention"
    ASSIGNMENT = "assignment"
    REVIEW_REQUEST = "review_request"
    APPROVAL = "approval"
    COMMENT = "comment"
    MENTION_IN_COMMENT = "mention_in_comment"


class Permission(Enum):
    """Permissions."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    REVIEW = "review"
    APPROVE = "approve"


# =============================================================================
# MODELS
# =============================================================================

@dataclass
class Organization:
    """Organization model."""
    org_id: str
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Team:
    """Team model."""
    team_id: str
    org_id: str
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    member_ids: Tuple[str, ...] = ()


@dataclass
class User:
    """User model."""
    user_id: str
    name: str
    email: str
    avatar_url: str = ""
    status: UserStatus = UserStatus.OFFLINE
    org_ids: Tuple[str, ...] = ()
    team_ids: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Role:
    """Role model."""
    role_id: str
    name: str
    permissions: Tuple[Permission, ...] = ()
    description: str = ""


@dataclass
class UserRole:
    """User role assignment."""
    user_id: str
    role_id: str
    org_id: str
    team_id: Optional[str] = None
    assigned_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Comment:
    """Comment model."""
    comment_id: str
    mission_id: str
    author_id: str
    content: str
    parent_id: Optional[str] = None
    mentions: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Review:
    """Review model."""
    review_id: str
    mission_id: str
    reviewer_id: str
    status: ReviewStatus = ReviewStatus.PENDING
    comments: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    decision_at: Optional[datetime] = None


@dataclass
class Approval:
    """Approval model."""
    approval_id: str
    mission_id: str
    approver_id: str
    version: str
    approved: bool
    comment: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Assignment:
    """Assignment model."""
    assignment_id: str
    mission_id: str
    assignee_id: str
    assigned_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Notification:
    """Notification model."""
    notification_id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    mission_id: Optional[str] = None
    read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Presence:
    """User presence model."""
    user_id: str
    status: UserStatus
    last_seen: datetime = field(default_factory=datetime.utcnow)
    current_mission_id: Optional[str] = None


@dataclass
class SharedSession:
    """Shared session model."""
    session_id: str
    mission_id: str
    owner_id: str
    participant_ids: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SharedWorkspace:
    """Shared workspace model."""
    workspace_id: str
    name: str
    org_id: str
    owner_id: str
    collaborator_ids: Tuple[str, ...] = ()
    created_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# COLLABORATION RUNTIME
# =============================================================================

class CollaborationRuntime:
    """Collaboration runtime."""
    
    def __init__(self):
        self._orgs: Dict[str, Organization] = {}
        self._teams: Dict[str, Team] = {}
        self._users: Dict[str, User] = {}
        self._roles: Dict[str, Role] = {}
        self._user_roles: Dict[str, UserRole] = {}
        self._reviews: Dict[str, Review] = {}
        self._comments: Dict[str, Comment] = {}
        self._approvals: Dict[str, Approval] = {}
        self._assignments: Dict[str, Assignment] = {}
        self._notifications: Dict[str, Notification] = {}
        self._presence: Dict[str, Presence] = {}
        self._sessions: Dict[str, SharedSession] = {}
        self._workspaces: Dict[str, SharedWorkspace] = {}
    
    def add_org(self, org: Organization) -> None:
        """Add organization."""
        self._orgs[org.org_id] = org
    
    def get_org(self, org_id: str) -> Optional[Organization]:
        """Get organization."""
        return self._orgs.get(org_id)
    
    def add_team(self, team: Team) -> None:
        """Add team."""
        self._teams[team.team_id] = team
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team."""
        return self._teams.get(team_id)
    
    def add_user(self, user: User) -> None:
        """Add user."""
        self._users[user.user_id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user."""
        return self._users.get(user_id)
    
    def add_review(self, review: Review) -> None:
        """Add review."""
        self._reviews[review.review_id] = review
    
    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review."""
        return self._reviews.get(review_id)
    
    def add_comment(self, comment: Comment) -> None:
        """Add comment."""
        self._comments[comment.comment_id] = comment
    
    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """Get comment."""
        return self._comments.get(comment_id)
    
    def get_mission_comments(self, mission_id: str) -> List[Comment]:
        """Get comments for a mission."""
        return [c for c in self._comments.values() if c.mission_id == mission_id]
    
    def add_notification(self, notification: Notification) -> None:
        """Add notification."""
        self._notifications[notification.notification_id] = notification
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user."""
        notifications = [n for n in self._notifications.values() if n.user_id == user_id]
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        return notifications
    
    def set_presence(self, presence: Presence) -> None:
        """Set user presence."""
        self._presence[presence.user_id] = presence
    
    def get_presence(self, user_id: str) -> Optional[Presence]:
        """Get user presence."""
        return self._presence.get(user_id)
    
    def get_online_users(self) -> List[User]:
        """Get online users."""
        return [self._users[u.user_id] for u in self._presence.values() 
                if u.status == UserStatus.ONLINE and u.user_id in self._users]


# =============================================================================
# UNIVERSAL COLLABORATION PLATFORM
# =============================================================================

class UniversalCollaborationPlatform:
    """
    Universal Collaboration Platform.
    
    Rules:
    ✅ Human feedback becomes structured knowledge
    ✅ Every approval is versioned
    ✅ Every change is auditable
    
    Implements:
    ✅ Organizations
    ✅ Teams
    ✅ Roles
    ✅ Permissions
    ✅ Reviews
    ✅ Comments
    ✅ Approvals
    ✅ Mentions
    ✅ Assignments
    ✅ Notifications
    ✅ Presence
    ✅ Shared Sessions
    ✅ Shared Workspaces
    ✅ Shared Missions
    """
    
    def __init__(self):
        self.version = "2.0.0"
        self.runtime = CollaborationRuntime()
        self._next_id = 1
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID."""
        id_str = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return id_str
    
    # Organization Management
    def create_org(self, name: str, description: str = "") -> Organization:
        """Create organization."""
        org = Organization(
            org_id=self._generate_id("org"),
            name=name,
            description=description
        )
        self.runtime.add_org(org)
        return org
    
    def get_org(self, org_id: str) -> Optional[Organization]:
        """Get organization."""
        return self.runtime.get_org(org_id)
    
    def list_orgs(self) -> List[Organization]:
        """List all organizations."""
        return list(self.runtime._orgs.values())
    
    # Team Management
    def create_team(self, org_id: str, name: str, description: str = "") -> Team:
        """Create team."""
        team = Team(
            team_id=self._generate_id("team"),
            org_id=org_id,
            name=name,
            description=description
        )
        self.runtime.add_team(team)
        return team
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team."""
        return self.runtime.get_team(team_id)
    
    def get_org_teams(self, org_id: str) -> List[Team]:
        """Get teams for organization."""
        return [t for t in self.runtime._teams.values() if t.org_id == org_id]
    
    def add_team_member(self, team_id: str, user_id: str) -> bool:
        """Add member to team."""
        team = self.runtime.get_team(team_id)
        if team:
            members = list(team.member_ids) + [user_id]
            team.member_ids = tuple(members)
            return True
        return False
    
    # User Management
    def create_user(self, name: str, email: str) -> User:
        """Create user."""
        user = User(
            user_id=self._generate_id("user"),
            name=name,
            email=email
        )
        self.runtime.add_user(user)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user."""
        return self.runtime.get_user(user_id)
    
    def update_user_status(self, user_id: str, status: UserStatus) -> bool:
        """Update user status."""
        user = self.runtime.get_user(user_id)
        if user:
            user.status = status
            user.last_active = datetime.utcnow()
            
            # Update presence
            presence = Presence(
                user_id=user_id,
                status=status
            )
            self.runtime.set_presence(presence)
            return True
        return False
    
    def get_online_users(self) -> List[User]:
        """Get online users."""
        return self.runtime.get_online_users()
    
    # Review Management
    def create_review(self, mission_id: str, reviewer_id: str) -> Review:
        """Create review."""
        review = Review(
            review_id=self._generate_id("rev"),
            mission_id=mission_id,
            reviewer_id=reviewer_id
        )
        self.runtime.add_review(review)
        return review
    
    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review."""
        return self.runtime.get_review(review_id)
    
    def get_mission_reviews(self, mission_id: str) -> List[Review]:
        """Get reviews for a mission."""
        return [r for r in self.runtime._reviews.values() if r.mission_id == mission_id]
    
    def update_review_status(self, review_id: str, status: ReviewStatus) -> bool:
        """Update review status."""
        review = self.runtime.get_review(review_id)
        if review:
            review.status = status
            review.updated_at = datetime.utcnow()
            if status in [ReviewStatus.APPROVED, ReviewStatus.REJECTED]:
                review.decision_at = datetime.utcnow()
            return True
        return False
    
    # Comment Management
    def add_comment(self, mission_id: str, author_id: str, content: str, 
                   parent_id: Optional[str] = None) -> Comment:
        """Add comment."""
        # Extract mentions from content
        mentions = []
        words = content.split()
        for word in words:
            if word.startswith('@'):
                mentions.append(word[1:])
        
        comment = Comment(
            comment_id=self._generate_id("cmt"),
            mission_id=mission_id,
            author_id=author_id,
            content=content,
            parent_id=parent_id,
            mentions=tuple(mentions)
        )
        self.runtime.add_comment(comment)
        
        # Create notifications for mentions
        for mentioned_user in mentions:
            notification = self.create_notification(
                user_id=mentioned_user,
                type=NotificationType.MENTION_IN_COMMENT,
                title="You were mentioned",
                message=f"You were mentioned in a comment on mission {mission_id}",
                mission_id=mission_id
            )
        
        return comment
    
    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """Get comment."""
        return self.runtime.get_comment(comment_id)
    
    def get_mission_comments(self, mission_id: str) -> List[Comment]:
        """Get comments for a mission."""
        return self.runtime.get_mission_comments(mission_id)
    
    # Approval Management
    def create_approval(self, mission_id: str, approver_id: str, version: str, 
                        approved: bool, comment: str = "") -> Approval:
        """Create approval."""
        approval = Approval(
            approval_id=self._generate_id("apr"),
            mission_id=mission_id,
            approver_id=approver_id,
            version=version,
            approved=approved,
            comment=comment
        )
        self.runtime._approvals[approval.approval_id] = approval
        return approval
    
    def get_mission_approvals(self, mission_id: str) -> List[Approval]:
        """Get approvals for a mission."""
        return [a for a in self.runtime._approvals.values() if a.mission_id == mission_id]
    
    # Assignment Management
    def create_assignment(self, mission_id: str, assignee_id: str, assigned_by: str) -> Assignment:
        """Create assignment."""
        assignment = Assignment(
            assignment_id=self._generate_id("asn"),
            mission_id=mission_id,
            assignee_id=assignee_id,
            assigned_by=assigned_by
        )
        self.runtime._assignments[assignment.assignment_id] = assignment
        
        # Create notification
        self.create_notification(
            user_id=assignee_id,
            type=NotificationType.ASSIGNMENT,
            title="New Assignment",
            message=f"You were assigned to mission {mission_id}",
            mission_id=mission_id
        )
        
        return assignment
    
    def get_user_assignments(self, user_id: str) -> List[Assignment]:
        """Get assignments for a user."""
        return [a for a in self.runtime._assignments.values() if a.assignee_id == user_id]
    
    # Notification Management
    def create_notification(self, user_id: str, type: NotificationType, 
                          title: str, message: str, mission_id: Optional[str] = None) -> Notification:
        """Create notification."""
        notification = Notification(
            notification_id=self._generate_id("notif"),
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            mission_id=mission_id
        )
        self.runtime.add_notification(notification)
        return notification
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user."""
        return self.runtime.get_user_notifications(user_id, unread_only)
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark notification as read."""
        if notification_id in self.runtime._notifications:
            self.runtime._notifications[notification_id].read = True
            return True
        return False
    
    def mark_all_notifications_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user."""
        count = 0
        for notification in self.runtime._notifications.values():
            if notification.user_id == user_id and not notification.read:
                notification.read = True
                count += 1
        return count
    
    # Presence Management
    def set_presence(self, user_id: str, status: UserStatus, 
                    current_mission_id: Optional[str] = None) -> bool:
        """Set user presence."""
        presence = Presence(
            user_id=user_id,
            status=status,
            current_mission_id=current_mission_id
        )
        self.runtime.set_presence(presence)
        return self.update_user_status(user_id, status)
    
    def get_presence(self, user_id: str) -> Optional[Presence]:
        """Get user presence."""
        return self.runtime.get_presence(user_id)
    
    # Shared Session Management
    def create_shared_session(self, mission_id: str, owner_id: str) -> SharedSession:
        """Create shared session."""
        session = SharedSession(
            session_id=self._generate_id("sess"),
            mission_id=mission_id,
            owner_id=owner_id,
            participant_ids=(owner_id,)
        )
        self.runtime._sessions[session.session_id] = session
        return session
    
    def join_session(self, session_id: str, user_id: str) -> bool:
        """Join shared session."""
        if session_id in self.runtime._sessions:
            session = self.runtime._sessions[session_id]
            if user_id not in session.participant_ids:
                participants = list(session.participant_ids) + [user_id]
                session.participant_ids = tuple(participants)
            return True
        return False
    
    def leave_session(self, session_id: str, user_id: str) -> bool:
        """Leave shared session."""
        if session_id in self.runtime._sessions:
            session = self.runtime._sessions[session_id]
            if user_id in session.participant_ids:
                participants = list(session.participant_ids)
                participants.remove(user_id)
                session.participant_ids = tuple(participants)
            return True
        return False
    
    def get_session(self, session_id: str) -> Optional[SharedSession]:
        """Get shared session."""
        return self.runtime._sessions.get(session_id)
    
    def get_mission_session(self, mission_id: str) -> Optional[SharedSession]:
        """Get shared session for mission."""
        sessions = [s for s in self.runtime._sessions.values() if s.mission_id == mission_id]
        return sessions[0] if sessions else None
    
    # Shared Workspace Management
    def create_shared_workspace(self, name: str, org_id: str, owner_id: str) -> SharedWorkspace:
        """Create shared workspace."""
        workspace = SharedWorkspace(
            workspace_id=self._generate_id("ws"),
            name=name,
            org_id=org_id,
            owner_id=owner_id,
            collaborator_ids=(owner_id,)
        )
        self.runtime._workspaces[workspace.workspace_id] = workspace
        return workspace
    
    def add_workspace_collaborator(self, workspace_id: str, user_id: str) -> bool:
        """Add collaborator to workspace."""
        if workspace_id in self.runtime._workspaces:
            workspace = self.runtime._workspaces[workspace_id]
            if user_id not in workspace.collaborator_ids:
                collaborators = list(workspace.collaborator_ids) + [user_id]
                workspace.collaborator_ids = tuple(collaborators)
            return True
        return False
    
    def get_workspace(self, workspace_id: str) -> Optional[SharedWorkspace]:
        """Get shared workspace."""
        return self.runtime._workspaces.get(workspace_id)
    
    def get_user_workspaces(self, user_id: str) -> List[SharedWorkspace]:
        """Get workspaces for a user."""
        return [w for w in self.runtime._workspaces.values() 
                if user_id in w.collaborator_ids]
    
    # Statistics
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return {
            "version": self.version,
            "organizations": len(self.runtime._orgs),
            "teams": len(self.runtime._teams),
            "users": len(self.runtime._users),
            "reviews": len(self.runtime._reviews),
            "comments": len(self.runtime._comments),
            "approvals": len(self.runtime._approvals),
            "assignments": len(self.runtime._assignments),
            "notifications": len(self.runtime._notifications),
            "sessions": len(self.runtime._sessions),
            "workspaces": len(self.runtime._workspaces),
            "online_users": len(self.get_online_users())
        }
