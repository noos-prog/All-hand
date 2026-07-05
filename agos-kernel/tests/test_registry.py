"""
AGOS Registry Tests
==================

Unit tests for registry modules.
"""

import unittest
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestComponentRegistry(unittest.TestCase):
    """Test ComponentRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        from registry.component import get_component_registry, ComponentRegistry, ComponentType
        self.registry = get_component_registry()
        self.ComponentType = ComponentType
    
    def test_singleton(self):
        """Test singleton pattern."""
        from registry.component import get_component_registry
        reg2 = get_component_registry()
        self.assertIs(self.registry, reg2)
    
    def test_register_component(self):
        """Test component registration."""
        class TestComponent:
            pass
        
        component_id = self.registry.register(
            cls=TestComponent,
            component_id="test_component",
            component_type=self.ComponentType.RUNTIME,
        )
        
        self.assertEqual(component_id, "test_component")
        
        # Check it was registered
        component = self.registry.get("test_component")
        self.assertIsNotNone(component)
        self.assertEqual(component.id, "test_component")
    
    def test_unregister_component(self):
        """Test component unregistration."""
        class TestComponent2:
            pass
        
        self.registry.register(
            cls=TestComponent2,
            component_id="test_component_2",
            component_type=self.ComponentType.RUNTIME,
        )
        
        # Verify registered
        self.assertIsNotNone(self.registry.get("test_component_2"))
        
        # Unregister
        result = self.registry.unregister("test_component_2")
        self.assertTrue(result)
        
        # Should be gone
        self.assertIsNone(self.registry.get("test_component_2"))
    
    def test_list_all(self):
        """Test listing all components."""
        components = self.registry.list_all()
        self.assertIsInstance(components, list)
    
    def test_activate_all(self):
        """Test activating all components."""
        results = self.registry.activate_all()
        self.assertIsInstance(results, dict)


class TestCapabilityRegistry(unittest.TestCase):
    """Test CapabilityRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        from registry.cap_registry import get_capability_registry
        self.registry = get_capability_registry()
    
    def test_singleton(self):
        """Test singleton pattern."""
        from registry.cap_registry import get_capability_registry
        reg2 = get_capability_registry()
        self.assertIs(self.registry, reg2)
    
    def test_register_capability(self):
        """Test capability registration."""
        class TestCapability:
            pass
        
        cap_id = self.registry.register(
            cls=TestCapability,
            capability_id="test_cap",
            name="Test Capability",
        )
        
        self.assertIsNotNone(cap_id)
    
    def test_list_all(self):
        """Test listing all capabilities."""
        caps = self.registry.list_all()
        self.assertIsInstance(caps, list)


class TestKnowledgeRegistry(unittest.TestCase):
    """Test KnowledgeRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        from registry.knowledge_registry import get_knowledge_registry, KnowledgeType
        self.registry = get_knowledge_registry()
        self.KnowledgeType = KnowledgeType
    
    def test_singleton(self):
        """Test singleton pattern."""
        from registry.knowledge_registry import get_knowledge_registry
        reg2 = get_knowledge_registry()
        self.assertIs(self.registry, reg2)
    
    def test_add_knowledge(self):
        """Test adding knowledge."""
        entry_id = self.registry.add(
            title="Test Knowledge",
            knowledge_type=self.KnowledgeType.FACT,
            content={"test": "data"},
            tags=["test"],
        )
        
        self.assertIsNotNone(entry_id)
        
        # Verify it was added
        entry = self.registry.get(entry_id)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.title, "Test Knowledge")
    
    def test_search(self):
        """Test searching knowledge."""
        results = self.registry.search("test")
        self.assertIsInstance(results, list)


class TestWorkflowRegistry(unittest.TestCase):
    """Test WorkflowRegistry."""
    
    def setUp(self):
        """Set up test fixtures."""
        from registry.workflow_registry import get_workflow_registry
        self.registry = get_workflow_registry()
    
    def test_singleton(self):
        """Test singleton pattern."""
        from registry.workflow_registry import get_workflow_registry
        reg2 = get_workflow_registry()
        self.assertIs(self.registry, reg2)
    
    def test_register_workflow(self):
        """Test workflow registration."""
        class TestWorkflow:
            pass
        
        wf_id = self.registry.register(
            cls=TestWorkflow,
            workflow_id="test_workflow",
            name="Test Workflow",
        )
        
        self.assertIsNotNone(wf_id)


if __name__ == '__main__':
    unittest.main()
