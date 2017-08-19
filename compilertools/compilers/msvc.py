# -*- coding: utf-8 -*-
""" Microsoft Visual C++ Compiler"""
# https://docs.microsoft.com/cpp/build/reference/c-cpp-building-reference

# TODO: boost.simd "#BOOST_SIMD_ASSUME_{SIMD_EXT}" preprocessor symbols
#       auto-add to C/C++ sources
# https://developer.numscale.com/boost.simd/documentation/develop/quickstart.html#win-compilation

# TODO : Use of '/arch:IA32' (MSVC11+) ?

import sys
from compilertools.compilers import CompilerBase

__all__ = ['Compiler']


class Compiler(CompilerBase):
    """Microsoft Visual C++"""

    def __init__(self):
        CompilerBase.__init__(self)

        # Compiler version
        self._get_build_version()

        # Arguments
        self._attributes['fast_fpmath'] = '/fp:fast'
        self._attributes['openmp_compile'] = '/openmp'

    def _get_build_version(self):
        """Update ompiler version with the one that was used to build Python.
        """
        if 'MSC v.' not in sys.version:
            # Assume compiler is MSVC6
            self._attributes['version'] = 6.0
            return

        version_str = sys.version.split('MSC v.')[1].split(' ', 1)[0]
        version = float('.'.join((version_str[:-2], version_str[-2:]))) - 6.0
        if int(version) >= 13:
            # 13.0 was skipped
            version += 1.0
        version += float()
        self._attributes['version'] = version

    def compile_args_matrix(self, arch):
        """Return Microsoft Visual C++ compiler options availables for the
        specified CPU architecture.

        arch: CPU Architecture str."""
        cpu = self._cpu

        # Fix arch name
        if '_' in arch:
            # Cross compilation, get only target arch
            arch = arch.rsplit('_', 1)[1]

        args = [
            # Generic optimisation
            [self.Arg(args=['/O2', '/GL'])],

            # CPU Instructions sets
            [self.Arg(args='/arch:AVX2',
                      suffix='avx2',
                      import_if=('avx2' in cpu.features and
                                 cpu.system_support_avx and
                                 self.version >= 12.0),
                      build_if=self.version >= 12.0),

             self.Arg(args='/arch:AVX',
                      suffix='avx',
                      import_if=('avx' in cpu.features and
                                 cpu.system_support_avx and
                                 self.version >= 10.0),
                      build_if=self.version >= 10.0),

             self.Arg(args='/arch:SSE2',
                      suffix='sse2',
                      import_if='sse2' in cpu.features and arch == 'x86',
                      build_if=arch == 'x86'),

             self.Arg(args='/arch:SSE',
                      suffix='sse',
                      import_if='sse' in cpu.features and arch == 'x86',
                      build_if=arch == 'x86'),

             self.Arg(),
            ],

            # CPU Generic vendor/brand optimisations
            [self.Arg(args='/favor:ATOM',
                      suffix='intel_atom',
                      import_if=(cpu.vendor == 'GenuineIntel' and
                                 'Atom' in cpu.brand and
                                 self.version >= 11.0),
                      build_if=self.version >= 11.0),

             self.Arg(args='/favor:INTEL64',
                      suffix='intel',
                      import_if=(cpu.vendor == 'GenuineIntel' and
                                 arch == 'amd64'),
                      build_if=arch == 'amd64'),

             self.Arg(args='/favor:AMD64',
                      suffix='amd',
                      import_if=(cpu.vendor == 'AuthenticAMD' and
                                 arch == 'amd64'),
                      build_if=arch == 'amd64'),

             self.Arg(import_if=(cpu.vendor not in ('GenuineIntel',
                                                    'AuthenticAMD'))),
            ]
        ]

        return args
