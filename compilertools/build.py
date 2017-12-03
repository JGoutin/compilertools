# -*- coding: utf-8 -*-
"""Building functions"""

from functools import wraps
from copy import deepcopy

try:
    # Import Setuptools if available for enabling its distutils patches
    import setuptools
except ImportError:
    pass

from distutils.sysconfig import get_config_var
from distutils.command.build_ext import build_ext

from compilertools._config_build import CONFIG_BUILD
from compilertools._core import (
    suffixe_from_args, get_compile_args, get_compiler)
from compilertools._src_files import _use_api_pragma


__all__ = ['get_build_compile_args', 'get_build_link_args', 'CONFIG_BUILD']


def get_build_compile_args(compiler=None, arch=None, current_machine=None,
                           ext_suffix=None, use_option=None, use_api=None):
    """Get compiler args for build as a dict of file suffixes as key and
    args string as values.

    compiler: compiler name or instance. If None, use distutils default value
    arch: target architecture name.
    current_machine: return only one suffixe/args pair optimized for current
        machine only. If None, use CONFIG_BUILD value.
    ext_suffix: extensions to use after suffix.
    use_option: List of options to use (fast_fpmath, ...).
    use_api: List of API to use (openmp, ...).
        If None, don't enable API.
    """
    # Default values
    if ext_suffix is None:
        ext_suffix = get_config_var('EXT_SUFFIX')
    if current_machine is None:
        current_machine = CONFIG_BUILD.get('current_machine', False)

    # Compiler and base arguments
    build_args = {}
    compiler = get_compiler(compiler)

    # Optimized args for current machine
    if current_machine:
        build_args[ext_suffix] = [compiler.compile_args_current_machine()]

    # Args for multiple machines
    else:
        args = get_compile_args(compiler, arch, current_compiler=True)
        suffixes = suffixe_from_args(args, ext_suffix, True)
        for arg, suffix in zip(args.values(), suffixes):
            build_args[suffix] = arg

    # Extend args with special options
    arg_ext = []

    if use_api:
        # Add API args
        _add_args(compiler, build_args, 'api', 'compile', use_api)

    if use_option:
        # Add options args
        _add_args(compiler, build_args, 'option', 'compile', use_option)

    if arg_ext:
        for suffix in build_args:
            build_args[suffix].extend(arg_ext)

    return build_args


def get_build_link_args(compiler=None, use_api=None, use_option=None):
    """Get linker arg for build as a list of args string.

    compiler: compiler name or instance.
        If None, use distutils default value
    use_api: List of API to use (openmp, ...).
        If None, don't enable API.
    use_option: List of options to use (fast_fpmath, ...).
    """
    # Compiler and base arguments
    compiler = get_compiler(compiler)

    # Extend args with special options
    build_args = []

    if use_api:
        # Add API args
        _add_args(compiler, build_args, 'api', 'link', use_api)

    if use_option:
        # Add options args
        _add_args(compiler, build_args, 'option', 'link', use_option)

    return build_args


def _add_args(compiler, arg_list, arg_cat, arg_type, args_names):
    """Update arguments list with API specific arguments

    arg_list: list to update.
    arg_cat: 'api' or 'option'
    arg_type: 'link' or 'compile'.
    args_names: list of args names to use."""
    for name in args_names:
        arg = compiler.get(arg_cat, {}).get(arg_type, {}).get(name)
        if arg:
            arg_list.append(arg)


def _update_extension(self, ext):
    """Update build_ext extensions for add new args and suffixes based on the
    current extension.

    self: build_ext instance
    ext: Extension instance from build_ext.extensions"""
    if CONFIG_BUILD.get('disabled', False):
        return [ext]

    compiler = get_compiler(self.compiler.compiler_type)

    # Options list
    config_options = CONFIG_BUILD.get('option', {})
    option_list = [option for option in config_options
                   if config_options[option]]

    # API detection
    api_list = []
    for api in CONFIG_BUILD.get('api', {}):
        if _use_api_pragma(ext.sources, compiler, api, **CONFIG_BUILD['api'][api]):
            api_list.append(api)

    # Optimized arguments
    args = get_build_compile_args(
        compiler, self.plat_name, ext_suffix='',
        use_api=api_list, use_option=option_list)

    # Get extension extra compile arguments
    extra_compile_args = ext.extra_compile_args or []

    # Update link arguments
    ext.extra_link_args = (
        get_build_link_args(compiler,use_api=api_list, use_option=option_list)
        + (ext.extra_link_args or []))

    # Update Extensions and build
    exts = []
    for suffix in args:
        # Retrieve argument and suffix
        compile_args = args[suffix]

        # Create an Extension copy
        ext._compilertools_updated = True
        if suffix:
            ext_copy = deepcopy(ext)
            ext_copy._compilertools_extended_suffix = '.' + suffix
            # String deepcopy, for extension identification based only on this
            # poor info in "_patch_get_ext_filename"
            ext_copy.name = (ext.name + ' ')[:-1]
        else:
            ext_copy = ext

        # Update args. Add Extensions arguments at end for give to them
        # priority over optimized args on some compilers
        ext_copy.extra_compile_args = compile_args + extra_compile_args

        # Add extension to extensions list
        if ext_copy not in self.extensions:
            self.extensions.append(ext_copy)
        exts.append(ext_copy)

    return exts


# Distutils "distutils.command.build_ext.build_ext" Monkey-Patches
# with wrapping

def _patch_build_extension(build_extension):
    """Patch build_ext.build_extension for run it as many time as needed for
    newly updated extensions"""
    @wraps(build_extension)
    def patched(self, ext):
        # Already updated, only need to build
        if hasattr(ext, '_compilertools_updated'):
            return build_extension(self, ext)

        # Not updated, update and build
        for updated_ext in _update_extension(self, ext):
            build_extension(self, updated_ext)

    return patched


def _patch_get_ext_filename(get_ext_filename):
    """Patch build_ext.get_ext_filename for return the filename with our
    suffixes"""
    @wraps(get_ext_filename)
    def patched(self, ext_name):
        # Find extension linked to name, and eventually extended suffix
        extended = ''
        for ext in self.extensions:
            # This function don't give link to Extension, we only have the
            # name. For find extensions, we need to check if the name is the
            # the one from the extension. But, for this we need to first be
            # sure each name have a different ID
            # (see _update_extension "String Deepcopy")
            if ext_name is ext.name:
                if hasattr(ext, '_compilertools_extended_suffix'):
                    extended = ext._compilertools_extended_suffix.replace(
                        '.', '#')
                    ext_name = ext_name + extended
                break

        # Use classic function to find filename
        ext_filename = get_ext_filename(self, ext_name)

        # Clean up name and return
        if extended:
            ext_filename = ext_filename.replace('#', '.')
        return ext_filename

    return patched


# Apply monkey-patches to distutils
build_ext.build_extension = _patch_build_extension(
    build_ext.build_extension)
build_ext.get_ext_filename = _patch_get_ext_filename(
    build_ext.get_ext_filename)
