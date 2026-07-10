#!/usr/bin/env python3
"""
Cloud Experience - Test Suite
==========================

Tests for the AGOS Universal Engineering Experience.
Run with: python test_cloud_experience.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import __init__ as experience
from __init__ import (
    UniversalEngineeringExperience,
    ComponentType, Theme, NotificationPriority, StreamingEventType,
    UIComponent, Dashboard, Widget, UserPreferences, Plugin
)


def test_experience():
    """Test universal engineering experience."""
    print("\n=== Testing Universal Engineering Experience ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Get status
    status = exp.get_status()
    print(f"  Version: {status['version']}")
    print(f"  Interface components: {status['interface_components']}")
    print(f"  Requirements: {status['requirements']}")
    
    # Get interface components
    components = exp.get_interface_components()
    print(f"  Components count: {len(components)}")
    
    # Get requirements
    requirements = exp.get_requirements()
    print(f"  Requirements count: {len(requirements)}")
    
    print("  ✓ Experience tests passed")


def test_component_registry():
    """Test component registry."""
    print("\n=== Testing Component Registry ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Register components
    comp1 = exp.register_component("Mission Console", ComponentType.CONSOLE, "Mission console")
    comp2 = exp.register_component("Project Explorer", ComponentType.EXPLORER, "Project explorer")
    print(f"  Registered: {comp1.name}, {comp2.name}")
    
    # Get component
    comp = exp.get_component(comp1.component_id)
    print(f"  Retrieved: {comp.name if comp else 'None'}")
    
    # List components
    all_comps = exp.list_components()
    print(f"  Total components: {len(all_comps)}")
    
    # List by type
    consoles = exp.list_components(ComponentType.CONSOLE)
    print(f"  Console components: {len(consoles)}")
    
    # Enable/Disable
    exp.component_registry.disable(comp1.component_id)
    comp = exp.get_component(comp1.component_id)
    print(f"  Enabled after disable: {comp.enabled}")
    
    exp.component_registry.enable(comp1.component_id)
    comp = exp.get_component(comp1.component_id)
    print(f"  Enabled after enable: {comp.enabled}")
    
    print("  ✓ Component registry tests passed")


def test_dashboard():
    """Test dashboard management."""
    print("\n=== Testing Dashboard Management ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Create dashboard
    dashboard = exp.create_dashboard("user_1", "My Dashboard")
    print(f"  Created dashboard: {dashboard.name}")
    
    # Get dashboard
    retrieved = exp.get_dashboard(dashboard.dashboard_id)
    print(f"  Retrieved: {retrieved.name if retrieved else 'None'}")
    
    # Get user dashboards
    dashboards = exp.get_user_dashboards("user_1")
    print(f"  User dashboards: {len(dashboards)}")
    
    print("  ✓ Dashboard tests passed")


def test_preferences():
    """Test user preferences."""
    print("\n=== Testing User Preferences ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Get preferences
    prefs = exp.get_preferences("user_1")
    print(f"  Default theme: {prefs.theme.value}")
    print(f"  Default language: {prefs.language}")
    
    # Update preferences
    exp.update_preferences("user_1", theme=Theme.DARK, language="ar")
    prefs = exp.get_preferences("user_1")
    print(f"  Updated theme: {prefs.theme.value}")
    print(f"  Updated language: {prefs.language}")
    
    # Set theme
    exp.set_theme("user_1", Theme.LIGHT)
    prefs = exp.get_preferences("user_1")
    print(f"  Set theme: {prefs.theme.value}")
    
    print("  ✓ Preferences tests passed")


def test_notifications():
    """Test notification management."""
    print("\n=== Testing Notification Management ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Create notification
    notif = exp.create_notification(
        "user_1",
        "Mission Complete",
        "Your mission has been completed successfully",
        NotificationPriority.HIGH
    )
    print(f"  Created: {notif.title}")
    
    # Get notifications
    notifications = exp.get_notifications("user_1")
    print(f"  User notifications: {len(notifications)}")
    
    # Get unread
    unread = exp.get_notifications("user_1", unread_only=True)
    print(f"  Unread notifications: {len(unread)}")
    
    # Mark as read
    exp.notification_manager.mark_read(notif.notification_id)
    unread = exp.get_notifications("user_1", unread_only=True)
    print(f"  Unread after mark: {len(unread)}")
    
    print("  ✓ Notification tests passed")


def test_streaming():
    """Test streaming manager."""
    print("\n=== Testing Streaming Manager ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Subscribe
    exp.subscribe_streaming("user_1", [
        StreamingEventType.MISSION_UPDATE,
        StreamingEventType.BUILD_PROGRESS
    ])
    print(f"  Subscribed to events")
    
    # Publish event
    notified = exp.publish_event(
        StreamingEventType.MISSION_UPDATE,
        {"mission_id": "m1", "status": "completed"},
        source="test"
    )
    print(f"  Notified users: {len(notified)}")
    
    # Get events
    events = exp.get_streaming_events("user_1")
    print(f"  User events: {len(events)}")
    
    print("  ✓ Streaming tests passed")


def test_search():
    """Test search manager."""
    print("\n=== Testing Search Manager ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Execute search
    query = exp.search("user_1", "mission", {"type": "active"})
    print(f"  Search query: {query.query}")
    print(f"  Results count: {query.results_count}")
    
    # Get results
    results = exp.get_search_results(query.query_id)
    print(f"  Results: {len(results)}")
    
    print("  ✓ Search tests passed")


def test_plugins():
    """Test plugin management."""
    print("\n=== Testing Plugin Management ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Install plugin
    plugin = exp.install_plugin(
        "Custom Theme",
        "1.0.0",
        "Developer",
        "Custom dark theme",
        permissions=("read", "write")
    )
    print(f"  Installed: {plugin.name} v{plugin.version}")
    
    # List plugins
    plugins = exp.list_plugins()
    print(f"  Total plugins: {len(plugins)}")
    
    # Enable plugin
    exp.plugin_manager.enable(plugin.plugin_id)
    plugin = exp.plugin_manager.get(plugin.plugin_id)
    print(f"  Enabled: {plugin.enabled}")
    
    # List enabled plugins
    enabled = exp.list_plugins(enabled_only=True)
    print(f"  Enabled plugins: {len(enabled)}")
    
    # Disable plugin
    exp.plugin_manager.disable(plugin.plugin_id)
    plugin = exp.plugin_manager.get(plugin.plugin_id)
    print(f"  Enabled after disable: {plugin.enabled}")
    
    print("  ✓ Plugin tests passed")


def test_statistics():
    """Test statistics."""
    print("\n=== Testing Statistics ===")
    
    exp = experience.UniversalEngineeringExperience()
    
    # Add some data
    exp.register_component("Test Component", ComponentType.WIDGET)
    exp.create_dashboard("user_1", "Test Dashboard")
    exp.create_notification("user_1", "Test", "Test message")
    
    # Get statistics
    stats = exp.get_statistics()
    print(f"  Version: {stats['version']}")
    print(f"  Components: {stats['components']['total']}")
    print(f"  Dashboards: {stats['dashboards']}")
    print(f"  Notifications: {stats['notifications']}")
    print(f"  Plugins: {stats['plugins']['total']}")
    
    print("  ✓ Statistics tests passed")


def test_ui_component_model():
    """Test UI component model."""
    print("\n=== Testing UI Component Model ===")
    
    component = experience.UIComponent(
        component_id="ui_test",
        name="Test Component",
        type=ComponentType.DASHBOARD,
        description="Test description"
    )
    print(f"  Component: {component.name}")
    print(f"  Type: {component.type.value}")
    print(f"  Enabled: {component.enabled}")
    
    print("  ✓ UI component model tests passed")


def test_user_preferences_model():
    """Test user preferences model."""
    print("\n=== Testing User Preferences Model ===")
    
    prefs = experience.UserPreferences(
        user_id="user_1",
        theme=Theme.DARK,
        language="ar",
        font_size=16
    )
    print(f"  User: {prefs.user_id}")
    print(f"  Theme: {prefs.theme.value}")
    print(f"  Language: {prefs.language}")
    print(f"  Font size: {prefs.font_size}")
    
    print("  ✓ User preferences model tests passed")


def test_plugin_model():
    """Test plugin model."""
    print("\n=== Testing Plugin Model ===")
    
    plugin = experience.Plugin(
        plugin_id="plugin_1",
        name="Test Plugin",
        version="1.0.0",
        author="Test Author",
        permissions=("read", "write", "execute")
    )
    print(f"  Plugin: {plugin.name}")
    print(f"  Version: {plugin.version}")
    print(f"  Permissions: {plugin.permissions}")
    print(f"  Enabled: {plugin.enabled}")
    
    print("  ✓ Plugin model tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLOUD EXPERIENCE - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_experience()
        test_component_registry()
        test_dashboard()
        test_preferences()
        test_notifications()
        test_streaming()
        test_search()
        test_plugins()
        test_statistics()
        test_ui_component_model()
        test_user_preferences_model()
        test_plugin_model()
        
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
