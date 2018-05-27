# -*- coding: utf-8 -*-
"""Extra configuration for build"""


class ConfigBuild:
    """Build configuration"""

    #: Disable compilertools's optimization while building
    disabled = False

    #: Compiles optimized for current machine only
    #: (If not compile for a cluster of possibles machines)
    #: True or False for manually set value;
    #: 'autodetect' for automatically set value to True if build from
    #: PIP
    current_machine = 'autodetect'

    #: Enabled suffixes in files matrix definition.
    #: If this set is not empty, includes only suffixes specified
    #: inside it.
    #: This does not affect current machine builds.
    suffixes_includes = set()

    #: Disabled suffixes in files matrix definition.
    #: If 'suffixes_includes' is empty, completes this set to not
    #: build files for a specific architecture.
    #: This does not affect current machine builds.
    suffixes_excludes = {
        'sse', 'ssse3', 'sse4_1', 'sse4_2', 'intel_atom', 'intel', 'amd'
    }

    #: Enables compilers options
    option = {
        # Enables Fast floating point math
        'fast_fpmath': False
    }

    #: Specific API are auto-enabled when compiling and linking
    #: if following preprocessors are detected in source files
    api = {
        # openMP
        'openmp': {
            'c': '#pragma omp ',
            'fortran': ('!$omp ', 'c$omp ', '*$omp ')},
        # OpenACC
        'openacc': {
            'c': '#pragma acc ',
            'fortran': ('!$acc ', 'c$acc ', '*$acc ')},
        # Intel Cilk Plus
        'cilkplus': {
            'c': '#pragma simd ',
            'fortran': '!dir$ simd '}
    }

    #: Sources files extensions for code analysis
    extensions = {
        #: C/C++ sources files extensions
        'c': ('.c', '.cpp', '.cxx', '.cc', '.c++', '.cp'),
        #: Fortran sources files extensions
        'fortran': ('.f', '.for', '.f90', '.f95', '.f03', '.f08', '.f15')
    }
