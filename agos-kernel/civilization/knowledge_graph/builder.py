"""
Knowledge Graph Builder
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

Builds knowledge graphs from repositories.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field

from agos_kernel.civilization.knowledge_graph.nodes.base import (
    GraphNode, NodeType, NodeMetadata
)

try:
    from agos_kernel.civilization.knowledge_graph.relationships import (
        Relationship, RelationshipType, create_relationship
    )
except ImportError:
    # Will be loaded later
    Relationship = None
    RelationshipType = None
    create_relationship = None


@dataclass
class BuildResult:
    """Result of building a graph."""
    success: bool = False
    nodes_created: int = 0
    relationships_created: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class GraphBuilder:
    """
    Knowledge Graph Builder.
    
    Builds knowledge graphs from source code repositories.
    """
    
    def __init__(self, graph: Optional[KnowledgeGraph] = None):
        self.graph = graph or KnowledgeGraph()
        self._node_cache: Dict[str, str] = {}  # path -> node_id
        self._module_cache: Dict[str, Set[str]] = {}  # repo -> set of modules
    
    def build_repository_graph(self, repo_path: str) -> BuildResult:
        """
        Build complete repository graph.
        
        Creates:
        - Repository node
        - Directory nodes
        - File nodes
        - Code nodes (classes, functions, etc.)
        - All relationships
        """
        result = BuildResult()
        repo_path = Path(repo_path)
        
        if not repo_path.exists():
            result.errors.append(f"Repository path does not exist: {repo_path}")
            return result
        
        print(f"Building graph for repository: {repo_path.name}")
        
        try:
            # Create repository node
            repo_node = self._create_repository_node(repo_path)
            self.graph.add_node(repo_node)
            result.nodes_created += 1
            
            # Scan and create nodes
            self._scan_directory(repo_path, repo_node.id, result)
            
            # Build relationships
            self._build_relationships(repo_path, result)
            
            result.success = True
            print(f"  ✓ Created {result.nodes_created} nodes")
            print(f"  ✓ Created {result.relationships_created} relationships")
            
        except Exception as e:
            result.errors.append(str(e))
            print(f"  ✗ Error: {e}")
        
        return result
    
    def _create_repository_node(self, repo_path: Path) -> GraphNode:
        """Create repository node."""
        import subprocess
        
        node = GraphNode(
            type=NodeType.REPOSITORY,
            name=repo_path.name,
            path=str(repo_path),
            repository=repo_path.name,
        )
        
        # Get git info if available
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                node.metadata.properties['remote_url'] = result.stdout.strip()
        except Exception:
            pass
        
        return node
    
    def _scan_directory(self, directory: Path, parent_id: str, result: BuildResult) -> None:
        """Recursively scan directory and create nodes."""
        try:
            for item in sorted(directory.iterdir()):
                # Skip excluded patterns
                if self._should_exclude(item):
                    continue
                
                if item.is_dir():
                    # Create directory node
                    dir_node = GraphNode(
                        type=NodeType.DIRECTORY,
                        name=item.name,
                        path=str(item.relative_to(directory.parent)),
                        repository=directory.parent.name,
                    )
                    self.graph.add_node(dir_node)
                    self._node_cache[str(item)] = dir_node.id
                    result.nodes_created += 1
                    
                    # Add CONTAINS relationship
                    self._add_relationship(
                        RelationshipType.CONTAINS,
                        parent_id,
                        dir_node.id,
                        parent_id,
                        dir_node.id
                    )
                    result.relationships_created += 1
                    
                    # Recurse
                    self._scan_directory(item, dir_node.id, result)
                    
                elif item.is_file():
                    # Create file node
                    file_node = self._create_file_node(item, directory.parent)
                    self.graph.add_node(file_node)
                    self._node_cache[str(item)] = file_node.id
                    result.nodes_created += 1
                    
                    # Add CONTAINS relationship
                    self._add_relationship(
                        RelationshipType.CONTAINS,
                        parent_id,
                        file_node.id,
                        parent_id,
                        file_node.id
                    )
                    result.relationships_created += 1
                    
                    # If Python file, analyze for code nodes
                    if item.suffix == '.py':
                        self._analyze_python_file(item, file_node.id, result)
                        
        except PermissionError:
            result.warnings.append(f"Permission denied: {directory}")
    
    def _create_file_node(self, file_path: Path, repo_root: Path) -> GraphNode:
        """Create file node."""
        stat = file_path.stat()
        
        node = GraphNode(
            type=NodeType.FILE,
            name=file_path.name,
            path=str(file_path.relative_to(repo_root)),
            repository=repo_root.name,
        )
        
        node.lines_of_code = self._count_lines(file_path)
        node.metadata.properties['size'] = stat.st_size
        node.metadata.properties['extension'] = file_path.suffix
        
        return node
    
    def _analyze_python_file(self, file_path: Path, file_node_id: str, result: BuildResult) -> None:
        """Analyze Python file for code nodes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            # Module name
            module_name = file_path.stem
            
            # Walk through AST
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_node = self._create_class_node(node, file_path)
                    self.graph.add_node(class_node)
                    result.nodes_created += 1
                    
                    # Link to file
                    self._add_relationship(
                        RelationshipType.CONTAINS,
                        file_node_id,
                        class_node.id,
                        file_path.name,
                        class_node.name
                    )
                    result.relationships_created += 1
                    
                    # Track class methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_node = self._create_method_node(item, node.name, file_path)
                            self.graph.add_node(method_node)
                            result.nodes_created += 1
                            
                            self._add_relationship(
                                RelationshipType.CONTAINS,
                                class_node.id,
                                method_node.id,
                                class_node.name,
                                method_node.name
                            )
                            result.relationships_created += 1
                            
                            # Add IMPORTS relationships for imports
                            for import_node in ast.walk(item):
                                if isinstance(import_node, ast.Name):
                                    self._add_import_relationship(
                                        method_node.id,
                                        import_node.id,
                                        file_path
                                    )
                
                elif isinstance(node, ast.FunctionDef):
                    # Module-level function
                    func_node = self._create_function_node(node, file_path)
                    self.graph.add_node(func_node)
                    result.nodes_created += 1
                    
                    self._add_relationship(
                        RelationshipType.CONTAINS,
                        file_node_id,
                        func_node.id,
                        file_path.name,
                        func_node.name
                    )
                    result.relationships_created += 1
                    
        except SyntaxError as e:
            result.warnings.append(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            result.warnings.append(f"Error analyzing {file_path}: {e}")
    
    def _create_class_node(self, node: ast.ClassDef, file_path: Path) -> GraphNode:
        """Create class node from AST."""
        class_node = GraphNode(
            type=NodeType.CLASS,
            name=node.name,
            path=str(file_path),
            repository=file_path.parent.parent.name,
        )
        
        class_node.description = ast.get_docstring(node) or ""
        
        # Bases
        class_node.bases = [
            base.attr if isinstance(base, ast.Attribute) else getattr(base, 'id', str(base))
            for base in node.bases
        ]
        
        # Methods
        class_node.methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        
        # Lines
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            class_node.lines_of_code = (node.end_lineno or 0) - (node.lineno or 0) + 1
        
        return class_node
    
    def _create_method_node(self, node: ast.FunctionDef, parent_class: str, file_path: Path) -> GraphNode:
        """Create method node from AST."""
        method_node = GraphNode(
            type=NodeType.METHOD,
            name=node.name,
            path=str(file_path),
            repository=file_path.parent.parent.name,
        )
        
        method_node.parent_class = parent_class
        method_node.is_async = isinstance(node, ast.AsyncFunctionDef)
        
        # Parameters
        method_node.parameters = [
            arg.arg for arg in node.args.args
        ]
        
        # Lines
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            method_node.lines_of_code = (node.end_lineno or 0) - (node.lineno or 0) + 1
        
        return method_node
    
    def _create_function_node(self, node: ast.FunctionDef, file_path: Path) -> GraphNode:
        """Create function node from AST."""
        func_node = GraphNode(
            type=NodeType.FUNCTION,
            name=node.name,
            path=str(file_path),
            repository=file_path.parent.parent.name,
        )
        
        func_node.description = ast.get_docstring(node) or ""
        func_node.is_async = isinstance(node, ast.AsyncFunctionDef)
        
        # Parameters
        func_node.parameters = [
            arg.arg for arg in node.args.args
        ]
        
        # Lines
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            func_node.lines_of_code = (node.end_lineno or 0) - (node.lineno or 0) + 1
        
        return func_node
    
    def _add_relationship(
        self,
        rel_type: RelationshipType,
        source_id: str,
        target_id: str,
        source_name: str = "",
        target_name: str = ""
    ) -> None:
        """Add relationship to graph."""
        rel = create_relationship(
            rel_type,
            source_id,
            target_id,
            source_name,
            target_name
        )
        self.graph.add_relationship(rel)
    
    def _add_import_relationship(
        self,
        source_node_id: str,
        imported_name: str,
        file_path: Path
    ) -> None:
        """Add import relationship."""
        # Try to find the imported module
        for path, node_id in self._node_cache.items():
            if Path(path).stem == imported_name or imported_name in Path(path).stem:
                self._add_relationship(
                    RelationshipType.IMPORTS,
                    source_node_id,
                    node_id,
                    source_node_id,
                    node_id
                )
                break
    
    def _build_relationships(self, repo_path: Path, result: BuildResult) -> None:
        """Build additional relationships based on content."""
        for py_file in repo_path.rglob('*.py'):
            if self._should_exclude(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content, filename=str(py_file))
                
                file_node_id = self._node_cache.get(str(py_file))
                if not file_node_id:
                    continue
                
                # Find imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module:
                            # Create IMPORTS relationship
                            module_path = str(py_file.parent / f"{node.module.split('.')[0]}.py")
                            if module_path in self._node_cache:
                                target_id = self._node_cache[module_path]
                                
                                # Find source node in file
                                for child in ast.walk(tree):
                                    if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                                        child_node_id = self._get_node_by_name_and_path(
                                            child.name, str(py_file)
                                        )
                                        if child_node_id:
                                            self._add_relationship(
                                                RelationshipType.IMPORTS,
                                                child_node_id,
                                                target_id,
                                                child.name,
                                                node.module
                                            )
                                            result.relationships_created += 1
                    
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            module_path = str(repo_path / f"{alias.name.split('.')[0]}.py")
                            if module_path in self._node_cache:
                                target_id = self._node_cache[module_path]
                                
                                for child in ast.walk(tree):
                                    if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                                        child_node_id = self._get_node_by_name_and_path(
                                            child.name, str(py_file)
                                        )
                                        if child_node_id:
                                            self._add_relationship(
                                                RelationshipType.IMPORTS,
                                                child_node_id,
                                                target_id,
                                                child.name,
                                                alias.name
                                            )
                                            result.relationships_created += 1
                                                    
            except Exception as e:
                result.warnings.append(f"Error building relationships for {py_file}: {e}")
    
    def _get_node_by_name_and_path(self, name: str, path: str) -> Optional[str]:
        """Get node ID by name and path."""
        for node_id, node in self.graph._nodes.items():
            if node.name == name and node.path == path:
                return node_id
        return None
    
    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        excluded = [
            '__pycache__', '.git', '.svn', '.hg',
            'node_modules', 'venv', '.venv', 'env',
            'dist', 'build', '.egg-info',
            '*.pyc', '*.pyo', '.pytest_cache',
            '.mypy_cache', '.tox', '.coverage',
            '.DS_Store', 'Thumbs.db',
        ]
        
        name = path.name
        for ex in excluded:
            if ex.startswith('*'):
                if name.endswith(ex[1:]):
                    return True
            elif name == ex:
                return True
        
        return False
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception:
            return 0
