"""Data models for Code Intelligence."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class SymbolType(Enum):
    """Types of code symbols."""
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = "interface"
    METHOD = "method"
    PROPERTY = "property"
    VARIABLE = "variable"
    CONSTANT = "constant"
    ENUM = "enum"
    STRUCT = "struct"
    MODULE = "module"
    PACKAGE = "package"
    TYPE = "type"
    DECORATOR = "decorator"
    ANNOTATION = "annotation"


class ComplexityLevel(Enum):
    """Code complexity levels."""
    TRIVIAL = "trivial"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class PatternType(Enum):
    """Code patterns."""
    SINGLETON = "singleton"
    FACTORY = "factory"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    ADAPTER = "adapter"
    DECORATOR = "decorator"
    FACADE = "facade"
    PROXY = "proxy"
    BUILDER = "builder"
    COMMAND = "command"
    REPOSITORY = "repository"
    MVC = "mvc"
    MICROSERVICE = "microservice"
    EVENT_DRIVEN = "event_driven"


@dataclass
class Location:
    """Source code location."""
    file: str
    line: int
    column: int = 0
    end_line: Optional[int] = None
    end_column: Optional[int] = None


@dataclass
class Symbol:
    """A code symbol (function, class, etc.)."""
    name: str
    type: SymbolType
    location: Location
    file: str
    docstring: Optional[str] = None
    signature: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    annotations: List[str] = field(default_factory=list)
    generics: List[str] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    implements: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)  # Functions/methods called
    called_by: List[str] = field(default_factory=list)  # Who calls this
    complexity: int = 0
    lines: int = 0
    is_async: bool = False
    is_test: bool = False
    visibility: str = "public"  # public, private, protected, internal


@dataclass
class Import:
    """An import statement."""
    module: str
    names: List[str] = field(default_factory=list)
    alias: Optional[str] = None
    is_wildcard: bool = False
    line: int = 0
    file: str = ""


@dataclass
class CallGraph:
    """Call graph relationships."""
    source_file: str
    caller: str
    callee: str
    line: int = 0
    is_dynamic: bool = False


@dataclass
class ImportGraph:
    """Import/dependency graph."""
    source_file: str
    target_module: str
    imported_names: List[str] = field(default_factory=list)
    line: int = 0


@dataclass
class InheritanceRelationship:
    """Inheritance relationship between classes."""
    child: str
    parent: str
    child_file: str
    parent_file: str
    relationship: str = "extends"  # extends, implements


@dataclass
class Duplication:
    """Code duplication."""
    hash: str
    files: List[str] = field(default_factory=list)
    lines: int = 0
    lines_detail: List[Tuple[str, int, int]] = field(default_factory=list)  # (file, start, end)


@dataclass
class DeadCode:
    """Dead code detection."""
    type: str  # unused_function, unused_class, unused_variable
    name: str
    file: str
    line: int
    reason: str = ""


@dataclass
class CodePattern:
    """Detected code pattern."""
    type: PatternType
    name: str
    files: List[str] = field(default_factory=list)
    confidence: float = 0.0
    description: str = ""


@dataclass
class CodeHealth:
    """Overall code health metrics."""
    complexity_score: float = 0.0
    duplication_percentage: float = 0.0
    test_coverage: float = 0.0
    doc_coverage: float = 0.0
    dead_code_count: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 0.0


@dataclass
class FileAnalysis:
    """Analysis of a single file."""
    path: str
    language: str
    symbols: List[Symbol] = field(default_factory=list)
    imports: List[Import] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    complexity: int = 0
    lines: int = 0
    docstring: Optional[str] = None
    has_tests: bool = False
    related_test_file: Optional[str] = None


@dataclass
class CodeGenome:
    """Complete DNA of source code."""
    # Files
    files: List[str] = field(default_factory=list)
    file_analysis: Dict[str, FileAnalysis] = field(default_factory=dict)
    
    # Symbols
    functions: List[Symbol] = field(default_factory=list)
    classes: List[Symbol] = field(default_factory=list)
    interfaces: List[Symbol] = field(default_factory=list)
    all_symbols: List[Symbol] = field(default_factory=list)
    
    # Relationships
    call_graph: List[CallGraph] = field(default_factory=list)
    import_graph: List[ImportGraph] = field(default_factory=list)
    inheritance: List[InheritanceRelationship] = field(default_factory=list)
    
    # Analysis
    patterns: List[CodePattern] = field(default_factory=list)
    duplications: List[Duplication] = field(default_factory=list)
    dead_code: List[DeadCode] = field(default_factory=list)
    
    # Metrics
    health: CodeHealth = field(default_factory=CodeHealth)
    total_functions: int = 0
    total_classes: int = 0
    total_interfaces: int = 0
    total_lines: int = 0
    complexity_distribution: Dict[str, int] = field(default_factory=dict)
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    
    def get_symbol(self, name: str) -> Optional[Symbol]:
        """Get symbol by name."""
        for symbol in self.all_symbols:
            if symbol.name == name:
                return symbol
        return None
    
    def get_file_symbols(self, file: str) -> List[Symbol]:
        """Get all symbols in a file."""
        return [s for s in self.all_symbols if s.file == file]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "files_count": len(self.files),
            "functions_count": self.total_functions,
            "classes_count": self.total_classes,
            "complexity_distribution": self.complexity_distribution,
            "health": {
                "duplication_percentage": self.health.duplication_percentage,
                "dead_code_count": self.health.dead_code_count,
            },
        }
