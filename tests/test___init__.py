"""Test module import."""


def tests_get_processor():
    """Test function redirection."""
    import compilertools
    from compilertools.processors import get_processor as _get_processor

    assert compilertools.get_processor() == _get_processor(
        arch=None, current_machine=True
    )


def tests_get_compiler():
    """Test function redirection."""
    import compilertools
    from compilertools.compilers import get_compiler as _get_compiler

    assert compilertools.get_compiler() == _get_compiler(current_compiler=True)
