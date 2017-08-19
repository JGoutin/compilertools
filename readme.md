[![Build Status](https://travis-ci.org/JGoutin/compilertools.svg?branch=master)](https://travis-ci.org/JGoutin/compilertools)
[![Build status](https://ci.appveyor.com/api/projects/status/khsf4rjrjo78xcmm?svg=true)](https://ci.appveyor.com/project/JGoutin/compilertools)
[![Coverage Status](https://coveralls.io/repos/github/JGoutin/compilertools/badge.svg?branch=master)](https://coveralls.io/github/JGoutin/compilertools?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b6b8b68a45904966a02289c6d371d77b/badge.svg)](https://www.quantifiedcode.com/app/project/b6b8b68a45904966a02289c6d371d77b)

*This module is experimental*

Actually, even if wheels provide pre-compiled extensions, binaries need to be hightly compatible with all possibles machines for the specified CPU architecture.
There is no easy solution to provide pre-compiled extensions using specific optimisation like SIMD (SSE, AVX, FMA, ...).

This module help to easily build and distributes optimized Python extensions for multiples architectures.

It is compatible with any existing modules and don't need to change any line of code (Other than an eventual import in module's *setup.py* by maintainer).

## Features

### Multi-architecture optimized compilation for distribution

#### At build time

Make optimized ".so"/".pyd" for each architecture and name files with tagged suffixes : 

>Example:
>module.avx2.cp36-win_amd64.pyd -> Optimized variant for AVX2 SIMD Extensions
>module.avx.cp36-win_amd64.pyd -> Optimized variant for AVX SIMD Extensions
>module.cp36-win_amd64.pyd -> Classic hightly-compatible variant

These optimized files must be packaged in the same wheel when distributing (Don't need to create a wheel by variant).

Requierement:
* Import *compilertools.build* before build module normally.

#### At runtime

Autodetect and choose the best optimized ".so"/".pyd" to run based on CPU informations.

If the best file not exist, search for the second best file, etc... If nothing found, use the highly-compatible one. 

Requierement:
* Import *compilertools* one time before import optimized modules (This add a new import hook to Python).

### Current-architecture optimized compilation

Find the best compiler options for the current architecture and current compiler and build only one optimized ".so"/".pyd" with classic name.

Requierement:
* Import *compilertools.build* before build module normally.

### Build-time all-compiler optimizations

Dynamically set link options and compile options depending on the currently used compiler.

Avoid to have to specify compiler specific options in sources or setup files.

Requierement:
* Import *compilertools.build* before build module normally.
* For some options, eventually set a variable in "setup.py".

#### *openMP*, *OpenACC*, *Intel Cilk Plus* API auto-detection

Search in source files for API *pragma* preprocessor calls and enable compiler and linker options if needed.

#### Fast-math mode

Enable or disable fast-math compiler option.

### Supported compilers

* GCC [Work in progress]
* Microsoft Visual C++

### Supported processors

* x86
* amd64 (x86-64)

### Build tools compatiblity

* distutils
* setuptools
* numpy.distutils [Planned: maybe already OK, but actually not tested]

### Python compatibility

* Python 3.4 minimum.

## Work in progress

* Module core : Done
* MSVC on Windows amd64, configuration and test : Done
* GCC on Linux amd64, configuration and test : Work in progress
* openMP detection and configuration : Done
* openACC detection and configuration : Done but untested
* Intel Cilk Plus detection and configuration : Done but untested
* Unit test (pytest) and continuous integration : Work in progress
* x86/amd64 CPUID : Partial, actually based on external library, but maybe better to internalise this, and if possible, in pure Python.

## Ideas & possibles futures features

* Tags selection at build time (Actually always use all tags available). And create a default tag pre-selection for supporting most current configurations.
* Ability to auto-enable "Current-architecture optimized compilation" with *pip* when installing from sources.
* Ability to force the use of an API (openMP, ...)
* Add it as an option *setuptools* (or eventually merge it in *setuptools*).
* Since this module get many informations on CPU, give possibility to users to access them easily as a dict.

## Help aprecied

* Tweak of GCC compilers options.
* x86 CPUID implementation.
* Add support for more compilers (Intel, ...). The aim is to support all compilers availables with *distutils* and *numpy.distutils*.
* Add support for more processors (ARM, ARM64, ...).
* Add support for Python 2.7, eventually.
