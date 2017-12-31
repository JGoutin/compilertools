# -*- coding: utf-8 -*-
"""Test for core functionalities"""

def tests_version():
    """Test __version__ presence and format"""
    from compilertools import __version__
    from distutils.version import StrictVersion
    assert StrictVersion(__version__)


def tests_get_compile_args():
    """Test get_compile_args"""
    from collections import OrderedDict
    from compilertools._core import get_compile_args
    from compilertools.compilers import CompilerBase

    # Create a compiler
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

    compiler = Compiler()

    # Full args list
    excepted = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('inst2-arch2', ['--generic', '--inst2', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])
    assert get_compile_args(compiler, arch='arch1') == excepted

    # Current machine only args list
    excepted = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst2-arch1', ['--generic', '--inst2', '--arch1']),
        ('arch1', ['--generic', '--arch1'])])
    assert get_compile_args(compiler, arch='arch1', current_machine=True) == excepted

    # Current compiler only args list
    excepted = OrderedDict([
        ('inst1-arch1', ['--generic', '--inst1', '--arch1']),
        ('inst1-arch2', ['--generic', '--inst1', '--arch2']),
        ('arch1', ['--generic', '--arch1']),
        ('arch2', ['--generic', '--arch2'])])
    assert get_compile_args(Compiler(current_compiler=True), arch='arch1') == excepted


def tests_suffixe_from_args():
    """Test suffixe_from_args"""
    from collections import OrderedDict
    from compilertools._core import suffixe_from_args

    args = OrderedDict([('suffixe1', ['-arg1', '-arg2']),
                        ('suffixe2', ['-arg1', '-arg3']),
                        ('', ['-arg1'])])

    # Default
    assert suffixe_from_args(args) == [
        '.suffixe1', '.suffixe2']

    # With extension
    assert suffixe_from_args(args, '.pyd') == [
        '.suffixe1.pyd', '.suffixe2.pyd']

    # With empty suffixes
    assert suffixe_from_args(args, return_empty_suffixes=True) == [
        '.suffixe1', '.suffixe2', '']

    # With extension and emtpy suffixes
    assert suffixe_from_args(args, '.pyd', True) == [
        '.suffixe1.pyd', '.suffixe2.pyd', '.pyd']
