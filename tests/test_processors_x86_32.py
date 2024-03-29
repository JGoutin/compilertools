"""Tests for x86-32 CPU."""


def tests_processor_nocpu():
    """Tests Processor methods that don't need a real x86_32 CPU."""
    from compilertools.processors.x86_32 import Processor
    from compilertools.processors import x86_32

    # Initialise dummy CPUID
    string = "Test"
    encoded = 0x74736554
    flags = 0b10000000000000000000000000000001

    registers = {
        0: {"ebx": encoded, "ecx": encoded, "edx": encoded},
        1: {"ecx": flags, "edx": flags},
        7: {"ebx": flags, "ecx": flags, "edx": flags},
        0x80000000: {"eax": flags, "ebx": flags, "ecx": flags, "edx": flags},
        0x80000001: {"eax": flags, "ebx": flags, "ecx": flags, "edx": flags},
        0x80000002: {"eax": encoded, "ebx": encoded, "ecx": encoded, "edx": encoded},
        0x80000003: {"eax": encoded, "ebx": encoded, "ecx": encoded, "edx": encoded},
        0x80000004: {"eax": encoded, "ebx": encoded, "ecx": encoded, "edx": encoded},
    }

    class Cpuid(x86_32.Cpuid):
        """Mock CPUID function."""

        def __init__(self, eax=0, ecx=None):
            self._eax = eax
            self._ecx = ecx

        @property
        def eax(self):
            """EAX."""
            return registers[self._eax]["eax"]

        @property
        def ebx(self):
            """EBX."""
            return registers[self._eax]["ebx"]

        @property
        def ecx(self):
            """ECX."""
            return registers[self._eax]["ecx"]

        @property
        def edx(self):
            """EDX."""
            return registers[self._eax]["edx"]

    x86_cpuid = x86_32.Cpuid
    x86_32.Cpuid = Cpuid

    try:
        # Tests registers_to_str
        assert x86_32.Cpuid.registers_to_str(encoded, encoded, encoded) == string * 3

        # Test default values
        processor = Processor()
        assert processor.current_machine is False
        assert processor.vendor == ""
        assert processor.cpuid_highest_extended_function == 0
        assert processor.brand == ""
        assert processor.os_supports_xsave is False
        assert processor.features == []

        # Initialize processor as current one
        processor = Processor(current_machine=True)
        assert processor.current_machine is True

        # Test cpuid_highest_extended_function
        assert processor.cpuid_highest_extended_function == flags

        # Test vendor (With dummy CPUID)
        assert processor.vendor == string * 3

        # Test no brand (With dummy CPUID)
        processor["cpuid_highest_extended_function"] = 0x80000000
        assert processor.brand == ""

        # Test brand (With dummy CPUID)
        processor["cpuid_highest_extended_function"] = 0x80000004
        del processor["brand"]
        assert processor.brand == string * 12

        # Test limited features (With dummy CPUID)
        processor["cpuid_highest_extended_function"] = 0x80000000
        assert processor.features == {
            "PREFETCHWT1",
            "PBE",
            "FPU",
            "HYPERVISOR",
            "FSGSBASE",
            "AVX512VL",
            "SSE3",
        }

        # Test full features (With dummy CPUID)
        processor["cpuid_highest_extended_function"] = 0x80000001
        del processor["features"]
        assert processor.features == {
            "3DNOW",
            "LAHF_LM",
            "AVX512VL",
            "FPU",
            "FSGSBASE",
            "HYPERVISOR",
            "PBE",
            "PREFETCHWT1",
            "SSE3",
        }

        # Test os_support_avx
        assert processor.os_supports_xsave is False
        del processor["os_supports_xsave"]
        processor["features"].update(("XSAVE", "OSXSAVE"))
        assert processor.os_supports_xsave is True

    finally:
        x86_32.Cpuid = x86_cpuid


