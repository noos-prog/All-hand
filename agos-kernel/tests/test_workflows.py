"""
AGOS Workflow Tests
=================

Unit tests for workflow modules.
"""

import unittest
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPipeline(unittest.TestCase):
    """Test Pipeline."""
    
    def test_pipeline_creation(self):
        """Test pipeline can be created."""
        from workflows import Pipeline, PipelineConfig
        config = PipelineConfig(name="TestPipeline")
        pipeline = Pipeline(config=config)
        
        self.assertIsNotNone(pipeline)
        self.assertEqual(pipeline.config.name, "TestPipeline")
    
    def test_add_step(self):
        """Test adding steps to pipeline."""
        from workflows import Pipeline, PipelineStep
        
        pipeline = Pipeline()
        
        def handler(ctx):
            return "done"
        
        step = PipelineStep(
            id="step1",
            name="First Step",
            handler=handler,
        )
        
        pipeline.add_step(step)
        self.assertEqual(len(pipeline.steps), 1)
    
    def test_pipeline_run(self):
        """Test running pipeline."""
        from workflows import Pipeline, PipelineStep, ExecutionContext
        
        pipeline = Pipeline()
        
        def handler1(ctx):
            ctx.set_var("step1_done", True)
            return "step1_result"
        
        def handler2(ctx):
            return f"step2_result: {ctx.get_var('step1_done')}"
        
        pipeline.add_step(PipelineStep(id="s1", name="Step 1", handler=handler1))
        pipeline.add_step(PipelineStep(id="s2", name="Step 2", handler=handler2))
        
        context = ExecutionContext(pipeline_id=pipeline.id)
        results = pipeline.run(context)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].output, "step1_result")
        self.assertEqual(results[1].output, "step2_result: True")
    
    def test_pipeline_with_condition(self):
        """Test pipeline with conditional step."""
        from workflows import Pipeline, PipelineStep, ExecutionContext, StepStatus
        
        pipeline = Pipeline()
        
        def always_run(ctx):
            ctx.set_var("flag", True)
            return "done"
        
        def conditional_run(ctx):
            return "conditional_done"
        
        pipeline.add_step(PipelineStep(
            id="s1", name="Step 1", handler=always_run
        ))
        pipeline.add_step(PipelineStep(
            id="s2", name="Step 2", handler=conditional_run,
            condition=lambda ctx: ctx.get_var("flag") == True
        ))
        
        context = ExecutionContext(pipeline_id=pipeline.id)
        results = pipeline.run(context)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1].status, StepStatus.COMPLETED)


class TestExecutor(unittest.TestCase):
    """Test Executor."""
    
    def test_executor_creation(self):
        """Test executor can be created."""
        from workflows import Executor, ExecutionConfig
        config = ExecutionConfig(timeout=10)
        executor = Executor(config=config)
        
        self.assertIsNotNone(executor)
    
    def test_execute_success(self):
        """Test successful execution."""
        from workflows import Executor
        
        executor = Executor()
        
        def handler():
            return "success"
        
        result = executor.execute("test_step", handler)
        
        self.assertEqual(result.status, "completed")
    
    def test_execute_with_error(self):
        """Test execution with error."""
        from workflows import Executor
        
        executor = Executor()
        
        def handler():
            raise ValueError("Test error")
        
        result = executor.execute("test_step", handler)
        
        self.assertEqual(result.status, "failed")
    
    def test_execute_with_retry(self):
        """Test execution with retry."""
        from workflows import Executor, ExecutionConfig
        
        config = ExecutionConfig(retry_count=2)
        executor = Executor(config=config)
        
        attempts = {"count": 0}
        
        def handler():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise ValueError("Retry")
            return "success"
        
        result = executor.execute("test_step", handler)
        
        self.assertEqual(result.status, "completed")


class TestMonitor(unittest.TestCase):
    """Test Monitor."""
    
    def test_monitor_creation(self):
        """Test monitor can be created."""
        from workflows import Monitor, MonitorConfig
        config = MonitorConfig(check_interval=5)
        monitor = Monitor(config=config)
        
        self.assertIsNotNone(monitor)
    
    def test_record_execution(self):
        """Test recording execution."""
        from workflows import Monitor
        
        monitor = Monitor()
        
        exec_id = monitor.record_execution(
            pipeline_id="test-pipeline",
            status="completed",
            duration_ms=1000,
        )
        
        self.assertIsNotNone(exec_id)
        
        record = monitor.get_execution(exec_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.pipeline_id, "test-pipeline")
    
    def test_get_health(self):
        """Test getting health status."""
        from workflows import Monitor
        
        monitor = Monitor()
        
        health = monitor.get_health()
        self.assertIsNotNone(health)
    
    def test_get_metrics(self):
        """Test getting metrics."""
        from workflows import Monitor
        
        monitor = Monitor()
        
        metrics = monitor.get_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("health_status", metrics)


if __name__ == '__main__':
    unittest.main()
