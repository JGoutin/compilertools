[![Build Status](https://travis-ci.org/JGoutin/compilertools.svg?branch=master)](https://travis-ci.org/JGoutin/compilertools)
[![Build status](https://ci.appveyor.com/api/projects/status/khsf4rjrjo78xcmm?svg=true)](https://ci.appveyor.com/project/JGoutin/compilertools)
[![Coverage Status](https://coveralls.io/repos/github/JGoutin/compilertools/badge.svg?branch=master)](https://coveralls.io/github/JGoutin/compilertools?branch=master)
[![Documentation Status](https://readthedocs.org/projects/compilertools/badge/?version=latest)](http://compilertools.readthedocs.io/en/latest/?badge=latest)

*This module is experimental*

Python uses the Wheel format for simplified package distribution. However,
it does not allow to distribute packages optimized for each machine but highly compatible ones.
The user must compile the package himself to take advantage of optimization like SIMD (SSE, AVX, FMA, ...).

Compilertools allows to work around this problem and distribute optimized packages for several machines while keeping the simplicity of Wheel.
It works in the background and has been created with the aim of being easy to use.
Package maintainer requires only to import it at runtime and buildtime. Everything is transparent for the end user.

Its secondary objective is also to help the package maintainer to optimally compile its package with multiple compilers by configuring options for him.

Documentation: http://compilertools.readthedocs.io/

## Features

### Multi-architecture optimized compilation for distribution

#### At build time

Make optimized ".so"/".pyd" for each architecture and name files with tagged suffixes : 

Example:
* module.avx2.cp36-win_amd64.pyd -> Optimized variant for AVX2 SIMD Extensions
* module.avx.cp36-win_amd64.pyd -> Optimized variant for AVX SIMD Extensions
* module.cp36-win_amd64.pyd -> Classic highly-compatible variant

These optimized files must be packaged in the same wheel when distributing (Don't need to create a wheel by variant).

Requirement:
* Import *compilertools.build* before build module normally.

#### At runtime

Autodetect and choose the best optimized ".so"/".pyd" to run based on CPU information.

If the best file not exist, search for the second best file, etc... If nothing found, use the highly-compatible one. 

Requirement:
* Import *compilertools* one time before import optimized modules (This add a new import hook to Python).

### Current-architecture optimized compilation

Find the best compiler options for the current architecture and current compiler and build only one optimized ".so"/".pyd" with classic name.

Requirement:
* Import *compilertools.build* before build module normally.

### Build-time all-compiler optimizations

Dynamically set link options and compile options depending on the currently used compiler.

Avoid to have to specify compiler specific options in sources or setup files.

Requirement:
* Import *compilertools.build* before build module normally.
* For some options, eventually set a variable in "setup.py".

#### *openMP*, *OpenACC*, *Intel Cilk Plus* API auto-detection

Search in source files for API *pragma* preprocessor calls and enable compiler and linker options if needed.

#### Extra generic compilers options

Enable or disable generic extra compiler options like fast math.

### Supported compilers

* GCC
* Microsoft Visual C++

### Supported processors

* x86 (32 and 64 bits)

### Build tools compatibility

* distutils
* setuptools
* numpy.distutils

### Python compatibility

* Python 3.4 minimum.

## Work in progress

* Module core : Done
* Microsoft Visual C++ compiler support : Done
* GNU Compiler Collection support : Done
* API autodetection: Done (openMP, openACC, Intel Cilk Plus)
* Unit test (pytest): Done
* Continuous integration: Done
* x86 CPUID : Done
* Extended configuration: Done
* PIP autodetection: Done
* Documentation with sphinx and readthedoc: In progress...

## Ideas & possibles futures features

* Ability to force the use of an API (openMP, ...)
* Add it as an option in *setuptools* (or eventually merge it in *setuptools*).
* Since this module get many information on CPU, give possibility to users to access them easily as a dict.
* Add support for more compilers (Intel, LLVM, ...). The aim is to support all compilers available with *distutils* and *numpy.distutils*.
* Add support for more processors (ARM, ...).
