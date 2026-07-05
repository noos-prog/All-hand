"""
CAPABILITY-000005: Repository Structure Analysis

PURPOSE: Extract complete directory structure.

VERSION: 1.0.0
"""
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class StructureNode:
    """A node in the directory tree."""
    path: str
    is_dir: bool
    size: int = 0
    children: List['StructureNode'] = field(default_factory=list)

@dataclass
class StructureAnalysis:
    """Complete directory structure."""
    root: str
    total_files: int = 0
    total_dirs: int = 0
    total_size: int = 0
    max_depth: int = 0
    tree: List[StructureNode] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "root": self.root,
            "total_files": self.total_files,
            "total_dirs": self.total_dirs,
            "total_size": self.total_size,
            "max_depth": self.max_depth,
            "analyzed_at": self.analyzed_at.isoformat(),
        }

class StructureAnalysisCapability:
    """
    CAPABILITY-000005: Repository Structure Analysis
    """
    VERSION = "1.0.0"
    CAPABILITY_ID = "CAPABILITY-000005"
    
    @property
    def name(self) -> str:
        return "StructureAnalysis"
    
    @property
    def description(self) -> str:
        return "Extracts complete directory structure"
    
    @property
    def version(self) -> str:
        return self.VERSION
    
    def execute(self, input_data: Dict[str, Any]) -> StructureAnalysis:
        """Execute structure analysis."""
        path = input_data.get("path", "")
        if not path:
            raise ValueError("Path is required")
        
        root = path
        tree = []
        total_files = 0
        total_dirs = 0
        total_size = 0
        max_depth = 0
        
        def walk(dir_path: str, depth: int = 0) -> List[StructureNode]:
            nonlocal total_files, total_dirs, total_size, max_depth
            
            nodes = []
            try:
                for item in os.listdir(dir_path):
                    if item.startswith("."):
                        continue
                    
                    item_path = os.path.join(dir_path, item)
                    rel_path = os.path.relpath(item_path, root)
                    
                    if os.path.isdir(item_path):
                        total_dirs += 1
                        children = walk(item_path, depth + 1)
                        nodes.append(StructureNode(
                            path=rel_path,
                            is_dir=True,
                            children=children
                        ))
                    else:
                        total_files += 1
                        try:
                            size = os.path.getsize(item_path)
                            total_size += size
                        except:
                            size = 0
                        nodes.append(StructureNode(
                            path=rel_path,
                            is_dir=False,
                            size=size
                        ))
            except PermissionError:
                pass
            
            if depth > max_depth:
                max_depth = depth
            
            return nodes
        
        tree = walk(path)
        
        return StructureAnalysis(
            root=root,
            total_files=total_files,
            total_dirs=total_dirs,
            total_size=total_size,
            max_depth=max_depth,
            tree=tree,
        )
