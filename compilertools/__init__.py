"""A library for helping optimizing Python extensions compilation."""

from sys import version_info as _version_info

if _version_info[0] < 3 or (_version_info[0] == 3 and _version_info[1] < 6):
    raise ImportError("Compilertools needs Python 3.6 or above.")
del _version_info

from compilertools._version import __version__  # noqa: E402

from compilertools import imports  # noqa: E402

from compilertools.processors import get_processor as _get_processor  # noqa: E402
from compilertools.compilers import get_compiler as _get_compiler  # noqa: E402


def get_compiler():
    """
    Get current compiler information.

    Returns
    -------
    compilertools.processors.ProcessorBase subclass instance
        Processor
    """
    return _get_compiler(current_compiler=True)


def get_processor():
    """
    Get current processor information.

    Returns
    -------
    compilertools.compilers.CompilerBase subclass instance
        Compiler
    """
    return _get_processor(arch=None, current_machine=True)


__all__ = ["imports", "get_compiler", "get_processor", "__version__"]
