# -*- coding: utf-8 -*-
"""Tests for Microsoft Visual C++ Compiler"""


def tests_compiler():
    """Test Compiler"""
    import platform
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.msvc import Compiler

    # Test version
    # Monkey patch platform.python_compiler for
    # forcing its value
    version = ''

    def dummy_compiler():
        """platform.python_compiler"""
        return version

    platform_python_compiler = platform.python_compiler
    platform.python_compiler = dummy_compiler

    compiler = Compiler(current_compiler=True)

    # Check not existing version
    assert compiler.version == 0.0

    # Check existing version
    version = 'MSC v.1800 64 bit'
    del compiler['version']
    assert compiler.version == 12.0

    # Check 13.0 skipped
    version = 'MSC v.1900 64 bit'
    del compiler['version']
    assert compiler.version == 14.0

    # Not current compiler
    assert Compiler().version == 0.0

    # Clean up
    platform.python_compiler = platform_python_compiler

    # Test _compile_args_matrix
    arch, cpu = _get_arch_and_cpu('x86_32')
    assert compiler._compile_args_matrix(arch, cpu)
