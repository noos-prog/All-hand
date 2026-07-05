"""
AGOS Patterns Module
==================

Design patterns implementation for AGOS.
"""

from .patterns import (
    Singleton,
    Factory,
    Adapter,
    Strategy,
    get_registry,
)

__all__ = ["Singleton", "Factory", "Adapter", "Strategy", "get_registry"]
