#!/usr/bin/env python3
"""
Cloud Execution - Test Suite
==========================

Tests for the AGOS Universal Execution Cloud.
Run with: python test_cloud_execution.py
"""

import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

import __init__ as execution
from __init__ import (
    UniversalExecutionCloud,
    WorkerType, JobStatus, ExecutionEnvironment,
    ExecutionCluster, ExecutionQueue, ExecutionRouter, ExecutionScaler
)


def test_execution_cloud():
    """Test universal execution cloud."""
    print("\n=== Testing Universal Execution Cloud ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Submit jobs
    job1 = cloud.submit_job("mission_1", WorkerType.CONTAINER, priority=1)
    job2 = cloud.submit_job("mission_2", WorkerType.GPU_WORKER, priority=5)
    job3 = cloud.submit_job("mission_3", WorkerType.SERVERLESS, priority=9)
    
    print(f"  Submitted jobs: {job1.job_id}, {job2.job_id}, {job3.job_id}")
    
    # List jobs
    jobs = cloud.list_jobs()
    print(f"  Total jobs: {len(jobs)}")
    
    # Get statistics
    stats = cloud.get_statistics()
    print(f"  Statistics: queued={stats['queued_jobs']}, running={stats['running_jobs']}")
    
    print("  ✓ Execution cloud tests passed")


def test_job_lifecycle():
    """Test job lifecycle."""
    print("\n=== Testing Job Lifecycle ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Submit job
    job = cloud.submit_job("mission_test", WorkerType.CONTAINER)
    print(f"  Job submitted: {job.job_id}, status={job.status.value}")
    
    # Schedule
    result = cloud.schedule_job(job.job_id, "worker_1")
    print(f"  Scheduled: {result}")
    job = cloud.get_job(job.job_id)
    print(f"  Status after schedule: {job.status.value}")
    
    # Start
    result = cloud.start_job(job.job_id)
    print(f"  Started: {result}")
    job = cloud.get_job(job.job_id)
    print(f"  Status after start: {job.status.value}")
    
    # Complete
    result = cloud.complete_job(job.job_id, success=True)
    print(f"  Completed: {result}")
    job = cloud.get_job(job.job_id)
    print(f"  Final status: {job.status.value}")
    
    print("  ✓ Job lifecycle tests passed")


def test_job_retry():
    """Test job retry."""
    print("\n=== Testing Job Retry ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Submit and fail job
    job = cloud.submit_job("mission_fail", WorkerType.CONTAINER)
    cloud.schedule_job(job.job_id, "worker_1")
    cloud.start_job(job.job_id)
    cloud.complete_job(job.job_id, success=False)
    
    job = cloud.get_job(job.job_id)
    print(f"  Failed job retry_count: {job.retry_count}")
    
    # Retry
    result = cloud.retry_job(job.job_id)
    print(f"  Retry result: {result}")
    job = cloud.get_job(job.job_id)
    print(f"  Status after retry: {job.status.value}")
    
    print("  ✓ Job retry tests passed")


def test_execution_queue():
    """Test execution queue."""
    print("\n=== Testing Execution Queue ===")
    
    queue = execution.ExecutionQueue()
    
    # Enqueue
    queue.enqueue("job_1", priority=1)
    queue.enqueue("job_2", priority=5)
    queue.enqueue("job_3", priority=9)
    print(f"  Queue size: {queue.size()}")
    
    # Dequeue
    job = queue.dequeue()
    print(f"  Dequeued: {job} (should be job_1 - high priority)")
    
    job = queue.dequeue()
    print(f"  Dequeued: {job} (should be job_2 - normal priority)")
    
    # Get priority
    queue.enqueue("job_4", priority=2)
    priority = queue.get_priority("job_4")
    print(f"  Priority of job_4: {priority}")
    
    print("  ✓ Execution queue tests passed")


def test_execution_scaler():
    """Test execution scaler."""
    print("\n=== Testing Execution Scaler ===")
    
    config = execution.ScalingConfig(min_workers=1, max_workers=10)
    scaler = execution.ExecutionScaler(config)
    
    print(f"  Current workers: {scaler.current_workers}")
    
    # Scale up
    scaled = scaler.scale_up(3)
    print(f"  Scaled up by: {scaled}")
    print(f"  Current workers: {scaler.current_workers}")
    
    # Scale down
    scaled = scaler.scale_down(2)
    print(f"  Scaled down by: {scaled}")
    print(f"  Current workers: {scaler.current_workers}")
    
    # Should scale up check
    should = scaler.should_scale_up(0.9)
    print(f"  Should scale up (util=0.9): {should}")
    
    # Should scale down check
    should = scaler.should_scale_down(0.1)
    print(f"  Should scale down (util=0.1): {should}")
    
    print("  ✓ Execution scaler tests passed")


def test_execution_router():
    """Test execution router."""
    print("\n=== Testing Execution Router ===")
    
    router = execution.ExecutionRouter()
    
    # Add routes
    router.add_route(WorkerType.CONTAINER, "container-pool")
    router.add_route(WorkerType.GPU_WORKER, "gpu-pool")
    router.add_route(WorkerType.SERVERLESS, "serverless-pool")
    
    print(f"  Container route: {router.get_route(WorkerType.CONTAINER)}")
    print(f"  GPU route: {router.get_route(WorkerType.GPU_WORKER)}")
    print(f"  Serverless route: {router.get_route(WorkerType.SERVERLESS)}")
    
    print("  ✓ Execution router tests passed")


def test_execution_cluster():
    """Test execution cluster."""
    print("\n=== Testing Execution Cluster ===")
    
    cluster = execution.ExecutionCluster()
    
    # Submit job
    job = execution.ExecutionJob(
        job_id="job_1",
        mission_id="mission_1",
        worker_type=WorkerType.CONTAINER
    )
    cluster.submit_job(job)
    print(f"  Job submitted: {job.job_id}")
    
    # Get job
    retrieved = cluster.get_job("job_1")
    print(f"  Job retrieved: {retrieved.job_id if retrieved else 'None'}")
    
    # List jobs
    jobs = cluster.list_jobs()
    print(f"  Total jobs: {len(jobs)}")
    
    # Update status
    cluster.update_job_status("job_1", JobStatus.RUNNING)
    job = cluster.get_job("job_1")
    print(f"  Status updated: {job.status.value}")
    
    print("  ✓ Execution cluster tests passed")


def test_execution_storage():
    """Test execution storage."""
    print("\n=== Testing Execution Storage ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Store artifact
    artifact_id = "artifact_1"
    data = b"test data"
    cloud.storage.store(artifact_id, data)
    print(f"  Stored artifact: {artifact_id}")
    
    # Retrieve
    retrieved = cloud.storage.retrieve(artifact_id)
    print(f"  Retrieved: {retrieved == data}")
    
    # List
    artifacts = cloud.storage.list_artifacts()
    print(f"  Total artifacts: {len(artifacts)}")
    
    # Delete
    result = cloud.storage.delete(artifact_id)
    print(f"  Deleted: {result}")
    
    print("  ✓ Execution storage tests passed")


def test_execution_cache():
    """Test execution cache."""
    print("\n=== Testing Execution Cache ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Set cache
    cloud.cache.set("key1", "value1")
    cloud.cache.set("key2", "value2")
    print(f"  Cache entries: {cloud.cache.get_stats()['entries']}")
    
    # Get cache
    value = cloud.cache.get("key1")
    print(f"  Retrieved value: {value}")
    
    # Hit count
    cloud.cache.get("key1")
    print(f"  Hit count: {cloud.cache.get('key1') is not None}")
    
    # Delete
    result = cloud.cache.delete("key1")
    print(f"  Deleted: {result}")
    
    print("  ✓ Execution cache tests passed")


def test_execution_telemetry():
    """Test execution telemetry."""
    print("\n=== Testing Execution Telemetry ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Record metrics
    cloud.record_metric("job_1", "cpu_usage", 75.5, "%")
    cloud.record_metric("job_1", "memory_usage", 512.0, "MB")
    cloud.record_metric("job_2", "cpu_usage", 60.0, "%")
    
    # Get job metrics
    metrics = cloud.telemetry.get_job_metrics("job_1")
    print(f"  Job 1 metrics: {len(metrics)}")
    
    # Get summary
    summary = cloud.telemetry.get_summary()
    print(f"  Total jobs: {summary['total_jobs']}")
    print(f"  Total metrics: {summary['total_metrics']}")
    
    print("  ✓ Execution telemetry tests passed")


def test_snapshot_and_restore():
    """Test snapshot and restore."""
    print("\n=== Testing Snapshot and Restore ===")
    
    cloud = execution.UniversalExecutionCloud()
    
    # Create job
    job = cloud.submit_job("mission_snapshot", WorkerType.CONTAINER)
    
    # Create snapshot
    state = {"step": 5, "data": [1, 2, 3], "progress": 0.5}
    snapshot_id = cloud.create_snapshot(job.job_id, state, "Checkpoint at step 5")
    print(f"  Snapshot created: {snapshot_id}")
    
    # Continue work
    job = cloud.get_job(job.job_id)
    print(f"  Job status: {job.status.value}")
    
    # Restore
    restored = cloud.restore_snapshot(snapshot_id)
    print(f"  Restored state: {restored}")
    
    print("  ✓ Snapshot and restore tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("CLOUD EXECUTION - RUNNING ALL TESTS")
    print("=" * 70)
    
    try:
        test_execution_cloud()
        test_job_lifecycle()
        test_job_retry()
        test_execution_queue()
        test_execution_scaler()
        test_execution_router()
        test_execution_cluster()
        test_execution_storage()
        test_execution_cache()
        test_execution_telemetry()
        test_snapshot_and_restore()
        
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
