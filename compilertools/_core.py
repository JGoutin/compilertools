# -*- coding: utf-8 -*-
"""Core functionalities"""

from compilertools.compilers import get_compiler
from compilertools._utils import always_str_list


__all__ = ['get_compile_args', 'get_compiler', 'suffixe_from_args']


def get_compile_args(compiler=None, arch=None, current_machine=False,
                     current_compiler=False):
    """Get compiler args OrderedDict for a specific compiler and architecture
    combination.

    compiler: compiler name or instance.
    arch: target architecture name.
    current_machine: Only compatibles with current machine CPU
    current_compiler : If True, return only arguments compatibles with
    current compiler."""
    # Generate options matrix for compiler and architecture
    return get_compiler(compiler).compile_args(
        arch, current_machine, current_compiler)


def suffixe_from_args(args, extension='', return_empty_suffixes=False):
    """Return suffixes from args.

    args: args OrderedDict
    extension : File extensions, single str or list of str
    return_empty_suffixes : If True, return '' suffixes."""
    # suffixe filtering

    suffixes = []
    for suffix in args:
        # Create string
        if extension:
            if suffix:
                for ext in always_str_list(extension):
                    suffixes.append('.%s%s' % (suffix, ext))
            elif return_empty_suffixes:
                for ext in always_str_list(extension):
                    suffixes.append(ext)
        elif suffix:
            suffixes.append('.%s' % suffix)
        elif return_empty_suffixes:
            suffixes.append('')

    # Return with same form as input
    return suffixes
