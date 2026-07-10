#!/usr/bin/env python3
"""
ARI - Genome Engine
=================

Analyzes agent genomes and capabilities.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from datetime import datetime
import random


class GeneType(Enum):
    """Types of genes."""
    CAPABILITY = "capability"
    BEHAVIOR = "behavior"
    TRAIT = "trait"
    SKILL = "skill"


@dataclass
class Gene:
    """A gene in the agent genome."""
    gene_id: str
    name: str
    gene_type: GeneType
    
    # Value
    value: Any
    weight: float = 1.0
    
    # Expression
    expressed: bool = True
    expression_level: float = 1.0  # 0-1
    
    # Metadata
    description: Optional[str] = None
    source: str = "discovered"


@dataclass
class Genome:
    """A complete agent genome."""
    genome_id: str
    name: str
    agent_type: str
    
    # Genes
    genes: Tuple[Gene, ...]
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Performance
    fitness_score: float = 0.0
    generations: int = 0
    
    # Origin
    parent_ids: Tuple[str, ...] = ()  # For tracking lineage


class GenomeAnalyzer:
    """
    Analyzes agent genomes.
    """
    
    def __init__(self):
        self._analyzers: Dict[str, Callable] = {}
    
    def register_analyzer(
        self,
        name: str,
        analyzer: Callable[[Genome], Dict]
    ) -> None:
        """Register an analyzer."""
        self._analyzers[name] = analyzer
    
    def analyze(self, genome: Genome) -> Dict[str, Any]:
        """Analyze a genome."""
        analysis = {
            "genome_id": genome.genome_id,
            "name": genome.name,
            "gene_count": len(genome.genes),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Run all analyzers
        for name, analyzer in self._analyzers.items():
            try:
                result = analyzer(genome)
                analysis[name] = result
            except Exception as e:
                analysis[f"{name}_error"] = str(e)
        
        return analysis
    
    def analyze_capabilities(self, genome: Genome) -> Dict[str, Any]:
        """Analyze capability genes."""
        capability_genes = [
            g for g in genome.genes if g.gene_type == GeneType.CAPABILITY
        ]
        
        return {
            "capability_count": len(capability_genes),
            "capabilities": [g.name for g in capability_genes],
        }
    
    def analyze_traits(self, genome: Genome) -> Dict[str, Any]:
        """Analyze trait genes."""
        trait_genes = [
            g for g in genome.genes if g.gene_type == GeneType.TRAIT
        ]
        
        return {
            "trait_count": len(trait_genes),
            "traits": [g.name for g in trait_genes],
        }


class GenomeMutator:
    """
    Mutates genomes for evolution.
    """
    
    def __init__(self):
        self._mutation_rate = 0.1
        self._crossover_rate = 0.7
    
    def set_mutation_rate(self, rate: float) -> None:
        """Set mutation rate."""
        self._mutation_rate = rate
    
    def mutate(self, genome: Genome) -> Genome:
        """Mutate a genome."""
        new_genes = []
        
        for gene in genome.genes:
            if random.random() < self._mutation_rate:
                # Mutate this gene
                mutated_gene = self._mutate_gene(gene)
                new_genes.append(mutated_gene)
            else:
                new_genes.append(gene)
        
        return Genome(
            genome_id=f"{genome.genome_id}_mut_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            name=genome.name,
            agent_type=genome.agent_type,
            genes=tuple(new_genes),
            generations=genome.generations + 1,
            parent_ids=(genome.genome_id,),
        )
    
    def _mutate_gene(self, gene: Gene) -> Gene:
        """Mutate a single gene."""
        if gene.gene_type == GeneType.CAPABILITY:
            # Capability genes: toggle expression
            return Gene(
                gene_id=f"{gene.gene_id}_mut",
                name=gene.name,
                gene_type=gene.gene_type,
                value=gene.value,
                weight=gene.weight,
                expressed=not gene.expressed if random.random() < 0.5 else gene.expressed,
                expression_level=max(0, min(1, gene.expression_level + random.uniform(-0.2, 0.2))),
                description=gene.description,
                source="mutated",
            )
        else:
            # Other genes: adjust weight
            return Gene(
                gene_id=f"{gene.gene_id}_mut",
                name=gene.name,
                gene_type=gene.gene_type,
                value=gene.value,
                weight=max(0, gene.weight + random.uniform(-0.1, 0.1)),
                expressed=gene.expressed,
                expression_level=gene.expression_level,
                description=gene.description,
                source="mutated",
            )
    
    def crossover(
        self,
        parent1: Genome,
        parent2: Genome
    ) -> Genome:
        """Perform crossover between two genomes."""
        if random.random() > self._crossover_rate:
            # No crossover, return copy of first parent
            return self.mutate(parent1)
        
        # Mix genes from both parents
        genes1 = {g.name: g for g in parent1.genes}
        genes2 = {g.name: g for g in parent2.genes}
        
        all_genes = list(parent1.genes)
        
        # For genes unique to parent2, add them
        for name, gene in genes2.items():
            if name not in genes1:
                all_genes.append(gene)
        
        return Genome(
            genome_id=f"offspring_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            name=f"{parent1.name} x {parent2.name}",
            agent_type=parent1.agent_type,
            genes=tuple(all_genes),
            generations=0,
            parent_ids=(parent1.genome_id, parent2.genome_id),
        )


class GenomeEngine:
    """
    Main genome engine.
    """
    
    def __init__(self):
        self._genomes: Dict[str, Genome] = {}
        self._analyzer = GenomeAnalyzer()
        self._mutator = GenomeMutator()
        
        # Register default analyzers
        self._analyzer.register_analyzer("capabilities", self._analyzer.analyze_capabilities)
        self._analyzer.register_analyzer("traits", self._analyzer.analyze_traits)
    
    def create_genome(
        self,
        name: str,
        agent_type: str,
        genes: List[Dict[str, Any]]
    ) -> Genome:
        """Create a new genome."""
        genome_genes = [
            Gene(
                gene_id=f"gene_{i}",
                name=g.get("name", f"Gene {i}"),
                gene_type=GeneType(g.get("type", "capability")),
                value=g.get("value", None),
                weight=g.get("weight", 1.0),
                description=g.get("description"),
            )
            for i, g in enumerate(genes)
        ]
        
        genome = Genome(
            genome_id=f"genome_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            name=name,
            agent_type=agent_type,
            genes=tuple(genome_genes),
        )
        
        self._genomes[genome.genome_id] = genome
        return genome
    
    def get_genome(self, genome_id: str) -> Optional[Genome]:
        """Get a genome by ID."""
        return self._genomes.get(genome_id)
    
    def analyze_genome(self, genome_id: str) -> Dict[str, Any]:
        """Analyze a genome."""
        genome = self._genomes.get(genome_id)
        if not genome:
            return {"error": "Genome not found"}
        
        return self._analyzer.analyze(genome)
    
    def mutate_genome(self, genome_id: str) -> Optional[Genome]:
        """Mutate a genome."""
        genome = self._genomes.get(genome_id)
        if not genome:
            return None
        
        mutated = self._mutator.mutate(genome)
        self._genomes[mutated.genome_id] = mutated
        return mutated
    
    def evolve(
        self,
        parent1_id: str,
        parent2_id: str,
        generations: int = 1
    ) -> List[Genome]:
        """Evolve a genome through generations."""
        parent1 = self._genomes.get(parent1_id)
        parent2 = self._genomes.get(parent2_id)
        
        if not parent1 or not parent2:
            return []
        
        offspring = self._mutator.crossover(parent1, parent2)
        self._genomes[offspring.genome_id] = offspring
        
        # Continue evolving
        evolved = [offspring]
        current = offspring
        
        for _ in range(generations - 1):
            current = self._mutator.mutate(current)
            self._genomes[current.genome_id] = current
            evolved.append(current)
        
        return evolved
    
    def compare_genomes(
        self,
        genome1_id: str,
        genome2_id: str
    ) -> Dict[str, Any]:
        """Compare two genomes."""
        g1 = self._genomes.get(genome1_id)
        g2 = self._genomes.get(genome2_id)
        
        if not g1 or not g2:
            return {"error": "One or both genomes not found"}
        
        # Find common and unique genes
        genes1 = {g.name for g in g1.genes}
        genes2 = {g.name for g in g2.genes}
        
        common = genes1 & genes2
        unique1 = genes1 - genes2
        unique2 = genes2 - genes1
        
        return {
            "genome1": {"id": g1.genome_id, "name": g1.name},
            "genome2": {"id": g2.genome_id, "name": g2.name},
            "common_genes": list(common),
            "unique_to_1": list(unique1),
            "unique_to_2": list(unique2),
            "similarity": len(common) / max(len(genes1), len(genes2), 1),
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        by_type = {}
        total_genes = 0
        avg_genes = 0
        
        for genome in self._genomes.values():
            gtype = genome.agent_type
            by_type[gtype] = by_type.get(gtype, 0) + 1
            total_genes += len(genome.genes)
        
        if self._genomes:
            avg_genes = total_genes / len(self._genomes)
        
        return {
            "total_genomes": len(self._genomes),
            "by_agent_type": by_type,
            "total_genes": total_genes,
            "avg_genes_per_genome": round(avg_genes, 1),
        }
