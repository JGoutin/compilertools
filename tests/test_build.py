# -*- coding: utf-8 -*-
"""Tests for building"""

# Get methods references before compilertools.build path them
from distutils.command.build_ext import build_ext
BUILD_EXTENSION = build_ext.build_extension
GET_EXT_FILENAME = build_ext.get_ext_filename
GET_EXT_FULLNAME = build_ext.get_ext_fullname
BUILD_EXT_NEW = build_ext.__new__


def tests_get_build_compile_args():
    """Test get_build_compile_args"""
    from distutils.sysconfig import get_config_var
    from compilertools.compilers import CompilerBase
    from compilertools.build import get_build_compile_args
    from compilertools._config_build import CONFIG_BUILD

    # File extension
    ext_suffix = get_config_var('EXT_SUFFIX')

    # Initialize compiler
    class Compiler(CompilerBase):
        """Dummy Compiler"""

        def __init__(self, current_compiler=False):
            CompilerBase.__init__(self, current_compiler=current_compiler)
            self['api']['api_name'] = {
                'compile': '--api-compile', 'link': '--api-link'}
            self['option']['option_name'] = {
                'compile': '--option-compile', 'link': '--option-link'}

        def _compile_args_matrix(self, arch, cpu):
            """Return test args matrix"""
            return [[self.Arg(args='--arch1', suffix='arch1',
                              build_if=(arch == 'arch1')),
                     self.Arg(args='--arch2', suffix='arch2',
                              build_if=(arch == 'arch2')),
                     self.Arg(args='--arch2_opt', suffix='arch2_opt',
                              build_if=(arch == 'arch2'))]]

        def _compile_args_current_machine(self, arch, cpu):
            """return current machine args"""
            return '--native'

    compiler = Compiler(current_compiler=True)

    # Test default values
    assert get_build_compile_args(compiler, 'arch1') == {
        '.arch1%s' % ext_suffix: ['--arch1']}

    # Test current_machine
    assert get_build_compile_args(compiler, current_machine=True) == {
        ext_suffix: ['--native']}

    # Test current_machine from CONFIG_BUILD
    CONFIG_BUILD['current_machine'] = True
    assert get_build_compile_args(compiler) == {ext_suffix: ['--native']}
    CONFIG_BUILD['current_machine'] = False

    # Test ext_suffix
    assert get_build_compile_args(compiler, 'arch1', ext_suffix='.ext') == {
        '.arch1.ext': ['--arch1']}

    # Test use_api
    assert get_build_compile_args(compiler, 'arch1', use_api=['api_name']) == {
        '.arch1%s' % ext_suffix: ['--arch1', '--api-compile']}

    # Test use_option
    assert get_build_compile_args(
        compiler, 'arch1', use_option=['option_name']) == {
            '.arch1%s' % ext_suffix: ['--arch1', '--option-compile']}

    # Test filtering suffixes
    assert get_build_compile_args(compiler, 'arch2') == {
        '.arch2%s' % ext_suffix: ['--arch2'],
        '.arch2_opt%s' % ext_suffix: ['--arch2_opt']}
    CONFIG_BUILD['suffixes_excludes'].add('arch2_opt')
    assert get_build_compile_args(compiler, 'arch2') == {
        '.arch2%s' % ext_suffix: ['--arch2']}
    CONFIG_BUILD['suffixes_excludes'].remove('arch2_opt')
    CONFIG_BUILD['suffixes_includes'].add('arch2')
    assert get_build_compile_args(compiler, 'arch2') == {
        '.arch2%s' % ext_suffix: ['--arch2']}
    CONFIG_BUILD['suffixes_includes'].remove('arch2')

def tests_get_build_link_args():
    """Test get_build_link_args"""
    from compilertools.compilers import CompilerBase
    from compilertools.build import get_build_link_args

    class Compiler(CompilerBase):
        """Dummy Compiler"""
        def __init__(self):
            CompilerBase.__init__(self)
            self['api']['api_name'] = {
                'compile': '--api-compile', 'link': '--api-link'}
            self['option']['option_name'] = {
                'compile': '--option-compile', 'link': '--option-link'}

    compiler = Compiler()

    # Test default values
    assert get_build_link_args(compiler) == []

    # Test use_api
    assert get_build_link_args(
        compiler, use_api=['api_name']) == ['--api-link']

    # Test use_option
    assert get_build_link_args(
        compiler, use_option=['option_name']) == ['--option-link']


def tests_find_if_current_machine():
    """Test _find_if_current_machine"""
    from sys import argv
    import os
    from compilertools.build import _find_if_current_machine
    from compilertools._config_build import CONFIG_BUILD

    w_dir = os.getcwd()

    def dummy_getcwd():
        return w_dir

    os_getcwd = os.getcwd
    os.getcwd = dummy_getcwd

    # Set by configuration
    CONFIG_BUILD['current_machine'] = False
    assert _find_if_current_machine() is False
    CONFIG_BUILD['current_machine'] = True
    assert _find_if_current_machine() is True

    # Pip detection
    CONFIG_BUILD['current_machine'] = 'autodetect'
    w_dir = 'dir/not_current_machine'
    assert _find_if_current_machine() is False
    w_dir = 'dir/pip-‌​current_machine'
    assert _find_if_current_machine() is True

    # Cleaning
    os.getcwd = os_getcwd
    CONFIG_BUILD['current_machine'] = False


