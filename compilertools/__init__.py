# -*- coding: utf-8 -*-
"""A library for helping optimizing Python extensions compilation."""
# Load version
from compilertools._version import __version__

# Load only imports part at start, build part can be imported if needed
from compilertools import imports
__all__ = ['imports']
