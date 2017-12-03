# -*- coding: utf-8 -*-
"""Tests for generic utilities"""


def test_baseclass():
    """"Test BaseClass"""
    from compilertools._utils import BaseClass

    # Instanciate
    baseclass = BaseClass()

    # Tests items access
    baseclass['exists'] = 1
    assert len(baseclass) == 1
    assert baseclass['exists'] == 1

    for key in baseclass:
        assert baseclass[key] == baseclass._items[key]

    del baseclass['exists']
    assert baseclass.get('exists') is None


def tests_import_class():
    """"Test import_class"""
    from compilertools._utils import import_class

    class Dummy():
        """Dummy class"""
        pass

    class_exists = import_class(
        'compilers', '_core', 'CompilerBase', Dummy)
    module_not_exists = import_class(
        'not_exists', '_core', 'CompilerBase', Dummy)
    class_not_exists = import_class(
        'compilers', '_core', 'Not_Exists', Dummy)

    # Return excepted class
    from compilertools.compilers._core import CompilerBase
    assert class_exists is CompilerBase

    # Or return default class if not found
    assert module_not_exists is Dummy
    assert class_not_exists is Dummy


def tests_always_str_list():
    """"Test always_str_list"""
    from compilertools._utils import always_str_list

    assert always_str_list(['0', '1']) == ['0', '1']
    assert always_str_list('0') == ('0',)
