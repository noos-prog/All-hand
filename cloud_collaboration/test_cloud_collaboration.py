#!/usr/bin/env python3
"""
Cloud Collaboration - Test Suite
=============================

Tests for the AGOS Universal Collaboration Platform.
Run with: python test_cloud_collaboration.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import __init__ as collaboration
from __init__ import (
    UniversalCollaborationPlatform,
    UserStatus, ReviewStatus, NotificationType, Permission,
    Organization, Team, User, Review, Comment, Assignment, Notification
)


def test_organization():
    """Test organization management."""
    print("\n=== Testing Organization Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create organization
    org = platform.create_org("AGOS Inc", "Autonomous Engineering Company")
    print(f"  Created org: {org.name}")
    
    # Get organization
    org2 = platform.get_org(org.org_id)
    print(f"  Retrieved org: {org2.name if org2 else 'None'}")
    
    # List organizations
    orgs = platform.list_orgs()
    print(f"  Total orgs: {len(orgs)}")
    
    print("  ✓ Organization management passed")


def test_team():
    """Test team management."""
    print("\n=== Testing Team Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create org
    org = platform.create_org("Test Org")
    
    # Create teams
    team1 = platform.create_team(org.org_id, "Backend Team", "Backend developers")
    team2 = platform.create_team(org.org_id, "Frontend Team", "Frontend developers")
    print(f"  Created teams: {team1.name}, {team2.name}")
    
    # Get team
    team = platform.get_team(team1.team_id)
    print(f"  Retrieved team: {team.name if team else 'None'}")
    
    # List org teams
    teams = platform.get_org_teams(org.org_id)
    print(f"  Org teams: {len(teams)}")
    
    # Add member
    platform.add_team_member(team1.team_id, "user_1")
    team = platform.get_team(team1.team_id)
    print(f"  Team members: {len(team.member_ids)}")
    
    print("  ✓ Team management passed")


def test_user():
    """Test user management."""
    print("\n=== Testing User Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create users
    user1 = platform.create_user("Alice", "alice@example.com")
    user2 = platform.create_user("Bob", "bob@example.com")
    print(f"  Created users: {user1.name}, {user2.name}")
    
    # Get user
    user = platform.get_user(user1.user_id)
    print(f"  Retrieved user: {user.name if user else 'None'}")
    
    # Update status
    platform.update_user_status(user1.user_id, UserStatus.ONLINE)
    user = platform.get_user(user1.user_id)
    print(f"  User status: {user.status.value}")
    
    print("  ✓ User management passed")


def test_review():
    """Test review management."""
    print("\n=== Testing Review Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create users
    user1 = platform.create_user("Reviewer", "reviewer@example.com")
    
    # Create review
    review = platform.create_review("mission_123", user1.user_id)
    print(f"  Created review: {review.review_id}")
    
    # Get review
    rev = platform.get_review(review.review_id)
    print(f"  Retrieved review: {rev.review_id if rev else 'None'}")
    
    # Update status
    platform.update_review_status(review.review_id, ReviewStatus.APPROVED)
    rev = platform.get_review(review.review_id)
    print(f"  Review status: {rev.status.value}")
    
    # Get mission reviews
    reviews = platform.get_mission_reviews("mission_123")
    print(f"  Mission reviews: {len(reviews)}")
    
    print("  ✓ Review management passed")


def test_comment():
    """Test comment management."""
    print("\n=== Testing Comment Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create user
    user = platform.create_user("Commenter", "commenter@example.com")
    
    # Add comment
    comment = platform.add_comment(
        mission_id="mission_123",
        author_id=user.user_id,
        content="This looks good! @alice please review."
    )
    print(f"  Created comment: {comment.comment_id}")
    print(f"  Mentions: {comment.mentions}")
    
    # Get comment
    cmt = platform.get_comment(comment.comment_id)
    print(f"  Retrieved comment: {cmt.content[:20]}...")
    
    # Get mission comments
    comments = platform.get_mission_comments("mission_123")
    print(f"  Mission comments: {len(comments)}")
    
    print("  ✓ Comment management passed")


def test_approval():
    """Test approval management."""
    print("\n=== Testing Approval Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create user
    user = platform.create_user("Approver", "approver@example.com")
    
    # Create approval
    approval = platform.create_approval(
        mission_id="mission_123",
        approver_id=user.user_id,
        version="v1.0",
        approved=True,
        comment="LGTM!"
    )
    print(f"  Created approval: {approval.approval_id}")
    print(f"  Approved: {approval.approved}")
    
    # Get mission approvals
    approvals = platform.get_mission_approvals("mission_123")
    print(f"  Mission approvals: {len(approvals)}")
    
    print("  ✓ Approval management passed")


def test_assignment():
    """Test assignment management."""
    print("\n=== Testing Assignment Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create users
    manager = platform.create_user("Manager", "manager@example.com")
    developer = platform.create_user("Developer", "dev@example.com")
    
    # Create assignment
    assignment = platform.create_assignment(
        mission_id="mission_123",
        assignee_id=developer.user_id,
        assigned_by=manager.user_id
    )
    print(f"  Created assignment: {assignment.assignment_id}")
    
    # Get user assignments
    assignments = platform.get_user_assignments(developer.user_id)
    print(f"  User assignments: {len(assignments)}")
    
    print("  ✓ Assignment management passed")


def test_notification():
    """Test notification management."""
    print("\n=== Testing Notification Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create user
    user = platform.create_user("Notifier", "notifier@example.com")
    
    # Create notification
    notification = platform.create_notification(
        user_id=user.user_id,
        type=NotificationType.ASSIGNMENT,
        title="New Task",
        message="You have a new task assigned",
        mission_id="mission_123"
    )
    print(f"  Created notification: {notification.notification_id}")
    
    # Get notifications
    notifications = platform.get_user_notifications(user.user_id)
    print(f"  User notifications: {len(notifications)}")
    
    # Get unread notifications
    unread = platform.get_user_notifications(user.user_id, unread_only=True)
    print(f"  Unread notifications: {len(unread)}")
    
    # Mark as read
    platform.mark_notification_read(notification.notification_id)
    unread = platform.get_user_notifications(user.user_id, unread_only=True)
    print(f"  Unread after mark: {len(unread)}")
    
    print("  ✓ Notification management passed")


def test_presence():
    """Test presence management."""
    print("\n=== Testing Presence Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create user
    user = platform.create_user("Presence", "presence@example.com")
    
    # Set presence
    platform.set_presence(user.user_id, UserStatus.ONLINE, "mission_123")
    presence = platform.get_presence(user.user_id)
    print(f"  Presence status: {presence.status.value}")
    print(f"  Current mission: {presence.current_mission_id}")
    
    # Get online users
    online = platform.get_online_users()
    print(f"  Online users: {len(online)}")
    
    print("  ✓ Presence management passed")


def test_shared_session():
    """Test shared session management."""
    print("\n=== Testing Shared Session Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create users
    owner = platform.create_user("Owner", "owner@example.com")
    participant = platform.create_user("Participant", "participant@example.com")
    
    # Create session
    session = platform.create_shared_session("mission_123", owner.user_id)
    print(f"  Created session: {session.session_id}")
    print(f"  Participants: {len(session.participant_ids)}")
    
    # Join session
    platform.join_session(session.session_id, participant.user_id)
    session = platform.get_session(session.session_id)
    print(f"  After join: {len(session.participant_ids)}")
    
    # Leave session
    platform.leave_session(session.session_id, participant.user_id)
    session = platform.get_session(session.session_id)
    print(f"  After leave: {len(session.participant_ids)}")
    
    # Get mission session
    mission_session = platform.get_mission_session("mission_123")
    print(f"  Mission session: {mission_session.session_id if mission_session else 'None'}")
    
    print("  ✓ Shared session management passed")


def test_shared_workspace():
    """Test shared workspace management."""
    print("\n=== Testing Shared Workspace Management ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create org and users
    org = platform.create_org("Test Org")
    owner = platform.create_user("Owner", "owner@example.com")
    collaborator = platform.create_user("Collaborator", "collab@example.com")
    
    # Create workspace
    workspace = platform.create_shared_workspace("My Workspace", org.org_id, owner.user_id)
    print(f"  Created workspace: {workspace.name}")
    print(f"  Collaborators: {len(workspace.collaborator_ids)}")
    
    # Add collaborator
    platform.add_workspace_collaborator(workspace.workspace_id, collaborator.user_id)
    workspace = platform.get_workspace(workspace.workspace_id)
    print(f"  After add: {len(workspace.collaborator_ids)}")
    
    # Get user workspaces
    workspaces = platform.get_user_workspaces(owner.user_id)
    print(f"  User workspaces: {len(workspaces)}")
    
    print("  ✓ Shared workspace management passed")


def test_statistics():
    """Test statistics."""
    print("\n=== Testing Statistics ===")
    
    platform = collaboration.UniversalCollaborationPlatform()
    
    # Create some data
    platform.create_org("Test Org")
    user = platform.create_user("Stats", "stats@example.com")
    platform.create_team("org_1", "Test Team")
    platform.add_comment("mission_1", user.user_id, "Test comment")
    platform.set_presence(user.user_id, UserStatus.ONLINE)
    
    # Get statistics
    stats = platform.get_statistics()
    print(f"  Version: {stats['version']}")
    print(f"  Organizations: {stats['organizations']}")
    print(f"  Users: {stats['users']}")
    print(f"  Teams: {stats['teams']}")
    print(f"  Comments: {stats['comments']}")
    print(f"  Online users: {stats['online_users']}")
    
    print("  ✓ Statistics passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLOUD COLLABORATION - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_organization()
        test_team()
        test_user()
        test_review()
        test_comment()
        test_approval()
        test_assignment()
        test_notification()
        test_presence()
        test_shared_session()
        test_shared_workspace()
        test_statistics()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
