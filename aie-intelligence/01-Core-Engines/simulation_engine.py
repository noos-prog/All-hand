#!/usr/bin/env python3
"""
AIE - Simulation Engine
====================

The Simulation Engine runs what-if scenarios and predictions.
It simulates outcomes before committing to decisions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import random


class SimulationType(Enum):
    """Types of simulation."""
    MONTE_CARLO = "monte_carlo"
    AGENT_BASED = "agent_based"
    SYSTEM_DYNAMICS = "system_dynamics"
    MARKOV_CHAIN = "markov_chain"
    MONTE_CARLO_TREE = "monte_carlo_tree"


class SimulationStatus(Enum):
    """Status of simulation."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class StateVector:
    """
    Represents a state in the simulation.
    """
    state_id: str
    values: Dict[str, Any]              # Variable values
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def distance_to(self, other: "StateVector") -> float:
        """Calculate distance to another state."""
        distance = 0.0
        for key in self.values:
            if key in other.values:
                v1 = self.values[key]
                v2 = other.values[key]
                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    distance += (v1 - v2) ** 2
        return distance ** 0.5
    
    def clone(self) -> "StateVector":
        """Create a copy of this state."""
        return StateVector(
            state_id=f"{self.state_id}_clone",
            values=self.values.copy(),
            timestamp=datetime.utcnow().isoformat(),
            metadata=self.metadata.copy(),
        )


@dataclass
class StateTransition:
    """
    A transition between states.
    """
    transition_id: str
    from_state: str
    to_state: str
    action: str                        # Action that caused transition
    probability: float                  # 0-1 probability
    reward: float = 0.0               # Reward/cost
    duration_ms: int = 0              # Time taken
    
    def is_probable(self, threshold: float = 0.5) -> bool:
        """Check if transition is likely."""
        return self.probability >= threshold


@dataclass
class SimulationScenario:
    """
    A simulation scenario to run.
    """
    scenario_id: str
    name: str
    description: str
    
    # Initial state
    initial_state: StateVector
    
    # Transitions
    transitions: Tuple[StateTransition, ...] = ()
    
    # Constraints
    max_steps: int = 100
    max_duration_ms: int = 60000
    
    # Simulation parameters
    simulation_type: SimulationType = SimulationType.MONTE_CARLO
    iterations: int = 1000
    
    def get_valid_transitions(self, current_state_id: str) -> List[StateTransition]:
        """Get valid transitions from a state."""
        return [
            t for t in self.transitions
            if t.from_state == current_state_id
        ]


