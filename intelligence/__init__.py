"""
AGOS Intelligence Platform
======================

Universal engineering intelligence for millions of AI agents.
One unified platform for cognitive capabilities, tool cognition, and engineering ontology.

Author: AGOS Team
Version: 1.0.0
"""

from .ai_execution import (
    AIExecutionFabric, AIProvider, AIModel, AIExecutionRequest, AIExecutionResult,
    AIModelType, AIExecutionStatus
)
from .tool_cognition import (
    ToolCognition, ToolCapability, ToolDescriptor, ToolInput, ToolOutput,
    ToolConstraint, ToolRequirement
)
from .ontology import (
    EngineeringOntology, Concept, ConceptRelation, OntologyNode,
    ConceptType, RelationType
)
from .protocol import (
    ProtocolHandler, ProtocolType, Message, ProtocolMessage,
    ConnectionState
)
from .cognitive_engine import (
    CognitiveEngine, CognitiveContext, CognitiveResult, ReasoningStrategy,
    KnowledgeGraph, MemorySystem
)
from .platform import (
    UniversalIntelligence, IntelligenceService, AgentRegistry,
    CapabilityDiscovery
)

__all__ = [
    # AI Execution
    "AIExecutionFabric", "AIProvider", "AIModel", "AIExecutionRequest",
    "AIExecutionResult", "AIModelType", "AIExecutionStatus",
    # Tool Cognition
    "ToolCognition", "ToolCapability", "ToolDescriptor", "ToolInput",
    "ToolOutput", "ToolConstraint", "ToolRequirement",
    # Ontology
    "EngineeringOntology", "Concept", "ConceptRelation", "OntologyNode",
    "ConceptType", "RelationType",
    # Protocol
    "ProtocolHandler", "ProtocolType", "Message", "ProtocolMessage",
    "ConnectionState",
    # Cognitive Engine
    "CognitiveEngine", "CognitiveContext", "CognitiveResult",
    "ReasoningStrategy", "KnowledgeGraph", "MemorySystem",
    # Platform
    "UniversalIntelligence", "IntelligenceService", "AgentRegistry",
    "CapabilityDiscovery",
]

__version__ = "1.0.0"
