"""
Evolution Engine Module
======================

Self-evolution engine using genetic algorithms and adaptive optimization.
Enables AGOS to evolve its own capabilities and optimize performance.

Author: AGOS Team
Version: 1.0.0
"""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class SelectionMethod(Enum):
    """Selection methods for genetic algorithms."""
    TOURNAMENT = "tournament"
    ROULETTE = "roulette"
    RANK = "rank"
    TRUNCATION = "truncation"


@dataclass
class Chromosome:
    """
    A chromosome representing a candidate solution in the evolution process.
    Contains genes that encode the solution parameters.
    """
    chromosome_id: str
    genes: List[Any]
    fitness: float = 0.0
    age: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def mutate(self, mutation_rate: float = 0.1) -> None:
        """Mutate genes based on mutation rate."""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                if isinstance(self.genes[i], (int, float)):
                    self.genes[i] = self.genes[i] * random.uniform(0.8, 1.2)
                elif isinstance(self.genes[i], str):
                    self.genes[i] = self.genes[i][::-1] if len(self.genes[i]) > 1 else self.genes[i]
                elif isinstance(self.genes[i], bool):
                    self.genes[i] = not self.genes[i]
        self.age = 0
    
    def copy(self) -> Chromosome:
        """Create a deep copy of this chromosome."""
        return Chromosome(
            chromosome_id=f"{self.chromosome_id}_copy_{uuid.uuid4().hex[:4]}",
            genes=self.genes.copy(),
            fitness=self.fitness,
            age=0,
            metadata=self.metadata.copy(),
        )


@dataclass
class Population:
    """
    A population of chromosomes representing the current generation.
    """
    population_id: str
    chromosomes: List[Chromosome] = field(default_factory=list)
    generation: int = 0
    best_fitness: float = 0.0
    average_fitness: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_chromosome(self, chromosome: Chromosome) -> None:
        """Add a chromosome to the population."""
        self.chromosomes.append(chromosome)
    
    def remove_chromosome(self, chromosome_id: str) -> bool:
        """Remove a chromosome from the population."""
        for i, c in enumerate(self.chromosomes):
            if c.chromosome_id == chromosome_id:
                self.chromosomes.pop(i)
                return True
        return False
    
    def get_best(self) -> Optional[Chromosome]:
        """Get the chromosome with highest fitness."""
        if not self.chromosomes:
            return None
        return max(self.chromosomes, key=lambda c: c.fitness)
    
    def get_elite(self, count: int) -> List[Chromosome]:
        """Get the top N chromosomes by fitness."""
        sorted_chromosomes = sorted(self.chromosomes, key=lambda c: c.fitness, reverse=True)
        return sorted_chromosomes[:count]
    
    def update_statistics(self) -> None:
        """Update population statistics."""
        if not self.chromosomes:
            self.best_fitness = 0.0
            self.average_fitness = 0.0
            return
        
        fitnesses = [c.fitness for c in self.chromosomes]
        self.best_fitness = max(fitnesses)
        self.average_fitness = sum(fitnesses) / len(fitnesses)


