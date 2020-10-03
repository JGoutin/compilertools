"""Building functions"""

from functools import wraps as _wraps
from distutils.command.build_ext import build_ext as _build_ext

from compilertools._config_build import ConfigBuild
from compilertools._core import (
    suffix_from_args,
    get_compile_args,
    get_compiler,
    log_exception as _log_exception,
)

__all__ = [
    "ConfigBuild",
    "get_build_compile_args",
    "get_build_link_args",
    "get_compile_args",
    "get_compiler",
    "suffix_from_args",
]


def get_build_compile_args(
    compiler=None,
    arch=None,
    current_machine=None,
    ext_suffix=None,
    use_option=None,
    use_api=None,
):
    """Gets compiler args for build as a dict of file suffixes as key and args string as
    values.

    Parameters
    ----------
    compiler : str or compilertools.compilers.CompilerBase subclass
        compiler name or instance. If None, use distutils default value
    arch : str
        target architecture name.
    current_machine : bool
        return only one suffix/args pair optimized for current machine only. If None,
        use CONFIG_BUILD value.
    ext_suffix : list of str
        Extensions to use after suffix.
    use_option : list of str
        List of options to use (fast_fpmath, ...).
    use_api : list of str
        List of API to use (openmp, ...). If None, don't enable API.

    Returns
    -------
    dict with str as keys and values
        Suffixes are keys, arguments are values.
    """
    if ext_suffix is None:
        from distutils.sysconfig import get_config_var

        ext_suffix = get_config_var("EXT_SUFFIX")
    if current_machine is None:
        current_machine = _find_if_current_machine()
    if arch is None:
        from distutils.util import get_platform

        arch = get_platform()

    build_args = {}
    compiler = get_compiler(compiler, current_compiler=True)

    if current_machine:
        try:
            build_args[ext_suffix] = [compiler.compile_args_current_machine()]

        except Exception:
            # Compilertools should not break compilation in this case because it may be
            # called from a Pip install. It should only back to compatible default in
            # this case.
            _log_exception()
            build_args[ext_suffix] = []

    else:
        include = ConfigBuild.suffixes_includes
        if not include:
            exclude = ConfigBuild.suffixes_excludes

            def filter_suffix(suffix_to_test):
                """Filter by exclusion"""
                return suffix_to_test in exclude

        else:

            def filter_suffix(suffix_to_test):
                """Filter by inclusion"""
                return suffix_to_test not in include

        args = get_compile_args(compiler, arch, current_compiler=True)

        for suffixes in set(args):
            for suffix in suffixes.split("-"):
                if filter_suffix(suffix):
                    del args[suffixes]
                    break

        for arg, suffix in zip(args.values(), suffix_from_args(args, ext_suffix, True)):
            build_args[suffix] = arg

    arg_ext = []

    _add_args(compiler, arg_ext, "api", "compile", use_api)

    _add_args(compiler, arg_ext, "option", "compile", use_option)

    if arg_ext:
        for suffix in build_args:
            build_args[suffix].extend(arg_ext)

    return build_args


def get_build_link_args(compiler=None, use_api=None, use_option=None):
    """Gets linker arg for build as a list of args string.

    Parameters
    ----------
    compiler : str or compilertools.compilers.CompilerBase subclass
        compiler name or instance. If None, use distutils default value
    use_api : list of str
        List of API to use (openmp, ...). If None, don't enable API.
    use_option : list of str
        List of options to use (fast_fpmath, ...).
    """
    compiler = get_compiler(compiler)
    build_args = []
    _add_args(compiler, build_args, "api", "link", use_api)
    _add_args(compiler, build_args, "option", "link", use_option)
    return build_args


def _add_args(compiler, arg_list, arg_cat, arg_type, args_names):
    """Updates arguments list with API specific arguments

    Parameters
    ----------
    arg_list : list of str
        List of arguments to update.
    arg_cat : {'api', 'option'}
        Category of argument.
    arg_type : {'link', 'compile'}
        Type of argument.
    args_names : list of str
        Arguments names to use."""
    if args_names:
        for name in args_names:
            try:
                arg_list.append(compiler[arg_cat][name][arg_type])
            except KeyError:
                continue


def _find_if_current_machine():
    """Checks configuration and if current machine is not specified, tries to set it.

    Returns
    -------
    str
        Current machine."""
    current_machine = ConfigBuild.current_machine
    if not isinstance(current_machine, bool):
        from os import getcwd
        from os.path import basename

        return basename(getcwd()).startswith("pip-")
    return current_machine


class _String(str):
    """str with "parent_extension" extra attribute."""

    parent_extension = None

    @_wraps(str.split)
    def split(self, *args, **kwargs):
        """Split String, but keep "parent_extension" attribute.

        See str.split for more information."""
        splitted = str.split(self, *args, **kwargs)
        for i, string in enumerate(splitted):
            splitted[i] = _String(string)
            splitted[i].parent_extension = self.parent_extension
        return splitted


