"""
Universal Capability Runtime
PHASE-02: EXECUTION-000006 - Universal Capability Runtime

Standardizes the lifecycle of every Capability.
"""

__version__ = "1.0"

from agos_kernel.civilization.capability_runtime.contract import (
    CapabilityContract,
    CapabilityRegistryEntry,
    CapabilityDomain,
    ExecutionMode,
    CertificationStatus,
    InputSpec,
    OutputSpec,
    ConfigurationSchema,
    ExecutionConstraint,
    SecurityRequirement,
    PerformanceTarget,
    CompatibilityEntry,
)
from agos_kernel.civilization.capability_runtime.runtime import (
    LifecycleStage,
    CapabilityStatus,
    CapabilityContext,
    ExecutionResult,
    CapabilityInstance,
    CapabilityLoader,
    CapabilityResolver,
    CapabilityValidator,
    CapabilityScheduler,
    CapabilityExecutor,
    CapabilitySandbox,
    CapabilityMonitor,
    CapabilityRecoveryEngine,
    CapabilityBenchmarkEngine,
    CapabilityCertificationEngine,
    CapabilityRuntime,
)

__all__ = [
    'CapabilityContract',
    'CapabilityRegistryEntry',
    'CapabilityDomain',
    'ExecutionMode',
    'CertificationStatus',
    'InputSpec',
    'OutputSpec',
    'ConfigurationSchema',
    'ExecutionConstraint',
    'SecurityRequirement',
    'PerformanceTarget',
    'CompatibilityEntry',
    'LifecycleStage',
    'CapabilityStatus',
    'CapabilityContext',
    'ExecutionResult',
    'CapabilityInstance',
    'CapabilityLoader',
    'CapabilityResolver',
    'CapabilityValidator',
    'CapabilityScheduler',
    'CapabilityExecutor',
    'CapabilitySandbox',
    'CapabilityMonitor',
    'CapabilityRecoveryEngine',
    'CapabilityBenchmarkEngine',
    'CapabilityCertificationEngine',
    'CapabilityRuntime',
]
