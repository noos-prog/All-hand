"""
CGP Services Module
=================

Services aggregated from capabilities.
"""

from .aggregator import (
    Service, ServiceAggregator,
    ServiceRegistry
)

__all__ = [
    "Service",
    "ServiceAggregator",
    "ServiceRegistry",
]