def _update_extension(self, ext):
    """Updates build_ext extensions for add new args and suffixes based on the current
    extension.

    Parameters
    ----------
    self : build_ext instance
        Patched build_ext.
    ext : Extension instance
        Extension from build_ext.extensions.

    Returns
    -------
    list of Extension
        Patched build_ext.extensions."""
    if ConfigBuild.disabled:
        return [ext]

    compiler = get_compiler(self.compiler.compiler_type, current_compiler=True)
    self.compilertools_compiler_name = compiler.name

    if not hasattr(self, "compilertools_store_compiler"):
        from distutils.ccompiler import get_default_compiler

        default_compiler = get_default_compiler(self.plat_name)
        if default_compiler == "unix":
            default_compiler = "gcc"
        self.compilertools_store_compiler = default_compiler != compiler.name
        self.compilertools_extra_ouputs = []

    if self.compilertools_store_compiler:
        from os.path import join

        self.compilertools_extra_ouputs.append(
            join(*self.get_ext_fullname(ext.name).split(".")) + ".compilertools"
        )

    config_options = ConfigBuild.option
    option_list = [option for option in config_options if config_options[option]]

    from compilertools._src_files import _use_api_pragma

    api_list = []
    config_api = ConfigBuild.api
    for api in config_api:
        if _use_api_pragma(ext.sources, compiler, api, **config_api[api]):
            api_list.append(api)

    args = get_build_compile_args(
        compiler,
        self.plat_name,
        ext_suffix="",
        use_api=api_list,
        use_option=option_list,
    )

    extra_compile_args = ext.extra_compile_args or []

    ext.extra_link_args = get_build_link_args(
        compiler, use_api=api_list, use_option=option_list
    ) + (ext.extra_link_args or [])

    exts = []
    from copy import deepcopy

    for suffix in args:
        compile_args = args[suffix]

        ext.compilertools_updated = True
        if suffix:
            ext_copy = deepcopy(ext)
            ext_copy.compilertools_extended_suffix = suffix
            ext_copy.name = _String(ext.name)
            ext_copy.name.parent_extension = ext_copy
        else:
            ext_copy = ext

        ext_copy.extra_compile_args = compile_args + extra_compile_args

        if ext_copy not in self.extensions:
            self.extensions.append(ext_copy)
        exts.append(ext_copy)

    return exts


# Distutils "distutils.command.build_ext.build_ext" Monkey-Patches with wrapping


def _patch_build_extension(build_extension):
    """Decorates build_ext.build_extension for run it as many time as needed for newly
    updated extensions"""
    if build_extension.__module__.startswith("compilertools."):
        return build_extension

    @_wraps(build_extension)
    def patched(self, ext):
        """Patched build_extension"""
        if hasattr(ext, "compilertools_updated"):
            return build_extension(self, ext)

        for updated_ext in _update_extension(self, ext):
            build_extension(self, updated_ext)

    patched.__module__ = f"compilertools.{patched.__module__}"
    return patched


def _patch_get_ext_filename(get_ext_filename):
    """Decorates build_ext.get_ext_fullname for return the filename with our suffixes"""
    if get_ext_filename.__module__.startswith("compilertools."):
        return get_ext_filename

    @_wraps(get_ext_filename)
    def patched(self, ext_name):
        """Patched get_ext_filename"""
        try:
            extended = ext_name.parent_extension.compilertools_extended_suffix
        except AttributeError:
            extended = ""

        if extended:
            return get_ext_filename(
                self, f"{ext_name}{extended.replace('.', '#')}"
            ).replace("#", ".")

        return get_ext_filename(self, ext_name)

    patched.__module__ = f"compilertools.{patched.__module__}"
    return patched


def _patch_get_ext_fullname(get_ext_fullname):
    """Decorates build_ext.get_ext_fullname for _String type conservation"""
    if get_ext_fullname.__module__.startswith("compilertools."):
        return get_ext_fullname

    @_wraps(get_ext_fullname)
    def patched(self, ext_name):
        """Patched get_ext_fullname"""
        full_name = get_ext_fullname(self, ext_name)

        if isinstance(ext_name, _String) and not isinstance(full_name, _String):
            full_name = _String(full_name)
            full_name.parent_extension = ext_name.parent_extension

        return full_name

    patched.__module__ = f"compilertools.{patched.__module__}"
    return patched


def _patch_get_outputs(get_outputs):
    """Decorates build_ext.get_outputs for compiler memorization"""
    if get_outputs.__module__.startswith("compilertools."):
        return get_outputs

    @_wraps(get_outputs)
    def patched(self):
        """Patched get_outputs"""
        outputs = get_outputs(self)

        if (
            hasattr(self, "compilertools_store_compiler")
            and self.compilertools_store_compiler
        ):
            extra_outputs = self.compilertools_extra_ouputs
            if not self.inplace:
                from os.path import join

                extra_outputs = [join(self.build_lib, path) for path in extra_outputs]

            for path in extra_outputs:
                with open(path, "wt") as file:
                    file.write(self.compilertools_compiler_name)

            outputs.extend(extra_outputs)
        return outputs

    patched.__module__ = f"compilertools.{patched.__module__}"
    return patched


def _patch___new__(__new__):
    """Patches "build_ext.__new__" for helping patching subclasses.

    This is needed when subclass totally override methods without calling parent's
    methods inside them.

    (This is the case in "numpy.distutils")."""

    def patched(cls, _):
        """Patched __new__"""
        cls.build_extension = _patch_build_extension(cls.build_extension)
        cls.get_ext_filename = _patch_get_ext_filename(cls.get_ext_filename)
        cls.get_ext_fullname = _patch_get_ext_fullname(cls.get_ext_fullname)
        cls.get_outputs = _patch_get_outputs(cls.get_outputs)

        return __new__(cls)

    return patched


# Applies monkey-patches to distutils
_build_ext.build_extension = _patch_build_extension(_build_ext.build_extension)
_build_ext.get_ext_filename = _patch_get_ext_filename(_build_ext.get_ext_filename)
_build_ext.get_ext_fullname = _patch_get_ext_fullname(_build_ext.get_ext_fullname)
_build_ext.get_outputs = _patch_get_outputs(_build_ext.get_outputs)
_build_ext.__new__ = _patch___new__(_build_ext.__new__)
