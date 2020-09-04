"""Core functionalities"""

from compilertools.compilers import get_compiler
from compilertools._utils import always_str_list


__all__ = ["get_compile_args", "get_compiler", "suffix_from_args", "log_exception"]


def get_compile_args(
    compiler=None, arch=None, current_machine=False, current_compiler=False
):
    """Gets compiler args OrderedDict for a specific compiler and architecture
    combination.

    Parameters
    ----------
    compiler : str or compilertools.compilers.CompilerBase subclass
        Compiler name or instance.
    arch : str
        Target architecture name.
    current_machine : bool
        Only compatibles with current machine CPU
    current_compiler : bool
        If True, return only arguments compatibles with current compiler.

    Returns
    -------
    collections.OrderedDict
        Arguments
    """
    return get_compiler(compiler, current_compiler).compile_args(arch, current_machine)


def suffix_from_args(args, extension="", return_empty_suffixes=False):
    """Returns suffixes from args.

    Parameters
    ----------
    args : collections.OrderedDict
        Arguments.
    extension : str or list of str
        File extensions.
    return_empty_suffixes : bool
        If True, return '' suffixes.

    Returns
    -------
    list of str
        Suffixes"""
    suffixes = []
    for suffix in args:
        if extension:
            if suffix:
                for ext in always_str_list(extension):
                    suffixes.append(f".{suffix}{ext}")
            elif return_empty_suffixes:
                for ext in always_str_list(extension):
                    suffixes.append(ext)
        elif suffix:
            suffixes.append(f".{suffix}")
        elif return_empty_suffixes:
            suffixes.append("")

    return suffixes


def log_exception():
    """
    Log exception with system info.

    Must be called in exception handler.
    """
    from compilertools._config import CONFIG

    if CONFIG.get("logging", True):
        from logging import getLogger
        import platform

        getLogger("compilertools").exception(
            "\n".join(
                (
                    "Compilertools: Exception when trying to enable optimization, "
                    "Back to compatible mode.",
                    f"  OS: {platform.platform()}",
                    f"  CPU: {platform.processor()}",
                    f"  Python: {platform.python_version()} "
                    f"[{platform.python_compiler()}]",
                )
            )
        )
