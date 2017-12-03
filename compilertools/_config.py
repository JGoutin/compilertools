# -*- coding: utf-8 -*-
"""General Configuration"""

# Default configuration
CONFIG = {

    # Architectures names aliases
    'arch_alias': {
        # x86_64
        'amd64': 'x86_64',
        'x86-64': 'x86_64',
        'em64t': 'x86_64',
        'x64': 'x86_64',
        'win-amd64': 'x86_64',
        # x86
        'i386': 'x86',
        'i686': 'x86',
        'ia32': 'x86',
        'win32': 'x86'
            },

    # Compiler names aliases
    'compiler_alias': {
        # GCC
        'unix': 'gcc',
        'mingw32': 'gcc',
        'cygwin': 'gcc'
            },
    }
