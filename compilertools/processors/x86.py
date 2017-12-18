# -*- coding: utf-8 -*-
"""X86 Processors"""
# For more X86 CPUID informations : http://www.sandpile.org/x86/cpuid.htm

# TODO: implement more CPUID (Other feature flags, L2 caches, ...)

# TODO: 0x80000001, select value based on CPU name for bit that have 2
# possibles flags

# TODO: replace x86cpu with pure Python solution ? :
#       https://github.com/flababah/cpuid.py/blob/master/cpuid.py
#       https://github.com/workhorsy/py-cpuinfo/blob/master/cpuinfo/cpuinfo.py

from compilertools.processors import ProcessorBase as _ProcessorBase

__all__ = ['Processor']


class Processor(_ProcessorBase):
    """x86 CPU"""

    def __init__(self, current_machine=False):
        _ProcessorBase.__init__(self, current_machine)
        self._default['os_supports_avx'] = False
        self._default['cpuid_highest_extended_function'] = 0

        if current_machine:
            # CPUID functions
            self['cpuid_highest_extended_function'] = (
                Cpuid(0x80000000).eax)
            self._cpuid_vendor_id()
            self._cpuid_brand()
            self._cpuid_feature_flags()
            self['os_supports_avx'] = (
                'xsave' in self['features'] and 'osxsave' in self['features'])

    @staticmethod
    def _uint_to_str(*uints):
        """Convert unsigned integers from CPUID register to ASCII string

        uints: list of unsigned integers to concatenate and convert to string.
        """
        from struct import pack
        return pack('<%s' % ('I' * len(uints)),
                    *uints).decode('ASCII').strip('\x00 ')

    def _cpuid_vendor_id(self):
        """Update current CPU's manufacturer ID from CPUID"""
        reg = Cpuid(0)
        self['vendor'] = self._uint_to_str(reg.ebx, reg.edx, reg.ecx)

    def _cpuid_brand(self):
        """Update current CPU's brand from CPUID"""
        if self.cpuid_highest_extended_function < 0x80000004:
            return

        brand_list = []
        for avx in (0x80000002, 0x80000003, 0x80000004):
            reg = Cpuid(avx)
            brand_list += [reg.eax, reg.ebx, reg.ecx, reg.edx]
        self['brand'] = self._uint_to_str(*brand_list)

    def _cpuid_feature_flags(self):
        """Update current CPU's features flags from CPUID"""
        # feature bits description
        # feature_bits_desc: {avx_number: registers_dict}
        # registers_dict: {register_name: [feature_list]}
        # feature_list: bits ordered features list in register
        feature_bits_desc = {
            1: {
                'edx': (             # 1 EDX: Intel Standard features
                    'fpu',              # 00: Onboard x87 Floating-point Unit
                    'vme',              # 01: Virtual 8086 Mode Extensions
                    'de',               # 02: Debugging Extensions
                    'pse',              # 03: Page Size Extension
                    'tsc',              # 04: Time Stamp Counter
                    'msr',              # 05: Model-Specific Registers RDMSR/WRMSR
                    'pae',              # 06: Physical Address Extensions
                    'mce',              # 07: Machine Check Exception
                    'cx8',              # 08: Compare-and-exchange 8 byte
                    'apic',             # 09: Onboard Advanced Programmable Interrupt Controller
                    None,               # 10: ?
                    'sep',              # 11: SYSENTER and SYSEXIT
                    'mtrr',             # 12: Memory Type Range Registers
                    'pge',              # 13: Page Global Enable
                    'mca',              # 14: Machine Check Architecture
                    'cmov',             # 15: Conditional Move/Compare
                    'pat',              # 16: Page Attribute Table
                    'pse36',            # 17: 36-bit Page Size Extension
                    'psn',              # 18: Processor Serial Number
                    'clfl',             # 19: CLFLUSH
                    None,               # 20: ?
                    'dtes',             # 21: Debug Trace and EMON Store MSRs
                    'acpi',             # 22: Thermal Monitor & Software Controlled Clock Facilities
                    'mmx',              # 23: MMX
                    'fxsr',             # 24: FXSAVE/FXRESTOR
                    'sse',              # 25: Streaming SIMD Extensions
                    'sse2',             # 26: Streaming SIMD Extensions 2
                    'ss',               # 27: Self-Snoop
                    'htt',              # 28: Max APIC IDs reserved field is Valid
                    'tm1',              # 29: Thermal Monitor
                    'ia64',             # 30: IA64 processor emulating x86
                    'pbe'),             # 31: Pending Break Enable

                'ecx': (             # 1 ECX: Intel Standard features
                    'sse3',             # 00: Streaming SIMD Extensions 3
                    'pclmul',           # 01: Carryless Multiplication
                    'dtes64',           # 02: 64-bit Debug Store Area
                    'mon',              # 03: MONITOR and MWAIT
                    'dscpl',            # 04: CPL qualified debug store
                    'vmx',              # 05: Virtual Machine Extensions
                    'smx',              # 06: Safer Mode Extensions
                    'est',              # 07: Enhanced SpeedStep Technology
                    'tm2',              # 08: Thermal Monitor 2
                    'ssse3',            # 09: Supplemental Streaming SIMD Extensions 3
                    'cid',              # 10: L1 Context ID
                    'sdbg',             # 11: Silicon Debug interface
                    'fma3',             # 12: Fused Multiply–Add 3
                    'cx16',             # 13: CMPXCHG16B
                    'etprd',            # 14: xTPR Update Control
                    'pdcm',             # 15: Perf/Debug Capability MSR
                    None,               # 16: ?
                    'pcid',             # 17: Process Context Identifiers
                    'dca',              # 18: Direct Cache Access
                    'sse4.1',           # 19: Streaming SIMD Extensions 4.1
                    'sse4.2',           # 20: Streaming SIMD Extensions 4.2
                    'x2apic',           # 21: x2APIC support
                    'movbe',            # 22: MOVBE
                    'popcnt',           # 23: POPCNT
                    'tscd',             # 24: TSC deadline
                    'aes',              # 25: Advanced Encryption Standard
                    'xsave',            # 26: XSAVE, XRESTOR, XSETBV, XGETBV
                    'osxsave',          # 27: XSAVE enabled by OS
                    'avx',              # 28: Advanced Vector Extensions
                    'f16c',             # 29: 16-bit floating-point conversion
                    'rdrand',           # 30: RDRAND support
                    'hv')},             # 31: Hypervisor
            7: {
                'ebx': (             # 7 EBX: Intel Extended features
                    'fsgsbase',         # 00: Access to base of %fs and %gs
                    'tsc_adjust',       # 01: Time Stamp counter Adjustment
                    'sgx',              # 02: Software Guard Extensions
                    'bmi1',             # 03: Bit Manipulation Instruction Set 1
                    'hle',              # 04: Transactional Synchronization Extensions
                    'avx2',             # 05: Advanced Vector Extensions 2
                    'fpdp',             # 06: Floating Point Data Pointer
                    'smep',             # 07: Supervisor-Mode Execution Prevention
                    'bmi2',             # 08: Bit Manipulation Instruction Set 2
                    'erms',             # 09: Enhanced REP MOVSB/STOSB
                    'invpcid',          # 10: INVPCID
                    'rtm',              # 11: Transactional Synchronization Extensions
                    'pqm',              # 12: Platform Quality of Service Monitoring
                    'fpcsds',           # 13: Deprecate FPU CS and FPU DS
                    'mpx',              # 14: Memory Protection Extensions
                    'pqe',              # 15: Platform Quality of Service Enforcement
                    'avx512f',          # 16: AVX-512 Foundation
                    'avx512dq',         # 17: AVX-512 Doubleword and Quadword
                    'rdseed',           # 18: RDSEED
                    'adx',              # 19: Multi-Precision Add-Carry Instruction Extensions
                    'smap',             # 20: Supervisor Mode Access Prevention
                    'avx512ifma',       # 21: AVX-512 Integer Fused Multiply-Add
                    'pcommit',          # 22: PCOMMIT
                    'clflushopt',       # 23: CLFLUSHOPT
                    'clwb',             # 24: CLWB
                    'pt',               # 25: Intel Processor Trace
                    'avx512pf',         # 26: AVX-512 Prefetch
                    'avx512er',         # 27: AVX-512 Exponential and Reciprocal
                    'avx512cd',         # 28: AVX-512 Conflict Detection
                    'sha',              # 29: Secure Hash Algorithm extensions
                    'avx512bw',         # 30: AVX-512 Byte and Word
                    'avx512vl'),        # 31: AVX-512 Vector Length Extensions

                'ecx': (             # 7 ECX: Intel Extended features
                    'prefetchwt1',      # 00: PREFETCHWT1
                    'avx512vbmi',       # 01: AVX-512 Vector Bit Manipulation
                    'umip',             # 02: User-mode Instruction Prevention
                    'pku',              # 03: Memory Protection Keys for User-mode pages
                    'ospke',            # 04: PKU enabled by OS
                    None,               # 05: ?
                    None,               # 06: ?
                    'cet',              # 07: CR4.CET
                    None,               # 08: ?
                    None,               # 09: ?
                    None,               # 10: ?
                    None,               # 11: ?
                    None,               # 12: ?
                    None,               # 13: ?
                    'avx512vpopcntdq',  # 14: AVX-512 Vector Population Count D/Q
                    None,               # 15: ?
                    'va57',             # 16: CR4.VA57
                    None,               # 17: ?
                    None,               # 18: ?
                    None,               # 19: ?
                    None,               # 20: ?
                    None,               # 21: ?
                    'rdpid',            # 22: Read Processor ID
                    None,               # 23: ?
                    None,               # 24: ?
                    None,               # 25: ?
                    None,               # 26: ?
                    None,               # 27: ?
                    None,               # 28: ?
                    None,               # 29: ?
                    'sgx_lc',           # 30: SGX Launch Configuration
                    None),              # 31: ?

                'edx': (             # 7 EDX: Intel Extended features
                    None,               # 00: ?
                    None,               # 01: ?
                    'avx512qvnniw',     # 02: AVX-512 Neural Network
                    'avx512qfma',       # 03: AVX-512 Multiply Accumulation Single precision
                    None,               # 04: ?
                    None,               # 05: ?
                    None,               # 06: ?
                    None,               # 07: ?
                    None,               # 08: ?
                    None,               # 09: ?
                    None,               # 10: ?
                    None,               # 11: ?
                    None,               # 12: ?
                    None,               # 13: ?
                    None,               # 14: ?
                    None,               # 15: ?
                    None,               # 16: ?
                    None,               # 17: ?
                    None,               # 18: ?
                    None,               # 19: ?
                    None,               # 20: ?
                    None,               # 21: ?
                    None,               # 22: ?
                    None,               # 23: ?
                    None,               # 24: ?
                    None,               # 25: ?
                    None,               # 26: ?
                    None,               # 27: ?
                    None,               # 28: ?
                    None,               # 29: ?
                    None,               # 30: ?
                    None)}}             # 31: ?
        if self.cpuid_highest_extended_function >= 0x80000001:
            feature_bits_desc[0x80000001] = {
                'edx': (    # 0x80000001 EDX: AMD Extended features
                    'fpu',              # 00: Onboard x87 Floating-point Unit
                    'vme',              # 01: Virtual mode extensions
                    'de',               # 02: Debugging Extensions
                    'pse',              # 03: Page Size Extension
                    'tsc',              # 04: Time Stamp Counter
                    'msr',              # 05: Model-specific Registers
                    'pae',              # 06: Physical Address Extension
                    'mce',              # 07: Machine Check Exception
                    'cx8',              # 08: CMPXCHG8
                    'apic',             # 09: Advanced Programmable Interrupt Controller
                    None,               # 10: ?
                    'sep',              # 11: SYSCALL and SYSRET
                    'mtrr',             # 12: Memory Type Range Registers
                    'pge',              # 13: Page Global Enable
                    'mca',              # 14: Machine Check Architecture
                    'cmov',             # 15: Floating Point Conditional Move
                    'pat',              # 16: Page Attribute Table
                    'pse36',            # 17: 36-bit Page Size Zxtension
                    None,               # 18: ?
                    'mp',               # 19: Multiprocessor Capable
                    'nx',               # 20: No-eXecute
                    None,               # 21: ?
                    'mmx+',             # 22: Extended MMX
                    'mmx',              # 23: MMX
                    'fxsr',             # 24: FXSAVE, FXRSTOR
                    'ffxsr',            # 25: FXSAVE/FXRSTOR optimizations
                    'pg1g',             # 26: Gibibyte pages
                    'tscp',             # 27: RDTSCP
                    None,               # 28: ?
                    'lm',               # 29: Long Mode
                    '3dnow!+',          # 30: Extended 3DNow!
                    '3dnow!'),          # 31: 3DNow!

                'ecx': (    # 0x80000001 ECX: AMD Extended features
                    'ahf64',            # 00: LAHF/SAHF in long mode
                    'cmp',              # 01: Hyperthreading
                    'svm',              # 02: Secure Virtual Machine
                    'eas',              # 03: Extended APIC
                    'cr8d',             # 04: CR8 in 32-bit mode
                    'lzcnt',            # 05: Advanced Bit Manipulation
                    'sse4a',            # 06: Streaming SIMD Extensions 4a
                    'msse',             # 07: Misaligned SSE mode
                    '3dnow!p',          # 08: PREFETCH and PREFETCHW
                    'osvw',             # 09: OS Visible Workaround
                    'ibs',              # 10: Instruction Based Sampling
                    'xop',              # 11: eXtended Operations
                    'skinit',           # 12: SKINIT/STGI
                    'wdt',              # 13: Watchdog timer
                    None,               # 14: ?
                    'lwp',              # 15: Light Weight Profiling
                    'fma4',             # 16: Fused Multiply–Add 4
                    'tce',              # 17: Translation Cache Extension
                    None,               # 18: ?
                    'nodeid',           # 19: NodeID MSR
                    None,               # 20: ?
                    'tbm',              # 21: Trailing Bit Manipulation
                    'topx',             # 22: Topology Extensions
                    'pcx_core',         # 23: Core performance counter extensions
                    'pcx_nb',           # 24: NB performance counter extensions
                    None,               # 25: ?
                    'dbx',              # 26: Data breakpoint extensions
                    'perftsc',          # 27: Performance TSC
                    'pcx_l2i',          # 28: L2I perf counter extensions
                    'monx',             # 29: MONITORX/MWAITX
                    None,               # 30: ?
                    None)}              # 31: ?

        # Return features flags for current CPU
        flags = set()
        add_flag = flags.add
        for avx in sorted(feature_bits_desc):
            reg = Cpuid(avx)
            reg_desc = feature_bits_desc[avx]
            for exx in reg_desc:
                bits = getattr(reg, exx)
                for bit, feature in enumerate(reg_desc[exx]):
                    if feature is None:
                        continue
                    elif ((1 << bit) & bits) != 0:
                        add_flag(feature)

        # Return flags
        self['features'] = flags