@dataclass
class SimulationResult:
    """
    Result of a simulation run.
    """
    result_id: str
    scenario_id: str
    status: SimulationStatus
    paths_explored: int
    states_reached: int
    success_rate: float
    avg_duration_ms: float
    avg_reward: float
    outcome_distribution: Dict[str, int]
    started_at: str
    best_path: Optional[List[str]] = None
    worst_path: Optional[List[str]] = None
    trajectories: Tuple[Tuple[str, ...], ...] = ()
    confidence: float = 0.0
    completed_at: Optional[str] = None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of results."""
        return {
            "result_id": self.result_id,
            "status": self.status.value,
            "success_rate": f"{self.success_rate:.1%}",
            "paths_explored": self.paths_explored,
            "avg_duration": f"{self.avg_duration_ms:.0f}ms",
            "confidence": f"{self.confidence:.1%}",
        }


class SimulationEngine:
    """
    The Simulation Engine - fourth stage of AIE.
    
    Responsibilities:
    - Run what-if scenarios
    - Simulate outcomes
    - Predict results
    - Explore state spaces
    
    The Simulation Engine does NOT:
    - Make decisions
    - Choose actions
    """
    
    def __init__(self):
        self._scenarios: Dict[str, SimulationScenario] = {}
        self._results: Dict[str, SimulationResult] = {}
        self._state_cache: Dict[str, StateVector] = {}
        self._initialized = True
    
    def create_scenario(
        self,
        scenario_id: str,
        name: str,
        description: str,
        initial_values: Dict[str, Any],
        transitions: List[Dict[str, Any]]
    ) -> SimulationScenario:
        """Create a simulation scenario."""
        initial_state = StateVector(
            state_id="initial",
            values=initial_values,
            timestamp=datetime.utcnow().isoformat(),
        )
        
        state_transitions = [
            StateTransition(
                transition_id=t.get("id", f"t_{i}"),
                from_state=t["from_state"],
                to_state=t["to_state"],
                action=t.get("action", "default"),
                probability=t.get("probability", 1.0),
                reward=t.get("reward", 0.0),
                duration_ms=t.get("duration_ms", 100),
            )
            for i, t in enumerate(transitions)
        ]
        
        scenario = SimulationScenario(
            scenario_id=scenario_id,
            name=name,
            description=description,
            initial_state=initial_state,
            transitions=tuple(state_transitions),
        )
        
        self._scenarios[scenario_id] = scenario
        return scenario
    
    def run_simulation(
        self,
        scenario_id: str,
        simulation_type: SimulationType = SimulationType.MONTE_CARLO,
        iterations: int = 1000
    ) -> SimulationResult:
        """Run a simulation."""
        scenario = self._scenarios.get(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        result_id = f"result_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        started_at = datetime.utcnow().isoformat()
        
        # Run simulation based on type
        if simulation_type == SimulationType.MONTE_CARLO:
            result = self._run_monte_carlo(scenario, iterations)
        elif simulation_type == SimulationType.MARKOV_CHAIN:
            result = self._run_markov_chain(scenario, iterations)
        else:
            result = self._run_monte_carlo(scenario, iterations)
        
        # Set result metadata
        result.result_id = result_id
        result.scenario_id = scenario_id
        result.started_at = started_at
        result.completed_at = datetime.utcnow().isoformat()
        
        # Calculate confidence
        result.confidence = self._calculate_confidence(result, iterations)
        
        self._results[result_id] = result
        return result
    
    def _run_monte_carlo(
        self,
        scenario: SimulationScenario,
        iterations: int
    ) -> SimulationResult:
        """Run Monte Carlo simulation."""
        trajectories = []
        outcomes = {}
        durations = []
        rewards = []
        success_count = 0
        
        for _ in range(iterations):
            path, outcome, duration, reward = self._simulate_path(scenario)
            trajectories.append(tuple(path))
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            durations.append(duration)
            rewards.append(reward)
            if outcome == "success":
                success_count += 1
        
        # Find best and worst paths
        best_path = min(trajectories, key=lambda p: sum(r for r in rewards if r), default=None)
        worst_path = max(trajectories, key=lambda p: sum(r for r in rewards if r), default=None)
        
        return SimulationResult(
            result_id="",
            scenario_id=scenario.scenario_id,
            status=SimulationStatus.COMPLETED,
            paths_explored=iterations,
            states_reached=len(set(s for t in trajectories for s in t)),
            success_rate=success_count / iterations if iterations > 0 else 0,
            avg_duration_ms=sum(durations) / len(durations) if durations else 0,
            avg_reward=sum(rewards) / len(rewards) if rewards else 0,
            outcome_distribution=outcomes,
            best_path=list(best_path) if best_path else None,
            worst_path=list(worst_path) if worst_path else None,
            trajectories=tuple(trajectories),
            confidence=0.0,
            started_at="",
        )
    
    def _run_markov_chain(
        self,
        scenario: SimulationScenario,
        iterations: int
    ) -> SimulationResult:
        """Run Markov chain simulation."""
        # Simplified Markov chain simulation
        current_state = scenario.initial_state.state_id
        path = [current_state]
        total_reward = 0.0
        total_duration = 0
        
        for _ in range(scenario.max_steps):
            valid_transitions = scenario.get_valid_transitions(current_state)
            
            if not valid_transitions:
                break
            
            # Choose transition by probability
            chosen = self._choose_by_probability(valid_transitions)
            if not chosen:
                break
            
            total_reward += chosen.reward
            total_duration += chosen.duration_ms
            current_state = chosen.to_state
            path.append(current_state)
            
            if current_state == "terminal":
                break
        
        outcome = "success" if total_reward > 0 else "failure"
        
        return SimulationResult(
            result_id="",
            scenario_id=scenario.scenario_id,
            status=SimulationStatus.COMPLETED,
            paths_explored=1,
            states_reached=len(set(path)),
            success_rate=1.0 if outcome == "success" else 0.0,
            avg_duration_ms=total_duration,
            avg_reward=total_reward,
            outcome_distribution={outcome: 1},
            best_path=path,
            worst_path=path,
            trajectories=(tuple(path),),
            confidence=0.0,
            started_at="",
        )
    
    def _simulate_path(
        self,
        scenario: SimulationScenario
    ) -> Tuple[List[str], str, int, float]:
        """Simulate a single path through the scenario."""
        current_state = scenario.initial_state.state_id
        path = [current_state]
        total_reward = 0.0
        total_duration = 0
        
        for _ in range(scenario.max_steps):
            valid_transitions = scenario.get_valid_transitions(current_state)
            
            if not valid_transitions:
                break
            
            # Check probability threshold
            possible_transitions = [t for t in valid_transitions if t.is_probable(0.3)]
            if not possible_transitions:
                possible_transitions = valid_transitions
            
            # Random selection
            chosen = random.choice(possible_transitions)
            
            total_reward += chosen.reward
            total_duration += chosen.duration_ms
            current_state = chosen.to_state
            path.append(current_state)
            
            if current_state == "terminal":
                break
        
        outcome = "success" if total_reward > 0 else "failure"
        return path, outcome, total_duration, total_reward
    
    def _choose_by_probability(
        self,
        transitions: List[StateTransition]
    ) -> Optional[StateTransition]:
        """Choose a transition based on probability."""
        if not transitions:
            return None
        
        # Normalize probabilities
        total_prob = sum(t.probability for t in transitions)
        if total_prob == 0:
            return None
        
        rand = random.random() * total_prob
        cumulative = 0.0
        
        for t in transitions:
            cumulative += t.probability
            if rand <= cumulative:
                return t
        
        return transitions[-1]
    
    def _calculate_confidence(
        self,
        result: SimulationResult,
        iterations: int
    ) -> float:
        """Calculate confidence based on sample size and variance."""
        if result.paths_explored < 100:
            return 0.5
        
        # Confidence increases with more samples
        base_confidence = min(0.95, result.paths_explored / 1000)
        
        # Penalize for high variance (simplified)
        outcome_dist = result.outcome_distribution
        if len(outcome_dist) > 1:
            max_proportion = max(outcome_dist.values()) / sum(outcome_dist.values())
            variance_penalty = (1 - max_proportion) * 0.2
            base_confidence -= variance_penalty
        
        return round(base_confidence, 3)
    
    def predict_outcome(
        self,
        scenario_id: str,
        num_predictions: int = 100
    ) -> Dict[str, float]:
        """Predict likely outcomes."""
        result = self.run_simulation(scenario_id, iterations=num_predictions)
        
        # Convert to probabilities
        total = sum(result.outcome_distribution.values())
        predictions = {
            outcome: count / total
            for outcome, count in result.outcome_distribution.items()
        }
        
        return predictions
    
    def get_result(self, result_id: str) -> Optional[SimulationResult]:
        """Get a simulation result."""
        return self._results.get(result_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        total_simulations = len(self._results)
        completed = len([r for r in self._results.values() if r.status == SimulationStatus.COMPLETED])
        
        return {
            "total_scenarios": len(self._scenarios),
            "total_simulations": total_simulations,
            "completed_simulations": completed,
            "avg_success_rate": (
                sum(r.success_rate for r in self._results.values()) / total_simulations
                if total_simulations > 0 else 0
            ),
        }
