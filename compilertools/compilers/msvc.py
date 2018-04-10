# -*- coding: utf-8 -*-
"""Microsoft Visual C++ Compiler"""
# https://docs.microsoft.com/cpp/build/reference/c-cpp-building-reference

from compilertools.compilers import CompilerBase as _CompilerBase

__all__ = ['Compiler']


class Compiler(_CompilerBase):
    """Microsoft Visual C++"""

    @_CompilerBase._memoized_property
    def option(self):
        """Compatibles Options

        Returns
        -------
        dict
            Keys are options names, values are dict of arguments
            with keys in {'link', 'compile'}."""
        return {'fast_fpmath': {'compile': '/fp:fast'}}

    @_CompilerBase._memoized_property
    def api(self):
        """Compatibles API

        Returns
        -------
        dict
            Keys are API names, values are dict of arguments
            with keys in {'link', 'compile'}."""
        return {'openmp': {'compile': '/openmp'}}

    @_CompilerBase._memoized_property
    def version(self):
        """For Microsoft Visual C++,
        Compiler version used to build need to be
        the same that the one used to build Python.

        Returns
        -------
        float
            Version.
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
        """Returns Microsoft Visual C++ compiler options available for the
        specified CPU architecture.

        Parameters
        ----------
        arch : str
            CPU Architecture.
        cpu : compilertools.processors.ProcessorBase subclass
            Processor instance

        Returns
        -------
        list of CompilerBase.Arg
            Arguments matrix."""
        # Computes arguments
        args = [
            # Generic optimisation
            [self.Arg(args=['/O2', '/GL'])],

            # CPU Instructions sets
            [self.Arg(args='/arch:AVX2',
                      suffix='avx2',
                      import_if=('AVX2' in cpu.features and
                                 cpu.os_supports_xsave and
                                 self.version >= 12.0),
                      build_if=self.version >= 12.0),

             self.Arg(args='/arch:AVX',
                      suffix='avx',
                      import_if=('AVX' in cpu.features and
                                 cpu.os_supports_xsave and
                                 self.version >= 10.0),
                      build_if=self.version >= 10.0),

             self.Arg(args='/arch:SSE2',
                      suffix='sse2',
                      import_if='SSE2' in cpu.features and arch == 'x86_32',
                      build_if=arch == 'x86_32'),

             self.Arg(args='/arch:SSE',
                      suffix='sse',
                      import_if='SSE' in cpu.features and arch == 'x86_32',
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
