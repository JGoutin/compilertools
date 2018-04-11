Welcome to Compilertools's documentation!
=========================================

Python uses the Wheel format for simplified package distribution. However,
it does not allow to distribute packages optimized for each machine but highly compatible ones.
The user must compile the package himself to take advantage of optimization like SIMD (SSE, AVX, FMA, ...).

Compilertools allows to work around this problem and distribute optimized packages for several machines while keeping the simplicity of Wheel.
It works in the background and has been created with the aim of being easy to use.
Package maintainer requires only to import it at runtime and buildtime. Everything is transparent for the end user.

Its secondary objective is also to help the package maintainer to optimally compile its package with multiple compilers by configuring options for him.

Features:
=========

* Compiles and distributes optimized binaries for a variety of machines in a single Wheel package.
* Helps to build optimized package from sources for current machine.
* Handles automatically compiling and linking options for a variety of compilers.
* Autodetects openMP, OpenACC or Intel Cilk Plus in source code and automatically sets related compiling and linking options.
* Support extra compiling options like fast math.
* Provides build time settings for package maintainer to tweak compilation.
* Provides API for getting information on current machine CPU.

Supported compilers:

* GCC
* Microsoft Visual C++

Supported processors:

* x86 (32 and 64 bits)

Build tools compatibility

* distutils
* setuptools
* numpy.distutils

Python compatibility

* Python 3.4 minimum.

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: User Documentation:

   getting_started

.. toctree::
   :maxdepth: 2
   :caption: API documentation:

   api_build
   api_compilers
   api_imports
   api_processors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
