# -*- coding: utf-8 -*-
"""Import machinery"""

import sys
from os.path import exists, join
from importlib.abc import MetaPathFinder
from importlib.machinery import (
    EXTENSION_SUFFIXES, ModuleSpec, ExtensionFileLoader)
from compilertools._core import suffixe_from_args, get_compile_args

__all__ = ['ARCH_SUFFIXES', 'update_extensions_suffixes']

# Current arch compatibles suffixes
ARCH_SUFFIXES = suffixe_from_args(get_compile_args(current_machine=True),
                                  EXTENSION_SUFFIXES)


def update_extensions_suffixes(compiler):
    """Update file extensions suffixes compatibles with current machine
    with ones froms specified compiler.

    compiler: compiler name."""
    suffixes = suffixe_from_args(
        get_compile_args(compiler, current_machine=True), EXTENSION_SUFFIXES,
        compiler)
    for suffixe in suffixes:
        if suffixe not in ARCH_SUFFIXES:
            ARCH_SUFFIXES.append(suffixe)


# Update Python import hook

class ExtensionFileFinder(MetaPathFinder):
    """Path finder for extensions with architecture specific optimizations"""

    def find_spec(self, fullname, path=None, *args, **kwargs):
        """Find module spec using new arch specific suffixes"""
        for suffixe in ARCH_SUFFIXES:
            # Search for each suffixe
            file_name = '%s%s' % (fullname, suffixe)
            for sys_path in sys.path:
                # Search in all sys.path
                file_path = join(sys_path, file_name)
                if exists(file_path):
                    # Use standard .pyd loader and specified spec
                    loader = ExtensionFileLoader(fullname, file_path)
                    return ModuleSpec(fullname, loader, origin=file_path)
        return None


sys.meta_path.insert(0, ExtensionFileFinder())  # Loaded before legacy loaders
