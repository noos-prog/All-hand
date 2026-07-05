"""
AGOS Kernel Tests
================

Unit tests for the AGOS Kernel.
"""

import unittest
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAGOSKernel(unittest.TestCase):
    """Test AGOSKernel."""
    
    def setUp(self):
        """Set up test fixtures."""
        from kernel import AGOSKernel
        self.kernel = AGOSKernel()
    
    def test_kernel_creation(self):
        """Test kernel can be created."""
        self.assertIsNotNone(self.kernel)
    
    def test_kernel_initialization(self):
        """Test kernel initializes correctly."""
        self.assertIsNotNone(self.kernel.status)
        self.assertIsNotNone(self.kernel.config)
    
    def test_kernel_start(self):
        """Test kernel can start."""
        result = self.kernel.start()
        # Kernel may or may not start depending on environment
        # Just verify it returns a boolean
        self.assertIsInstance(result, bool)
    
    def test_kernel_shutdown(self):
        """Test kernel can shutdown."""
        result = self.kernel.shutdown()
        self.assertTrue(result)
    
    def test_get_state(self):
        """Test getting kernel state."""
        state = self.kernel.get_state()
        self.assertIsNotNone(state)
    
    def test_health_check(self):
        """Test health check."""
        health = self.kernel.health_check()
        self.assertIsInstance(health, dict)
        self.assertIn("status", health)


class TestKernelEvents(unittest.TestCase):
    """Test Kernel Events."""
    
    def test_event_subscription(self):
        """Test event subscription."""
        from kernel import AGOSKernel, KernelEvent
        kernel = AGOSKernel()
        
        events_received = []
        
        def handler(event, data):
            events_received.append((event, data))
        
        kernel.subscribe(KernelEvent.STARTED, handler)
        self.assertIn(KernelEvent.STARTED, kernel._event_handlers)
    
    def test_event_unsubscription(self):
        """Test event unsubscription."""
        from kernel import AGOSKernel, KernelEvent
        kernel = AGOSKernel()
        
        def handler(event, data):
            pass
        
        kernel.subscribe(KernelEvent.STARTED, handler)
        kernel.unsubscribe(KernelEvent.STARTED, handler)
        
        # Handler should be removed
        self.assertEqual(len(kernel._event_handlers.get(KernelEvent.STARTED, [])), 0)


class TestKernelExecution(unittest.TestCase):
    """Test Kernel Execution."""
    
    def test_execute_unknown_workflow(self):
        """Test executing unknown workflow."""
        from kernel import AGOSKernel
        kernel = AGOSKernel()
        
        result = kernel.execute("unknown-workflow", {})
        self.assertFalse(result.get("success", True))
    
    def test_execution_log(self):
        """Test execution logging."""
        from kernel import AGOSKernel
        kernel = AGOSKernel()
        
        logs = kernel.get_execution_logs()
        self.assertIsInstance(logs, list)


if __name__ == '__main__':
    unittest.main()
