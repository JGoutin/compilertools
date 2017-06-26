# -*- coding: utf-8 -*-
"""Source files parsing functionalities"""

from os.path import splitext

__all__ = ['get_compile_args', 'get_compiler']


def _any_line_startwith(sources, criterion):
    """Detect if any line in source files start with a specific string.

    sources: list of str, sources files paths
    criterion: dict with keys equal to lower case file extension, and
        value equal to lower case startwith string criterion."""
    for source in sources:
        startswith = criterion.get(splitext(source)[1].lower(), '')
        if not startswith:
            continue
        with open(source, 'rt') as file:
            for line in file:
                if line.lstrip().lower().startswith(startswith):
                    return True
    return False


def use_openmp_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for openMP preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    if compiler is not None:
        if not compiler.support_api('openmp'):
            return False
    return _any_line_startwith(sources, {
        '.c': '#pragma omp ', '.cpp': '#pragma omp ', '.f': '!$omp '})


def use_openacc_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for OpenACC preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    if compiler is not None:
        if not compiler.support_api('openacc'):
            return False
    return _any_line_startwith(sources, {
        '.c': '#pragma acc ', '.cpp': '#pragma acc ', '.f': '!$acc '})


def use_cilkplus_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for Intel® Cilk™ Plus preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    if compiler is not None:
        if not compiler.support_api('opencilkplus'):
            return False
    return _any_line_startwith(sources, {
        '.c': '#pragma simd ', '.cpp': '#pragma simd ', '.f': '!dir$ simd '})
