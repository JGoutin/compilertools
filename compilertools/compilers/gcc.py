# -*- coding: utf-8 -*-
"""GNU Compiler Collection"""
# https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html


from compilertools.compilers import CompilerBase as _CompilerBase

__all__ = ['Compiler']


class Compiler(_CompilerBase):
    """GNU Compiler Collection"""

    def __init__(self, current_compiler=False):
        _CompilerBase.__init__(self, current_compiler)
        self._default['python_build_version'] = 0.0

        # Options
        self['option']['fast_fpmath'] = {
            'compile': '-Ofast'}

        # API
        self['api']['openmp'] = {
            'compile': '-fopenmp',
            'link': '-fopenmp'}

        self['api']['openacc'] = {
            'compile': '-fopenacc'}

        self['api']['cilkplus'] = {
            'compile': '-fcilkplus -lcilkrts',
            'link': '-fcilkplus -lcilkrts'}

    @_CompilerBase._memoized_property
    def version(self):
        """Compiler version used.
        """
        if not self.current_compiler:
            return

        from subprocess import Popen, PIPE
        try:
            version_str = Popen(
                ['gcc', '--version'],
                stdout=PIPE, universal_newlines=True).stdout.read()
        except OSError:
            return
        version_str = version_str.rstrip().split('\n', 1)[0]

        if not version_str.lower().startswith('gcc'):
            return

        version_str = version_str.rsplit(maxsplit=1)[-1]

        # Keep only major and minor
        return float(version_str.rsplit('.', 1)[0])

    @_CompilerBase._memoized_property
    def python_build_version(self):
        """Compiler version that was used to build Python.
        """
        from platform import python_compiler
        version_str = python_compiler()

        if 'GCC' not in version_str:
            return

        version_str = version_str.split(' ', 2)[1]

        # Keep only major and minor
        return float(version_str.rsplit('.', 1)[0])

    def _compile_args_matrix(self, arch, cpu):
        """Return GCC compiler options availables for the
        specified CPU architecture.

        arch: CPU Architecture str."""
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
                          import_if=('avx512f' in cpu.features and
                                     'avx512cd' in cpu.features and
                                     cpu.os_supports_avx),
                          build_if=self.version >= 4.9),

                 self.Arg(args='-mavx2',
                          suffix='avx2',
                          import_if=(self.version >= 4.7 and
                                     'avx2' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args='-mavx',
                          suffix='avx',
                          import_if=(self.version >= 4.4 and
                                     'avx' in cpu.features and
                                     cpu.os_supports_avx)),
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
                                     'avx2' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mfpmath=sse', '-mavx'],
                          suffix='avx',
                          import_if=(self.version >= 4.4 and
                                     'avx' in cpu.features and
                                     cpu.os_supports_avx)),

                 self.Arg(args=['-mfpmath=sse', '-msse4'],
                          suffix='sse4',
                          import_if=('sse4.1' in cpu.features and
                                     'sse4.2' in cpu.features),
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4.2'],
                          suffix='sse4_2',
                          import_if='sse4.2' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4.1'],
                          suffix='sse4_1',
                          import_if='sse4.1' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse4a'],
                          suffix='sse4a',
                          import_if=(self.version >= 4.9 and
                                     'sse4a' in cpu.features and
                                     cpu.vendor == 'AuthenticAMD')),

                 self.Arg(args=['-mfpmath=sse', '-mssse3'],
                          suffix='ssse3',
                          import_if='ssse3' in cpu.features,
                          build_if=self.version >= 4.3),

                 self.Arg(args=['-mfpmath=sse', '-msse2'],
                          suffix='sse2',
                          import_if='sse2' in cpu.features,
                          build_if=self.version >= 3.3),

                 self.Arg(args=['-mfpmath=sse', '-msse'],
                          suffix='sse',
                          import_if='sse' in cpu.features,
                          build_if=self.version >= 3.1),

                 self.Arg(args='-mfpmath=387'),
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
        """Return auto-optimised compiler arguments for current machine"""
        # Base native optimisation
        args = ['-march=native -flto']

        # Arch specific optimizations
        if arch == 'x86_32':
            args.append('-m32')
            if 'sse' in cpu.features and self.version >= 3.1:
                args.append('-mfpmath=sse')

        elif arch == 'x86_64':
            args.append('-m64')

        return ' '.join(args)
