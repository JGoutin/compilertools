Using it as system information library
======================================

Compilertools gets system information to optimize build and import. So, it can also be used as library that provides
this information.

CPU information
---------------

Compilertools can provide information on current CPU (Using ``CPUID`` or equivalent):

.. code-block:: python

    import compilertools

    # Gets current processor (arch=None for autodetect current CPU architecture)
    cpu = compilertools.processors.get_processor(arch=None, current_machine=True)

    # Gets features flags for current CPU as property
    cpu.features
    >>> {'SSE3', 'LAHF_LM', 'PSE36', 'ADX', 'MCA', 'XTPR', 'POPCNT', 'CLFLUSH', 'DE', 'TSC', 'MSR',
         'MTRR', 'SSE4_1', 'F16C', 'TSC_ADJUST', 'INVPCID', 'ABM', 'SMX', 'SDBG', 'VME', 'FXSR',
         'CX16', 'MOVBE', 'DTES64', 'AVX', 'AVX2', 'ERMS', 'RDTSCP', 'PCID', 'CLFLUSHOPT', 'MCE',
         'RDRAND', 'SMEP', 'TM2', 'SMAP', 'LM', '3DNOWPREFETCH', 'XSAVE', 'DS', 'RTM', 'PSE',
         'TSC_DEADLINE_TIMER', 'FSGSBASE', 'SSE4_2', 'TM', 'PDPE1GB', 'PAT', 'DS_CPL', 'SSE2', 'FMA',
         'VMX', 'BMI2', 'CX8', 'X2APIC', 'HLE', 'AES', 'EST', 'PAE', 'SSSE3', 'SYSCALL', 'HT', 'MMX',
         'SEP', 'PDCM', 'CMOV', 'SS', 'MONITOR', 'BMI1', 'MPX', 'PCLMULQDQ', 'OSXSAVE', 'NX', 'SSE',
         'APIC', 'PGE', 'FPU', 'ACPI', 'RDSEED', 'PBE'}

see :doc:`API documentation<api_processors>` for available properties.

Compiler information
--------------------

Compilertools can provide information on compiler:

.. code-block:: python

    import compilertools

    # Gets current compiler
    compiler = compilertools.compilers.get_compiler(current_compiler=True)

    # Gets current compiler version as property
    compiler.version
    >>> 6.3

see :doc:`API documentation<api_compilers>` for available properties.