class Cpuid:
    """Get Processor CPUID
    eax_value: EAX register value
    ecx_value: ECX register value"""
    def __init__(self, eax_value=0, ecx_value=0):
        # Define bytecode base
        bytecode = []
        for reg, value in ((0x0, eax_value), (0x1, ecx_value)):
            if value == 0:
                # Set to 0 (XOR reg, reg)
                bytecode += (
                    # XOR
                    b'\x31',
                    # reg, reg
                    (0b11000000 | reg | (reg << 3)).to_bytes(1, 'little'))
            else:
                # set other value (MOV reg, value)
                bytecode += (
                    # MOV reg,
                    (0b10111000 | reg).to_bytes(1, 'little'),
                    # Value
                    (value).to_bytes(4, 'little'))

        self._bytecode_base = b''.join(
            bytecode +
            # CPUID
            [b'\x0F\xA2'])

    def _get_cpuid(self, reg):
        """Get specified register CPUID result.
        reg: Register address"""
        from platform import system
        from ctypes import (
            c_void_p, c_size_t, c_ulong, c_uint32, c_int,
            CFUNCTYPE, memmove)

        # Complete bytecode with result address and RET
        bytecode = [self._bytecode_base]

        if reg != 0x0:
            # MOV EAX, reg
            bytecode += [
                # MOV
                b'\x89',
                # EAX, reg
                (0b11000000 | (reg << 3)).to_bytes(1, 'little')]

        bytecode = b''.join(
            bytecode +
            # RET
            [b'\xC3'])

        # Execute bytecode
        is_windows = system() == 'Windows'

        size = len(bytecode)
        if size < 0x1000:
            size = 0x1000

        try:
            # Allocate memory
            if is_windows:
                from ctypes import windll
                lib = windll.kernel32
                valloc = lib.VirtualAlloc
                valloc.argtypes = [c_void_p, c_size_t, c_ulong, c_ulong]
                args = (None, size, 0x1000, 0x40)
            else:
                from ctypes import cdll
                lib = cdll.LoadLibrary(None)
                valloc = lib.valloc
                valloc.argtypes = [c_size_t]
                args = (c_size_t(size), )

            valloc.restype = c_void_p
            address = valloc(*args)
            if address == 0:
                raise RuntimeError('Failed to allocate memory')

            if not is_windows:
                # Set memory executable
                mprotect = lib.mprotect
                mprotect.restype = c_int
                mprotect.argtypes = [c_void_p, c_size_t, c_int]
                if mprotect(address, size, 1 | 2 | 4) != 0:
                    raise RuntimeError('Failed to memory protect')

            # Copy bytecode to memory
            memmove(address, bytecode, size)

            # Create and execute function
            result = CFUNCTYPE(c_uint32)(address)()

        finally:
            # Free memory
            if is_windows:
                lib.VirtualFree(c_ulong(address), 0, 0x8000)
            else:
                mprotect(address, size, 1 | 2)
                lib.free(c_void_p(address))
        return result

    @property
    def eax(self):
        """Get EAX register CPUID result"""
        return self._get_cpuid(0x0)

    @property
    def ebx(self):
        """Get EBX register CPUID result"""
        return self._get_cpuid(0x3)

    @property
    def ecx(self):
        """Get ECX register CPUID result"""
        return self._get_cpuid(0x1)

    @property
    def edx(self):
        """Get EDX register CPUID result"""
        return self._get_cpuid(0x2)
