"""Tests for x86-64 CPU."""


def tests_processor():
    """
    Tests Processor.

    Inherit from X86 CPU, tests for 64bits specifics functions only
    """
    # Check architecture and skip if not compatible
    from compilertools.processors import get_arch

    if get_arch() != "x86_64":
        from pytest import skip

        skip("Current processor is not x86-64")

    # Test instantiation
    from compilertools.processors.x86_64 import Processor

    processor = Processor(current_machine=True)
    assert processor.features
