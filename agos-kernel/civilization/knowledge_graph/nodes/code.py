"""
Code Nodes
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

First-class nodes for code-level concepts.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from agos_kernel.civilization.knowledge_graph.nodes.base import (
    GraphNode, NodeType, NodeMetadata
)


@dataclass
class ClassNode(GraphNode):
    """Class node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.CLASS, **kwargs)
        self.class_name: str = kwargs.get('class_name', '')
        self.bases: List[str] = kwargs.get('bases', [])
        self.methods: List[str] = kwargs.get('methods', [])
        self.attributes: List[str] = kwargs.get('attributes', [])
        self.is_abstract: bool = kwargs.get('is_abstract', False)
        self.is_interface: bool = kwargs.get('is_interface', False)


@dataclass
class InterfaceNode(GraphNode):
    """Interface node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.INTERFACE, **kwargs)
        self.interface_name: str = kwargs.get('interface_name', '')
        self.methods: List[str] = kwargs.get('methods', [])
        self.extends: List[str] = kwargs.get('extends', [])


@dataclass
class TraitNode(GraphNode):
    """Trait node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.TRAIT, **kwargs)
        self.trait_name: str = kwargs.get('trait_name', '')
        self.methods: List[str] = kwargs.get('methods', [])


@dataclass
class StructNode(GraphNode):
    """Struct node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.STRUCT, **kwargs)
        self.struct_name: str = kwargs.get('struct_name', '')
        self.fields: List[str] = kwargs.get('fields', [])


@dataclass
class EnumNode(GraphNode):
    """Enum node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.ENUM, **kwargs)
        self.enum_name: str = kwargs.get('enum_name', '')
        self.values: List[str] = kwargs.get('values', [])


@dataclass
class FunctionNode(GraphNode):
    """Function node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.FUNCTION, **kwargs)
        self.function_name: str = kwargs.get('function_name', '')
        self.parameters: List[Dict] = kwargs.get('parameters', [])
        self.return_type: str = kwargs.get('return_type', '')
        self.is_async: bool = kwargs.get('is_async', False)
        self.is_generator: bool = kwargs.get('is_generator', False)
        self.locals: List[str] = kwargs.get('locals', [])


@dataclass
class MethodNode(GraphNode):
    """Method node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.METHOD, **kwargs)
        self.method_name: str = kwargs.get('method_name', '')
        self.parameters: List[Dict] = kwargs.get('parameters', [])
        self.return_type: str = kwargs.get('return_type', '')
        self.is_static: bool = kwargs.get('is_static', False)
        self.is_abstract: bool = kwargs.get('is_abstract', False)
        self.is_private: bool = kwargs.get('is_private', False)
        self.parent_class: str = kwargs.get('parent_class', '')


@dataclass
class VariableNode(GraphNode):
    """Variable node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.VARIABLE, **kwargs)
        self.variable_name: str = kwargs.get('variable_name', '')
        self.data_type: str = kwargs.get('data_type', '')
        self.initial_value: str = kwargs.get('initial_value', '')
        self.is_mutable: bool = kwargs.get('is_mutable', True)
        self.is_local: bool = kwargs.get('is_local', True)


@dataclass
class ConstantNode(GraphNode):
    """Constant node."""
    
    def __init__(self, **kwargs):
        super().__init__(type=NodeType.CONSTANT, **kwargs)
        self.constant_name: str = kwargs.get('constant_name', '')
        self.value: str = kwargs.get('value', '')
        self.data_type: str = kwargs.get('data_type', '')
