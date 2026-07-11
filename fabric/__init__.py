"""AGOS Fabric - Neural network of AI agents and capabilities."""

from .brain import FabricBrain, NeuralLayer, Neuron, NeuronType
from .capability import FabricCapability, CapabilityChain, Capability, CapabilityType
from .execution import FabricExecution, ExecutionGraph, ExecutionNode, ExecutionNodeType, ExecutionStatus
from .mission import FabricMission, MissionPlanner, MissionStatus, MissionPriority, MissionObjective
from .knowledge import FabricKnowledge, KnowledgeEntry, KnowledgeType

__all__ = [
    "FabricBrain", "NeuralLayer", "Neuron", "NeuronType",
    "FabricCapability", "CapabilityChain", "Capability", "CapabilityType",
    "FabricExecution", "ExecutionGraph", "ExecutionNode", "ExecutionNodeType", "ExecutionStatus",
    "FabricMission", "MissionPlanner", "MissionStatus", "MissionPriority", "MissionObjective",
    "FabricKnowledge", "KnowledgeEntry", "KnowledgeType",
]

__version__ = "1.0.0"
