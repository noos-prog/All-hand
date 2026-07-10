#!/usr/bin/env python3
"""
ARI - Model Module
===============

Model registry and comparison.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ModelProvider(Enum):
    """Model providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    DEEPSEEK = "deepseek"
    OTHER = "other"


class ModelType(Enum):
    """Model types."""
    TEXT = "text"
    CODE = "code"
    VISION = "vision"
    MULTIMODAL = "multimodal"
    EMBEDDING = "embedding"
    SPEECH = "speech"


@dataclass
class ModelMetrics:
    """Metrics for a model."""
    # Performance
    coding_score: float = 0.0
    reasoning_score: float = 0.0
    memory_score: float = 0.0
    instruction_following_score: float = 0.0
    
    # Benchmarks
    humaneval_score: float = 0.0
    mbpp_score: float = 0.0
    math_score: float = 0.0
    mmlu_score: float = 0.0
    
    # Cost
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0
    
    # Latency
    avg_latency_ms: float = 0.0
    time_to_first_token_ms: float = 0.0
    
    def get_overall_score(self) -> float:
        """Calculate overall model score."""
        weights = {
            "coding": 0.4,
            "reasoning": 0.3,
            "memory": 0.15,
            "instruction": 0.15,
        }
        
        total = (
            weights["coding"] * self.coding_score +
            weights["reasoning"] * self.reasoning_score +
            weights["memory"] * self.memory_score +
            weights["instruction"] * self.instruction_following_score
        )
        
        return round(total, 3)


