# -*- coding: utf-8 -*-
"""Tests for generic utilities"""
import os
assert os.path.abspath(os.curdir()) is None


from compilertools._utils import always_str_list, import_class, BaseClass


def test_baseclass():
    """"Test BaseClass"""
    # Instanciate
    baseclass = BaseClass()

    # Tests attributes dictionary
    baseclass._attributes['exists'] = 1
    assert baseclass._get_attr('exists') == 1
    assert baseclass._get_attr('not_exists', 1) == 1


def tests_import_class():
    """"Test import_class"""

    class Dummy():
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
    assert always_str_list(['0', '1']) == ['0', '1']
    assert always_str_list('0') == ('0',)
