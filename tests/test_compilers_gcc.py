# -*- coding: utf-8 -*-
"""Tests for GNU Compiler Collection"""


def tests_compiler_base():
    """Test Compiler"""
    import platform
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.gcc import Compiler

    # Initialize compiler
    compiler = Compiler()

    # Test _get_build_version
    # Monkey patch platform.python_compiler for
    # forcing its value
    version = ''

    def dummy_compiler():
        return version

    platform_python_compiler = platform.python_compiler
    platform.python_compiler = dummy_compiler

    # Check not existing version
    compiler._get_build_version()
    assert compiler.version == 0.0

    # Check existing version
    version = 'GCC 6.3.1 64bit'
    compiler._get_build_version()
    assert compiler.version == 6.3

    # Initialize system configurations
    arch_x86, cpu_x86 = _get_arch_and_cpu('x86_32')
    arch_amd64, cpu_amd64 = _get_arch_and_cpu('x86_64')

    # Test _compile_args_matrix
    assert compiler._compile_args_matrix(arch_x86, cpu_x86)
    assert compiler._compile_args_matrix(arch_amd64, cpu_amd64)

    # Test _compile_args_current_machine with x86
    args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
    assert args
    assert '-march=native' in args

    # Check retun a result also with amd64 
    assert compiler._compile_args_current_machine(arch_amd64, cpu_amd64)

    # Check -mfpmath with or without SSE
    cpu_x86['features'] = ['sse']
    args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
    assert '-mfpmath=sse' in args

    cpu_x86['features'] = []
    args = compiler._compile_args_current_machine(arch_x86, cpu_x86)
    assert '-mfpmath=sse' not in args

    # Clean up
    platform.python_compiler = platform_python_compiler
