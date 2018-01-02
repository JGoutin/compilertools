# -*- coding: utf-8 -*-
"""Test module import"""


def tests_init():
    """Test __version__ presence and format"""
    from pytest import raises
    from collections import namedtuple
    import sys

    sys_version_info = sys.version_info
    version_info = namedtuple(
        'Version_Info',
        ['major', 'minor', 'micro', 'releaselevel', 'serial'])

    try:
        with raises(ImportError):
            sys.version_info = version_info(3, 3, 0, 'final', 0)
            import compilertools

    # Cleaning
    finally:
        sys.version_info = sys_version_info
