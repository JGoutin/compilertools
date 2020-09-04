"""Generic utilities"""
import sys
from importlib import import_module
from collections.abc import MutableMapping
from functools import wraps

__all__ = ["always_str_list", "import_class", "BaseClass"]


def always_str_list(list_or_str):
    """Makes sure list_or_str is always a tuple or list

    Parameters
    ----------
    list_or_str: str or str iterable (tuple, list, ...)
        Parameter to set as iterable if single str.

    Returns
    -------
    Iterable
        Iterable equivalent to list_or_str."""
    if isinstance(list_or_str, str):
        return (list_or_str,)
    return list_or_str


def import_class(package_name, module_name, class_name, default_class):
    """Imports a sub module by name

    Parameters
    ----------
    package_name : str
        Package name in compilertools.
    module_name : str
        Module name in package.
    class_name : str
        Class name in module.
    default_class : class
        Default class to return if import or attribute error

    Returns
    -------
    class
        Imported class."""
    path = f"compilertools.{package_name}.{module_name}"
    try:
        import_module(path)
    except ImportError:
        return default_class
    try:
        return getattr(sys.modules[path], class_name)
    except AttributeError:
        return default_class


class BaseClass(MutableMapping):
    """Base class for data storage classes with default values, attribute/item access
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

            try:
                return self._items.__getitem__(key)
            except KeyError:
                pass

            value = class_property(self)

            if value is None:
                try:
                    value = self._default.__getitem__(key)
                except KeyError:
                    pass

            self._items[key] = value
            return value

        return _property

    def __getitem__(self, key):
        try:
            return self._items.__getitem__(key)
        except KeyError:
            pass

        if hasattr(self, key):
            return getattr(self, key)

        return self._default.__getitem__(key)

    def __getattr__(self, name):
        try:
            return self._items.__getitem__(name)
        except KeyError:
            pass

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


def dump_version(command):
    """
    Dump version for GCC/Clang compilers

    Parameters
    ----------
    command : str
        Compiler command.

    Returns
    -------
        float or None: version if found else None
    """
    from subprocess import run, PIPE, CalledProcessError

    try:
        if (
            command
            not in run(
                [command, "--version"],
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True,
                check=True,
            ).stdout
        ):
            # Command is linked to another compiler
            return
    except (FileNotFoundError, CalledProcessError):
        return

    for method in ("-dumpversion", "-dumpfullversion"):
        process = run(
            [command, method], stdout=PIPE, stderr=PIPE, universal_newlines=True
        )
        if not process.returncode and "." in process.stdout:
            return float(".".join(process.stdout.split(".", 2)[:2]))


def python_version(name):
    """
    Get compiler version used in Python.

    Parameters
    ----------
    name : str
        Compiler name.

    Returns
    -------
        float: version
    """
    from platform import python_compiler

    version_str = python_compiler()
    if name not in version_str.lower():
        return 0.0
    return float(version_str.split(" ", 2)[1].rsplit(".", 1)[0])
