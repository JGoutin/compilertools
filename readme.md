[![Build Status](https://travis-ci.org/JGoutin/compilertools.svg?branch=master)](https://travis-ci.org/JGoutin/compilertools)
[![Build status](https://ci.appveyor.com/api/projects/status/khsf4rjrjo78xcmm?svg=true)](https://ci.appveyor.com/project/JGoutin/compilertools)
[![codecov](https://codecov.io/gh/JGoutin/compilertools/branch/master/graph/badge.svg)](https://codecov.io/gh/JGoutin/compilertools)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f56d272d071b4674abe1547c33d18aeb)](https://www.codacy.com/app/ginnungagap/compilertools?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JGoutin/compilertools&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/compilertools/badge/?version=latest)](http://compilertools.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/compilertools.svg)](https://pypi.org/project/compilertools)

Python uses the Wheel format for simplified package distribution. However,
it does not allow to distribute packages optimized for each machine but highly compatible ones.
The user must compile the package himself to take advantage of optimization like SIMD (SSE, AVX, FMA, ...).

Compilertools allows to work around this problem and distribute optimized packages for several machines while keeping
the simplicity of Wheel. It works in the background and has been created with the aim of being easy to use.
Package maintainer requires only to import it at runtime and buildtime. Everything is transparent for the end user.

Its secondary objective is also to help the package maintainer to optimally compile its package with multiple compilers
by configuring options for him.

Documentation:
--------------
[**Compilertools Documentation**](http://compilertools.readthedocs.io)


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
* Lightweight pure Python module with no dependency that use lazy import and evaluation as possible.

How that works ?
================

Compilertools dynamically sets link options and compile options depending on the currently used compiler and targeted
architecture.

This avoid to have to specify compiler specific options in sources or setup files.

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

If the best file not exist, search for the second best file, etc... If nothing found, use the highly-compatible one.

Requirement:

* Import ``compilertools`` one time before import optimized modules (This add a new import hook to Python).

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

Compilertools implements support for following compilers:

* GCC
* LLVM Clang
* Microsoft Visual C++

Supported Processors
--------------------

Compilertools implements support for following CPU:

* x86 (32 and 64 bits)

Build tools compatibility
-------------------------

Compilertools have been tested with following build tools:

* Distutils
* Setuptools
* Numpy.distutils
* Cython

Python compatibility
--------------------

* Python 3.4 minimum.
