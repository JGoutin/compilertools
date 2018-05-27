# -*- coding: utf-8 -*-
"""General Configuration"""

# Default configuration
CONFIG = {

    # Architectures
    # Key is name or alias
    # Value is name to use
    'architectures': {
        # ARM 32bits
        'arm': 'arm_32',

        # ARM 64bits
        'arm64': 'arm_64',

        # x86 32bits
        'x86_32': 'x86_32',
        'x86': 'x86_32',
        'i386': 'x86_32',
        'i686': 'x86_32',
        'ia32': 'x86_32',
        'win32': 'x86_32',

        # x86 64bits
        'x86_64': 'x86_64',
        'x86-64': 'x86_64',
        'amd64': 'x86_64',
        'em64t': 'x86_64',
        'x64': 'x86_64',
    },

    # Compilers
    # Key is name or alias
    # Value is name to use
    'compilers': {
        # GNU Compiler Collection
        'gcc': 'gcc',
        'g++': 'gcc',
        'gfortran': 'gcc',
        'gnu fortran': 'gcc',
        'mingw32': 'gcc',
        'cygwin': 'gcc',
        'cc': 'gcc',
        'c++': 'gcc',
        'unix': 'gcc',

        # LLVM (Not implemented yet)
        # 'clang': 'llvm',
        # 'clang++': 'llvm',
        # 'flang': 'llvm',

        # Microsoft Visual C
        'msvc': 'msvc',
    },
}
