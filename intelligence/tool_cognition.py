"""AGOS Universal Tool Cognition Layer - Semantic understanding layer for every engineering tool."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

TOOL_MODEL_FIELDS = ["Inputs", "Outputs", "Constraints", "Requirements", "Capabilities", "Performance", "Reliability", "Cost", "Dependencies"]


@dataclass
class ToolInput:
    """Input specification for a tool."""
    name: str
    type: str
    required: bool = True
    description: str = ""
    default: Optional[Any] = None


@dataclass
class ToolOutput:
    """Output specification for a tool."""
    name: str
    type: str
    description: str = ""


@dataclass
class ToolConstraint:
    """Constraint for tool execution."""
    constraint_type: str
    value: Any
    description: str = ""


@dataclass
class ToolRequirement:
    """Requirement for using a tool."""
    requirement_type: str
    value: Any
    description: str = ""


@dataclass
class ToolCapability:
    """A capability provided by a tool."""
    capability_id: str
    name: str
    description: str
    inputs: List[ToolInput] = field(default_factory=list)
    outputs: List[ToolOutput] = field(default_factory=list)
    constraints: List[ToolConstraint] = field(default_factory=list)
    requirements: List[ToolRequirement] = field(default_factory=list)


@dataclass
class ToolDescriptor:
    """Complete descriptor for a tool."""
    tool_id: str
    name: str
    category: str
    description: str
    version: str
    capabilities: List[ToolCapability] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ToolCognition:
    """
    Universal Tool Cognition Layer.
    
    Target: Every engineering tool represented as structured knowledge
    
    Model Fields:
    ✅ Inputs, Outputs, Constraints, Requirements
    ✅ Capabilities, Performance, Reliability, Cost, Dependencies
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self._tools: Dict[str, ToolDescriptor] = {}
        self._capabilities_index: Dict[str, List[str]] = {}
    
    def register_tool(self, tool: ToolDescriptor) -> None:
        """Register a tool with its capabilities."""
        self._tools[tool.tool_id] = tool
        for cap in tool.capabilities:
            if cap.name not in self._capabilities_index:
                self._capabilities_index[cap.name] = []
            self._capabilities_index[cap.name].append(tool.tool_id)
    
    def get_tool(self, tool_id: str) -> Optional[ToolDescriptor]:
        """Get a tool by ID."""
        return self._tools.get(tool_id)
    
    def find_tools_by_capability(self, capability: str) -> List[ToolDescriptor]:
        """Find tools that provide a specific capability."""
        tool_ids = self._capabilities_index.get(capability, [])
        return [self._tools[tid] for tid in tool_ids if tid in self._tools]
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "registered_tools": len(self._tools),
            "capabilities": len(self._capabilities_index),
        }
