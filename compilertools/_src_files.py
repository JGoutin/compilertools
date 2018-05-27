# -*- coding: utf-8 -*-
"""Source files parsing functionalities"""

from os.path import splitext
from itertools import product
from compilertools._config_build import ConfigBuild

__all__ = []


def _any_line_startswith(sources, criterion):
    """Detects if any line in source files start with a specific string.

    Parameters
    ----------
    sources : str or list of str
        Sources files paths
    criterion : dict with str as keys and values
        Dictionary with keys equal to lower case file extension, and
        value equal to a list of lower case startswith string criterion.

    Returns
    -------
    bool
        Returns True if criterion detected."""
    # Makes sure arguments are iterable
    if isinstance(sources, str):
        sources = (sources,)

    # Checks files for criterions
    for source in sources:
        # Selects criterions based on file extension
        try:
            startswiths = criterion[splitext(source)[1].lower()]
        except KeyError:
            continue

        # Checks criterions
        with open(source, 'rt') as file:
            for line, startswith in product(file, startswiths):
                if line.lstrip().lower().startswith(startswith):
                    return True
    return False


def _ignore_api(compiler, api):
    """Returns True if this API is not supported by
    the specified compiler. If compiler is None,
    always return False.

    Parameters
    ----------
    compiler: str or compilertools.compilers.CompilerBase or None
        Compiler to check.
    api: str
        API to check the compiler support.

    Returns
    -------
    bool
        Returns True if API not supported."""
    if compiler is None or api in compiler['api']:
        return False
    return True


def _startswith_exts(**startswiths_dict):
    """
    Returns a dict with file extensions as key and startswith as values.

    Parameters
    ----------
    startswiths_dict : dict with str as keys and values
        Dictionary with key as lower case language and value as list
        of startswith values.

    Returns
    -------
    dict with str as keys and values
        Keys are file extensions, values are startswith.
    """
    startswith_exts = {}

    config_extensions = ConfigBuild.extensions
    for key in startswiths_dict:
        startswiths = startswiths_dict[key]
        if startswiths is None:
            continue

        try:
            exts = config_extensions[key]
        except KeyError:
            continue

        # Makes sure arguments are iterable
        if isinstance(startswiths, str):
            startswiths = (startswiths,)

        # Insert Data
        for ext in exts:
            startswith_exts[ext] = startswiths

    return startswith_exts


def _use_api_pragma(sources, compiler, api, **startswith):
    """Generic API preprocessors checker

    Parameters
    ----------
    sources : str or list of str
        sources files to check.
    compiler, api
        See "_ignore_api" arguments.
    startswith
        See "_startswith_exts" arguments.

    Returns
    -------
    bool
        Returns True if API preprocessor usage detected.
    """
    if _ignore_api(compiler, api):
        return False
    return _any_line_startswith(sources, _startswith_exts(**startswith))
