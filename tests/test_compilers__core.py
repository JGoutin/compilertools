# -*- coding: utf-8 -*-
"""Tests for compilers core"""


def tests_get_compiler():
    """Test get_compiler"""
    from os import listdir
    from os.path import splitext, dirname
    from compilertools._config import CONFIG
    from compilertools.compilers import CompilerBase, _core
    from compilertools.compilers._core import get_compiler
    from distutils.ccompiler import get_default_compiler

    # Initialise compiler
    compiler = CompilerBase()

    # Return compiler in parameter
    assert get_compiler(compiler) is compiler

    # Return default compiler
    name = get_default_compiler()
    assert (get_compiler().__class__.__module__ ==
            'compilertools.compilers.%s' %
            CONFIG['compilers'].get(name, name))

    # Return compiler by name
    # with all file in "compilertools.compilers"
    for file in listdir(dirname(_core.__file__)):
        if file.startswith('_'):
            continue
        name = splitext(file)[0]
        assert (get_compiler(name).__class__.__module__ ==
                'compilertools.compilers.%s' % name)

    # Test aliases
    for name in CONFIG['compilers']:
        assert (get_compiler(name).__class__.__module__ ==
                'compilertools.compilers.%s' %
                CONFIG['compilers'][name])


def tests_get_arch_and_cpu():
    """Test _get_arch_and_cpu"""
    from os import listdir
    from os.path import splitext, dirname
    from compilertools.processors import _core
    from compilertools.processors._core import get_processor
    from compilertools.compilers._core import _get_arch_and_cpu

    for file in listdir(dirname(_core.__file__)):
        if file.startswith('_'):
            continue
        arch = splitext(file)[0]

        # Get arch and CPU from function
        result_arch, result_cpu = _get_arch_and_cpu(arch)

        # Check arch
        assert result_arch == arch

        # Check processor
        assert result_cpu == get_processor(arch)


def tests_compiler_base():
    """Test CompilerBase & _order_args_matrix"""
    from collections import OrderedDict
    from pytest import raises
    from compilertools.compilers import CompilerBase
    from compilertools.compilers._core import _order_args_matrix

    # Test name
    assert CompilerBase().name == '_core'

    # Create compilers
    class Compiler(CompilerBase):
        """Dummy Compiler"""

        def _compile_args_matrix(self, arch, cpu):
            """Return test args matrix"""
            return [
                [self.Arg(args=['--generic'])],
                [self.Arg(args='--inst1', suffix='inst1'),
                 self.Arg(args='--inst2', suffix='inst2',
                          # Not compatible with current compiler
                          build_if=False),
                 self.Arg()],

                # Compatible only with a specific arch
                [self.Arg(args='--arch1', suffix='arch1',
                          import_if=(arch == 'arch1')),
                 self.Arg(args='--arch2', suffix='arch2',
                          import_if=(arch == 'arch2'))]]

    compiler1 = Compiler()

    class Compiler2(CompilerBase):
        """Dummy Compiler"""

        def _compile_args_matrix(self, arch, cpu):
            """Return test args matrix"""
            return [
                [self.Arg(args=['--generic'])],
                [self.Arg(args='--inst1', suffix='inst1'),
                 self.Arg(args='--inst2', suffix='inst2',
                          # Not compatible with current compiler
                          build_if=False),
                 self.Arg()],
                [self.Arg(args='--arch1', suffix='arch1', import_if=True),
                 self.Arg(args='--arch2', suffix='arch2', import_if=False)]]

    compiler2 = Compiler2()

    # Excepted args results
    excepted = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('inst2-arch2', ['--generic', '--inst2', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])

    excepted_currentmachine = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('arch1', ['--generic', '--arch1'])])

    excepted_currentcompiler = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])

    # Test _compile_args_matrix: abstract method
    with raises(NotImplementedError):
        CompilerBase()._compile_args_matrix('arch1', None)

    # Test _order_args_matrix
    matrix = compiler1._compile_args_matrix('arch1', None)
    assert _order_args_matrix(matrix) == excepted
    assert _order_args_matrix(
        matrix, current_machine=True) == excepted_currentmachine
    assert _order_args_matrix(
        matrix, current_compiler=True) == excepted_currentcompiler

    # Test compile_args
    assert compiler1.compile_args(arch='arch1') == excepted
    assert compiler1.compile_args(
        arch='arch1', current_machine=True) == excepted_currentmachine
    assert Compiler(current_compiler=True).compile_args(
        arch='arch1') == excepted_currentcompiler

    # Test compile_args_current_machine
    assert (compiler2.compile_args_current_machine() ==
            excepted['inst1-arch1'])
    assert compiler1.compile_args_current_machine() == []

    # Test Properties
    assert compiler1.version == 0.0
    compiler1['version'] = 9.9
    assert compiler1.version == 9.9