@dataclass
class Model:
    """An AI model."""
    model_id: str
    name: str
    provider: ModelProvider
    model_type: ModelType
    
    # Details
    display_name: str
    description: Optional[str] = None
    version: Optional[str] = None
    
    # Capabilities
    context_window: int = 0
    max_output_tokens: int = 0
    supports_streaming: bool = False
    supports_function_calling: bool = False
    
    # Metrics
    metrics: ModelMetrics = field(default_factory=ModelMetrics)
    
    # Metadata
    release_date: Optional[str] = None
    deprecation_date: Optional[str] = None
    documentation_url: Optional[str] = None
    
    # API
    api_endpoint: Optional[str] = None
    api_version: Optional[str] = None
    
    def get_cost_per_1k_tokens(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost per 1K tokens."""
        input_cost = (input_tokens / 1000) * self.metrics.input_cost_per_1k
        output_cost = (output_tokens / 1000) * self.metrics.output_cost_per_1k
        return input_cost + output_cost
    
    def get_summary(self) -> Dict[str, Any]:
        """Get model summary."""
        return {
            "name": self.display_name,
            "provider": self.provider.value,
            "type": self.model_type.value,
            "context_window": f"{self.metrics.context_window // 1000}K",
            "overall_score": f"{self.get_overall_score():.1%}",
        }


class ModelRegistry:
    """
    Registry of AI models.
    """
    
    def __init__(self):
        self._models: Dict[str, Model] = {}
        self._by_provider: Dict[ModelProvider, List[str]] = {}
        self._by_type: Dict[ModelType, List[str]] = {}
    
    def register(self, model: Model) -> str:
        """Register a model."""
        self._models[model.model_id] = model
        
        # Index by provider
        if model.provider not in self._by_provider:
            self._by_provider[model.provider] = []
        self._by_provider[model.provider].append(model.model_id)
        
        # Index by type
        if model.model_type not in self._by_type:
            self._by_type[model.model_type] = []
        self._by_type[model.model_type].append(model.model_id)
        
        return model.model_id
    
    def get(self, model_id: str) -> Optional[Model]:
        """Get a model by ID."""
        return self._models.get(model_id)
    
    def get_by_provider(self, provider: ModelProvider) -> List[Model]:
        """Get all models by provider."""
        ids = self._by_provider.get(provider, [])
        return [self._models[i] for i in ids if i in self._models]
    
    def get_by_type(self, model_type: ModelType) -> List[Model]:
        """Get all models by type."""
        ids = self._by_type.get(model_type, [])
        return [self._models[i] for i in ids if i in self._models]
    
    def search(
        self,
        provider: Optional[ModelProvider] = None,
        model_type: Optional[ModelType] = None,
        min_score: float = 0.0,
        max_cost: Optional[float] = None,
        limit: int = 100
    ) -> List[Model]:
        """Search models."""
        results = list(self._models.values())
        
        if provider:
            results = [m for m in results if m.provider == provider]
        
        if model_type:
            results = [m for m in results if m.model_type == model_type]
        
        if min_score > 0:
            results = [m for m in results if m.get_overall_score() >= min_score]
        
        if max_cost:
            results = [
                m for m in results
                if m.metrics.input_cost_per_1k + m.metrics.output_cost_per_1k <= max_cost
            ]
        
        # Sort by overall score
        results.sort(key=lambda m: m.get_overall_score(), reverse=True)
        
        return results[:limit]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        by_provider = {p.value: len(ids) for p, ids in self._by_provider.items()}
        by_type = {t.value: len(ids) for t, ids in self._by_type.items()}
        
        return {
            "total_models": len(self._models),
            "by_provider": by_provider,
            "by_type": by_type,
        }


class ModelComparison:
    """
    Compare AI models.
    """
    
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
    
    def compare(
        self,
        model_ids: List[str],
        criteria: List[str] = None
    ) -> Dict[str, Any]:
        """Compare multiple models."""
        models = [self.registry.get(mid) for mid in model_ids]
        models = [m for m in models if m is not None]
        
        if not models:
            return {"error": "No models found"}
        
        if criteria is None:
            criteria = ["overall", "coding", "reasoning", "cost"]
        
        comparison = {
            "models": [
                {
                    "model_id": m.model_id,
                    "name": m.display_name,
                    "provider": m.provider.value,
                }
                for m in models
            ],
            "criteria": {},
        }
        
        for criterion in criteria:
            if criterion == "overall":
                comparison["criteria"]["overall"] = {
                    m.model_id: m.get_overall_score()
                    for m in models
                }
            elif criterion == "coding":
                comparison["criteria"]["coding"] = {
                    m.model_id: m.metrics.coding_score
                    for m in models
                }
            elif criterion == "reasoning":
                comparison["criteria"]["reasoning"] = {
                    m.model_id: m.metrics.reasoning_score
                    for m in models
                }
            elif criterion == "cost":
                comparison["criteria"]["cost"] = {
                    m.model_id: m.metrics.input_cost_per_1k + m.metrics.output_cost_per_1k
                    for m in models
                }
        
        # Determine winners
        comparison["winners"] = {}
        for criterion, scores in comparison["criteria"].items():
            winner_id = max(scores, key=scores.get)
            comparison["winners"][criterion] = winner_id
        
        return comparison
    
    def rank_by_cost_efficiency(
        self,
        model_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """Rank models by cost efficiency (score per dollar)."""
        models = [self.registry.get(mid) for mid in model_ids]
        models = [m for m in models if m is not None]
        
        ranked = []
        for model in models:
            total_cost = model.metrics.input_cost_per_1k + model.metrics.output_cost_per_1k
            if total_cost > 0:
                efficiency = model.get_overall_score() / total_cost
            else:
                efficiency = float('inf')
            
            ranked.append({
                "model_id": model.model_id,
                "name": model.display_name,
                "overall_score": model.get_overall_score(),
                "cost_per_1k": total_cost,
                "efficiency": efficiency,
            })
        
        return sorted(ranked, key=lambda x: x["efficiency"], reverse=True)
    
    def suggest_model(
        self,
        requirements: Dict[str, Any]
    ) -> Optional[Model]:
        """Suggest a model based on requirements."""
        models = list(self.registry._models.values())
        
        # Filter by requirements
        if "min_context_window" in requirements:
            models = [m for m in models if m.context_window >= requirements["min_context_window"]]
        
        if "supports_function_calling" in requirements:
            models = [m for m in models if m.supports_function_calling == requirements["supports_function_calling"]]
        
        if "max_cost" in requirements:
            models = [
                m for m in models
                if m.metrics.input_cost_per_1k + m.metrics.output_cost_per_1k <= requirements["max_cost"]
            ]
        
        # Score based on requirements
        scored = []
        for model in models:
            score = 0.0
            
            if "min_coding_score" in requirements:
                if model.metrics.coding_score >= requirements["min_coding_score"]:
                    score += model.metrics.coding_score
            
            if "min_reasoning_score" in requirements:
                if model.metrics.reasoning_score >= requirements["min_reasoning_score"]:
                    score += model.metrics.reasoning_score
            
            scored.append((model, score))
        
        if not scored:
            return None
        
        return max(scored, key=lambda x: x[1])[0]
