"""
AGOS Cognitive Engines
======================

Small, composable engines that each solve one narrow cognitive problem:
intent, goals, context, constraints, reasoning, planning, strategy,
deliberation, evaluation, decisions.

They share the primitive types from :mod:`cognition.model` so an agent
can wire any subset together without adapters.
"""

from .constraint import Constraint, ConstraintEngine, ConstraintViolation
from .context import ContextEngine, ContextFrame
from .decision import DecisionEngine
from .deliberation import DeliberationEngine, DeliberationResult
from .evaluation import EvaluationEngine, EvaluationResult
from .goal import GoalEngine
from .intent import IntentEngine
from .planning import PlanningEngine
from .reasoning import ReasoningEngine, ReasoningStep
from .strategy import Strategy, StrategyEngine

__all__ = [
    "Constraint",
    "ConstraintEngine",
    "ConstraintViolation",
    "ContextEngine",
    "ContextFrame",
    "DecisionEngine",
    "DeliberationEngine",
    "DeliberationResult",
    "EvaluationEngine",
    "EvaluationResult",
    "GoalEngine",
    "IntentEngine",
    "PlanningEngine",
    "ReasoningEngine",
    "ReasoningStep",
    "Strategy",
    "StrategyEngine",
]
