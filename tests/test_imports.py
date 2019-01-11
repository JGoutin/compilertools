# -*- coding: utf-8 -*-
"""Tests for imports"""


def tests_update_ext_suffixes():
    """Test update_extensions_suffixes & ARCH_SUFFIXES"""
    from collections import OrderedDict
    from importlib.machinery import EXTENSION_SUFFIXES
    import compilertools._core as core
    from compilertools._core import suffix_from_args
    from compilertools.imports import (
        ARCH_SUFFIXES, update_extensions_suffixes)

    # Create fake compiler and extensions on environments without ARCH_SUFFIXES
    if not ARCH_SUFFIXES:
        ARCH_SUFFIXES += ['.fake1', '.fake2']

        def get_compile_args(*_, **__):
            """Mocker function"""
            return OrderedDict([
                ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
                ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
                ('arch1', ['--generic', '--arch1']),
                ('arch2', ['--generic', '--arch2'])])

        core_get_compile_args = core.get_compile_args
        core.get_compile_args = get_compile_args

    else:
        get_compile_args = core.get_compile_args
        core_get_compile_args = None

    # Test
    try:
        # Test update
        update_extensions_suffixes('gcc')

        get_compile_args('gcc', current_machine=True)
        suffixes = suffix_from_args(
            get_compile_args('gcc', current_machine=True),
            EXTENSION_SUFFIXES)

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

        # Tests not crash on exception
        update_extensions_suffixes('fake_compiler')

    # Restore mocked objects
    finally:
        if core_get_compile_args:
            ARCH_SUFFIXES.clear()
            core.get_compile_args = core_get_compile_args


def tests_extension_file_finder():
    """Test _ExtensionFileFinder"""
    import sys
    from os.path import join
    from tempfile import TemporaryDirectory
    import importlib.machinery as machinery
    import compilertools.imports as imports
    from compilertools.imports import (
        _ExtensionFileFinder, ARCH_SUFFIXES, _PROCESSED_COMPILERS)

    # Create fake compiler and extensions on environments without ARCH_SUFFIXES
    if not ARCH_SUFFIXES:
        ARCH_SUFFIXES += ['.fake1', '.fake2']
        _PROCESSED_COMPILERS.add('fake_compiler')

        def update_extensions_suffixes(compiler):
            """Mocker function"""
            _PROCESSED_COMPILERS.add(compiler)

        imports_update_extensions_suffixes = imports.update_extensions_suffixes
        imports.update_extensions_suffixes = update_extensions_suffixes

    else:
        imports_update_extensions_suffixes = None

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

    try:
        for use_compiler_file in (False, True):
            with TemporaryDirectory() as tmp:
                # Add temporary dir to sys.path
                sys.path.insert(0, tmp)

                # Create a dummy file
                name = "compilertools_dummy_file"
                ext = ARCH_SUFFIXES[0]
                file_path = join(tmp, ''.join([name, ext]))
                with open(file_path, 'wt') as file:
                    file.write('')

                # Create a dummy compiler file
                if use_compiler_file:
                    compiler = _PROCESSED_COMPILERS.pop()
                    assert compiler not in _PROCESSED_COMPILERS
                    path_compiler = join(tmp, ''.join([name, '.compilertools']))
                    with open(path_compiler, 'wt') as file:
                        file.write(compiler)

                # Initialize file finder
                file_finder = _ExtensionFileFinder()

                # Existing file
                assert file_finder.find_spec(name, '') == file_path

                if use_compiler_file:
                    assert compiler in _PROCESSED_COMPILERS

                    # Checks called twice
                    assert file_finder.find_spec(name, '') == file_path

                # non-existing file
                assert file_finder.find_spec(
                    "compilertools_notexists_file", '') is None

                # Clean up
                sys.path.remove(tmp)

    # Clean up
    finally:
        machinery.ModuleSpec = module_spec
        machinery.ExtensionFileLoader = extension_file_loader

        if imports_update_extensions_suffixes:
            ARCH_SUFFIXES.clear()
            _PROCESSED_COMPILERS.discard('fake_compiler')
            imports.update_extensions_suffixes = \
                imports_update_extensions_suffixes
