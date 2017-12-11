# -*- coding: utf-8 -*-
"""General Configuration"""

# Default configuration
CONFIG = {

    # Architectures
    # Key is name or alias
    # Value is name to use
    'architectures': {
        # ARM
        'arm': 'arm',

        # ARM64
        'arm64': 'arm64',

        # x86
        'x86': 'x86',
        'i386': 'x86',
        'i686': 'x86',
        'ia32': 'x86',
        'win32': 'x86',

        # x86_64
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
        # GCC
        'gcc': 'gcc',
        'unix': 'gcc',
        'mingw32': 'gcc',
        'cygwin': 'gcc',

        # MSVC
        'msvc': 'msvc',
            },
    }