@dataclass
class GeneticAlgorithm:
    """
    Genetic algorithm implementation for evolution.
    Supports multiple selection methods and genetic operators.
    """
    algorithm_id: str
    population_size: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elite_count: int = 2
    selection_method: SelectionMethod = SelectionMethod.TOURNAMENT
    tournament_size: int = 3
    
    def __post_init__(self):
        self.current_population: Optional[Population] = None
    
    def initialize_population(
        self,
        gene_factory: Callable[[], List[Any]],
        population_id: Optional[str] = None,
    ) -> Population:
        """Initialize a new population with random chromosomes."""
        chromosomes = []
        for _ in range(self.population_size):
            chromosome = Chromosome(
                chromosome_id=f"chrom_{uuid.uuid4().hex[:8]}",
                genes=gene_factory(),
            )
            chromosomes.append(chromosome)
        
        self.current_population = Population(
            population_id=population_id or f"pop_{uuid.uuid4().hex[:8]}",
            chromosomes=chromosomes,
        )
        return self.current_population
    
    def _select_parent(self, population: Population) -> Chromosome:
        """Select a parent chromosome based on the selection method."""
        if self.selection_method == SelectionMethod.TOURNAMENT:
            tournament = random.sample(population.chromosomes, min(self.tournament_size, len(population.chromosomes)))
            return max(tournament, key=lambda c: c.fitness)
        
        elif self.selection_method == SelectionMethod.ROULETTE:
            total_fitness = sum(c.fitness for c in population.chromosomes)
            if total_fitness <= 0:
                return random.choice(population.chromosomes)
            pick = random.uniform(0, total_fitness)
            cumulative = 0
            for c in population.chromosomes:
                cumulative += c.fitness
                if cumulative >= pick:
                    return c
            return population.chromosomes[-1]
        
        elif self.selection_method == SelectionMethod.RANK:
            sorted_chromosomes = sorted(population.chromosomes, key=lambda c: c.fitness)
            n = len(sorted_chromosomes)
            ranks = list(range(1, n + 1))
            total_rank = sum(ranks)
            pick = random.uniform(0, total_rank)
            cumulative = 0
            for i, c in enumerate(sorted_chromosomes):
                cumulative += ranks[i]
                if cumulative >= pick:
                    return c
            return sorted_chromosomes[-1]
        
        elif self.selection_method == SelectionMethod.TRUNCATION:
            elite = population.get_elite(max(1, len(population.chromosomes) // 2))
            return random.choice(elite)
        
        return random.choice(population.chromosomes)
    
    def _crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """Perform crossover between two parent chromosomes."""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        point = random.randint(1, len(parent1.genes) - 1)
        child1_genes = parent1.genes[:point] + parent2.genes[point:]
        child2_genes = parent2.genes[:point] + parent1.genes[point:]
        
        child1 = Chromosome(
            chromosome_id=f"chrom_{uuid.uuid4().hex[:8]}",
            genes=child1_genes,
        )
        child2 = Chromosome(
            chromosome_id=f"chrom_{uuid.uuid4().hex[:8]}",
            genes=child2_genes,
        )
        
        return child1, child2
    
    def evolve_generation(self, fitness_function: Callable[[Chromosome], float]) -> Population:
        """Evolve one generation using genetic operators."""
        if not self.current_population:
            raise ValueError("Population not initialized")
        
        # Evaluate fitness
        for chromosome in self.current_population.chromosomes:
            chromosome.fitness = fitness_function(chromosome)
        
        self.current_population.update_statistics()
        
        # Create next generation
        new_chromosomes = []
        
        # Keep elite chromosomes
        elite = self.current_population.get_elite(self.elite_count)
        new_chromosomes.extend([c.copy() for c in elite])
        
        # Generate offspring
        while len(new_chromosomes) < self.population_size:
            parent1 = self._select_parent(self.current_population)
            parent2 = self._select_parent(self.current_population)
            child1, child2 = self._crossover(parent1, parent2)
            child1.mutate(self.mutation_rate)
            child2.mutate(self.mutation_rate)
            new_chromosomes.extend([child1, child2])
        
        # Trim to population size
        new_chromosomes = new_chromosomes[:self.population_size]
        
        # Age chromosomes
        for c in new_chromosomes:
            c.age += 1
        
        # Create new population
        self.current_population = Population(
            population_id=f"pop_{uuid.uuid4().hex[:8]}",
            chromosomes=new_chromosomes,
            generation=self.current_population.generation + 1,
        )
        
        return self.current_population
    
    def get_best_solution(self) -> Optional[Chromosome]:
        """Get the best solution from current population."""
        if not self.current_population:
            return None
        return self.current_population.get_best()


@dataclass
class EvolutionEngine:
    """
    Main evolution engine that orchestrates the self-improvement process.
    Combines genetic algorithms with domain-specific optimization.
    """
    engine_id: str
    genetic_algorithm: Optional[GeneticAlgorithm] = None
    objectives: Dict[str, float] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.genetic_algorithm:
            self.genetic_algorithm = GeneticAlgorithm(algorithm_id=f"ga_{uuid.uuid4().hex[:8]}")
    
    def set_objectives(self, objectives: Dict[str, float]) -> None:
        """Set optimization objectives with weights."""
        self.objectives = objectives
    
    def add_constraint(self, name: str, constraint: Any) -> None:
        """Add an optimization constraint."""
        self.constraints[name] = constraint
    
    def create_population(
        self,
        gene_factory: Callable[[], List[Any]],
        population_id: Optional[str] = None,
    ) -> Population:
        """Create a new population for evolution."""
        return self.genetic_algorithm.initialize_population(gene_factory, population_id)
    
    def evaluate(
        self,
        chromosome: Chromosome,
        fitness_function: Callable[[Chromosome, Dict], float],
    ) -> float:
        """Evaluate a chromosome's fitness."""
        return fitness_function(chromosome, {"objectives": self.objectives, "constraints": self.constraints})
    
    def step(self, fitness_function: Callable[[Chromosome], float]) -> Population:
        """Execute one evolution step."""
        population = self.genetic_algorithm.evolve_generation(fitness_function)
        
        # Record history
        self.history.append({
            "generation": population.generation,
            "best_fitness": population.best_fitness,
            "average_fitness": population.average_fitness,
            "timestamp": datetime.utcnow().isoformat(),
        })
        
        return population
    
    def evolve(
        self,
        gene_factory: Callable[[], List[Any]],
        fitness_function: Callable[[Chromosome], float],
        generations: int = 100,
        target_fitness: Optional[float] = None,
    ) -> Chromosome:
        """Run full evolution process."""
        self.create_population(gene_factory)
        
        for _ in range(generations):
            self.step(fitness_function)
            best = self.get_best_solution()
            
            if best and target_fitness and best.fitness >= target_fitness:
                break
        
        return self.get_best_solution()
    
    def get_best_solution(self) -> Optional[Chromosome]:
        """Get the best solution found so far."""
        return self.genetic_algorithm.get_best_solution()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get evolution statistics."""
        return {
            "engine_id": self.engine_id,
            "generations": len(self.history),
            "objectives": self.objectives,
            "constraints": list(self.constraints.keys()),
            "history": self.history[-10:],  # Last 10 generations
            "best_fitness": self.history[-1]["best_fitness"] if self.history else None,
        }


def create_evolution_engine(name: str = "Default Engine") -> EvolutionEngine:
    """Factory function to create a standard evolution engine."""
    ga = GeneticAlgorithm(
        algorithm_id=f"ga_{uuid.uuid4().hex[:8]}",
        population_size=50,
        mutation_rate=0.1,
        crossover_rate=0.7,
    )
    return EvolutionEngine(
        engine_id=f"engine_{uuid.uuid4().hex[:8]}",
        genetic_algorithm=ga,
        objectives={"performance": 1.0, "efficiency": 0.8, "reliability": 0.6},
    )
