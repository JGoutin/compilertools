"""Import machinery"""

import sys as _sys
from os.path import join as _join
from os.path import isfile as _isfile
from importlib.abc import MetaPathFinder as _MetaPathFinder
import importlib.machinery as _machinery

__all__ = ["ARCH_SUFFIXES", "update_extensions_suffixes"]

#: Current arch compatibles suffixes
ARCH_SUFFIXES = []
_PROCESSED_COMPILERS = set()


def update_extensions_suffixes(compiler):
    """Updates file extensions suffixes compatibles with current machine with ones from
    a specified compiler.

    Parameters
    ----------
        compiler : str or None
            compiler name. If None, uses default compiler name on current platform"""
    from compilertools._core import (
        suffix_from_args,
        get_compile_args,
        get_compiler,
        log_exception,
    )

    try:

        compiler = get_compiler(compiler)

        suffixes = suffix_from_args(
            get_compile_args(compiler, current_machine=True),
            _machinery.EXTENSION_SUFFIXES,
        )

        suffixes_index = ARCH_SUFFIXES.index
        suffixes_insert = ARCH_SUFFIXES.insert
        index = 0
        for suffix in suffixes:
            try:
                index = suffixes_index(suffix, index) + 1
            except ValueError:
                suffixes_insert(index, suffix)
                index += 1

        _PROCESSED_COMPILERS.add(compiler.name)

    except Exception:
        # Compilertools should not break user application, but only back to compatible
        # mode. Exception is logged instead of risen.
        log_exception()


update_extensions_suffixes(None)


class _ExtensionFileFinder(_MetaPathFinder):
    """Path finder for extensions with architecture specific optimizations"""

    def find_spec(self, fullname, *args, path=None, **kwargs):
        """Finds module spec using new arch specific suffixes

        See importlib.abc.MetaPathFinder.find_spec for more information."""
        sys_paths = _sys.path

        file_name = f"{fullname}.compilertools"
        for sys_path in sys_paths:
            file_path = _join(sys_path, file_name)
            if _isfile(file_path):
                with open(file_path, "rt") as file:
                    compiler = file.read()

                if compiler not in _PROCESSED_COMPILERS:
                    update_extensions_suffixes(compiler)

                sys_paths = [sys_path]
                break

        for suffix in ARCH_SUFFIXES:
            file_name = f"{fullname}{suffix}"
            for sys_path in sys_paths:
                file_path = _join(sys_path, file_name)
                if _isfile(file_path):
                    loader = _machinery.ExtensionFileLoader(fullname, file_path)
                    return _machinery.ModuleSpec(fullname, loader, origin=file_path)
        return None


_sys.meta_path.insert(0, _ExtensionFileFinder())
