# -*- coding: utf-8 -*-
"""Tests for GNU Compiler Collection"""


def tests_compiler():
    """Test Compiler"""
    import platform
    import subprocess
    from io import StringIO
    from compilertools.compilers._core import _get_arch_and_cpu
    from compilertools.compilers.gcc import Compiler

    # Test python_build_version and version
    # Monkey patch platform.python_compiler and subprocess.Popen for
    # forcing version value
    version = ''
    version_cmd = ''
    raise_error = False

    class DummyPopen:
        """Always return version in stdout"""

        def __init__(self, *args, **kwargs):
            """Ignore arguments and raise exception on demand"""
            if raise_error:
                raise OSError

        @property
        def stdout(self):
            """Dummy stdout"""
            return StringIO(version_cmd)

    def dummy_compiler():
        """Force version"""
        return version

    platform_python_compiler = platform.python_compiler
    platform.python_compiler = dummy_compiler
    subprocess_popen = subprocess.Popen
    subprocess.Popen = DummyPopen

    # Initialize compiler
    compiler = Compiler(current_compiler=True)

    # Check not existing version
    assert compiler.python_build_version == 0.0
    assert compiler.version == 0.0

    # Check existing version
    version = 'GCC 6.3.1 64bit'
    version_cmd = 'gcc (GCC) 6.3.1\n...'
    del compiler['python_build_version']
    del compiler['version']
    assert compiler.python_build_version == 6.3
    assert compiler.version == 6.3

    # Not current compiler
    assert Compiler().version == 0.0

    # Test Error
    del compiler['version']
    raise_error = True
    assert compiler.version == 0.0

    # Initialize system configurations
    compiler['version'] = 6.3
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
    subprocess.Popen = subprocess_popen


def tests_compiler_gcc_command():
    """Test Compiler if CC/GCC command available"""
    from platform import system
    from subprocess import Popen, PIPE
    try:
        version_str = Popen(['gcc', '--version'])
    except OSError:
        from pytest import skip
        skip('GCC not available')

    version_str = Popen(
        ['gcc' if system() == 'Windows' else 'cc', '--version'],
        stdout=PIPE, universal_newlines=True).stdout.read()
    if (version_str.rstrip().split(maxsplit=1)[0].lower()
            not in ('gcc', 'cc')):
        from pytest import skip
        skip('"CC" is not GCC')

    from compilertools.compilers.gcc import Compiler
    assert Compiler(current_compiler=True).version != 0.0
