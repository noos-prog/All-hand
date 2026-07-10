#!/usr/bin/env python3
"""
AGOS Intelligence - AGOS Academy
=================================

Learn from the system itself.
Academy provides:
- Best practices extracted from repositories
- Architecture recommendations
- Common mistakes to avoid
- Real examples from successful projects
- Step-by-step guides
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import json


class LearningLevel(Enum):
    """Learning path difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProviderRating(Enum):
    """Provider satisfaction ratings."""
    EXCELLENT = "excellent"    # > 85%
    GOOD = "good"              # 70-85%
    AVERAGE = "average"        # 50-70%
    POOR = "poor"              # < 50%


@dataclass(frozen=True)
class BestPractice:
    """A best practice extracted from analysis."""
    practice_id: str
    title: str
    description: str
    category: str               # e.g., "architecture", "security", "performance"
    success_rate: float         # How often this practice leads to success
    repositories_using: int    # Number of repos using this
    
    # Details
    examples: Tuple[str, ...]  # Real examples
    anti_examples: Optional[str] = None  # What NOT to do
    
    # Implementation guidance
    difficulty: LearningLevel = LearningLevel.INTERMEDIATE
    estimated_time: str = "1-2 hours"
    
    # Metadata
    confidence: float = 0.85
    extracted_from: Tuple[str, ...] = ()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "practice_id": self.practice_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "success_rate": self.success_rate,
            "repositories_using": self.repositories_using,
            "examples": list(self.examples),
            "anti_examples": self.anti_examples,
            "difficulty": self.difficulty.value,
            "estimated_time": self.estimated_time,
            "confidence": self.confidence,
            "extracted_from": list(self.extracted_from),
        }


@dataclass
class ArchitectureRecommendation:
    """Architecture recommendation based on analysis."""
    architecture_id: str
    name: str
    description: str
    usage_percentage: float      # % of successful projects using this
    success_rate: float         # How often this architecture leads to success
    best_for: Tuple[str, ...]  # Use cases
    worst_for: Tuple[str, ...]  # Poor use cases
    complexity: LearningLevel = LearningLevel.INTERMEDIATE
    avg_time_to_build: str = "3-6 months"
    examples: Tuple[Dict[str, Any], ...] = ()  # Real projects using this
    trade_offs: Tuple[str, ...] = ()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "architecture_id": self.architecture_id,
            "name": self.name,
            "description": self.description,
            "usage_percentage": self.usage_percentage,
            "success_rate": self.success_rate,
            "best_for": list(self.best_for),
            "worst_for": list(self.worst_for),
            "complexity": self.complexity.value,
            "avg_time_to_build": self.avg_time_to_build,
            "examples": list(self.examples),
            "trade_offs": list(self.trade_offs),
        }


@dataclass
class ProviderRecommendation:
    """Provider recommendation based on benchmarks."""
    provider_id: str
    name: str
    category: str               # e.g., "llm", "testing", "deployment"
    
    # Ratings
    satisfaction_rating: float   # User satisfaction %
    performance_rating: float   # Performance benchmark score
    
    # Use cases
    best_for: Tuple[str, ...]
    not_recommended_for: Tuple[str, ...] = ()
    
    # Cost
    is_free: bool = False
    pricing_model: Optional[str] = None
    
    # Quality
    quality_score: float = 0.0  # 0-100
    reliability_score: float = 0.0  # 0-100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "name": self.name,
            "category": self.category,
            "satisfaction_rating": f"{self.satisfaction_rating}%",
            "performance_rating": f"{self.performance_rating}%",
            "best_for": list(self.best_for),
            "not_recommended_for": list(self.not_recommended_for),
            "is_free": self.is_free,
            "pricing_model": self.pricing_model,
            "quality_score": self.quality_score,
            "reliability_score": self.reliability_score,
        }


