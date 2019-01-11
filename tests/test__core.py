# -*- coding: utf-8 -*-
"""Test for core functionalities"""


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


def tests_suffix_from_args():
    """Test suffix_from_args"""
    from collections import OrderedDict
    from compilertools._core import suffix_from_args

    args = OrderedDict([('suffix1', ['-arg1', '-arg2']),
                        ('suffix2', ['-arg1', '-arg3']),
                        ('', ['-arg1'])])

    # Default
    assert suffix_from_args(args) == [
        '.suffix1', '.suffix2']

    # With extension
    assert suffix_from_args(args, '.pyd') == [
        '.suffix1.pyd', '.suffix2.pyd']

    # With empty suffixes
    assert suffix_from_args(args, return_empty_suffixes=True) == [
        '.suffix1', '.suffix2', '']

    # With extension and emtpy suffixes
    assert suffix_from_args(args, '.pyd', True) == [
        '.suffix1.pyd', '.suffix2.pyd', '.pyd']


def tests_log_exception(caplog):
    """Test log_exception"""
    from compilertools._core import log_exception
    import compilertools._config as _config

    config_logging = _config.CONFIG['logging']
    message = 'Compilertools: Exception when trying to enable optimization'

    # Tests
    try:
        # Logging enabled
        _config.CONFIG['logging'] = True

        try:
            raise RuntimeError
        except RuntimeError:
            log_exception()

        assert message in ''.join((
            rec.message for rec in caplog.records))

        # Logging disabled
        caplog.clear()
        _config.CONFIG['logging'] = False

        try:
            raise RuntimeError
        except RuntimeError:
            log_exception()

        assert not ''.join((rec.message for rec in caplog.records))

    # Restore configuration
    finally:
        _config.CONFIG['logging'] = config_logging
