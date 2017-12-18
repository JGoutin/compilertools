# -*- coding: utf-8 -*-
"""Tests for x86 CPU"""

def tests_processor_nocpu():
    """Tests Processor methods that don't need a real x86 CPU"""
    from compilertools.processors.x86 import Processor
    from compilertools.processors import x86
    processor = Processor()

    # Test properties
    assert processor.cpuid_highest_extended_function == 0
    processor['cpuid_highest_extended_function'] = 0x80000000
    assert processor.cpuid_highest_extended_function == 0x80000000

    assert processor.os_supports_avx is False
    processor['os_supports_avx'] = True
    assert processor.os_supports_avx is True

    # Initialise dummy CPUID
    string = 'Test'
    encoded = 0x74736554
    flags = 0b10000000000000000000000000000001

    registers = {
        0: {'ebx': encoded, 'ecx': encoded, 'edx': encoded},
        1: {'ecx': flags, 'edx': flags},
        7: {'ebx': flags, 'ecx': flags, 'edx': flags},
        0x80000000: {'eax': flags, 'ebx': flags,
                     'ecx': flags, 'edx': flags},
        0x80000001: {'eax': flags, 'ebx': flags,
                     'ecx': flags, 'edx': flags},
        0x80000002: {'eax': encoded, 'ebx': encoded,
                     'ecx': encoded, 'edx': encoded},
        0x80000003: {'eax': encoded, 'ebx': encoded,
                     'ecx': encoded, 'edx': encoded},
        0x80000004: {'eax': encoded, 'ebx': encoded,
                     'ecx': encoded, 'edx': encoded},
        }

    class Cpuid():
        """Dummy CPUID function"""
        
        def __init__(self, eax, ecx=None):
            self._eax = eax
            self._ecx = ecx

        @property
        def eax(self):
            """EAX"""
            return registers[self._eax]['eax']

        @property
        def ebx(self):
            """EAX"""
            return registers[self._eax]['ebx']

        @property
        def ecx(self):
            """EAX"""
            return registers[self._eax]['ecx']

        @property
        def edx(self):
            """EAX"""
            return registers[self._eax]['edx']

    x86.Cpuid = Cpuid

    # Tests _uint_to_str
    assert Processor._uint_to_str(
        encoded, encoded, encoded) == string * 3

    # Test _cpuid_vendor_id (With dummy CPUID)
    processor._cpuid_vendor_id()
    assert processor.vendor == string * 3

    # Test no _cpuid_brand (With dummy CPUID)
    processor['cpuid_highest_extended_function'] = 0x80000000
    processor._cpuid_brand()
    assert processor.brand is ''

    # Test _cpuid_brand (With dummy CPUID)
    processor['cpuid_highest_extended_function'] = 0x80000004
    processor._cpuid_brand()
    assert processor.brand == string * 12

    # Test limited _cpuid_feature_flags (With dummy CPUID)
    processor['cpuid_highest_extended_function'] = 0x80000000
    processor._cpuid_feature_flags()
    assert processor.features == {
        'prefetchwt1', 'pbe', 'fpu', 'hv', 'fsgsbase', 'avx512vl', 'sse3'}

    # Test full _cpuid_feature_flags (With dummy CPUID)
    processor['cpuid_highest_extended_function'] = 0x80000001
    processor._cpuid_feature_flags()
    assert processor.features == {
        '3dnow!', 'ahf64', 'avx512vl', 'fpu', 'fsgsbase', 'hv', 'pbe',
        'prefetchwt1', 'sse3'}


def tests_processor():
    """Tests Processor methods that need a real x86 CPU"""
    # Check architecture and skip if not compatible
    from compilertools.processors import get_arch

    if get_arch() != 'x86':
        from pytest import skip
        skip("Current processor is not x86")

    # Test instanciation
    from compilertools.processors.x86 import Processor
    processor = Processor(current_machine=True)
    assert processor.features

 
def tests_cpuid():
    """Test cpuid"""
    try:
        from x86cpu import cpuid as cpuid_ref
    except ImportError:
        from pytest import skip
        skip("x86cpu package not installed")
    from compilertools.processors.x86 import Cpuid
    
    for eax, ecx in (
            (0, 0), (1, 0), (2, 0), (3, 0),
            (4, 0), (7, 0), (0x80000000, 0),
            (0x80000001, 0), (0x80000002, 0),
            (0x80000003, 0), (0x80000004, 0)):

        ref = cpuid_ref(eax, ecx)
        cpuid = Cpuid(eax, ecx)
        assert cpuid.eax == ref['eax']
        assert cpuid.ecx == ref['ecx']
        assert cpuid.ebx == ref['ebx']
        assert cpuid.edx == ref['edx']
