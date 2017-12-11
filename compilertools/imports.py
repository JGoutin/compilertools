# -*- coding: utf-8 -*-
"""Import machinery"""

import sys as _sys
from os.path import join as _join
from os.path import isfile as _isfile
from importlib.abc import MetaPathFinder as _MetaPathFinder
import importlib.machinery as _machinery


__all__ = ['ARCH_SUFFIXES', 'update_extensions_suffixes']

# Current arch compatibles suffixes
ARCH_SUFFIXES = []


def update_extensions_suffixes(compiler):
    """Update file extensions suffixes compatibles with current machine
    with ones from a specified compiler.

    compiler: compiler name."""
    from compilertools._core import suffixe_from_args, get_compile_args

    suffixes = suffixe_from_args(
        get_compile_args(compiler, current_machine=True),
        _machinery.EXTENSION_SUFFIXES, compiler)

    for suffixe in suffixes:
        if suffixe not in ARCH_SUFFIXES:
            ARCH_SUFFIXES.append(suffixe)

update_extensions_suffixes(None)

# Update Python import hook

class _ExtensionFileFinder(_MetaPathFinder):
    """Path finder for extensions with architecture specific optimizations"""

    def find_spec(self, fullname, path=None, *args, **kwargs):
        """Find module spec using new arch specific suffixes"""
        for suffixe in ARCH_SUFFIXES:
            # Search for each suffixe
            file_name = '%s%s' % (fullname, suffixe)
            for sys_path in _sys.path:
                # Search in all sys.path
                file_path = _join(sys_path, file_name)
                if _isfile(file_path):
                    # Use standard extension loader and specified spec
                    loader = _machinery.ExtensionFileLoader(
                        fullname, file_path)
                    return _machinery.ModuleSpec(
                        fullname, loader, origin=file_path)
        return None

_sys.meta_path.insert(0, _ExtensionFileFinder())  # Loaded before legacy loaders
