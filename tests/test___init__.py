"""Test module import"""


def tests_init():
    """Test __version__ presence and format"""
    from pytest import raises
    from collections import namedtuple
    import sys

    sys_version_info = sys.version_info
    version_info = namedtuple(
        "Version_Info", ["major", "minor", "micro", "releaselevel", "serial"]
    )

    try:
        with raises(ImportError):
            sys.version_info = version_info(3, 3, 0, "final", 0)
            import compilertools  # noqa: F401

    finally:
        sys.version_info = sys_version_info


def tests_get_processor():
    """
    Test function redirection.
    """
    import compilertools
    from compilertools.processors import get_processor as _get_processor

    assert compilertools.get_processor() == _get_processor(
        arch=None, current_machine=True
    )


def tests_get_compiler():
    """
    Test function redirection.
    """
    import compilertools
    from compilertools.compilers import get_compiler as _get_compiler

    assert compilertools.get_compiler() == _get_compiler(current_compiler=True)
