"""
AGOS Factory — the agent factory that produces civilization agents on demand.

Public API:
    AgentBlueprint, BlueprintRegistry   -- what an agent of a given
                                           specialization IS (prompt, tool,
                                           concurrency limits).
    FactoryAgent                        -- an ephemeral, real agent instance
                                           (LLM brain + optional real tool).
    AgentPool                           -- a bounded, recyclable pool of
                                           live FactoryAgent instances for one
                                           specialization.
    Autoscaler                          -- decides pool target sizes from
                                           live utilization, not guesses.
    FactoryMetrics                      -- thread-safe/async-safe counters.
    AgentFactory                        -- the top-level orchestrator.
"""

from .blueprint import AgentBlueprint, BlueprintRegistry
from .agent import FactoryAgent
from .metrics import FactoryMetrics
from .pool import AgentPool
from .autoscaler import Autoscaler, AutoscalerPolicy
from .factory import AgentFactory

__all__ = [
    "AgentBlueprint",
    "BlueprintRegistry",
    "FactoryAgent",
    "FactoryMetrics",
    "AgentPool",
    "Autoscaler",
    "AutoscalerPolicy",
    "AgentFactory",
]
