# -*- coding: utf-8 -*-
"""Source files parsing functionalities"""

from os.path import splitext
from itertools import product

__all__ = ['use_openmp_pragma', 'use_openacc_pragma', 'use_cilkplus_pragma']


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


def _ignore_api(compiler, api):
    """Returne True if this API is not supported by
    the specified compiler. If compiler is None,
    always return False.

    compiler: Compiler to check.
    api: API to check the compiler support."""
    if compiler is None or compiler.support_api(api):
        return False
    return True


def _startwith_exts(c=None, fortran=None):
    """
    Returne a dict with file extensions as key and startswith as values.

    c: Startswith for C/C++.
    fortran: Startswith for Fortran.
    """
    startwith_exts = {}

    def insert(startswiths, exts):
        """startwith_exts inserter"""
        if startswiths is None:
            return

        # Make sure arguments are iterables
        if isinstance(startswiths, str):
            startswiths = (startswiths,)

        if isinstance(exts, str):
            exts = (exts,)

        # Insert Data
        for startswith, ext in product(startswiths, exts):
            startwith_exts[ext] = startswith

    insert(c, ('.c', '.cpp', '.cxx', '.cc', '.c++', '.cp'))
    insert(fortran, ('.f', '.for', '.f90', '.f95', '.f03', '.f08', '.f15'))

    return startwith_exts


def _use_api_pragma(sources, compiler, api, **startswith):
    """Generic API preprocessors checker

    sources: sources files to check.
    compiler/api: "_ignore_api" arguments.
    startswith: "_startwith_exts" arguments.
    """
    if _ignore_api(compiler, api):
        return False
    return _any_line_startwith(sources, _startwith_exts(**startswith))


def use_openmp_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for openMP preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    return _use_api_pragma(
        sources, compiler, 'openmp',
        c='#pragma omp ', fortran=('!$omp ', 'c$omp ', '*$omp '))


def use_openacc_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for OpenACC preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    return _use_api_pragma(
        sources, compiler, 'openacc',
        c='#pragma acc ', fortran=('!$acc ', 'c$acc ', '*$acc '))


def use_cilkplus_pragma(sources, compiler=None):
    """Check C/C++/Fortran sources for Intel® Cilk™ Plus preprocessors.

    sources: sources files to check.
    compiler: If specified, check if compiler is compatible with this
    API first and return immediatly False if not."""
    return _use_api_pragma(
        sources, compiler, 'opencilkplus',
        c='#pragma simd ', fortran='!dir$ simd ')
