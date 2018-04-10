# -*- coding: utf-8 -*-
"""GNU Compiler Collection"""
# https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html


from compilertools.compilers import CompilerBase as _CompilerBase

__all__ = ['Compiler']


class Compiler(_CompilerBase):
    """GNU Compiler Collection"""

    @_CompilerBase._memoized_property
    def option(self):
        """Compatibles Options

        Returns
        -------
        dict
            Keys are options names, values are dict of arguments
            with keys in {'link', 'compile'}."""
        return {'fast_fpmath': {'compile': '-Ofast'}}

    @_CompilerBase._memoized_property
    def api(self):
        """Compatibles API

        Returns
        -------
        dict
            Keys are API names, values are dict of arguments
            with keys in {'link', 'compile'}."""
        api = {}
        if self.version >= 4.2:
            api['openmp'] = {
                'compile': '-fopenmp',
                'link': '-fopenmp'}
        if self.version >= 4.9:
            api['cilkplus'] = {
                'compile': '-fcilkplus -lcilkrts',
                'link': '-fcilkplus -lcilkrts'}
        if self.version >= 6.1:
            api['openacc'] = {'compile': '-fopenacc'}
        return api

    @_CompilerBase._memoized_property
    def version(self):
        """Compiler version used.

        Returns
        -------
        float
            Version."""
        if not self.current_compiler:
            return

        from subprocess import Popen, PIPE
        from platform import system
        try:
            version_str = Popen(
                ['gcc' if system() == 'Windows' else 'cc', '--version'],
                stdout=PIPE, universal_newlines=True).stdout.read()
        except OSError:
            return

        if (not version_str or
                version_str.split('(', 1)[0].strip().lower()
                not in ('gcc', 'cc')):
            return

        version_str = version_str.split(')', 1)[1].rstrip().split(maxsplit=1)[0]

        # Keep only major and minor
        return float(version_str.rsplit('.', 1)[0])

    @_CompilerBase._memoized_property
    def python_build_version(self):
        """Compiler version that was used to build Python.

        Returns
        -------
        float
            Version."""
        from platform import python_compiler
        version_str = python_compiler()

        if 'GCC' not in version_str:
            return 0.0

        version_str = version_str.split(' ', 2)[1]

        # Keep only major and minor
        return float(version_str.rsplit('.', 1)[0])

    def _compile_args_matrix(self, arch, cpu):
        """Returns available GCC compiler options for the
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
        # Generic optimisation
        args = [[self.Arg(args=['-flto', '-O3'])]]

        # Architecture specific optimisations
        if arch == 'x86_64':
            args += [
                # CPU Generic optimisations
                [self.Arg(args='-m64')],

                # CPU Instructions sets
                [self.Arg(args=['-mavx512cd', '-mavx512f'],
                          suffix='avx512',
                          import_if=('AVX512F' in cpu.features and
                                     'AVX512CD' in cpu.features and
                                     cpu.os_supports_xsave),
                          build_if=self.version >= 4.9),

                 self.Arg(args='-mavx2',
                          suffix='avx2',
                          import_if=(self.version >= 4.7 and
                                     'AVX2' in cpu.features and
                                     cpu.os_supports_xsave)),

                 self.Arg(args='-mavx',
                          suffix='avx',
                          import_if=(self.version >= 4.4 and
                                     'AVX' in cpu.features and
                                     cpu.os_supports_xsave)),
                 self.Arg(),
                 ],

                # CPU Generic vendor/brand optimisations
                [self.Arg(args='-mtune=intel',
                          suffix='intel',
                          import_if=cpu.vendor == 'GenuineIntel',
                          build_if=self.version >= 4.9),

                 self.Arg(),
                 ]
            ]

        elif arch == 'x86_32':
            args += [
                # CPU Generic optimisations
                [self.Arg(args='-m32')],

                # CPU Instructions sets
                [self.Arg(args=['-mfpmath=sse', '-mavx2'],
                          suffix='avx2',
                          import_if=(self.version >= 4.7 and
                                     'AVX2' in cpu.features and
                                     cpu.os_supports_xsave)),

                 self.Arg(args=['-mfpmath=sse', '-mavx'],
                          suffix='avx',
                          import_if=(self.version >= 4.4 and
                                     'AVX' in cpu.features and
                                     cpu.os_supports_xsave)),

                 self.Arg(args=['-mfpmath=sse', '-msse4'],
                          suffix='sse4',
                          import_if=('SSE4_1' in cpu.features and
                                     'SSE4_2' in cpu.features),
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4.2'],
                          suffix='sse4_2',
                          import_if='SSE4_2' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4.1'],
                          suffix='sse4_1',
                          import_if='SSE4_1' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4a'],
                          suffix='sse4a',
                          import_if=(self.version >= 4.9 and
                                     'SSE4A' in cpu.features and
                                     cpu.vendor == 'AuthenticAMD')),

                 self.Arg(args=['-mfpmath=sse', '-mssse3'],
                          suffix='ssse3',
                          import_if='SSSE3' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse2'],
                          suffix='sse2',
                          import_if='SSE2' in cpu.features,
                          build_if=self.version >= 3.3),

                 self.Arg(args=['-mfpmath=sse', '-msse'],
                          suffix='sse',
                          import_if='SSE' in cpu.features,
                          build_if=self.version >= 3.1),

                 self.Arg(),
                 ],

                # CPU Generic vendor/brand optimisations
                [self.Arg(args='-mtune=intel',
                          suffix='intel',
                          import_if=cpu.vendor == 'GenuineIntel',
                          build_if=self.version >= 4.9),

                 self.Arg(),
                 ]
            ]

        return args

    def _compile_args_current_machine(self, arch, cpu):
        """Return auto-optimised GCC arguments for current machine.

        Parameters
        ----------
        arch : str
            CPU Architecture.
        cpu : compilertools.processors.ProcessorBase subclass
            Processor instance.

        Returns
        -------
        str
            Best compiler arguments for current machine."""
        # Base native optimisation
        args = ['-march=native -flto']

        # Arch specific optimizations
        if arch == 'x86_32':
            args.append('-m32')
            if 'SSE' in cpu.features and self.version >= 3.1:
                args.append('-mfpmath=sse')

        elif arch == 'x86_64':
            args.append('-m64')

        return ' '.join(args)