def tests_cpuid_nocpu():
    """Tests cpuid without x86 CPU."""
    from pytest import raises

    # Initialize dummy testing environment
    import platform
    import ctypes

    platform_system = platform.system
    ctypes_cdll = ctypes.cdll
    try:
        ctypes_windll = ctypes.windll
    except AttributeError:
        ctypes_windll = None
    ctypes_cfunctype = ctypes.CFUNCTYPE
    ctypes_memmove = ctypes.memmove
    ctypes_c_void_p = ctypes.c_void_p

    try:
        system = "Unix"
        mem_address = 1
        mprotect_success = 0
        func_result = {}

        def dummy_system():
            """Mock platform.system."""
            return system

        def dummy_generic(*_, **__):
            """Mock generic method."""

        def dummy_memmove(address, bytecode, size):
            """Mock ctypes.memmove. Store bytecode to execute."""
            func_result["address"] = address
            func_result["bytecode"] = bytecode
            func_result["size"] = size

        class DummyValloc:
            """Mock valloc."""

            def __new__(cls, *args, **kwargs):
                """Mock new."""
                return mem_address

        class DummyMprotect:
            """Mock mprotect."""

            def __call__(self, *args, **kwargs):
                """Mock call."""
                return mprotect_success

        class DummyCFuncType:
            """Mock ctypes.CFUNCTYPE."""

            def __init__(self, *args, **kwargs):
                """Mock init."""

            def __call__(self, *args, **kwargs):
                """Mock call."""

                def func(*_, **__):
                    """Return executed bytecode."""
                    return func_result

                return func

        class DummyCDll:
            """Mock ctypes.cdll."""

            class LoadLibrary:
                """Mock ctypes.cdll.LoadLibrary."""

                def __init__(self, *args, **kwargs):
                    """Mock init."""

                valloc = DummyValloc
                mprotect = DummyMprotect()
                free = dummy_generic

        class DummyWinDll:
            """Mock ctypes.windll."""

            class kernel32:
                """Mock ctypes.windll.kernel32."""

                VirtualAlloc = DummyValloc
                VirtualFree = dummy_generic

        platform.system = dummy_system
        ctypes.memmove = dummy_memmove
        ctypes.c_void_p = dummy_generic
        ctypes.CFUNCTYPE = DummyCFuncType
        ctypes.cdll = DummyCDll
        ctypes.windll = DummyWinDll

        from compilertools.processors.x86_32 import Cpuid

        for system in ("Unix", "Windows"):
            # Check assembly bytecode
            cpuid = Cpuid()
            assert cpuid.eax["bytecode"] == (
                b"\x31\xc0"  # XOR eax, eax
                b"\x31\xc9"  # XOR ecx, ecx
                b"\x0f\xa2"  # CPUID
                b"\xc3"
            )  # RET
            assert cpuid.ebx["bytecode"] == (
                b"\x31\xc0"  # XOR eax, eax
                b"\x31\xc9"  # XOR ecx, ecx
                b"\x0f\xa2"  # CPUID
                b"\x89\xd8"  # MOV eax, ebx
                b"\xc3"
            )  # RET
            assert cpuid.ecx["bytecode"] == (
                b"\x31\xc0"  # XOR eax, eax
                b"\x31\xc9"  # XOR ecx, ecx
                b"\x0f\xa2"  # CPUID
                b"\x89\xc8"  # MOV eax, ecx
                b"\xc3"
            )  # RET
            assert cpuid.edx["bytecode"] == (
                b"\x31\xc0"  # XOR eax, eax
                b"\x31\xc9"  # XOR ecx, ecx
                b"\x0f\xa2"  # CPUID
                b"\x89\xd0"  # MOV eax, edx
                b"\xc3"
            )  # RET

            assert Cpuid(7, 5).eax["bytecode"] == (
                b"\xb8\x07\x00\x00\x00"  # MOV eax, 0x00000007
                b"\xb9\x05\x00\x00\x00"  # MOV ecx, 0x00000005
                b"\x0f\xa2"  # CPUID
                b"\xc3"
            )  # RET

            # Test failed to allocate memory
            mem_address = 0
            with raises(RuntimeError):
                Cpuid().eax
            mem_address = 1

        # Test failed to mprotect
        system = "Unix"
        mprotect_success = 1
        with raises(RuntimeError):
            Cpuid().eax

    finally:
        platform.system = platform_system
        ctypes.cdll = ctypes_cdll
        if ctypes_windll is not None:
            ctypes.windll = ctypes_windll
        else:
            del ctypes.windll
        ctypes.CFUNCTYPE = ctypes_cfunctype
        ctypes.memmove = ctypes_memmove
        ctypes.c_void_p = ctypes_c_void_p


def tests_cpuid():
    """Test cpuid with a real x86 CPU."""
    from compilertools.processors import get_arch

    if get_arch().split("_")[0] != "x86":
        from pytest import skip

        skip("Current processor is not x86")

    try:
        from x86cpu import cpuid as cpuid_ref
    except ImportError:
        from pytest import skip

        skip("x86cpu package not installed")
    from compilertools.processors.x86_32 import Cpuid

    for eax, ecx in (
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (7, 0),
        (0x80000000, 0),
        (0x80000001, 0),
        (0x80000002, 0),
        (0x80000003, 0),
        (0x80000004, 0),
    ):
        ref = cpuid_ref(eax, ecx)
        cpuid = Cpuid(eax, ecx)
        assert cpuid.eax == ref["eax"]
        assert cpuid.ecx == ref["ecx"]
        assert cpuid.ebx == ref["ebx"]
        assert cpuid.edx == ref["edx"]


def tests_processor():
    """Tests Processor methods that need a real x86 CPU."""
    # Check architecture and skip if not compatible
    from compilertools.processors import get_arch

    if get_arch() != "x86_32":
        from pytest import skip

        skip("Current processor is not x86_32")

    # Test instantiation
    from compilertools.processors.x86_32 import Processor

    processor = Processor(current_machine=True)
    assert processor.features
