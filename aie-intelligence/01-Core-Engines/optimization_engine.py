#!/usr/bin/env python3
"""
AIE - Optimization Engine
=======================

The Optimization Engine finds the best solution among options.
It maximizes, minimizes, or balances objectives.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime


class OptimizationType(Enum):
    """Types of optimization."""
    LINEAR = "linear"
    INTEGER = "integer"
    QUADRATIC = "quadratic"
    GENETIC = "genetic"
    GRADIENT_DESCENT = "gradient_descent"
    SIMULATED_ANNEALING = "simulated_annealing"
    PARTICLE_SWARM = "particle_swarm"


class ConstraintType(Enum):
    """Types of constraints."""
    EQUALITY = "equality"
    INEQUALITY = "inequality"
    BOUND = "bound"


@dataclass
class Variable:
    """An optimization variable."""
    name: str
    lower_bound: float = float('-inf')
    upper_bound: float = float('inf')
    is_integer: bool = False
    current_value: Optional[float] = None
    
    def is_within_bounds(self, value: float) -> bool:
        """Check if value is within bounds."""
        return self.lower_bound <= value <= self.upper_bound


@dataclass
class Constraint:
    """An optimization constraint."""
    constraint_id: str
    name: str
    constraint_type: ConstraintType
    
    # Function that returns LHS value
    evaluate: Callable[[Dict[str, float]], float]
    
    # RHS value
    rhs_value: float
    
    # Tolerance for floating point
    tolerance: float = 1e-6
    
    def is_satisfied(self, values: Dict[str, float]) -> bool:
        """Check if constraint is satisfied."""
        lhs = self.evaluate(values)
        
        if self.constraint_type == ConstraintType.EQUALITY:
            return abs(lhs - self.rhs_value) < self.tolerance
        elif self.constraint_type == ConstraintType.INEQUALITY:
            return lhs >= self.rhs_value - self.tolerance
        else:  # BOUND
            return self.name.startswith("min_") and lhs >= self.rhs_value or lhs <= self.rhs_value
    
    def violation_amount(self, values: Dict[str, float]) -> float:
        """Calculate how much constraint is violated."""
        lhs = self.evaluate(values)
        
        if self.constraint_type == ConstraintType.EQUALITY:
            return abs(lhs - self.rhs_value)
        elif self.constraint_type == ConstraintType.INEQUALITY:
            return max(0, self.rhs_value - lhs)
        return 0.0


@dataclass
class OptimizationObjective:
    """An optimization objective."""
    objective_id: str
    name: str
    objective_type: str  # "minimize" or "maximize"
    
    # Objective function
    evaluate: Callable[[Dict[str, float]], float]
    
    # Weight for multi-objective
    weight: float = 1.0
    
    def evaluate_value(self, values: Dict[str, float]) -> float:
        """Evaluate objective."""
        value = self.evaluate(values)
        if self.objective_type == "minimize":
            return value
        else:
            return -value  # Convert maximize to minimize


@dataclass
class Solution:
    """A candidate solution."""
    solution_id: str
    values: Dict[str, float]
    objectives: Dict[str, float]              # Objective values
    total_cost: float                         # Total weighted cost
    is_feasible: bool                        # Satisfies all constraints
    constraint_violations: Dict[str, float]  # Violation amount per constraint
    
    def dominates(self, other: "Solution") -> bool:
        """Check if this solution dominates another (Pareto)."""
        if not self.is_feasible and other.is_feasible:
            return False
        if self.is_feasible and not other.is_feasible:
            return True
        
        at_least_as_good = all(
            self.objectives.get(k, 0) <= other.objectives.get(k, 0)
            for k in self.objectives
        )
        strictly_better = any(
            self.objectives.get(k, 0) < other.objectives.get(k, 0)
            for k in self.objectives
        )
        
        return at_least_as_good and strictly_better


@dataclass
class OptimizationResult:
    """Result of optimization."""
    result_id: str
    optimization_type: OptimizationType
    best_solution: Optional[Solution]
    iterations: int
    function_evaluations: int
    convergence_achieved: bool
    duration_ms: int
    timestamp: str
    pareto_front: Tuple[Solution, ...] = ()
    metadata: Dict[str, Any] = field(default_factory=dict)


class OptimizationEngine:
    """
    The Optimization Engine - fifth stage of AIE.
    
    Responsibilities:
    - Find optimal solutions
    - Handle constraints
    - Balance multiple objectives
    
    The Optimization Engine does NOT:
    - Make decisions
    - Execute actions
    """
    
    def __init__(self):
        self._variables: Dict[str, Variable] = {}
        self._constraints: Dict[str, Constraint] = {}
        self._objectives: Dict[str, OptimizationObjective] = {}
        self._results: List[OptimizationResult] = []
        self._initialized = True
    
    def define_variable(
        self,
        name: str,
        lower_bound: float = float('-inf'),
        upper_bound: float = float('inf'),
        is_integer: bool = False
    ) -> Variable:
        """Define an optimization variable."""
        variable = Variable(
            name=name,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            is_integer=is_integer,
        )
        self._variables[name] = variable
        return variable
    
    def add_constraint(
        self,
        constraint_id: str,
        name: str,
        constraint_type: ConstraintType,
        evaluate: Callable[[Dict[str, float]], float],
        rhs_value: float
    ) -> Constraint:
        """Add a constraint."""
        constraint = Constraint(
            constraint_id=constraint_id,
            name=name,
            constraint_type=constraint_type,
            evaluate=evaluate,
            rhs_value=rhs_value,
        )
        self._constraints[constraint_id] = constraint
        return constraint
    
    def add_objective(
        self,
        objective_id: str,
        name: str,
        objective_type: str,
        evaluate: Callable[[Dict[str, float]], float],
        weight: float = 1.0
    ) -> OptimizationObjective:
        """Add an objective."""
        objective = OptimizationObjective(
            objective_id=objective_id,
            name=name,
            objective_type=objective_type,
            evaluate=evaluate,
            weight=weight,
        )
        self._objectives[objective_id] = objective
        return objective
    
    def optimize(
        self,
        optimization_type: OptimizationType = OptimizationType.GENETIC,
        max_iterations: int = 1000,
        population_size: int = 100
    ) -> OptimizationResult:
        """Run optimization."""
        start_time = datetime.utcnow()
        result_id = f"opt_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        if optimization_type == OptimizationType.GENETIC:
            best, pareto = self._genetic_algorithm(max_iterations, population_size)
        elif optimization_type == OptimizationType.GRADIENT_DESCENT:
            best, pareto = self._gradient_descent(max_iterations)
        elif optimization_type == OptimizationType.SIMULATED_ANNEALING:
            best, pareto = self._simulated_annealing(max_iterations)
        else:
            best, pareto = self._genetic_algorithm(max_iterations, population_size)
        
        duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        result = OptimizationResult(
            result_id=result_id,
            optimization_type=optimization_type,
            best_solution=best,
            pareto_front=tuple(pareto),
            iterations=max_iterations,
            function_evaluations=max_iterations * population_size,
            convergence_achieved=True,
            duration_ms=duration,
            timestamp=datetime.utcnow().isoformat(),
        )
        
        self._results.append(result)
        return result
    
    def _genetic_algorithm(
        self,
        max_iterations: int,
        population_size: int
    ) -> Tuple[Optional[Solution], List[Solution]]:
        """Run genetic algorithm."""
        import random
        
        # Initialize population
        population = self._initialize_population(population_size)
        
        best_solution = None
        pareto_front = []
        
        for iteration in range(max_iterations):
            # Evaluate all solutions
            evaluated = []
            for solution in population:
                solution = self._evaluate_solution(solution)
                evaluated.append(solution)
                
                if not best_solution or solution.total_cost < best_solution.total_cost:
                    best_solution = solution
            
            # Update Pareto front
            pareto_front = self._update_pareto_front(pareto_front + evaluated)
            
            # Selection
            parents = self._select_parents(evaluated, population_size // 2)
            
            # Crossover
            offspring = self._crossover(parents)
            
            # Mutation
            offspring = [self._mutate(s) for s in offspring]
            
            # New population
            population = evaluated[:population_size // 2] + offspring
        
        return best_solution, pareto_front[:100]
    
    def _gradient_descent(self, max_iterations: int) -> Tuple[Optional[Solution], List[Solution]]:
        """Run gradient descent."""
        # Initialize
        values = {name: (v.lower_bound + v.upper_bound) / 2 for name, v in self._variables.items()}
        
        best_solution = None
        learning_rate = 0.1
        
        for _ in range(max_iterations):
            solution = self._evaluate_solution(values)
            
            if not best_solution or solution.total_cost < best_solution.total_cost:
                best_solution = solution
            
            # Gradient approximation
            for name in values:
                original = values[name]
                values[name] = original + learning_rate
                pos_value = self._evaluate_solution(values).total_cost
                
                values[name] = original - learning_rate
                neg_value = self._evaluate_solution(values).total_cost
                
                gradient = (pos_value - neg_value) / (2 * learning_rate)
                values[name] = original - learning_rate * gradient
                
                # Clamp to bounds
                var = self._variables[name]
                values[name] = max(var.lower_bound, min(var.upper_bound, values[name]))
        
        return best_solution, [best_solution] if best_solution else []
    
    def _simulated_annealing(self, max_iterations: int) -> Tuple[Optional[Solution], List[Solution]]:
        """Run simulated annealing."""
        import random
        import math
        
        # Initialize
        current = {name: random.uniform(v.lower_bound, v.upper_bound)
                  for name, v in self._variables.items()}
        current = self._evaluate_solution(current)
        
        best = current
        temperature = 1000.0
        cooling_rate = 0.995
        
        pareto_front = [best]
        
        for _ in range(max_iterations):
            # Generate neighbor
            neighbor = current.values.copy()
            var_name = random.choice(list(neighbor.keys()))
            var = self._variables[var_name]
            
            # Random change within bounds
            delta = random.uniform(-1, 1) * (var.upper_bound - var.lower_bound) * 0.1
            neighbor[var_name] = max(var.lower_bound, min(var.upper_bound, neighbor[var_name] + delta))
            
            neighbor = self._evaluate_solution(neighbor)
            
            # Accept or reject
            delta_cost = neighbor.total_cost - current.total_cost
            
            if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
                current = neighbor
                
                if current.total_cost < best.total_cost:
                    best = current
                    pareto_front.append(best)
            
            temperature *= cooling_rate
        
        return best, pareto_front
    
    def _initialize_population(self, size: int) -> List[Dict[str, float]]:
        """Initialize random population."""
        import random
        
        population = []
        for _ in range(size):
            values = {
                name: random.uniform(v.lower_bound, v.upper_bound)
                for name, v in self._variables.items()
            }
            population.append(values)
        
        return population
    
    def _evaluate_solution(self, values: Dict[str, float]) -> Solution:
        """Evaluate a solution."""
        solution_id = f"sol_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        # Evaluate objectives
        objective_values = {
            oid: obj.evaluate(values)
            for oid, obj in self._objectives.items()
        }
        
        # Calculate total cost (weighted sum)
        total_cost = sum(
            obj.evaluate_value(values) * obj.weight
            for obj in self._objectives.values()
        )
        
        # Check constraints
        violations = {}
        is_feasible = True
        for cid, constraint in self._constraints.items():
            if not constraint.is_satisfied(values):
                is_feasible = False
                violations[cid] = constraint.violation_amount(values)
        
        # Add penalty for infeasibility
        if not is_feasible:
            total_cost += sum(violations.values()) * 1000
        
        return Solution(
            solution_id=solution_id,
            values=values.copy(),
            objectives=objective_values,
            total_cost=total_cost,
            is_feasible=is_feasible,
            constraint_violations=violations,
        )
    
    def _select_parents(
        self,
        solutions: List[Solution],
        num_parents: int
    ) -> List[Solution]:
        """Select parents using tournament selection."""
        import random
        
        parents = []
        for _ in range(num_parents):
            tournament = random.sample(solutions, min(3, len(solutions)))
            winner = min(tournament, key=lambda s: s.total_cost)
            parents.append(winner)
        
        return parents
    
    def _crossover(self, parents: List[Solution]) -> List[Dict[str, float]]:
        """Create offspring through crossover."""
        import random
        
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            child1 = parents[i].values.copy()
            child2 = parents[i + 1].values.copy()
            
            # Single-point crossover
            crossover_point = random.choice(list(child1.keys()))
            temp = child1[crossover_point]
            child1[crossover_point] = child2[crossover_point]
            child2[crossover_point] = temp
            
            offspring.extend([child1, child2])
        
        return offspring
    
    def _mutate(self, values: Dict[str, float]) -> Dict[str, float]:
        """Mutate a solution."""
        import random
        
        mutated = values.copy()
        mutation_rate = 0.1
        
        for name, value in mutated.items():
            if random.random() < mutation_rate:
                var = self._variables[name]
                delta = random.uniform(-1, 1) * (var.upper_bound - var.lower_bound) * 0.2
                mutated[name] = max(var.lower_bound, min(var.upper_bound, value + delta))
        
        return mutated
    
    def _update_pareto_front(
        self,
        current_front: List[Solution],
        new_solutions: List[Solution]
    ) -> List[Solution]:
        """Update Pareto front with new solutions."""
        combined = current_front + new_solutions
        pareto = []
        
        for solution in combined:
            is_dominated = False
            to_remove = []
            
            for existing in pareto:
                if existing.dominates(solution):
                    is_dominated = True
                    break
                if solution.dominates(existing):
                    to_remove.append(existing)
            
            for remove in to_remove:
                pareto.remove(remove)
            
            if not is_dominated:
                pareto.append(solution)
        
        return pareto
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "variables_defined": len(self._variables),
            "constraints_defined": len(self._constraints),
            "objectives_defined": len(self._objectives),
            "optimizations_run": len(self._results),
            "avg_duration_ms": (
                sum(r.duration_ms for r in self._results) / len(self._results)
                if self._results else 0
            ),
        }
