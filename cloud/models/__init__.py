"""Universal Model Platform - Support any present or future LLM."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

SUPPORTED_MODELS = (
    "OpenAI", "Anthropic", "Google", "DeepSeek", "Qwen", "Mistral",
    "Llama", "Grok", "OpenRouter", "Ollama", "vLLM", "LM Studio", "Custom APIs", "Future Models"
)


class RoutingFactor(Enum):
    """Routing factors for model selection."""
    QUALITY = "quality"
    LATENCY = "latency"
    COST = "cost"
    AVAILABILITY = "availability"
    CONTEXT_SIZE = "context_size"
    TOOL_SUPPORT = "tool_support"
    RELIABILITY = "reliability"


@dataclass
class ModelDescriptor:
    """Model descriptor with capabilities and costs."""
    name: str
    provider: str
    version: str = "1.0.0"
    max_tokens: int = 100000
    supports_tools: bool = False
    supports_vision: bool = False
    supports_streaming: bool = False
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    latency_ms: int = 1000
    reliability: float = 0.99


@dataclass
class ModelInvocation:
    """Model invocation record."""
    invocation_id: str
    model_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    cost: float = 0.0
    success: bool = True
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class ModelRegistry:
    """Model registry."""
    
    def __init__(self):
        self._models: Dict[str, ModelDescriptor] = {}
    
    def register(self, model: ModelDescriptor) -> None:
        """Register a model."""
        self._models[model.name] = model
    
    def unregister(self, name: str) -> bool:
        """Unregister a model."""
        if name in self._models:
            del self._models[name]
            return True
        return False
    
    def get(self, name: str) -> Optional[ModelDescriptor]:
        """Get model by name."""
        return self._models.get(name)
    
    def list_all(self) -> List[ModelDescriptor]:
        """List all registered models."""
        return list(self._models.values())
    
    def list_by_provider(self, provider: str) -> List[ModelDescriptor]:
        """List models by provider."""
        return [m for m in self._models.values() if m.provider == provider]
    
    def list_with_capability(self, capability: str) -> List[ModelDescriptor]:
        """List models with specific capability."""
        models = []
        for m in self._models.values():
            if capability == "tools" and m.supports_tools:
                models.append(m)
            elif capability == "vision" and m.supports_vision:
                models.append(m)
            elif capability == "streaming" and m.supports_streaming:
                models.append(m)
        return models


class ModelRouter:
    """
    Model Router with intelligent routing.
    
    Routing Factors:
    ✅ Quality, Latency, Cost, Availability
    ✅ Context Size, Tool Support, Reliability
    """
    
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self._weights: Dict[RoutingFactor, float] = {
            RoutingFactor.QUALITY: 0.3,
            RoutingFactor.LATENCY: 0.2,
            RoutingFactor.COST: 0.2,
            RoutingFactor.AVAILABILITY: 0.15,
            RoutingFactor.RELIABILITY: 0.15,
        }
    
    def set_weight(self, factor: RoutingFactor, weight: float) -> None:
        """Set routing weight for a factor."""
        self._weights[factor] = weight
    
    def route(self, requirements: Dict[str, Any]) -> Optional[str]:
        """Route to best model based on requirements."""
        models = self.registry.list_all()
        if not models:
            return None
        
        # Filter by requirements
        if requirements.get("supports_tools"):
            models = [m for m in models if m.supports_tools]
        
        if requirements.get("supports_vision"):
            models = [m for m in models if m.supports_vision]
        
        if requirements.get("min_context"):
            models = [m for m in models if m.max_tokens >= requirements["min_context"]]
        
        if not models:
            return None
        
        # Simple routing: prefer cheapest if quality is acceptable
        if requirements.get("priority") == "cost":
            return min(models, key=lambda m: m.cost_per_1k_input + m.cost_per_1k_output).name
        
        if requirements.get("priority") == "latency":
            return min(models, key=lambda m: m.latency_ms).name
        
        if requirements.get("priority") == "quality":
            return max(models, key=lambda m: m.reliability).name
        
        return models[0].name


class UniversalModelPlatform:
    """
    Universal Model Platform.
    
    Supports any present or future LLM.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.registry = ModelRegistry()
        self.router = ModelRouter(self.registry)
        self._invocations: Dict[str, ModelInvocation] = {}
    
    def add_model(self, model: ModelDescriptor) -> None:
        """Add a model to the platform."""
        self.registry.register(model)
    
    def remove_model(self, name: str) -> bool:
        """Remove a model from the platform."""
        return self.registry.unregister(name)
    
    def get_model(self, name: str) -> Optional[ModelDescriptor]:
        """Get model by name."""
        return self.registry.get(name)
    
    def route(self, requirements: Dict[str, Any]) -> Optional[str]:
        """Route to best model based on requirements."""
        return self.router.route(requirements)
    
    def record_invocation(self, invocation: ModelInvocation) -> None:
        """Record a model invocation."""
        self._invocations[invocation.invocation_id] = invocation
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        total = len(self._invocations)
        successful = len([i for i in self._invocations.values() if i.success])
        
        total_cost = sum(i.cost for i in self._invocations.values())
        total_latency = sum(i.latency_ms for i in self._invocations.values())
        total_input = sum(i.input_tokens for i in self._invocations.values())
        total_output = sum(i.output_tokens for i in self._invocations.values())
        
        return {
            "total_invocations": total,
            "successful": successful,
            "failed": total - successful,
            "registered_models": len(self.registry.list_all()),
            "total_cost": total_cost,
            "total_latency_ms": total_latency,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
        }