def tests_add_args():
    """Test _add_args"""
    from compilertools.compilers import CompilerBase
    from compilertools.build import _add_args

    class Compiler(CompilerBase):
        """Dummy Compiler"""
        def __init__(self):
            CompilerBase.__init__(self)
            self['api']['api_name'] = {'compile': '--api-compile'}

    compiler = Compiler()

    # API & category exists
    args = []
    _add_args(compiler, args, 'api', 'compile', ['api_name'])
    assert args == ['--api-compile']

    # API exists, category not exists
    args = []
    _add_args(compiler, args, 'api', 'link', ['api_name'])
    assert args == []

    # API not exists, category exists
    args = []
    _add_args(compiler, args, 'api', 'compile', ['not_exist'])
    assert args == []


def tests_update_extension():
    """Test _update_extension, _patch_build_extension.patched and
    _patch_get_ext_filename.patched"""
    from os.path import join
    from tempfile import TemporaryDirectory
    from distutils.sysconfig import get_config_var
    from compilertools.compilers import CompilerBase
    from compilertools._config_build import CONFIG_BUILD
    from compilertools.build import (
        _update_extension, _patch_build_extension, _patch_get_ext_filename,
        _patch_get_ext_fullname, _String)

    # File extension
    ext_suffix = get_config_var('EXT_SUFFIX')

    # Initialize compiler
    class Compiler(CompilerBase):
        """Dummy Compiler"""
        def __init__(self):
            CompilerBase.__init__(self)
            self['api']['api_name'] = {
                'compile': '--api-compile', 'link': '--api-link'}
            self['option']['option_name'] = {
                'compile': '--option-compile', 'link': '--option-link'}

        def _compile_args_matrix(self, arch, cpu):
            """Return test args matrix"""
            return [
                [self.Arg(args='--inst', suffix='inst'), self.Arg()],
                [self.Arg(args='--arch', suffix='arch'), self.Arg()]]

    compiler = Compiler()

    # Create dummy distutils classes
    class DummyCompiler():
        """Dummy distutils.ccompiler.CCompiler"""
        def __init__(self):
            # Replace compiler type str by Compiler instance
            # This force the use of the testing compiler
            self.compiler_type = compiler


    class DummyExtension:
        """Dummy distutils.extension.Extension"""
        def __init__(self):
            self.sources = []
            self.extra_compile_args = ['--extra_compile']
            self.extra_link_args = ['--extra_link']
            self.name = 'package.module'


    class DummyBuildExt:
        """Dummy distutils.command.build_ext.build_ext"""
        def __init__(self):
            self.package = None
            self.extensions = []
            self.compiler = DummyCompiler()
            self.plat_name = 'arch'

        # Use build_ext.get_ext_filename directly
        get_ext_filename = GET_EXT_FILENAME
        get_ext_fullname = GET_EXT_FULLNAME

        def build_extension(self, _):
            """Dummy build_extension"""

    # Patch dummy build_ext
    DummyBuildExt.build_extension = _patch_build_extension(
        DummyBuildExt.build_extension)
    DummyBuildExt.get_ext_filename = _patch_get_ext_filename(
        DummyBuildExt.get_ext_filename)
    DummyBuildExt.build_extension = _patch_build_extension(
        DummyBuildExt.build_extension)
    DummyBuildExt.get_ext_fullname = _patch_get_ext_fullname(
        DummyBuildExt.get_ext_fullname)

    # Test with patched build_extension
    dummy_build_ext = DummyBuildExt()
    dummy_ext = DummyExtension()
    dummy_build_ext.build_extension(dummy_ext)
    results = dummy_build_ext.extensions

    # Check result count
    excepted_args = compiler.compile_args()
    assert len(results) == len(excepted_args)

    # Check results details
    results.sort(key=lambda x: getattr(x, 'compilertools_extended_suffix')
                 if hasattr(x, 'compilertools_extended_suffix') else '')

    for index, result in enumerate(results):
        # Get suffix (not for the legacy extension)
        if index == 0:
            assert not hasattr(result, 'compilertools_extended_suffix')
            suffix = ''
        else:
            suffix = result.compilertools_extended_suffix

        # Check compile args
        assert (result.extra_compile_args ==
                excepted_args[suffix.strip('.')] + ['--extra_compile'])

        # Check link args
        assert result.extra_link_args == ['--extra_link']

        # Check get_ext_filename
        assert (dummy_build_ext.get_ext_filename(result.name) ==
                '%s%s%s' % (join('package', 'module'), suffix, ext_suffix))

    # Check no duplicates if runned a second time
    dummy_build_ext.build_extension(dummy_ext)
    results = dummy_build_ext.extensions
    assert len(results) == len(excepted_args)

    # Test after disabling optimization with CONFIG_BUILD
    CONFIG_BUILD['disabled'] = True
    dummy_ext = DummyExtension()
    assert _update_extension(DummyBuildExt(), dummy_ext) == [dummy_ext]

    # Clean up
    CONFIG_BUILD['disabled'] = False

    # Test options activation
    CONFIG_BUILD['option']['option_name'] = True
    results = _update_extension(DummyBuildExt(), DummyExtension())
    for result in results:
        # Check option arguments presence
        assert result.extra_compile_args[-2] == '--option-compile'
        assert result.extra_link_args[-2] == '--option-link'

    # Clean up
    del CONFIG_BUILD['option']['option_name']

    # Test API activation with file analysis
    CONFIG_BUILD['api']['api_name'] = {'c':'#pragma api '}
    with TemporaryDirectory() as tmp:
        # Create dummy source file
        source = join(tmp, 'source.c')
        with open(source, 'wt') as file:
            file.write('#pragma api operation')

        # Reset extension and add file as source
        dummy_ext = DummyExtension()
        dummy_ext.sources.append(source)

        # Compute results
        results = _update_extension(DummyBuildExt(), dummy_ext)

    for result in results:
        # Check API arguments presence
        assert result.extra_compile_args[-2] == '--api-compile'
        assert result.extra_link_args[-2] == '--api-link'

    # Clean up
    del CONFIG_BUILD['api']['api_name']

    # Check type conservation with "get_ext_fullname"
    assert isinstance(DummyBuildExt().get_ext_fullname(_String('module')), _String)
    dummy_build_ext = DummyBuildExt()
    dummy_build_ext.package = 'package'
    assert isinstance(dummy_build_ext.get_ext_fullname(_String('module')), _String)


