# -*- coding: utf-8 -*-
"""Tests for imports"""


def tests_update_ext_suffixes():
    """Test update_extensions_suffixes & ARCH_SUFFIXES"""
    from importlib.machinery import EXTENSION_SUFFIXES
    from compilertools._core import suffixe_from_args, get_compile_args
    from compilertools.imports import (
        ARCH_SUFFIXES, update_extensions_suffixes)

    # Test update
    update_extensions_suffixes('gcc')

    get_compile_args('gcc', current_machine=True)
    suffixes = suffixe_from_args(
        get_compile_args('gcc', current_machine=True),
        EXTENSION_SUFFIXES, 'gcc')

    for suffixe in suffixes:
        assert suffixe in ARCH_SUFFIXES

    # Test extensions presence
    result = []
    for ext in EXTENSION_SUFFIXES:
        result.append(False)
        for arch_ext in ARCH_SUFFIXES:
            if ext in arch_ext:
                result[-1] = True
                break

    assert all(result)


def tests_extension_file_finder():
    """Test _ExtensionFileFinder"""
    import sys
    from os.path import join
    from tempfile import TemporaryDirectory
    import importlib.machinery as machinery
    from compilertools.imports import _ExtensionFileFinder, ARCH_SUFFIXES

    # Check presence in sys.meta_path
    assert isinstance(sys.meta_path[0], _ExtensionFileFinder)

    # Test find_spec
    # Monkey patch importlib machinery for don't need to import unexisting
    # file.
    module_spec = machinery.ModuleSpec
    extension_file_loader = machinery.ExtensionFileLoader

    def dummy_spec(_, loader, *, origin=None):
        """Dummy ModuleSpec"""
        assert loader == origin
        return origin

    def dummy_fileloader(_, path):
        """Dummy ExtensionFileLoader"""
        return path

    machinery.ModuleSpec = dummy_spec
    machinery.ExtensionFileLoader = dummy_fileloader

    with TemporaryDirectory() as tmp:
        # Add temporary dir to sys.path
        sys.path.insert(0, tmp)

        # Create a dummy file
        name = "compilertools_dummy_file"
        ext = ARCH_SUFFIXES[0]
        path = join(tmp, ''.join([name, ext]))
        with open(path, 'wt') as file:
            file.write('')

        # Initialize file finder
        file_finder = _ExtensionFileFinder()

        # Existing file
        assert file_finder.find_spec(name, '') == path

        # non-existing file
        assert file_finder.find_spec(
            "compilertools_notexists_file", '') is None

    # Clean up
    sys.path.remove(tmp)
    machinery.ModuleSpec = module_spec
    machinery.ExtensionFileLoader = extension_file_loader
