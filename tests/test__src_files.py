# -*- coding: utf-8 -*-
"""Tests for source file parsing utilities"""


def tests_any_line_startwith():
    """"Test _any_line_startwith"""
    from tempfile import TemporaryDirectory
    from os.path import join
    from compilertools._src_files import _any_line_startwith

    with TemporaryDirectory() as tmp:
        # Create file
        files = [join(tmp, 'file.ext1'), join(tmp, 'file.ext2')]
        with open(files[0], 'wt') as file:
            file.write("\nazerty\n\tuiop\nqsdfgh\n")
        with open(files[1], 'wt') as file:
            file.write("\tWXCVBN\nUIOP\n   JKLM\n")

        # Test files content
        assert _any_line_startwith(files, {
            '.ext1': 'uiop'})
        assert _any_line_startwith(files, {
            '.ext2': 'uiop'})
        assert not _any_line_startwith(files, {
            '.ext3': 'uiop'})
        assert not _any_line_startwith(files, {
            '.ext1': 'wxcvbn', '.ext2': 'azerty'})
        assert _any_line_startwith(files, {
            '.ext1': ['uiop', 'qsd']})

        # str argument
        assert _any_line_startwith(files[0], {
            '.ext1': 'uiop'})

def tests_ignore_api():
    """Test _ignore_api"""
    from compilertools.compilers import CompilerBase
    from compilertools._src_files import _ignore_api

    assert _ignore_api(None, 'test') is False

    # API not supported
    compiler = CompilerBase()
    assert _ignore_api(compiler, 'test') is True

    # API supported (compiler)
    compiler['api']['test'] = {}
    assert _ignore_api(compiler, 'test') is False

def tests_startwith_exts():
    """Test _startwith_exts"""
    from compilertools._src_files import _startwith_exts

    # List arguments
    result = _startwith_exts(c=['c1', 'c2'], fortran=['fortran'])
    assert list(result['.c']) == ['c1', 'c2']
    assert list(result['.f']) == ['fortran']

    # str or None arguments
    result = _startwith_exts(c='c', fortran=None)
    assert result['.c'] == ('c',)
    assert '.f' not in result


def tests_use_api_pragma():
    """Test _use_api_pragma"""
    from tempfile import TemporaryDirectory
    from os.path import join
    from compilertools.compilers import CompilerBase
    from compilertools._src_files import _use_api_pragma

    with TemporaryDirectory() as tmp:
        # Create file
        files = [join(tmp, 'file.c'), join(tmp, 'file.ext2')]
        with open(files[0], 'wt') as file:
            file.write("\nazerty\n\tuiop\nqsdfgh\n")
        with open(files[1], 'wt') as file:
            file.write("\tytreza\n\tuiop\nqsdfgh\n")

        # API not supported by compiler
        compiler = CompilerBase()
        assert _use_api_pragma(files, compiler, 'test', c='azerty') is False

        # API supported and file using it
        compiler['api']['test'] = {}
        assert _use_api_pragma(files, compiler, 'test', c='azerty') is True

        # API suppoted but file not using it
        assert _use_api_pragma(files, compiler, 'test', c='ytreza') is False
