# -*- coding: utf-8 -*-
"""Generic utilities"""
import sys
from importlib import import_module
from collections.abc import MutableMapping
from functools import wraps

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


class BaseClass(MutableMapping):
    """Base class for data storage classes
    with default values, attribute/item access
    and memoization"""

    def __init__(self):
        self._items = {}
        self._default = {}

    @staticmethod
    def _memoized_property(class_property):
        """Property decorator with memoization"""

        @property
        @wraps(class_property)
        def _property(self):
            key = class_property.__name__

            # Try getting cached value from dict
            try:
                return self._items.__getitem__(key)
            except KeyError:
                pass

            # Update value from property
            value = class_property(self)

            if value is None:
                # If None, try getting a default value
                try:
                    value = self._default.__getitem__(key)
                except KeyError:
                    pass

            self._items[key] = value
            return value
        return _property

    def __getitem__(self, key):
        # Try getting from dict
        try:
            return self._items.__getitem__(key)
        except KeyError:
            pass

        # Try getting from attributes
        if hasattr(self, key):
            return getattr(self, key)

        # Try getting from default values
        return self._default.__getitem__(key)

    def __getattr__(self, name):
        # Try getting from dict
        try:
            return self._items.__getitem__(name)
        except KeyError:
            pass

        # Try getting from default values
        try:
            return self._default.__getitem__(name)
        except KeyError:
            raise AttributeError

    def __setitem__(self, key, value):
        return self._items.__setitem__(key, value)

    def __delitem__(self, key):
        return self._items.__delitem__(key)

    def __len__(self):
        return self._items.__len__()

    def __iter__(self):
        return self._items.__iter__()
