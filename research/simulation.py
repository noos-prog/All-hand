"""Simulation Engine - Simulate agent behaviors and scenarios."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

SIMULATION_TYPES = ["Agent Behavior", "System Load", "Network", "Market", "Evolution", "Stress Test"]


class SimulationStatus(Enum):
    """Simulation status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Simulation:
    """A simulation scenario."""
    simulation_id: str
    name: str
    simulation_type: str
    duration_seconds: int
    agents: List[str] = field(default_factory=list)
    status: SimulationStatus = SimulationStatus.PENDING
    results: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SimulationResult:
    """Result of a simulation."""
    result_id: str
    simulation_id: str
    metrics: Dict[str, float] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)
    completed_at: datetime = field(default_factory=datetime.utcnow)


class SimulationEngine:
    """Engine for running simulations."""
    
    def __init__(self):
        self._simulations: Dict[str, Simulation] = {}
        self._results: Dict[str, SimulationResult] = {}
    
    def create_simulation(self, name: str, simulation_type: str, duration_seconds: int) -> Simulation:
        simulation = Simulation(
            simulation_id=str(uuid.uuid4()),
            name=name,
            simulation_type=simulation_type,
            duration_seconds=duration_seconds,
        )
        self._simulations[simulation.simulation_id] = simulation
        return simulation
    
    def run(self, simulation: Simulation) -> SimulationResult:
        simulation.status = SimulationStatus.RUNNING
        result = SimulationResult(
            result_id=str(uuid.uuid4()),
            simulation_id=simulation.simulation_id,
            metrics={"success_rate": 0.95, "avg_response_time": 100.0},
        )
        simulation.status = SimulationStatus.COMPLETED
        self._results[result.result_id] = result
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_simulations": len(self._simulations),
            "simulation_types": SIMULATION_TYPES,
        }
