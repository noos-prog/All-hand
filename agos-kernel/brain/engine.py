"""Universal Engineering Brain."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

import sys
sys.path.insert(0, '/workspace/All-hand/agos-kernel')

from knowledge.runtime import KnowledgeRuntime
from memory.runtime import MemoryRuntime, MemoryType, MemoryPriority
from learning.runtime import LearningRuntime, LearningSource
from experience.runtime import ExperienceRuntime, ExperienceType
from recommendation.runtime import RecommendationEngine, RecommendationType
from benchmark.runtime import BenchmarkPlatform, BenchmarkType


@dataclass
class BrainCapabilities:
    """Brain capabilities."""
    understands: bool = True
    plans: bool = True
    reasons: bool = True
    validates: bool = True
    decides: bool = True
    learns: bool = True
    recommends: bool = True
    optimizes: bool = True


@dataclass
class BrainMetrics:
    """Brain metrics."""
    thoughts_processed: int = 0
    decisions_made: int = 0
    recommendations_generated: int = 0
    learnings_integrated: int = 0
    optimizations_executed: int = 0


class EngineeringBrain:
    """
    Universal Engineering Brain.
    
    RULES:
    - Brain never executes
    - Brain never owns providers
    - Brain never owns agents
    - Brain only thinks
    """
    
    def __init__(self):
        """Initialize the brain."""
        # Core systems
        self.knowledge = KnowledgeRuntime()
        self.memory = MemoryRuntime()
        self.learning = LearningRuntime()
        self.experience = ExperienceRuntime()
        self.recommendation = RecommendationEngine()
        self.benchmark = BenchmarkPlatform()
        self.optimization = None
        
        # Brain state
        self.capabilities = BrainCapabilities()
        self.metrics = BrainMetrics()
        
        # Working memory
        self.working_memory = self.memory.create_memory(
            name="brain-working",
            memory_type=MemoryType.WORKING,
            priority=MemoryPriority.CRITICAL,
        )
    
    def think(self, query: str) -> Dict[str, Any]:
        """
        Think about a query using all knowledge systems.
        Brain only thinks - does not execute.
        """
        self.metrics.thoughts_processed += 1
        
        # Add to working memory
        self.memory.add_to_memory(
            self.working_memory.id,
            f"Thinking about: {query}",
            importance=0.8,
        )
        
        # Search knowledge
        relevant_knowledge = self.knowledge.search_knowledge(query)
        
        # Retrieve from memory
        relevant_memories = self.memory.retrieve(query, limit=10)
        
        # Get experiences
        experiences = self.experience.search_experiences(query, limit=5)
        
        return {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "relevant_knowledge": [k.to_dict() for k in relevant_knowledge],
            "relevant_memories": [
                {
                    "id": m.id,
                    "name": m.name,
                    "type": m.memory_type.value,
                }
                for m in relevant_memories
            ],
            "relevant_experiences": [
                {
                    "id": e.id,
                    "name": e.name,
                    "rank": e.rank,
                }
                for e in experiences
            ],
        }
    
    def recommend(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on context."""
        recommendations = []
        
        # Generate recommendations for each type
        for rec_type in RecommendationType:
            rec = self.recommendation.recommend(
                recommendation_type=rec_type,
                name=f"Based on context: {context.get('query', 'unknown')}",
                description=f"Recommendation for {rec_type.value}",
            )
            
            recommendations.append({
                "id": rec.id,
                "type": rec.recommendation_type.value,
                "name": rec.name,
                "description": rec.description,
                "score": rec.total_score,
                "confidence": rec.confidence,
            })
        
        self.metrics.recommendations_generated += len(recommendations)
        return recommendations
    
    def learn_from(self, source: LearningSource, content: str, evidence: Dict[str, Any]) -> bool:
        """Learn from source with evidence."""
        # Create learning item
        item = self.learning.learn(source, content, evidence)
        
        # Validate (rule: no learning without validation)
        is_valid = self.learning.validate(item.id, "brain-validator")
        
        if is_valid:
            # Integrate the learning
            self.learning.integrate(item.id)
            self.metrics.learnings_integrated += 1
            
            # Store in knowledge
            self.knowledge.create_knowledge(
                title=f"Learned: {content[:50]}",
                knowledge_type=None,  # Would determine from source
                content={"source": source.value, "content": content},
                description=content,
                evidence=[],
            )
        
        return is_valid
    
    def create_experience(
        self,
        name: str,
        experience_type: ExperienceType,
        content: str,
        success: bool,
    ) -> bool:
        """Create experience from validated outcome."""
        exp = self.experience.create_experience(
            name=name,
            experience_type=experience_type,
            content=content,
        )
        
        # Validate and rank
        self.experience.validate_experience(exp.id)
        self.experience.rank_experience(exp.id, success)
        
        return True
    
    def run_benchmark(self, name: str, benchmark_type: BenchmarkType, metrics: Dict[str, Any]) -> bool:
        """Run a benchmark."""
        result = self.benchmark.run_benchmark(name, benchmark_type, metrics)
        return result is not None
    
    def get_brain_stats(self) -> Dict[str, Any]:
        """Get brain statistics."""
        return {
            "metrics": {
                "thoughts_processed": self.metrics.thoughts_processed,
                "decisions_made": self.metrics.decisions_made,
                "recommendations_generated": self.metrics.recommendations_generated,
                "learnings_integrated": self.metrics.learnings_integrated,
                "optimizations_executed": self.metrics.optimizations_executed,
            },
            "knowledge_count": len(self.knowledge.knowledge_store),
            "memory_count": len(self.memory.memories),
            "learning_items": len(self.learning.items),
            "experiences_count": len(self.experience.experiences),
            "benchmarks_count": len(self.benchmark.benchmarks),
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check brain health."""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "capabilities": {
                "understands": self.capabilities.understands,
                "plans": self.capabilities.plans,
                "reasons": self.capabilities.reasons,
                "validates": self.capabilities.validates,
                "decides": self.capabilities.decides,
                "learns": self.capabilities.learns,
                "recommends": self.capabilities.recommends,
                "optimizes": self.capabilities.optimizes,
            },
            "all_capabilities_available": all([
                self.capabilities.understands,
                self.capabilities.plans,
                self.capabilities.reasons,
                self.capabilities.validates,
                self.capabilities.decides,
                self.capabilities.learns,
            ]),
        }


# Global brain instance
_brain: Optional[EngineeringBrain] = None


def get_brain() -> EngineeringBrain:
    """Get the global brain instance."""
    global _brain
    if _brain is None:
        _brain = EngineeringBrain()
    return _brain
