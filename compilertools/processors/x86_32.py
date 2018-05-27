# -*- coding: utf-8 -*-
"""X86-32 Processors"""
from compilertools.processors import ProcessorBase as _ProcessorBase

__all__ = ['Processor', 'Cpuid']


class Processor(_ProcessorBase):
    """x86-32 CPU"""

    def __init__(self, current_machine=False):
        _ProcessorBase.__init__(self, current_machine)
        self._default['os_supports_xsave'] = False
        self._default['cpuid_highest_extended_function'] = 0

    @_ProcessorBase._memoized_property
    def cpuid_highest_extended_function(self):
        """CPUID highest extended function.

        Returns
        -------
        int
            Related EAX value for CPUID."""
        if not self.current_machine:
            return

        return Cpuid(0x80000000).eax

    @_ProcessorBase._memoized_property
    def vendor(self):
        """CPU's manufacturer ID from CPUID.

        Returns
        -------
        str
            Manufacturer ID."""
        if not self.current_machine:
            return

        reg = Cpuid()
        return Cpuid.registers_to_str(reg.ebx, reg.edx, reg.ecx)

    @_ProcessorBase._memoized_property
    def brand(self):
        """CPU's brand from CPUID

        Returns
        -------
        str
            Brand."""
        if not self.current_machine:
            return

        if self.cpuid_highest_extended_function < 0x80000004:
            return

        brand_list = []
        for eax in (0x80000002, 0x80000003, 0x80000004):
            reg = Cpuid(eax)
            brand_list += [reg.eax, reg.ebx, reg.ecx, reg.edx]
        return Cpuid.registers_to_str(*brand_list)

    @_ProcessorBase._memoized_property
    def features(self):
        """CPU's features flags from CPUID

        Returns
        -------
        list of str
            Flags names.

        References
        ----------
        Reference: Linux kernel "arch/x86/include/asm/cpufeatures.h"

        Feature naming convention:
        Use "cpufeatures.h" quoted names in comments in priority,
        then use name from "cpufeatures.h" constants.

        Exceptions in names: PNI called SSE3 (like other SSE feature flags)"""

        if not self.current_machine:
            return

        # Feature bits description
        # feature_bits_desc: {(eax, ecx): registers_dict}
        # registers_dict: {register_name: feature_dict}
        # feature_dict: {bit: feature}
        feature_bits_desc = {
            # Intel
            (1, 0): {
                'edx': {
                    0: 'FPU', 1: 'VME', 2: 'DE', 3: 'PSE', 4: 'TSC', 5: 'MSR',
                    6: 'PAE', 7: 'MCE', 8: 'CX8', 9: 'APIC', 11: 'SEP',
                    12: 'MTRR', 13: 'PGE', 14: 'MCA', 15: 'CMOV', 16: 'PAT',
                    17: 'PSE36', 18: 'PN', 19: 'CLFLUSH', 21: 'DS', 22: 'ACPI',
                    23: 'MMX', 24: 'FXSR', 25: 'SSE', 26: 'SSE2', 27: 'SS', 
                    28: 'HT', 29: 'TM', 30: 'IA64', 31: 'PBE'},
                'ecx': {
                    0: 'SSE3', 1: 'PCLMULQDQ', 2: 'DTES64', 3: 'MONITOR',
                    4: 'DS_CPL', 5: 'VMX', 6: 'SMX', 7: 'EST', 8: 'TM2',
                    9: 'SSSE3', 10: 'CID', 11: 'SDBG', 12: 'FMA', 13: 'CX16',
                    14: 'XTPR', 15: 'PDCM', 17: 'PCID', 18: 'DCA',
                    19: 'SSE4_1', 20: 'SSE4_2', 21: 'X2APIC', 22: 'MOVBE',
                    23: 'POPCNT', 24: 'TSC_DEADLINE_TIMER', 25: 'AES',
                    26: 'XSAVE', 27: 'OSXSAVE', 28: 'AVX', 29: 'F16C',
                    30: 'RDRAND', 31: 'HYPERVISOR'}},
            # Intel structured extended
            (7, 0): {
                'ebx': {
                    0: 'FSGSBASE', 1: 'TSC_ADJUST', 3: 'BMI1', 4: 'HLE',
                    5: 'AVX2', 7: 'SMEP', 8: 'BMI2', 9: 'ERMS', 10: 'INVPCID',
                    11: 'RTM', 12: 'CQM', 14: 'MPX', 15: 'RDT_A',
                    16: 'AVX512F', 17: 'AVX512DQ', 18: 'RDSEED', 19: 'ADX',
                    20: 'SMAP', 21: 'AVX512IFMA', 23: 'CLFLUSHOPT', 24: 'CLWB',
                    26: 'AVX512PF', 27: 'AVX512ER', 28: 'AVX512CD',
                    29: 'SHA_NI', 30: 'AVX512BW', 31: 'AVX512VL'},
                'ecx': {
                    0: 'PREFETCHWT1', 1: 'AVX512VBMI', 2: 'UMIP', 3: 'PKU',
                    4: 'OSPKE', 6: 'AVX512_VBMI2', 8: 'GFNI', 9: 'VAES',
                    10: 'VPCLMULQDQ', 11: 'AVX512_VNNI', 12: 'AVX512_BITALG',
                    14: 'AVX512_VPOPCNTDQ', 16: 'LA57', 22: 'RDPID'},
                'edx': {
                    2: 'AVX512_4VNNIW', 3: 'AVX512_4FMAPS'}}}

        if self.cpuid_highest_extended_function >= 0x80000001:
            # AMD
            feature_bits_desc[(0x80000001, 0)] = {
                'edx': {
                    11: 'SYSCALL', 19: 'MP', 20: 'NX', 22: 'MMXEXT',
                    25: 'FXSR_OPT', 26: 'PDPE1GB', 27: 'RDTSCP', 29: 'LM',
                    30: '3DNOWEXT', 31: '3DNOW'},
                'ecx': {
                    0: 'LAHF_LM', 1: 'CMP_LEGACY', 2: 'SVM', 3: 'EXTAPIC',
                    4: 'CR8_LEGACY', 5: 'ABM', 6: 'SSE4A', 7: 'MISALIGNSSE',
                    8: '3DNOWPREFETCH', 9: 'OSVW', 10: 'IBS', 11: 'XOP',
                    12: 'SKINIT', 13: 'WDT', 15: 'LWP', 16: 'FMA4',
                    17: 'TCE', 19: 'NODEID_MSR', 21: 'TBM', 22: 'TOPOEXT',
                    23: 'PERFCTR_CORE', 24: 'PERFCTR_NB', 26: 'BPEXT',
                    27: 'PTSC', 28: 'PERFCTR_LLC', 29: 'MWAITX'}}

        # Returns features flags for current CPU
        flags = set()
        add_flag = flags.add
        for eax, ecx in feature_bits_desc:
            reg = Cpuid(eax, ecx)
            reg_desc = feature_bits_desc[(eax, ecx)]
            for exx in reg_desc:
                bits = getattr(reg, exx)
                reg_exx = reg_desc[exx]
                for bit in reg_exx:
                    if ((1 << bit) & bits) != 0:
                        add_flag(reg_exx[bit])

        # Returns flags
        return flags

    @_ProcessorBase._memoized_property
    def os_supports_xsave(self):
        """OS and CPU supports XSAVE instruction.

        Returns
        -------
        bool
            Supports if True."""
        if not self.current_machine:
            return

        return 'XSAVE' in self['features'] and 'OSXSAVE' in self['features']


