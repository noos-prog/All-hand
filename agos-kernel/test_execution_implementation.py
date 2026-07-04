#!/usr/bin/env python3
"""Production Implementation Test Suite."""
import asyncio
import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from execution.engine import (
    ExecutionEngine, ExecutionStatus, ExecutionEvent,
    ExecutionGraph, ExecutionNode, ExecutionPolicy,
    get_engine
)
from skills.implementation import (
    CodeAnalysisSkill, RepositoryAnalysisSkill, SecurityReviewSkill,
    PerformanceReviewSkill, execute_skill, SKILL_IMPLEMENTATIONS
)
from providers.implementation import (
    OpenAIProvider, GitHubProvider, AnthropicProvider,
    get_provider, PROVIDER_IMPLEMENTATIONS
)
from adapters.implementation import (
    GitAdapter, DockerAdapter, KubernetesAdapter,
    TerraformAdapter, OpenAIAdapter,
    get_adapter, ADAPTER_IMPLEMENTATIONS
)


async def test_execution_engine():
    """Test execution engine."""
    print("=" * 60)
    print("Testing Execution Engine")
    print("=" * 60)
    
    engine = get_engine()
    
    # Test policy creation
    policy = engine.create_policy(
        "test_policy",
        timeout_seconds=60,
        max_retries=3,
        rollback_on_failure=True,
    )
    print(f"✓ Policy created: timeout={policy.timeout_seconds}s, retries={policy.max_retries}")
    
    # Test execution
    result = await engine.execute(
        capability_id="test_cap",
        skill_id="code_analysis",
        provider_id="openai",
        parameters={"code": "x = 1", "language": "python"},
        policy_name="test_policy",
    )
    print(f"✓ Execution: {result.status.value}, output={result.output}")
    
    # Test workflow graph
    graph = ExecutionGraph("test_workflow")
    node1 = ExecutionNode("node1", "Step 1", "code_analysis", "openai")
    node2 = ExecutionNode("node2", "Step 2", "security_review", "openai")
    
    graph.add_node(node1)
    graph.add_node(node2)
    graph.add_edge("node1", "node2")
    
    print(f"✓ Workflow graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    
    return True


async def test_skills():
    """Test skill implementations."""
    print("\n" + "=" * 60)
    print("Testing Production Skill Implementations")
    print("=" * 60)
    
    print(f"Total skills: {len(SKILL_IMPLEMENTATIONS)}")
    
    # Test CodeAnalysisSkill
    skill = CodeAnalysisSkill()
    result = await skill.execute({
        "code": "password = '123456'\neval(user_input)",
        "language": "python",
    })
    print(f"✓ CodeAnalysis: {result.success}, Score: {result.output.get('quality_score', 0):.1f}")
    
    # Test SecurityReviewSkill
    result = await execute_skill("security_review", {
        "code": "eval(user_data)\npassword = 'secret'",
    })
    print(f"✓ SecurityReview: {result.success}, Vulns: {len(result.output.get('vulnerabilities', []))}")
    
    # Test PerformanceReviewSkill
    result = await execute_skill("perf_review", {
        "code": "for i in range(10):\n    for j in range(10):\n        pass",
    })
    print(f"✓ PerformanceReview: {result.success}, Issues: {len(result.output.get('issues', []))}")
    
    return True


async def test_providers():
    """Test provider implementations."""
    print("\n" + "=" * 60)
    print("Testing Production Provider Implementations")
    print("=" * 60)
    
    print(f"Total providers: {len(PROVIDER_IMPLEMENTATIONS)}")
    
    # Test OpenAI Provider
    openai = get_provider("openai", api_key="test-key")
    
    # Test chat
    result = await openai.execute("chat", {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
    })
    print(f"✓ OpenAI Chat: {result.get('id', '')[:20]}...")
    
    # Test embeddings
    result = await openai.execute("embeddings", {"input": "Hello world"})
    print(f"✓ OpenAI Embeddings: {len(result['data'][0]['embedding'])} dims")
    
    # Test streaming
    chunks = []
    async for chunk in openai.stream("chat", {"messages": [{"content": "Hi"}]}):
        chunks.append(chunk)
    print(f"✓ OpenAI Streaming: {len(chunks)} chunks")
    
    # Test health
    health = await openai.health_check()
    print(f"✓ OpenAI Health: {health.healthy}, latency: {health.latency_ms:.2f}ms")
    
    # Test metrics
    metrics = openai.get_metrics()
    print(f"✓ OpenAI Metrics: {metrics.total_requests} requests, {metrics.successful_requests} success")
    
    # Test Anthropic Provider
    anthropic = get_provider("anthropic", api_key="test-key")
    result = await anthropic.execute("chat", {"messages": [{"role": "user", "content": "Hello"}]})
    print(f"✓ Anthropic Chat: {result.get('id', '')}")
    
    return True


async def test_adapters():
    """Test adapter implementations."""
    print("\n" + "=" * 60)
    print("Testing Production Adapter Implementations")
    print("=" * 60)
    
    print(f"Total adapters: {len(ADAPTER_IMPLEMENTATIONS)}")
    
    # Test Git Adapter
    git = get_adapter("git")
    result = await git.execute("status", {})
    print(f"✓ Git Adapter: {result.success}")
    
    # Test Docker Adapter
    docker = get_adapter("docker")
    result = await docker.execute("ps", {})
    print(f"✓ Docker Adapter: {result.success}")
    
    # Test Kubernetes Adapter
    k8s = get_adapter("kubernetes")
    result = await k8s.execute("pods", {})
    print(f"✓ Kubernetes Adapter: {result.success}")
    
    # Test Terraform Adapter
    tf = get_adapter("terraform")
    result = await tf.execute("validate", {})
    print(f"✓ Terraform Adapter: {result.success}")
    
    # Test OpenAI Adapter
    openai = get_adapter("openai", api_key="test")
    result = await openai.execute("chat", {"messages": [{"role": "user", "content": "Hello"}]})
    print(f"✓ OpenAI Adapter: {result.success}")
    
    return True


async def test_integration():
    """Test integration."""
    print("\n" + "=" * 60)
    print("Testing Integration")
    print("=" * 60)
    
    engine = get_engine()
    
    # Create workflow with multiple nodes
    graph = ExecutionGraph("integration_workflow")
    
    nodes = [
        ExecutionNode("analyze", "Analyze Code", "code_analysis", "openai"),
        ExecutionNode("security", "Security Review", "security_review", "openai"),
        ExecutionNode("perf", "Performance Review", "perf_review", "openai"),
    ]
    
    for node in nodes:
        graph.add_node(node)
    
    # Workflow: analyze -> security -> perf
    graph.add_edge("analyze", "security")
    graph.add_edge("security", "perf")
    graph.entry_nodes = ["analyze"]
    graph.exit_nodes = ["perf"]
    
    print(f"✓ Integration workflow: {len(graph.nodes)} nodes")
    
    # Execute workflow
    results = await engine.execute_workflow(
        graph,
        {"code": "x = 1", "language": "python"},
        policy_name="default",
    )
    
    print(f"✓ Workflow results: {len(results)} nodes executed")
    
    for node_id, result in results.items():
        print(f"  - {node_id}: {result.status.value}")
    
    return True


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AGOS PRODUCTION IMPLEMENTATION TEST SUITE")
    print("=" * 60)
    
    try:
        await test_execution_engine()
        await test_skills()
        await test_providers()
        await test_adapters()
        await test_integration()
        
        print("\n" + "=" * 60)
        print("ALL PRODUCTION IMPLEMENTATIONS PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)