"""
CAPABILITY-000008: Code Indexing

PURPOSE: Index every engineering symbol.

VERSION: 1.0.0
"""
import ast
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class Symbol:
    """An indexed symbol."""
    name: str
    type: str  # class, function, method, variable
    file: str
    line: int
    docstring: str = ""

@dataclass
class CodeIndex:
    """Complete code index."""
    symbols: List[Symbol] = field(default_factory=list)
    files_indexed: int = 0
    total_symbols: int = 0
    indexed_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbols": [{"name": s.name, "type": s.type, "file": s.file, "line": s.line} for s in self.symbols],
            "files_indexed": self.files_indexed,
            "total_symbols": self.total_symbols,
            "indexed_at": self.indexed_at.isoformat(),
        }

class CodeIndexingCapability:
    """
    CAPABILITY-000008: Code Indexing
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000008"
    
    @property
    def name(self) -> str:
        return "CodeIndexing"
    
    @property
    def description(self) -> str:
        return "Indexes every engineering symbol"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> CodeIndex:
        """Execute code indexing."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        symbols = []
        files_indexed = 0
        
        for root, dirs, files in os.walk(path):
            if ".git" in root or "__pycache__" in root or "node_modules" in root:
                continue
            
            for filename in files:
                if filename.endswith(".py"):
                    filepath = os.path.join(root, filename)
                    try:
                        file_symbols = self._index_file(filepath, path)
                        symbols.extend(file_symbols)
                        files_indexed += 1
                    except:
                        pass
        
        return CodeIndex(
            symbols=symbols,
            files_indexed=files_indexed,
            total_symbols=len(symbols),
        )
    
    def _index_file(self, filepath: str, base_path: str) -> List[Symbol]:
        """Index a single file."""
        symbols = []
        rel_path = os.path.relpath(filepath, base_path)
        
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node) or ""
                    symbols.append(Symbol(
                        name=node.name,
                        type="class",
                        file=rel_path,
                        line=node.lineno,
                        docstring=docstring[:200],
                    ))
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            docstring = ast.get_docstring(item) or ""
                            symbols.append(Symbol(
                                name=f"{node.name}.{item.name}",
                                type="method",
                                file=rel_path,
                                line=item.lineno,
                                docstring=docstring[:200],
                            ))
                elif isinstance(node, ast.FunctionDef):
                    if not hasattr(node, 'parent'):
                        docstring = ast.get_docstring(node) or ""
                        symbols.append(Symbol(
                            name=node.name,
                            type="function",
                            file=rel_path,
                            line=node.lineno,
                            docstring=docstring[:200],
                        ))
        except:
            pass
        
        return symbols
