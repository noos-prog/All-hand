"""Evidence - Proof for detections."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Evidence:
    """Evidence for a detection."""
    file_path: str
    line_number: Optional[int] = None
    content: str = ""
    confidence: float = 1.0
    context: str = ""
    snippet: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "content": self.content,
            "confidence": self.confidence,
            "context": self.context,
            "snippet": self.snippet,
        }
