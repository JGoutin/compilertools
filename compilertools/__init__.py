# -*- coding: utf-8 -*-
"""A library for helping optimizing Python extensions compilation."""

# Check version compatibility
from sys import version_info as _version_info
if _version_info[0] < 3 or _version_info[1] < 4:
    raise ImportError('Compilertools needs Python 3.4 or above.')
del _version_info

# Load version
from compilertools._version import __version__

# Load only imports part at start, build part can be imported if needed
from compilertools import imports
__all__ = ['imports']
