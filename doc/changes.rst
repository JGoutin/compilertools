Changelog
=========

1.1.5 (2023/05/05)
------------------

Others:

* Ensure Python 3.11 compatibility.
* Drop Python 3.6 and 3.7 support.

1.1.3 (2021/11/09)
------------------

Fixes:

 * Remove ``-mtune`` generic optimization for LLVM.

Others:

* Ensure Python 3.10 compatibility.

1.1.2 (2020/10/03)
------------------

Fixes:

 * Fix GCC/LLVM version detection in some cases.

Others:

* Use ``-O3`` instead of ``-O2`` on GCC/LLVM.
* Ensure Python 3.9 compatibility.
* Drop Python 3.5 support.

1.1.1 (2020/01/29)
------------------

Others:

* Ensure Python 3.8 compatibility.
* Drop Python 3.4 support.

1.1.0 (2019/01/11)
------------------

New compilers support:

* LLVM Clang

Others:

* Add more easy access function to get current machine CPU and compiler
  information.
* Use ``-O2`` instead of ``-O3`` on GCC.

1.0.0 (2018/05/27)
------------------

**First version with following features:**

Compilers:

* Microsoft Visual C++ compiler
* GNU Compiler Collection

Processors:

* X86 (32/64 bits)
* x86 CPUID

Others:

* Multi-architecture optimized compilation for distribution
* Current-architecture optimized compilation
* API autodetection: openMP, openACC & Intel Cilk Plus
* Extra compilers options: fast math
* Extended configuration
* Build tools compatibility: Distutils, Setuptools, Numpy.distutils & Cython
* PIP autodetection
* Full Unittest with pytest and Continuous integration on Appveyor and Travis-CI
* Sphinx Documentation with Readthedoc

Ideas & possibles futures features
----------------------------------

* Ability to force the use of an API (openMP, ...)
* Add it as an option in *setuptools* (or eventually merge it in *setuptools*).
* Since this module get many information on CPU, give possibility to users to
  access them easily as a dict.
* Add support for more compilers (Intel, LLVM, ...). The aim is to support all
  compilers available with *distutils* and *numpy.distutils*.
* Add support for more processors (ARM, ...).