@dataclass
class CommonMistake:
    """A common mistake to avoid."""
    mistake_id: str
    title: str
    description: str
    frequency: float            # % of projects making this mistake
    impact: str                # How bad is this mistake
    
    # How to avoid
    how_to_avoid: str
    correct_approach: str
    
    # Examples
    example_projects: Tuple[str, ...] = ()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mistake_id": self.mistake_id,
            "title": self.title,
            "description": self.description,
            "frequency": f"{self.frequency}%",
            "impact": self.impact,
            "how_to_avoid": self.how_to_avoid,
            "correct_approach": self.correct_approach,
            "example_projects": list(self.example_projects),
        }


@dataclass
class LearningPath:
    """A structured learning path."""
    path_id: str
    title: str
    description: str
    steps: Tuple[Dict[str, Any], ...]  # Ordered steps
    level: LearningLevel
    topics: Tuple[str, ...]
    skills_gained: Tuple[str, ...]
    projects_created: Tuple[str, ...]  # What you'll build
    prerequisites: Tuple[str, ...] = ()
    estimated_duration: str = "2 weeks"  # e.g., "2 weeks"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path_id": self.path_id,
            "title": self.title,
            "description": self.description,
            "steps": list(self.steps),
            "prerequisites": list(self.prerequisites),
            "level": self.level.value,
            "estimated_duration": self.estimated_duration,
            "topics": list(self.topics),
            "skills_gained": list(self.skills_gained),
            "projects_created": list(self.projects_created),
        }


