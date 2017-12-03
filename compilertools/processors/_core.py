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

    # Aliases for architectures names
    arch = CONFIG.get('arch_alias', {}).get(arch, arch)

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

    @property
    def vendor(self):
        """CPU manufacturer"""
        return self.get('vendor', '')

    @property
    def brand(self):
        """CPU brand"""
        return self.get('brand', '')

    @property
    def features(self):
        """CPU features"""
        return self.get('features', [])

    @property
    def is_current_machine(self):
        """Return True is CPU is from current machine"""
        return self.get('current_machine', False)
