# -*- coding: utf-8 -*-
"""Tests for generic utilities"""


def test_baseclass():
    """"Test BaseClass"""
    from compilertools._utils import BaseClass
    from pytest import raises

    # Instanciate
    baseclass = BaseClass()

    # Test default values
    baseclass._default['with_default'] = 1
    assert baseclass['with_default'] == 1
    baseclass['with_default'] = 2
    assert baseclass['with_default'] == 2
    del baseclass['with_default']
    assert baseclass['with_default'] == 1

    # Tests items access
    baseclass['exists'] = 1
    assert len(baseclass) == 1
    assert baseclass['exists'] == 1
    assert baseclass.exists == 1

    for key in baseclass:
        assert baseclass[key] == baseclass._items[key]
        assert getattr(baseclass, key) == baseclass._items[key]

    del baseclass['exists']
    assert baseclass.get('exists') is None

    # Test access exceptions
    with raises(AttributeError):
        baseclass.do_not_exist

    with raises(KeyError):
        baseclass['do_not_exist']


def tests_import_class():
    """"Test import_class"""
    from compilertools._utils import import_class

    # Create dummy class for use ase default
    class Dummy():
        """Dummy class"""

    # Return excepted class
    from compilertools.compilers._core import CompilerBase
    assert import_class(
        'compilers', '_core', 'CompilerBase', Dummy) is CompilerBase

    # Module not exist: return default
    assert import_class(
        'not_exists', '_core', 'CompilerBase', Dummy) is Dummy

    # Class not exists: return default
    assert import_class(
        'compilers', '_core', 'Not_Exists', Dummy) is Dummy


def tests_always_str_list():
    """"Test always_str_list"""
    from compilertools._utils import always_str_list

    # not a str
    assert always_str_list(['0', '1']) == ['0', '1']

    # str to tuple
    assert always_str_list('0') == ('0',)
