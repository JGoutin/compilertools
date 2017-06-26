# -*- coding: utf-8 -*-
"""x86-64/amd64 Processors"""

from compilertools.processors.x86 import Processor as _X86_Processor

__all__ = ['Processor']


class Processor(_X86_Processor):
    """x86-64 CPU"""
    pass
