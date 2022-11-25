![tests](https://github.com/JGoutin/compilertools/workflows/tests/badge.svg)
[![codecov](https://codecov.io/gh/JGoutin/compilertools/branch/master/graph/badge.svg)](https://codecov.io/gh/JGoutin/compilertools)
[![PyPI](https://img.shields.io/pypi/v/compilertools.svg)](https://pypi.org/project/compilertools)

Python uses the Wheel format for simplified package distribution. However,
it does not allow distributing packages optimized for each machine but highly compatible ones.
The user must compile the package himself to take advantage of optimization like SIMD (SSE, AVX, FMA, ...).

Compilertools allows working around this problem and distributing optimized packages for several machines while keeping
the simplicity of Wheel. It works in the background and has been created with the aim of being easy to use.
Package maintainer requires only importing it at runtime and buildtime. Everything is transparent for the end user.

Its secondary objective is also to help the package maintainer to optimally compile its package with multiple compilers
by configuring options for him.

Documentation:
--------------
[**Compilertools Documentation**](https://jgoutin.github.io/compilertools/)


Features:
---------

* Compiles and distributes optimized binaries for a variety of machines in a single Wheel package.
* Helps to build optimized package from sources for current machine.
* Handles automatically compiling and linking options for a variety of compilers.
* Autodetects openMP, OpenACC or Intel Cilk Plus in source code and automatically sets related compiling and linking
  options.
* Support extra compiling options like fast math.
* Provides build time settings for package maintainer to tweak compilation.
* Provides API for getting information on current machine CPU.
* Lightweight pure Python module with no dependency that uses lazy import and evaluation as possible.

How that works ?
================

Compilertools dynamically sets link options and compiles options depending on the currently used compiler and targeted
architecture.

This avoids having to specify compiler-specific options in sources or setup files.

Multi-architecture optimized compilation for distribution
---------------------------------------------------------

**At build time:**

Compilertools helps to make optimized ".so"/".pyd" for each architecture and name files with tagged suffixes :

Example:

* *module.avx2.cp36-win_amd64.pyd* -> Optimized variant for AVX2 SIMD Extensions
* *module.avx.cp36-win_amd64.pyd* -> Optimized variant for AVX SIMD Extensions
* *module.cp36-win_amd64.pyd* -> Classic highly-compatible variant

These optimized files are packaged in the same wheel when distributing (Don't need to create a wheel by variant).

Requirement:

* Import ``compilertools.build`` before build module normally.
* Options can easily be changed directly in ``compilertools.build.CONFIG_BUILD`` dictionary.

**At runtime:**

Compilertools detects and chooses the best optimized ".so"/".pyd" to run based on CPU information.

If the best file not exists, search for the second best file, etc... If nothing found, use the highly-compatible one.

Requirement:

* Import ``compilertools`` one time before import-optimized modules (This adds a new import hook to Python).

Current-architecture optimized compilation
------------------------------------------

Compilertools finds the best compiler options for the current architecture and current compiler and build only one
optimized ".so"/".pyd" with classic name.

Requirement:

* Import ``compilertools.build`` before build module normally.

And also...
-----------

openMP, OpenACC, Intel Cilk Plus API auto-detection:
   Compilertools searches in source files for API ``pragma`` preprocessor calls and enables compiler and linker options
   if needed.

Extra generic compilers options:
   Compilertools can enable or disable generic extra compiler options like fast math.

Compatibility
=============

Supported Compilers
-------------------

Compilertools implements support for the following compilers:

* GCC
* LLVM Clang
* Microsoft Visual C++

Supported Processors
--------------------

Compilertools implements support for the following CPU:

* x86 (32 and 64 bits)

Build tools compatibility
-------------------------

Compilertools has been tested with the following build tools:

* Distutils
* Setuptools
* Numpy.distutils
* Cython
