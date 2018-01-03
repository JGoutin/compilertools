# -*- coding: utf-8 -*-
"""Base class and functions for CPU"""

from platform import machine
from compilertools._utils import import_class, BaseClass
from compilertools._config import CONFIG

__all__ = ['ProcessorBase', 'get_processor', 'get_arch']


def get_arch(arch=None):
    """Check achitecture name and return fixed name.

    arch : arch to be checked"""
    # Current machine architecture
    if arch is None:
        arch = machine()
    arch = arch.lower()

    arch_dict = CONFIG['architectures']

    # If cross compilation, keep only target architecture
    if '_' in arch:
        current, target = arch.split('_', 1)
        if current in arch_dict and target in arch_dict:
            arch = target

    # Prefixed architecture name ('linux-x86_64', 'win-amd64', ...)
    if arch not in arch_dict and '-' in arch:
        name = arch.rsplit('-', 1)[1]
        if name in arch_dict:
            arch = name

    # Aliases for architectures names
    arch = arch_dict.get(arch, arch)

    return arch


def get_processor(arch, *args, **kwargs):
    """Return processor class

    arch: processor architecture
    *args, **kwargs: args for class instanciation"""
    return import_class('processors', get_arch(arch), 'Processor',
                        ProcessorBase)(*args, **kwargs)


class ProcessorBase(BaseClass):
    """Base class for CPU"""

    def __init__(self, current_machine=False):
        BaseClass.__init__(self)
        self['current_machine'] = current_machine
        self._default['current_machine'] = False
        self._default['vendor'] = ''
        self._default['brand'] = ''
        self._default['features'] = []

    @BaseClass._memoized_property
    def arch(self):
        """processor architecture"""
        return self.__module__.rsplit('.', 1)[-1]
