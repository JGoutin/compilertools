# -*- coding: utf-8 -*-
"""Source files parsing functionalities"""

from os.path import splitext
from itertools import product
from compilertools._config_build import CONFIG_BUILD

__all__ = []


def _any_line_startswith(sources, criterion):
    """Detect if any line in source files start with a specific string.

    sources: str or list of str, sources files paths
    criterion: dict with keys equal to lower case file extension, and
        value equal to a list of lower case startswith string criterion."""
    # Make sure arguments are iterables
    if isinstance(sources, str):
        sources = (sources,)

    # Check files for criterions
    for source in sources:
        # Select criterions based on file extension
        try:
            startswiths = criterion[splitext(source)[1].lower()]
        except KeyError:
            continue

        # Check criterions
        with open(source, 'rt') as file:
            for line, startswith in product(file, startswiths):
                if line.lstrip().lower().startswith(startswith):
                    return True
    return False


def _ignore_api(compiler, api):
    """Return True if this API is not supported by
    the specified compiler. If compiler is None,
    always return False.

    compiler: Compiler to check.
    api: API to check the compiler support."""
    if compiler is None or api in compiler['api']:
        return False
    return True


def _startswith_exts(**startswiths_dict):
    """
    Return a dict with file extensions as key and startswith as values.

    startswiths_dict: dict with key as lower case language and value as list
        of startswith values.
    """
    startwith_exts = {}

    config_extensions = CONFIG_BUILD['extensions']
    for key in startswiths_dict:
        startswiths = startswiths_dict[key]
        if startswiths is None:
            continue

        try:
            exts = config_extensions[key]
        except KeyError:
            continue

        # Make sure arguments are iterables
        if isinstance(startswiths, str):
            startswiths = (startswiths,)

        # Insert Data
        for ext in exts:
            startwith_exts[ext] = startswiths

    return startwith_exts


def _use_api_pragma(sources, compiler, api, **startswith):
    """Generic API preprocessors checker

    sources: sources files to check.
    compiler/api: "_ignore_api" arguments.
    startswith: "_startswith_exts" arguments.
    """
    if _ignore_api(compiler, api):
        return False
    return _any_line_startswith(sources, _startswith_exts(**startswith))
