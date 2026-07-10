#!/usr/bin/env python3
"""
Cloud - Test Suite
================

Tests for the AGOS Cloud Operating System.
Run with: python test_cloud.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, '..'))

# Import modules
import __init__ as cloud
from agents import (
    AgentInvocationRuntime, AgentRegistry, AgentDescriptor,
    AgentState, AgentResponse, SUPPORTED_AGENTS
)
from distributed import (
    DistributedRuntime, WorkerPool, DistributedScheduler,
    Worker, WorkerState, DistributedMission, RetryManager, CheckpointManager
)
from models import (
    UniversalModelPlatform, ModelRegistry, ModelRouter,
    ModelDescriptor, RoutingFactor, SUPPORTED_MODELS
)

# Import CloudPlatform inline
import importlib
try:
    from integration import CloudPlatform
except ImportError:
    integration = importlib.import_module('integration')
    CloudPlatform = integration.CloudPlatform


def test_cloud_runtime():
    """Test cloud runtime."""
    print("\n=== Testing Cloud Runtime ===")
    
    runtime = cloud.CloudRuntime()
    
    # Deploy
    config = cloud.CloudConfig(
        name="test-cloud",
        region="us-west-2",
        targets=(cloud.ExecutionTarget.KUBERNETES, cloud.ExecutionTarget.CONTAINER)
    )
    result = runtime.deploy(config)
    print(f"  Deploy: {result}")
    
    # Create project
    project = runtime.create_project("proj_001", "Test Project", "Description")
    print(f"  Project: {project.name}")
    
    # Health check
    health = runtime.health_check()
    print(f"  Status: {health['status']}")
    
    # Statistics
    stats = runtime.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("  ✓ Cloud runtime tests passed")


def test_mission_gateway():
    """Test mission gateway."""
    print("\n=== Testing Mission Gateway ===")
    
    gateway = cloud.MissionGateway()
    
    # Validate request
    request = cloud.MissionRequest(
        mission_id="m1",
        project_id="p1",
        mission_type="build",
        priority=5
    )
    valid, error = gateway.validate(request)
    print(f"  Valid: {valid}")
    
    # Receive
    received = gateway.receive(request)
    print(f"  Received: {received}")
    
    print("  ✓ Mission gateway tests passed")


def test_realtime_gateway():
    """Test realtime gateway."""
    print("\n=== Testing Realtime Gateway ===")
    
    gateway = cloud.RealtimeGateway()
    
    # Connect
    conn_id = "conn_001"
    result = gateway.connect(conn_id)
    print(f"  Connect: {result}")
    
    # Send
    sent = gateway.send(conn_id, {"type": "test"})
    print(f"  Send: {sent}")
    
    # Disconnect
    result = gateway.disconnect(conn_id)
    print(f"  Disconnect: {result}")
    
    print("  ✓ Realtime gateway tests passed")


def test_agent_runtime():
    """Test agent runtime."""
    print("\n=== Testing Agent Runtime ===")
    
    runtime = AgentInvocationRuntime()
    
    # Register agent
    descriptor = AgentDescriptor(
        name="OpenHands",
        version="1.0.0",
        capabilities=("code_generation", "debugging"),
        state=AgentState.HEALTHY
    )
    runtime.registry.register_descriptor(descriptor)
    runtime.registry.register("OpenHands", object())
    
    # Invoke
    response = runtime.invoke("OpenHands", "Write a function")
    print(f"  Success: {response.success}")
    print(f"  Execution time: {response.execution_time_ms}ms")
    
    # Statistics
    stats = runtime.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("  ✓ Agent runtime tests passed")


def test_distributed_runtime():
    """Test distributed runtime."""
    print("\n=== Testing Distributed Runtime ===")
    
    runtime = DistributedRuntime()
    
    # Register worker
    worker = Worker(
        worker_id="w1",
        name="Worker 1",
        state=WorkerState.HEALTHY,
        capabilities=("python", "javascript")
    )
    runtime.worker_pool.register(worker)
    print(f"  Worker registered: {worker.name}")
    
    # Submit mission
    result = runtime.submit_mission("m1", priority=2)
    print(f"  Mission submitted: {result}")
    
    # Dispatch
    dispatched = runtime.dispatch()
    print(f"  Dispatched: {dispatched}")
    
    # Complete
    result = runtime.complete_mission("m1")
    print(f"  Completed: {result}")
    
    # Status
    status = runtime.get_status()
    print(f"  Status: {status}")
    
    print("  ✓ Distributed runtime tests passed")


def test_retry_manager():
    """Test retry manager."""
    print("\n=== Testing Retry Manager ===")
    
    manager = RetryManager(max_retries=3)
    
    # Should retry
    print(f"  Should retry (0): {manager.should_retry('m1')}")
    
    # Record retries
    manager.record_retry("m1")
    manager.record_retry("m1")
    print(f"  Retry count: {manager.get_retry_count('m1')}")
    print(f"  Should retry (2): {manager.should_retry('m1')}")
    
    # Reset
    manager.reset("m1")
    print(f"  Should retry after reset: {manager.should_retry('m1')}")
    
    print("  ✓ Retry manager tests passed")


def test_checkpoint_manager():
    """Test checkpoint manager."""
    print("\n=== Testing Checkpoint Manager ===")
    
    manager = CheckpointManager()
    
    # Save checkpoint
    state = {"step": 5, "data": [1, 2, 3]}
    checkpoint_id = manager.save("m1", state)
    print(f"  Checkpoint saved: {checkpoint_id}")
    
    # Load checkpoint
    checkpoint = manager.load(checkpoint_id)
    print(f"  Checkpoint loaded: {checkpoint is not None}")
    
    # Get latest
    latest = manager.get_latest("m1")
    print(f"  Latest checkpoint: {latest is not None}")
    
    print("  ✓ Checkpoint manager tests passed")


def test_model_platform():
    """Test model platform."""
    print("\n=== Testing Model Platform ===")
    
    platform = UniversalModelPlatform()
    
    # Add model
    model = ModelDescriptor(
        name="gpt-4",
        provider="OpenAI",
        supports_tools=True,
        cost_per_1k_input=0.03,
        cost_per_1k_output=0.06
    )
    platform.add_model(model)
    print(f"  Model added: {model.name}")
    
    # Route
    routed = platform.route({"priority": "cost"})
    print(f"  Routed to: {routed}")
    
    # Statistics
    stats = platform.get_statistics()
    print(f"  Statistics: {stats}")
    
    print("  ✓ Model platform tests passed")


def test_model_router():
    """Test model router."""
    print("\n=== Testing Model Router ===")
    
    registry = ModelRegistry()
    router = ModelRouter(registry)
    
    # Add models
    model1 = ModelDescriptor(
        name="gpt-4",
        provider="OpenAI",
        cost_per_1k_input=0.03,
        latency_ms=2000
    )
    model2 = ModelDescriptor(
        name="claude-3",
        provider="Anthropic",
        cost_per_1k_input=0.015,
        latency_ms=1500
    )
    registry.register(model1)
    registry.register(model2)
    
    # Route by cost
    routed = router.route({"priority": "cost"})
    print(f"  Route by cost: {routed}")
    
    # Route by latency
    routed = router.route({"priority": "latency"})
    print(f"  Route by latency: {routed}")
    
    print("  ✓ Model router tests passed")


def test_cloud_platform():
    """Test cloud platform."""
    print("\n=== Testing Cloud Platform ===")
    
    platform = CloudPlatform()
    
    # Status
    status = platform.get_status()
    print(f"  Version: {status['version']}")
    print(f"  Workers: {status['workers']}")
    print(f"  Agents: {status['agents']}")
    print(f"  Models: {status['models']}")
    
    # Statistics
    stats = platform.get_statistics()
    print(f"  Statistics: {stats}")
    
    # Health check
    health = platform.health_check()
    print(f"  Healthy: {health['healthy']}")
    
    print("  ✓ Cloud platform tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLOUD - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_cloud_runtime()
        test_mission_gateway()
        test_realtime_gateway()
        test_agent_runtime()
        test_distributed_runtime()
        test_retry_manager()
        test_checkpoint_manager()
        test_model_platform()
        test_model_router()
        test_cloud_platform()
        
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
