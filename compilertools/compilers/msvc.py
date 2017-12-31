# -*- coding: utf-8 -*-
"""Microsoft Visual C++ Compiler"""
# https://docs.microsoft.com/cpp/build/reference/c-cpp-building-reference

# TODO: boost.simd "#BOOST_SIMD_ASSUME_{SIMD_EXT}" preprocessor symbols
#       auto-add to C/C++ sources
# https://developer.numscale.com/boost.simd/documentation/develop/quickstart.html#win-compilation

# TODO: Use of '/arch:IA32' (MSVC11+) ?

from compilertools.compilers import CompilerBase as _CompilerBase

__all__ = ['Compiler']


class Compiler(_CompilerBase):
    """Microsoft Visual C++"""

    def __init__(self, current_compiler=False):
        _CompilerBase.__init__(self, current_compiler)

        # Options
        self['option']['fast_fpmath'] = {'compile': '/fp:fast'}

        # API
        self['api']['openmp'] = {'compile': '/openmp'}

    @_CompilerBase._memoized_property
    def version(self):
        """For Microsoft Visual C++,
        Compiler version used to build need to be
        the same that the one used to build Python.
        """
        if not self.current_compiler:
            return

        from platform import python_compiler
        version_str = python_compiler()

        if not version_str.startswith('MSC v.'):
            return

        version_str = version_str.split('MSC v.')[1].split(' ', 1)[0]
        version = float('.'.join((version_str[:-2], version_str[-2:]))) - 6.0
        if int(version) >= 13:
            # 13.0 was skipped
            version += 1.0
        return version

    def _compile_args_matrix(self, arch, cpu):
        """Return Microsoft Visual C++ compiler options availables for the
        specified CPU architecture.

        arch: CPU Architecture str."""
        # Compute carguments
        args = [
            # Generic optimisation
            [self.Arg(args=['/O2', '/GL'])],

            # CPU Instructions sets
            [self.Arg(args='/arch:AVX2',
                      suffix='avx2',
                      import_if=('avx2' in cpu.features and
                                 cpu.os_supports_avx and
                                 self.version >= 12.0),
                      build_if=self.version >= 12.0),

             self.Arg(args='/arch:AVX',
                      suffix='avx',
                      import_if=('avx' in cpu.features and
                                 cpu.os_supports_avx and
                                 self.version >= 10.0),
                      build_if=self.version >= 10.0),

             self.Arg(args='/arch:SSE2',
                      suffix='sse2',
                      import_if='sse2' in cpu.features and arch == 'x86_32',
                      build_if=arch == 'x86_32'),

             self.Arg(args='/arch:SSE',
                      suffix='sse',
                      import_if='sse' in cpu.features and arch == 'x86_32',
                      build_if=arch == 'x86_32'),

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
                                 arch == 'x86_64'),
                      build_if=arch == 'x86_64'),

             self.Arg(args='/favor:AMD64',
                      suffix='amd',
                      import_if=(cpu.vendor == 'AuthenticAMD' and
                                 arch == 'x86_64'),
                      build_if=arch == 'x86_64'),

             self.Arg(),
            ]
        ]

        return args
