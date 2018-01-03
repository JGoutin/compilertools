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
_PROCESSED_COMPILERS = set()


def update_extensions_suffixes(compiler):
    """Update file extensions suffixes compatibles with current machine
    with ones from a specified compiler.

    compiler: compiler name."""
    # Get suffixes
    from compilertools._core import (
        suffixe_from_args, get_compile_args, get_compiler)

    compiler = get_compiler(compiler)

    suffixes = suffixe_from_args(
        get_compile_args(compiler, current_machine=True),
        _machinery.EXTENSION_SUFFIXES)

    # Update list
    suffixes_index = ARCH_SUFFIXES.index
    suffixes_insert = ARCH_SUFFIXES.insert
    index = 0
    for suffixe in suffixes:
        try:
            index = suffixes_index(suffixe, index) + 1
        except ValueError:
            suffixes_insert(index, suffixe)
            index += 1

    # Memorize compiler as processed
    _PROCESSED_COMPILERS.add(compiler.name)

update_extensions_suffixes(None)

# Update Python import hook

class _ExtensionFileFinder(_MetaPathFinder):
    """Path finder for extensions with architecture specific optimizations"""

    def find_spec(self, fullname, *args, path=None, **kwargs):
        """Find module spec using new arch specific suffixes"""
        sys_paths = _sys.path

        # Search for compiler information file
        file_name = '%s.compilertools' % fullname
        for sys_path in sys_paths:
            file_path = _join(sys_path, file_name)
            if _isfile(file_path):
                # Get compiler name from file
                with open(file_path, 'rt') as file:
                    compiler = file.read()

                # If compiler not already processed, update suffixes
                if compiler not in _PROCESSED_COMPILERS:
                    update_extensions_suffixes(compiler)

                # Memorize path where file is for faster suffixed files
                # search
                sys_paths = [sys_path]
                break

        # Search for file
        for suffixe in ARCH_SUFFIXES:
            # Search for each suffix
            file_name = '%s%s' % (fullname, suffixe)
            for sys_path in sys_paths:
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
