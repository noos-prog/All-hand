"""
AGOS API Module
===============

API interfaces for the AGOS system.
Provides REST API and client interfaces.
"""

from .runtime import CivilizationAPI, APIEndpoint, SimulationRuntime, SimulationType
from .server import APIServer, HTTPMethod, Route, HTTPRequest, HTTPResponse, get_api_server

__all__ = [
    # Runtime
    "CivilizationAPI",
    "APIEndpoint",
    "SimulationRuntime",
    "SimulationType",
    # Server
    "APIServer",
    "HTTPMethod",
    "Route",
    "HTTPRequest",
    "HTTPResponse",
    "get_api_server",
]

