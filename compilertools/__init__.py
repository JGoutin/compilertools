"""A library for helping to optimize Python extensions compilation."""

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


__all__ = ["imports", "get_compiler", "get_processor"]
