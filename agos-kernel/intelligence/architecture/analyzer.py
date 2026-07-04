"""Architecture Intelligence Analyzer - Analyzes software architecture."""
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import (
    Layer, Boundary, Component, Interface, Contract, Event, Policy,
    ArchitectureGraph, ArchitectureScore, ArchitectureViolation, ArchitectureRisk,
    ArchitectureGenome, ArchitectureStyle, LayerType, ComponentType, BoundaryType
)


class ArchitectureAnalyzer:
    """Analyzes software architecture patterns."""
    
    # Layer patterns by name
    LAYER_PATTERNS = {
        'presentation': ['ui', 'web', 'frontend', 'client', 'views', 'templates'],
        'application': ['service', 'usecase', 'usecase', 'application', 'app', 'handlers'],
        'domain': ['domain', 'model', 'entity', 'aggregate', 'value'],
        'infrastructure': ['infra', 'infrastructure', 'persistence', 'repository', 'adapter'],
        'data': ['database', 'db', 'data', 'storage'],
        'external': ['external', 'client', 'api', 'gateway'],
    }
    
    # Component type detection
    COMPONENT_PATTERNS = {
        ComponentType.CONTROLLER: ['controller', 'rest', 'http', 'endpoint'],
        ComponentType.SERVICE: ['service', 'business', 'logic'],
        ComponentType.REPOSITORY: ['repository', 'dao', 'persistence'],
        ComponentType.FACTORY: ['factory', 'creator'],
        ComponentType.FACADE: ['facade'],
        ComponentType.MIDDLEWARE: ['middleware'],
        ComponentType.WORKER: ['worker', 'background', 'job'],
        ComponentType.GATEWAY: ['gateway', 'proxy'],
        ComponentType.HANDLER: ['handler', 'listener'],
    }
    
    # Directory structure patterns
    DIRECTORY_PATTERNS = {
        'src/main/java': 'java_standard',
        'src/main/kotlin': 'kotlin_standard',
        'src/main/scala': 'scala_standard',
        'cmd': 'go_standard',
        'internal': 'go_modules',
        'pkg': 'go_modules',
        'lib': 'library',
        'app': 'application',
        'services': 'service_oriented',
        'modules': 'modular',
    }
    
    def __init__(self, root_path: str):
        """Initialize analyzer."""
        self.root_path = Path(root_path)
        self.genome = ArchitectureGenome()
        self._component_counter = 0
    
    def analyze(self) -> ArchitectureGenome:
        """Run complete architecture analysis."""
        self._detect_architecture_style()
        self._extract_layers()
        self._extract_components()
        self._extract_interfaces()
        self._extract_contracts()
        self._build_graph()
        self._calculate_score()
        self._detect_violations()
        self._detect_risks()
        return self.genome
    
    def _detect_architecture_style(self) -> None:
        """Detect overall architecture style."""
        structure = self._analyze_directory_structure()
        
        # Count patterns
        style_scores = {
            ArchitectureStyle.MONOLITHIC: 0,
            ArchitectureStyle.LAYERED: 0,
            ArchitectureStyle.MICROSERVICE: 0,
            ArchitectureStyle.EVENT_DRIVEN: 0,
            ArchitectureStyle.HEXAGONAL: 0,
            ArchitectureStyle.CLEAN: 0,
        }
        
        # Monolithic indicators
        if structure.get('single_root', False):
            style_scores[ArchitectureStyle.MONOLITHIC] += 2
        
        # Layered indicators
        layer_indicators = ['presentation', 'application', 'domain', 'infrastructure']
        layer_count = sum(1 for l in layer_indicators if l in structure.get('directories', []))
        if layer_count >= 3:
            style_scores[ArchitectureStyle.LAYERED] += 3
        
        # Microservice indicators
        if structure.get('multiple_roots') or 'services' in structure.get('directories', []):
            style_scores[ArchitectureStyle.MICROSERVICE] += 2
        
        # Event-driven indicators
        if 'events' in structure.get('directories', []) or 'messaging' in str(structure.get('directories', [])):
            style_scores[ArchitectureStyle.EVENT_DRIVEN] += 2
        
        # Hexagonal/Ports and Adapters
        if 'ports' in structure.get('directories', []) and 'adapters' in structure.get('directories', []):
            style_scores[ArchitectureStyle.HEXAGONAL] += 3
        
        # Clean Architecture
        clean_indicators = ['entities', 'usecases', 'interfaces', 'external']
        clean_count = sum(1 for i in clean_indicators if i in structure.get('directories', []))
        if clean_count >= 3:
            style_scores[ArchitectureStyle.CLEAN] += 3
        
        # Determine best match
        best_style = max(style_scores.items(), key=lambda x: x[1])
        if best_style[1] > 0:
            self.genome.style = best_style[0]
            self.genome.confidence = min(best_style[1] / 5.0, 1.0)
        else:
            self.genome.style = ArchitectureStyle.UNKNOWN
    
    def _analyze_directory_structure(self) -> Dict[str, Any]:
        """Analyze directory structure."""
        directories = []
        has_single_root = False
        multiple_roots = False
        
        root_dirs = [d.name for d in self.root_path.iterdir() if d.is_dir()]
        
        # Check for single main directory
        if len(root_dirs) == 1 and root_dirs[0] in ['src', 'app', 'lib']:
            has_single_root = True
        
        # Check for multiple service directories
        service_dirs = ['services', 'microservices', 'apps']
        if any(s in root_dirs for s in service_dirs):
            multiple_roots = True
        
        # Collect all directories
        for d in self.root_path.rglob('*'):
            if d.is_dir():
                rel_path = str(d.relative_to(self.root_path))
                directories.append(rel_path)
        
        return {
            'directories': directories,
            'root_dirs': root_dirs,
            'single_root': has_single_root,
            'multiple_roots': multiple_roots,
        }
    
    def _extract_layers(self) -> None:
        """Extract architecture layers."""
        structure = self._analyze_directory_structure()
        detected_layers = []
        
        # Match directories to layers
        for dir_name in structure['root_dirs']:
            dir_lower = dir_name.lower()
            for layer_name, patterns in self.LAYER_PATTERNS.items():
                if any(p in dir_lower for p in patterns):
                    layer_type = LayerType(layer_name)
                    layer = Layer(
                        name=dir_name,
                        type=layer_type,
                        level=self._get_layer_level(layer_type)
                    )
                    detected_layers.append(layer)
                    break
        
        # Add default layers if not detected
        if not detected_layers:
            detected_layers = [
                Layer(name='src', type=LayerType.APPLICATION, level=1),
            ]
        
        self.genome.layers = detected_layers
    
    def _get_layer_level(self, layer_type: LayerType) -> int:
        """Get layer level (innermost = highest)."""
        levels = {
            LayerType.DOMAIN: 4,
            LayerType.APPLICATION: 3,
            LayerType.INFRASTRUCTURE: 2,
            LayerType.PRESENTATION: 1,
            LayerType.DATA: 1,
            LayerType.EXTERNAL: 0,
        }
        return levels.get(layer_type, 0)
    
    def _extract_components(self) -> None:
        """Extract architecture components."""
        components = {}
        
        # Analyze directory structure
        for root, dirs, files in os.walk(self.root_path):
            rel_root = Path(root).relative_to(self.root_path)
            depth = len(rel_root.parts)
            
            # Skip deep directories
            if depth > 4:
                continue
            
            dir_name = Path(root).name
            
            # Detect component type
            component_type = self._detect_component_type(dir_name, files)
            
            if component_type:
                component = Component(
                    name=dir_name,
                    type=component_type,
                    path=str(rel_root),
                    layer=self._get_component_layer(rel_root),
                    responsibilities=self._extract_responsibilities(root, files)
                )
                
                components[dir_name] = component
                self._component_counter += 1
        
        self.genome.components = components
    
    def _detect_component_type(self, dir_name: str, files: List[str]) -> Optional[ComponentType]:
        """Detect component type from directory name and contents."""
        dir_lower = dir_name.lower()
        
        for comp_type, patterns in self.COMPONENT_PATTERNS.items():
            if any(p in dir_lower for p in patterns):
                return comp_type
        
        # Infer from files
        if any(f.endswith('.py') for f in files):
            return ComponentType.MODULE
        
        return None
    
    def _get_component_layer(self, path: Path) -> Optional[str]:
        """Get layer for component based on path."""
        path_str = str(path).lower()
        
        for layer in self.genome.layers:
            if layer.name.lower() in path_str:
                return layer.name
        
        return None
    
    def _extract_responsibilities(self, path: str, files: List[str]) -> List[str]:
        """Extract component responsibilities."""
        responsibilities = []
        
        # Look for README or doc files
        for f in files:
            if 'readme' in f.lower() or 'doc' in f.lower():
                responsibilities.append('documentation')
        
        # Infer from file types
        if any(f.endswith('.py') for f in files):
            responsibilities.append('implements')
        
        return responsibilities
    
    def _extract_interfaces(self) -> None:
        """Extract component interfaces."""
        interfaces = []
        
        # Look for API files
        api_patterns = ['api.py', 'routes.py', 'endpoints.py', 'grpc']
        
        for root, _, files in os.walk(self.root_path):
            for f in files:
                if any(p in f.lower() for p in api_patterns):
                    rel_path = Path(root).relative_to(self.root_path)
                    interface = Interface(
                        name=Path(f).stem,
                        component=str(rel_path),
                        type='REST' if 'route' in f.lower() else 'UNKNOWN',
                        path=str(Path(root) / f)
                    )
                    interfaces.append(interface)
        
        self.genome.interfaces = interfaces
    
    def _extract_contracts(self) -> None:
        """Extract interface contracts."""
        contracts = []
        
        # Look for contract/schema files
        contract_patterns = ['schema', 'contract', 'interface']
        
        for root, _, files in os.walk(self.root_path):
            for f in files:
                if any(p in f.lower() for p in contract_patterns):
                    contracts.append(Contract(
                        name=Path(f).stem,
                        interface=f,
                        version='1.0.0'
                    ))
        
        self.genome.contracts = contracts
    
    def _build_graph(self) -> None:
        """Build architecture dependency graph."""
        nodes = list(self.genome.components.keys())
        edges = []
        
        # Add layer edges
        for layer in self.genome.layers:
            nodes.append(layer.name)
        
        # Add component edges (simplified - would need deeper analysis)
        for comp_name, comp in self.genome.components.items():
            if comp.layer:
                edges.append((comp_name, comp.layer, 'layer_dependency'))
        
        self.genome.graph = ArchitectureGraph(
            nodes=nodes,
            edges=edges,
            layers=self.genome.layers,
            boundaries=self.genome.boundaries
        )
    
    def _calculate_score(self) -> None:
        """Calculate architecture quality score."""
        components_count = len(self.genome.components)
        layers_count = len(self.genome.layers)
        
        # Modularity: based on layers and components
        modularity = min((layers_count * 10 + components_count) / 100, 1.0)
        
        # Cohesion: inversely proportional to components per layer
        avg_components = components_count / max(layers_count, 1)
        cohesion = max(0, 1 - (avg_components / 20))
        
        # Coupling: inversely proportional to violations
        violations_count = len(self.genome.violations)
        coupling = max(0, 1 - (violations_count / 10))
        
        # Overall
        overall = (modularity + cohesion + coupling) / 3
        
        self.genome.score = ArchitectureScore(
            overall=overall,
            modularity=modularity,
            cohesion=cohesion,
            coupling=coupling,
            maintainability=overall * 0.8,
            testability=overall * 0.7,
            reusability=cohesion * modularity
        )
    
    def _detect_violations(self) -> None:
        """Detect architecture violations."""
        violations = []
        
        # Check for circular dependencies
        violations.extend(self._check_circular_dependencies())
        
        # Check for layer violations
        violations.extend(self._check_layer_violations())
        
        # Check for god components
        violations.extend(self._check_god_components())
        
        self.genome.violations = violations
    
    def _check_circular_dependencies(self) -> List[ArchitectureViolation]:
        """Check for circular dependencies."""
        violations = []
        # Simplified check - would need full dependency analysis
        return violations
    
    def _check_layer_violations(self) -> List[ArchitectureViolation]:
        """Check for layer violations."""
        violations = []
        
        # Check if lower layers depend on higher layers
        for comp_name, comp in self.genome.components.items():
            if comp.layer:
                # This is a simplified check
                pass
        
        return violations
    
    def _check_god_components(self) -> List[ArchitectureViolation]:
        """Check for god components (too large/complex)."""
        violations = []
        
        for comp_name, comp in self.genome.components.items():
            # Simple heuristic: too many files
            if comp.path and len(list((self.root_path / comp.path).rglob('*'))) > 100:
                violations.append(ArchitectureViolation(
                    rule='god_component',
                    description=f'Component {comp_name} may be too large',
                    severity='warning',
                    component=comp_name
                ))
        
        return violations
    
    def _detect_risks(self) -> None:
        """Detect architecture risks."""
        risks = []
        
        # High coupling risk
        if self.genome.score.coupling < 0.5:
            risks.append(ArchitectureRisk(
                name='high_coupling',
                description='Architecture has high coupling between components',
                severity='high',
                affected_components=list(self.genome.components.keys())
            ))
        
        # Low cohesion risk
        if self.genome.score.cohesion < 0.5:
            risks.append(ArchitectureRisk(
                name='low_cohesion',
                description='Components may have low cohesion',
                severity='medium',
                affected_components=list(self.genome.components.keys())
            ))
        
        # Unknown architecture style
        if self.genome.style == ArchitectureStyle.UNKNOWN:
            risks.append(ArchitectureRisk(
                name='unknown_architecture',
                description='Could not determine architecture style',
                severity='low'
            ))
        
        self.genome.risks = risks