class Cpuid:
    """Gets Processor CPUID.

    Parameters
    ----------
    eax_value : int
        EAX register value
    ecx_value : int
        ECX register value"""
    def __init__(self, eax_value=0, ecx_value=0):
        # Defines bytecode base
        bytecode = []
        for reg, value in ((0x0, eax_value), (0x1, ecx_value)):
            if value == 0:
                # Sets to 0 (XOR reg, reg)
                bytecode += (
                    # XOR
                    b'\x31',
                    # reg, reg
                    (0b11000000 | reg | (reg << 3)).to_bytes(1, 'little'))
            else:
                # Sets other value (MOV reg, value)
                bytecode += (
                    # MOV reg,
                    (0b10111000 | reg).to_bytes(1, 'little'),
                    # Value
                    value.to_bytes(4, 'little'))

        self._bytecode_base = b''.join(
            bytecode +
            # CPUID
            [b'\x0F\xA2'])

    def _get_cpuid(self, reg):
        """Gets specified register CPUID result.

        Parameters
        ----------
        reg : int
            Register address.

        Returns
        -------
        int
            Raw CPUID Result as unsigned integer."""
        from platform import system
        from ctypes import (
            c_void_p, c_size_t, c_ulong, c_uint32, c_int,
            CFUNCTYPE, memmove)

        # Completes bytecode with result address and RET
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

        # Executes bytecode
        is_windows = system() == 'Windows'

        size = len(bytecode)
        if size < 0x1000:
            size = 0x1000

        try:
            # Allocates memory
            if is_windows:
                from ctypes import windll
                lib = windll.kernel32
                valloc = lib.VirtualAlloc
                valloc.argtypes = [c_void_p, c_size_t, c_ulong, c_ulong]
                args = (None, size, 0x1000, 0x40)
            else:
                from ctypes import cdll
                lib = cdll.LoadLibrary(None)
                mprotect = lib.mprotect
                valloc = lib.valloc
                valloc.argtypes = [c_size_t]
                args = (c_size_t(size), )

            valloc.restype = c_void_p
            address = valloc(*args)
            if address == 0:
                raise RuntimeError('Failed to allocate memory')

            if not is_windows:
                # Sets memory as executable
                mprotect.restype = c_int
                mprotect.argtypes = [c_void_p, c_size_t, c_int]
                if mprotect(address, size, 1 | 2 | 4) != 0:
                    raise RuntimeError('Failed to memory protect')

            # Copies bytecode to memory
            memmove(address, bytecode, size)

            # Creates and executes function
            result = CFUNCTYPE(c_uint32)(address)()

        finally:
            # Frees memory
            if is_windows:
                lib.VirtualFree(c_ulong(address), 0, 0x8000)
            else:
                mprotect(address, size, 1 | 2)
                lib.free(c_void_p(address))
        return result

    @property
    def eax(self):
        """Get EAX register CPUID result.

        Returns
        -------
        int
            Raw EAX register value."""
        return self._get_cpuid(0x0)

    @property
    def ebx(self):
        """Get EBX register CPUID result.

        Returns
        -------
        int
            Raw EAX register value."""
        return self._get_cpuid(0x3)

    @property
    def ecx(self):
        """Get ECX register CPUID result.

        Returns
        -------
        int
            Raw EAX register value."""
        return self._get_cpuid(0x1)

    @property
    def edx(self):
        """Get EDX register CPUID result.

        Returns
        -------
        int
            Raw EAX register value."""
        return self._get_cpuid(0x2)

    @staticmethod
    def registers_to_str(*uints):
        """Converts unsigned integers from CPUID register to ASCII string.

        Parameters
        ----------
        uints : int
            Unsigned integers to concatenate and convert to string.

        Returns
        -------
        str
            Result."""
        from struct import pack
        return pack('<%s' % ('I' * len(uints)),
                    *uints).decode('ASCII').strip('\x00 ')
