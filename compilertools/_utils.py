# -*- coding: utf-8 -*-
"""Generic utilities"""
import sys
from importlib import import_module

__all__ = ['always_str_list', 'import_class', 'BaseClass']


def always_str_list(list_or_str):
    """Make sure list_or_str is always a tuple or list

    list_or_str: str or str iterable (tuple, list, ...)"""
    if isinstance(list_or_str, str):
        return list_or_str,
    return list_or_str


def import_class(package_name, module_name, class_name, default_class):
    """import a sub module by name

    package_name : package name in compilertools
    module_name : module name in package
    class_name : class name in module
    default_class : default class to return if import or attribute error"""
    path = 'compilertools.%s.%s' % (package_name, module_name)
    try:
        import_module(path)
    except ImportError:
        return default_class
    try:
        return getattr(sys.modules[path], class_name)
    except AttributeError:
        return default_class


class BaseClass:
    """Base class for data storage classes"""

    def __init__(self):
        self._attributes = {}
        self._get_attr = self._attributes.get
