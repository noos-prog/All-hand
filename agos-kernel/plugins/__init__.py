"""
AGOS Plugins Module
=================

Plugin system for AGOS.
"""

from .plugins import PluginManager, Plugin, get_plugin_manager

__all__ = ["PluginManager", "Plugin", "get_plugin_manager"]

