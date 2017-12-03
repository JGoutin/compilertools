# -*- coding: utf-8 -*-
"""Tests for x86 CPU"""

def tests_processor_nocpu():
    """Tests Processor methods that don't need a real x86 CPU"""
    from compilertools.processors.x86 import Processor
    processor = Processor()

    # Test properties
    assert processor.cpuid_highest_extended_function == 0
    processor['cpuid_max_extended'] = 0x80000000
    assert processor.cpuid_highest_extended_function == 0x80000000

    assert processor.system_support_avx is False
    processor['os_supports_avx'] = True
    assert processor.system_support_avx is True

    # Tests _uint_to_str
    # TODO: test

    # Initialise dummy CPUID
    registers = {
        0: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        1: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        7: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        0x80000000: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        0x80000001: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        0x80000002: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        0x80000003: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        0x80000004: {'eax': 0,'ebx': 0, 'ecx': 0, 'edx': 0},
        }

    def cpuid(avx):
        """Dummy CPUID function"""
        return registers[avx]

    processor.cpuid = cpuid

    # Test _cpuid_vendor_id (With dummy CPUID)
    # TODO: test

    # Test _cpuid_brand (With dummy CPUID)
    # TODO: test

    # Test _cpuid_feature_flags (With dummy CPUID)
    # TODO: test


def tests_processor():
    """Tests Processor methods that need a real x86 CPU"""
    # Check architecture and skip if not compatible
    from compilertools.processors import get_arch

    if get_arch() != 'x86':
        from pytest import skip
        skip("Current processor is not x86")

    # Test CPUID
    # TODO: test

    # Test instanciation
    from compilertools.processors.x86 import Processor
    processor = Processor(current_machine=True)

    assert processor.features
