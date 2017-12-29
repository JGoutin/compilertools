# -*- coding: utf-8 -*-
"""x86-64 Processors"""

from compilertools.processors.x86_32 import Processor as _X86_32_Processor

__all__ = ['Processor']


class Processor(_X86_32_Processor):
    """x86-64 CPU"""
