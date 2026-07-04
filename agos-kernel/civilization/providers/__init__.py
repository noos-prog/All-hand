"""
Foundation Providers
PHASE-02: Foundation Civilization

Foundation Providers:
- Filesystem
- Git
- GitHub
- Docker
- CLI
"""

__version__ = "2.0.0"

from agos_kernel.civilization.providers.filesystem_provider import FilesystemProvider
from agos_kernel.civilization.providers.git_provider import GitProvider
from agos_kernel.civilization.providers.github_provider import GitHubProvider

__all__ = [
    'FilesystemProvider',
    'GitProvider',
    'GitHubProvider',
]