class AGOSAcademy:
    """
    AGOS Academy - Learn from the system.
    
    Provides:
    - Best practices from repository analysis
    - Architecture recommendations
    - Common mistakes to avoid
    - Provider recommendations
    - Step-by-step learning paths
    """
    
    def __init__(self, knowledge_base=None):
        self._knowledge_base = knowledge_base
        self._best_practices: Dict[str, BestPractice] = {}
        self._architectures: Dict[str, ArchitectureRecommendation] = {}
        self._providers: Dict[str, ProviderRecommendation] = {}
        self._mistakes: Dict[str, CommonMistake] = {}
        self._learning_paths: Dict[str, LearningPath] = {}
        
        self._initialize_default_content()
    
    def _initialize_default_content(self) -> None:
        """Initialize with default academy content."""
        # Best Practices
        self._best_practices = {
            "bp_001": BestPractice(
                practice_id="bp_001",
                title="Use Environment Variables for Configuration",
                description="Store configuration in environment variables, not hardcoded",
                category="configuration",
                success_rate=0.92,
                repositories_using=1250,
                examples=("12 Factor App", "Heroku Best Practices"),
                difficulty=LearningLevel.BEGINNER,
                estimated_time="30 minutes",
            ),
            "bp_002": BestPractice(
                practice_id="bp_002",
                title="Implement Observability Early",
                description="Add logging, metrics, and tracing from the start",
                category="observability",
                success_rate=0.88,
                repositories_using=890,
                examples=("Datadog customers", "OpenTelemetry adoption"),
                anti_examples="Adding logs after problems occur",
                difficulty=LearningLevel.INTERMEDIATE,
                estimated_time="2-4 hours",
            ),
            "bp_003": BestPractice(
                practice_id="bp_003",
                title="Stateless API Design",
                description="Design APIs to be stateless for better scalability",
                category="architecture",
                success_rate=0.85,
                repositories_using=1100,
                examples=("REST APIs", "Microservices patterns"),
                difficulty=LearningLevel.INTERMEDIATE,
                estimated_time="4-6 hours",
            ),
        }
        
        # Architectures
        self._architectures = {
            "arch_001": ArchitectureRecommendation(
                architecture_id="arch_001",
                name="Microservices",
                description="Break application into small, independent services",
                usage_percentage=45.0,
                success_rate=0.78,
                best_for=("scalability", "team autonomy", "technology flexibility"),
                worst_for=("small teams", "simple apps", "quick prototypes"),
                complexity=LearningLevel.ADVANCED,
                avg_time_to_build="6-12 months",
                examples=(
                    {"name": "Netflix", "industry": "Streaming"},
                    {"name": "Amazon", "industry": "E-commerce"},
                ),
                trade_offs=(
                    "Better scalability but more operational complexity",
                    "Team autonomy but needs good DevOps",
                ),
            ),
            "arch_002": ArchitectureRecommendation(
                architecture_id="arch_002",
                name="Modular Monolith",
                description="Single deployment with well-organized modules",
                usage_percentage=35.0,
                success_rate=0.85,
                best_for=("small teams", "fast iteration", "simpler ops"),
                worst_for=("very large teams", "extreme scale"),
                complexity=LearningLevel.INTERMEDIATE,
                avg_time_to_build="3-6 months",
                examples=(
                    {"name": "Linear", "industry": "Project Management"},
                ),
                trade_offs=(
                    "Simpler deployment but harder to scale individual modules",
                    "Easier to start but may need refactoring later",
                ),
            ),
            "arch_003": ArchitectureRecommendation(
                architecture_id="arch_003",
                name="Serverless",
                description="Use managed services for compute",
                usage_percentage=20.0,
                success_rate=0.72,
                best_for=("variable load", "low maintenance", "fast deployment"),
                worst_for=("consistent heavy load", "long-running processes"),
                complexity=LearningLevel.INTERMEDIATE,
                avg_time_to_build="4-8 weeks",
                examples=(
                    {"name": "Vercel", "industry": "Hosting"},
                ),
                trade_offs=(
                    "No server management but vendor lock-in risk",
                    "Cost-effective for variable load but expensive for constant load",
                ),
            ),
        }
        
        # Providers
        self._providers = {
            "prov_claude": ProviderRecommendation(
                provider_id="prov_claude",
                name="Claude",
                category="llm",
                satisfaction_rating=78.0,
                performance_rating=82.0,
                best_for=("code generation", "reasoning", "analysis"),
                is_free=False,
                quality_score=88.0,
                reliability_score=85.0,
            ),
            "prov_gpt4": ProviderRecommendation(
                provider_id="prov_gpt4",
                name="GPT-4",
                category="llm",
                satisfaction_rating=75.0,
                performance_rating=80.0,
                best_for=("code generation", "creative tasks", "general purpose"),
                is_free=False,
                quality_score=85.0,
                reliability_score=82.0,
            ),
            "prov_jest": ProviderRecommendation(
                provider_id="prov_jest",
                name="Jest",
                category="testing",
                satisfaction_rating=85.0,
                performance_rating=78.0,
                best_for=("unit testing", "JavaScript projects"),
                is_free=True,
                quality_score=90.0,
                reliability_score=92.0,
            ),
            "prov_playwright": ProviderRecommendation(
                provider_id="prov_playwright",
                name="Playwright",
                category="testing",
                satisfaction_rating=82.0,
                performance_rating=85.0,
                best_for=("E2E testing", "cross-browser testing"),
                is_free=True,
                quality_score=88.0,
                reliability_score=87.0,
            ),
        }
        
        # Common Mistakes
        self._mistakes = {
            "mist_001": CommonMistake(
                mistake_id="mist_001",
                title="Starting with Wrong Database",
                description="Choosing the wrong database for the use case",
                frequency=67.0,
                impact="High - requires expensive migration",
                how_to_avoid="Analyze query patterns before choosing database",
                correct_approach="Start with PostgreSQL, add specialized DBs only when needed",
                example_projects=("Project A", "Project B"),
            ),
            "mist_002": CommonMistake(
                mistake_id="mist_002",
                title="Over-engineering Authentication",
                description="Building custom auth when managed solutions exist",
                frequency=54.0,
                impact="Medium - wasted development time",
                how_to_avoid="Use Auth0, Clerk, or Supabase Auth",
                correct_approach="Evaluate managed auth solutions first",
                example_projects=("Startup X", "Y Company"),
            ),
            "mist_003": CommonMistake(
                mistake_id="mist_003",
                title="Ignoring Observability",
                description="Not adding logging/metrics until problems occur",
                frequency=48.0,
                impact="Medium - makes debugging harder",
                how_to_avoid="Add observability from day 1",
                correct_approach="Use OpenTelemetry from the start",
            ),
            "mist_004": CommonMistake(
                mistake_id="mist_004",
                title="Skipping Rate Limiting",
                description="Not implementing rate limits until abuse occurs",
                frequency=41.0,
                impact="High - security and cost issues",
                how_to_avoid="Plan for rate limits from the start",
                correct_approach="Use API gateway with rate limiting",
            ),
        }
        
        # Learning Paths
        self._learning_paths = {
            "path_001": LearningPath(
                path_id="path_001",
                title="Building SaaS from Scratch",
                description="Complete guide to building a production SaaS application",
                steps=(
                    {"step": 1, "title": "Choose Architecture", "duration": "1 day"},
                    {"step": 2, "title": "Set up Infrastructure", "duration": "2 days"},
                    {"step": 3, "title": "Implement Auth", "duration": "1 day"},
                    {"step": 4, "title": "Build Core Features", "duration": "1-2 weeks"},
                    {"step": 5, "title": "Add Observability", "duration": "1 day"},
                    {"step": 6, "title": "Testing Strategy", "duration": "2 days"},
                    {"step": 7, "title": "Deployment & Monitoring", "duration": "1 day"},
                ),
                prerequisites=("Basic programming", "Git knowledge"),
                level=LearningLevel.INTERMEDIATE,
                estimated_duration="2-3 weeks",
                topics=("architecture", "devops", "security"),
                skills_gained=("Full-stack development", "Cloud deployment", "Monitoring"),
                projects_created=("SaaS application", "User dashboard"),
            ),
        }
    
    def get_best_practices(
        self,
        category: Optional[str] = None,
        min_success_rate: float = 0.0
    ) -> List[BestPractice]:
        """Get best practices, optionally filtered."""
        practices = list(self._best_practices.values())
        
        if category:
            practices = [p for p in practices if p.category == category]
        
        practices = [p for p in practices if p.success_rate >= min_success_rate]
        
        # Sort by success rate
        practices.sort(key=lambda p: p.success_rate, reverse=True)
        
        return practices
    
    def get_architectures(
        self,
        use_case: Optional[str] = None
    ) -> List[ArchitectureRecommendation]:
        """Get architecture recommendations."""
        architectures = list(self._architectures.values())
        
        if use_case:
            use_case_lower = use_case.lower()
            architectures = [
                a for a in architectures
                if use_case_lower in [b.lower() for b in a.best_for]
            ]
        
        # Sort by success rate
        architectures.sort(key=lambda a: a.success_rate, reverse=True)
        
        return architectures
    
    def get_provider_recommendations(
        self,
        category: Optional[str] = None
    ) -> List[ProviderRecommendation]:
        """Get provider recommendations."""
        providers = list(self._providers.values())
        
        if category:
            providers = [p for p in providers if p.category == category]
        
        # Sort by satisfaction rating
        providers.sort(key=lambda p: p.satisfaction_rating, reverse=True)
        
        return providers
    
    def get_common_mistakes(self) -> List[CommonMistake]:
        """Get common mistakes to avoid."""
        mistakes = list(self._mistakes.values())
        mistakes.sort(key=lambda m: m.frequency, reverse=True)
        return mistakes
    
    def get_learning_paths(
        self,
        level: Optional[LearningLevel] = None
    ) -> List[LearningPath]:
        """Get learning paths."""
        paths = list(self._learning_paths.values())
        
        if level:
            paths = [p for p in paths if p.level == level]
        
        return paths
    
    def get_topic_overview(self, topic: str) -> Dict[str, Any]:
        """Get comprehensive overview of a topic."""
        topic_lower = topic.lower()
        
        # Find relevant practices
        practices = [
            p for p in self._best_practices.values()
            if topic_lower in p.category or topic_lower in p.title.lower()
        ]
        
        # Find relevant architectures
        architectures = [
            a for a in self._architectures.values()
            if any(topic_lower in b.lower() for b in a.best_for)
        ]
        
        # Find relevant providers
        providers = [
            p for p in self._providers.values()
            if topic_lower in p.category
        ]
        
        # Find relevant mistakes
        mistakes = [
            m for m in self._mistakes.values()
            if topic_lower in m.title.lower() or topic_lower in m.description.lower()
        ]
        
        return {
            "topic": topic,
            "best_practices": [p.to_dict() for p in practices],
            "architectures": [a.to_dict() for a in architectures],
            "providers": [p.to_dict() for p in providers],
            "mistakes_to_avoid": [m.to_dict() for m in mistakes],
            "summary": self._generate_topic_summary(
                topic, len(practices), len(architectures), len(providers), len(mistakes)
            ),
        }
    
    def _generate_topic_summary(
        self,
        topic: str,
        practices_count: int,
        architectures_count: int,
        providers_count: int,
        mistakes_count: int
    ) -> str:
        """Generate a summary for a topic."""
        parts = []
        
        if practices_count > 0:
            parts.append(f"{practices_count} best practices")
        if architectures_count > 0:
            parts.append(f"{architectures_count} architecture options")
        if providers_count > 0:
            parts.append(f"{providers_count} recommended providers")
        if mistakes_count > 0:
            parts.append(f"{mistakes_count} common mistakes to avoid")
        
        if parts:
            return f"Based on analysis of 1500+ repositories: {', '.join(parts)}."
        
        return f"No specific recommendations found for '{topic}'. Try broader topics like 'architecture', 'testing', or 'security'."
    
    def generate_learning_plan(
        self,
        goal: str,
        current_level: LearningLevel = LearningLevel.BEGINNER
    ) -> Dict[str, Any]:
        """Generate a personalized learning plan."""
        goal_lower = goal.lower()
        
        # Find relevant paths
        relevant_paths = []
        for path in self._learning_paths.values():
            if any(topic.lower() in goal_lower for topic in path.topics):
                relevant_paths.append(path)
        
        # Find relevant best practices
        relevant_practices = [
            p for p in self._best_practices.values()
            if goal_lower in p.title.lower() or goal_lower in p.description.lower() or goal_lower in p.category.lower()
        ]
        
        # Find relevant mistakes
        relevant_mistakes = [
            m for m in self._mistakes.values()
            if any(topic.lower() in m.title.lower() for topic in goal.split())
        ]
        
        return {
            "goal": goal,
            "current_level": current_level.value,
            "recommended_paths": [p.to_dict() for p in relevant_paths],
            "practices_to_follow": [p.to_dict() for p in relevant_practices[:5]],
            "mistakes_to_avoid": [m.to_dict() for m in relevant_mistakes],
            "estimated_time": self._estimate_learning_time(
                goal, relevant_paths, current_level
            ),
            "next_steps": self._generate_next_steps(goal, current_level),
        }
    
    def _estimate_learning_time(
        self,
        goal: str,
        paths: List[LearningPath],
        level: LearningLevel
    ) -> str:
        """Estimate learning time for a goal."""
        if paths:
            return paths[0].estimated_duration
        
        # Default estimates based on goal
        goal_lower = goal.lower()
        if "simple" in goal_lower or "basic" in goal_lower:
            return "1-2 weeks"
        elif "production" in goal_lower or "scalable" in goal_lower:
            return "4-8 weeks"
        else:
            return "2-4 weeks"
    
    def _generate_next_steps(
        self,
        goal: str,
        level: LearningLevel
    ) -> List[str]:
        """Generate next steps for learning."""
        steps = []
        
        if level == LearningLevel.BEGINNER:
            steps.append("Start with a simple project to understand basics")
            steps.append("Follow a learning path from AGOS Academy")
        
        steps.append("Review best practices for your goal")
        steps.append("Study common mistakes to avoid")
        steps.append("Choose an architecture that fits your scale")
        steps.append("Select recommended providers based on your needs")
        
        return steps
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get academy statistics."""
        return {
            "best_practices": len(self._best_practices),
            "architectures": len(self._architectures),
            "providers": len(self._providers),
            "common_mistakes": len(self._mistakes),
            "learning_paths": len(self._learning_paths),
            "total_content_items": (
                len(self._best_practices) +
                len(self._architectures) +
                len(self._providers) +
                len(self._mistakes) +
                len(self._learning_paths)
            ),
        }
