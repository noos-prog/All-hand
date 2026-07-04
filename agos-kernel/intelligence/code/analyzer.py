"""Code Intelligence Analyzer - Analyzes source code structure and patterns."""
import ast
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import (
    Symbol, SymbolType, Location, Import, CallGraph, ImportGraph,
    InheritanceRelationship, CodePattern, PatternType, FileAnalysis,
    CodeGenome, CodeHealth, Duplication, DeadCode, ComplexityLevel
)


class PythonCodeAnalyzer:
    """Analyzes Python source code."""
    
    def __init__(self):
        """Initialize analyzer."""
        self.current_file = ""
        self.imports: List[Import] = []
        self.symbols: List[Symbol] = []
        self.call_graph: List[CallGraph] = []
        self.import_graph: List[ImportGraph] = []
        self.inheritance: List[InheritanceRelationship] = []
    
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single Python file."""
        self.current_file = file_path
        self.imports = []
        self.symbols = []
        self.call_graph = []
        self.import_graph = []
        self.inheritance = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            tree = ast.parse(content, filename=file_path)
            self._extract_imports(tree, file_path)
            self._extract_symbols(tree, file_path, lines)
            
        except Exception as e:
            pass
        
        return FileAnalysis(
            path=file_path,
            language="python",
            symbols=self.symbols,
            imports=self.imports,
            exports=self._get_exports(),
            complexity=self._calculate_complexity(),
            lines=len(lines)
        )
    
    def _extract_imports(self, tree: ast.AST, file_path: str) -> None:
        """Extract import statements."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(Import(
                        module=alias.name,
                        names=[alias.asname or alias.name],
                        alias=alias.asname,
                        line=node.lineno,
                        file=file_path
                    ))
                    self.import_graph.append(ImportGraph(
                        source_file=file_path,
                        target_module=alias.name,
                        imported_names=[alias.asname or alias.name],
                        line=node.lineno
                    ))
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [a.asname or a.name for a in node.names]
                self.imports.append(Import(
                    module=module,
                    names=names,
                    is_wildcard=any(n.name == '*' for n in node.names),
                    line=node.lineno,
                    file=file_path
                ))
                self.import_graph.append(ImportGraph(
                    source_file=file_path,
                    target_module=module,
                    imported_names=names,
                    line=node.lineno
                ))
    
    def _extract_symbols(self, tree: ast.AST, file_path: str, lines: List[str]) -> None:
        """Extract symbols from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._extract_class(node, file_path, lines)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                if not self._is_method(node):
                    self._extract_function(node, file_path, lines)
            elif isinstance(node, ast.InterfaceDef):
                self._extract_interface(node, file_path, lines)
    
    def _extract_class(self, node: ast.ClassDef, file_path: str, lines: List[str]) -> None:
        """Extract class definition."""
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
        
        decorators = [d.attr if isinstance(d, ast.Attribute) else d.name 
                     for d in node.decorator_list]
        
        docstring = ast.get_docstring(node)
        
        # Calculate complexity
        complexity = self._calculate_node_complexity(node)
        
        # Count lines
        start_line = node.lineno
        end_line = node.end_lineno or start_line
        
        symbol = Symbol(
            name=node.name,
            type=SymbolType.CLASS,
            location=Location(file=file_path, line=start_line, end_line=end_line),
            file=file_path,
            docstring=docstring,
            decorators=decorators,
            base_classes=base_classes,
            complexity=complexity,
            lines=end_line - start_line + 1
        )
        self.symbols.append(symbol)
        
        # Track inheritance
        for base in base_classes:
            self.inheritance.append(InheritanceRelationship(
                child=node.name,
                parent=base,
                child_file=file_path,
                parent_file=file_path
            ))
        
        # Extract methods
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._extract_method(item, file_path, lines, node.name)
    
    def _extract_function(self, node: ast.FunctionDef, file_path: str, lines: List[str]) -> None:
        """Extract function definition."""
        is_test = node.name.startswith('test_') or node.name.endswith('_test')
        
        docstring = ast.get_docstring(node)
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        # Get signature
        signature = self._get_signature(node)
        
        # Get parameters
        parameters = []
        for arg in node.args.args:
            parameters.append({
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            })
        
        # Get return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        complexity = self._calculate_node_complexity(node)
        
        symbol = Symbol(
            name=node.name,
            type=SymbolType.FUNCTION,
            location=Location(
                file=file_path,
                line=node.lineno,
                end_line=node.end_lineno or node.lineno
            ),
            file=file_path,
            docstring=docstring,
            signature=signature,
            parameters=parameters,
            return_type=return_type,
            decorators=decorators,
            complexity=complexity,
            lines=(node.end_lineno or node.lineno) - node.lineno + 1,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_test=is_test,
            visibility=self._get_visibility(node.name)
        )
        self.symbols.append(symbol)
        
        # Extract calls
        self._extract_calls(node, file_path)
    
    def _extract_method(self, node: ast.FunctionDef, file_path: str, 
                       lines: List[str], class_name: str) -> None:
        """Extract method from class."""
        is_test = node.name.startswith('test_') or node.name.endswith('_test')
        
        docstring = ast.get_docstring(node)
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        signature = self._get_signature(node)
        
        parameters = []
        for arg in node.args.args[1:]:  # Skip self/cls
            parameters.append({
                'name': arg.arg,
                'annotation': ast.unparse(arg.annotation) if arg.annotation else None
            })
        
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        complexity = self._calculate_node_complexity(node)
        
        symbol = Symbol(
            name=f"{class_name}.{node.name}",
            type=SymbolType.METHOD,
            location=Location(
                file=file_path,
                line=node.lineno,
                end_line=node.end_lineno or node.lineno
            ),
            file=file_path,
            docstring=docstring,
            signature=signature,
            parameters=parameters,
            return_type=return_type,
            decorators=decorators,
            complexity=complexity,
            lines=(node.end_lineno or node.lineno) - node.lineno + 1,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_test=is_test,
            visibility=self._get_method_visibility(decorators)
        )
        self.symbols.append(symbol)
        
        self._extract_calls(node, file_path)
    
    def _extract_interface(self, node, file_path: str, lines: List[str]) -> None:
        """Extract interface definition."""
        symbol = Symbol(
            name=node.name,
            type=SymbolType.INTERFACE,
            location=Location(file=file_path, line=node.lineno),
            file=file_path,
            docstring=ast.get_docstring(node)
        )
        self.symbols.append(symbol)
    
    def _extract_calls(self, node: ast.FunctionDef, file_path: str) -> None:
        """Extract function/method calls."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    self.call_graph.append(CallGraph(
                        source_file=file_path,
                        caller=node.name,
                        callee=child.func.id,
                        line=child.lineno
                    ))
                elif isinstance(child.func, ast.Attribute):
                    attr_name = child.func.attr
                    self.call_graph.append(CallGraph(
                        source_file=file_path,
                        caller=node.name,
                        callee=attr_name,
                        line=child.lineno
                    ))
    
    def _get_signature(self, node: ast.FunctionDef) -> str:
        """Get function signature."""
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)
        
        signature = f"({', '.join(args)})"
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"
        
        return signature
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Get decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{ast.unparse(decorator)}"
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return str(decorator)
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (inside a class)."""
        return hasattr(node, '_parent') and isinstance(node._parent, ast.ClassDef)
    
    def _calculate_node_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _calculate_complexity(self) -> int:
        """Calculate file-level complexity."""
        return sum(s.complexity for s in self.symbols)
    
    def _get_exports(self) -> List[str]:
        """Get exported names (not starting with underscore)."""
        return [s.name for s in self.symbols if not s.name.startswith('_')]
    
    def _get_visibility(self, name: str) -> str:
        """Determine visibility from name."""
        if name.startswith('__') and not name.endswith('__'):
            return 'private'
        elif name.startswith('_'):
            return 'protected'
        return 'public'
    
    def _get_method_visibility(self, decorators: List[str]) -> str:
        """Determine method visibility from decorators."""
        if any('@private' in d for d in decorators):
            return 'private'
        return 'public'


class CodeIntelligenceEngine:
    """Main code intelligence engine."""
    
    LANGUAGE_ANALYZERS = {
        'python': PythonCodeAnalyzer,
    }
    
    def __init__(self, root_path: str):
        """Initialize engine."""
        self.root_path = Path(root_path)
        self.genome = CodeGenome()
        self._file_patterns = {
            'python': ['*.py'],
        }
    
    def analyze(self) -> CodeGenome:
        """Run complete code analysis."""
        self._find_source_files()
        self._analyze_all_files()
        self._detect_patterns()
        self._calculate_health()
        return self.genome
    
    def _find_source_files(self) -> None:
        """Find all source files."""
        patterns = self._file_patterns
        
        for ext_patterns in patterns.values():
            for pattern in ext_patterns:
                for file_path in self.root_path.rglob(pattern):
                    # Skip test directories
                    if 'test' not in str(file_path):
                        self.genome.files.append(str(file_path.relative_to(self.root_path)))
    
    def _analyze_all_files(self) -> None:
        """Analyze all source files."""
        for file_path in self.genome.files:
            full_path = self.root_path / file_path
            
            # Determine language
            ext = full_path.suffix
            lang_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
            }
            language = lang_map.get(ext, 'unknown')
            
            # Use appropriate analyzer
            if ext == '.py':
                analyzer = PythonCodeAnalyzer()
                analysis = analyzer.analyze_file(str(full_path))
                
                self.genome.file_analysis[str(file_path)] = analysis
                self.genome.all_symbols.extend(analysis.symbols)
                
                # Categorize symbols
                for symbol in analysis.symbols:
                    if symbol.type == SymbolType.CLASS:
                        self.genome.classes.append(symbol)
                        self.genome.total_classes += 1
                    elif symbol.type == SymbolType.FUNCTION:
                        self.genome.functions.append(symbol)
                        self.genome.total_functions += 1
                
                # Extend graphs
                self.genome.call_graph.extend(analyzer.call_graph)
                self.genome.import_graph.extend(analyzer.import_graph)
                self.genome.inheritance.extend(analyzer.inheritance)
        
        # Update totals
        self.genome.total_lines = sum(
            a.lines for a in self.genome.file_analysis.values()
        )
        
        # Calculate complexity distribution
        for symbol in self.genome.all_symbols:
            level = self._get_complexity_level(symbol.complexity)
            self.genome.complexity_distribution[level] = \
                self.genome.complexity_distribution.get(level, 0) + 1
    
    def _get_complexity_level(self, complexity: int) -> str:
        """Get complexity level from score."""
        if complexity <= 1:
            return 'trivial'
        elif complexity <= 5:
            return 'low'
        elif complexity <= 10:
            return 'medium'
        elif complexity <= 20:
            return 'high'
        elif complexity <= 50:
            return 'very_high'
        return 'extreme'
    
    def _detect_patterns(self) -> None:
        """Detect code patterns."""
        patterns = []
        
        # Singleton pattern
        singletons = self._detect_singleton()
        patterns.extend(singletons)
        
        # Factory pattern
        factories = self._detect_factory()
        patterns.extend(factories)
        
        # Observer pattern
        observers = self._detect_observer()
        patterns.extend(observers)
        
        self.genome.patterns = patterns
    
    def _detect_singleton(self) -> List[CodePattern]:
        """Detect singleton pattern."""
        singletons = []
        
        for symbol in self.genome.classes:
            doc = (symbol.docstring or '').lower()
            if 'singleton' in doc:
                singletons.append(CodePattern(
                    type=PatternType.SINGLETON,
                    name=f"Singleton: {symbol.name}",
                    files=[symbol.file],
                    confidence=1.0
                ))
        
        return singletons
    
    def _detect_factory(self) -> List[CodePattern]:
        """Detect factory pattern."""
        factories = []
        
        for symbol in self.genome.functions:
            if 'factory' in symbol.name.lower():
                factories.append(CodePattern(
                    type=PatternType.FACTORY,
                    name=f"Factory: {symbol.name}",
                    files=[symbol.file],
                    confidence=0.8
                ))
        
        return factories
    
    def _detect_observer(self) -> List[CodePattern]:
        """Detect observer pattern."""
        observers = []
        
        for symbol in self.genome.classes:
            doc = (symbol.docstring or '').lower()
            if 'observer' in doc or 'subscriber' in doc:
                observers.append(CodePattern(
                    type=PatternType.OBSERVER,
                    name=f"Observer: {symbol.name}",
                    files=[symbol.file],
                    confidence=0.8
                ))
        
        return observers
    
    def _calculate_health(self) -> None:
        """Calculate code health metrics."""
        total_symbols = len(self.genome.all_symbols)
        if total_symbols == 0:
            return
        
        # Doc coverage
        documented = sum(1 for s in self.genome.all_symbols if s.docstring)
        doc_coverage = documented / total_symbols * 100
        
        # Average complexity
        avg_complexity = sum(s.complexity for s in self.genome.all_symbols) / total_symbols
        
        self.genome.health = CodeHealth(
            complexity_score=avg_complexity,
            duplication_percentage=0.0,  # Would need more sophisticated analysis
            test_coverage=0.0,  # Would need coverage tool
            doc_coverage=doc_coverage,
            dead_code_count=len(self.genome.dead_code),
            cyclomatic_complexity=avg_complexity,
            maintainability_index=100 - (avg_complexity * 5)
        )