def tests_string():
    """Test _String"""
    from compilertools.build import _String

    string = _String('a.b')

    # Test parent_extension
    parent_extension = 'parent_extension'
    assert string.parent_extension is None
    string.parent_extension = parent_extension
    assert string.parent_extension == parent_extension

    # Test split
    splited = string.split('.')
    assert isinstance(splited[0], _String)
    assert isinstance(splited[1], _String)
    assert splited[0].parent_extension == parent_extension
    assert splited[1].parent_extension == parent_extension


def tests_patch_build_extension():
    """Test _patch_build_extension"""
    from compilertools.build import _patch_build_extension

    # Check if patched
    assert BUILD_EXTENSION is not build_ext.build_extension

    # Check wrap
    assert (build_ext.build_extension.__module__ ==
            'compilertools.%s' % BUILD_EXTENSION.__module__)
    assert build_ext.build_extension.__name__ == BUILD_EXTENSION.__name__

    # Test re-patch
    previous = build_ext.build_extension
    build_ext.build_extension = (_patch_build_extension(build_ext.build_extension))
    assert build_ext.build_extension is previous


def tests_patch_get_ext_filename():
    """Test _patch_get_ext_filename"""
    from compilertools.build import _patch_get_ext_filename

    # Check if patched
    assert GET_EXT_FILENAME is not build_ext.get_ext_filename

    # Check wrap
    assert (build_ext.get_ext_filename.__module__ ==
            'compilertools.%s' % GET_EXT_FILENAME.__module__)
    assert build_ext.get_ext_filename.__name__ == GET_EXT_FILENAME.__name__

    # Test re-patch
    previous = build_ext.get_ext_filename
    build_ext.get_ext_filename = (_patch_get_ext_filename(build_ext.get_ext_filename))
    assert build_ext.get_ext_filename is previous


def tests_patch_get_ext_fullname():
    """Test _patch_get_ext_filename"""
    from compilertools.build import _patch_get_ext_fullname

    # Check if patched
    assert GET_EXT_FULLNAME is not build_ext.get_ext_fullname

    # Check wrap
    assert (build_ext.get_ext_fullname.__module__ ==
            'compilertools.%s' % GET_EXT_FULLNAME.__module__)
    assert build_ext.get_ext_fullname.__name__ == GET_EXT_FULLNAME.__name__

    # Test re-patch
    previous = build_ext.get_ext_fullname
    build_ext.get_ext_fullname = (_patch_get_ext_fullname(build_ext.get_ext_fullname))
    assert build_ext.get_ext_fullname is previous


def tests_patch___new__():
    """Test _patch___new__"""
    from compilertools.build import _patch___new__

    # Check if patched
    assert BUILD_EXT_NEW is not build_ext.__new__

    # Check build_ext instantiation
    from distutils.dist import Distribution
    build_ext(Distribution())
    assert GET_EXT_FULLNAME is not build_ext.get_ext_fullname
    assert GET_EXT_FILENAME is not build_ext.get_ext_filename
    assert BUILD_EXTENSION is not build_ext.build_extension
