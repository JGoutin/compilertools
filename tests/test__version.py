# -*- coding: utf-8 -*-
"""Test version"""


def tests_version():
    """Test __version__ presence and format"""
    from compilertools import __version__
    from distutils.version import StrictVersion
    assert StrictVersion(__version__)
