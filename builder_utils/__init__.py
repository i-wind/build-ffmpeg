"""
  builder_utils
"""
from .build import Builder
from .config import logger, command
from .cache import Cache, CacheError


__version__ = (0, 1, 6)


def version():
    """version information"""
    return '.'.join([str(v) for v in __version__])
