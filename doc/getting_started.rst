Getting Started
===============

Installation
------------

Compilertools is available on PyPI and can be installed with pip:

.. code-block:: bash

    pip install compilertools


Enabling compilertools in a Python package
------------------------------------------

This explains how to enable compilertools in a Python package:

**Enabling compilertools import hook**

The import hook is used to select the best version of a compiled module on build time. It needs to be initialized on
module startup.

This can be done by simply importing ``compilertools`` on the top of the main module of the package
(``__init__.py`` depending of package architecture):

.. code-block:: python

    """Main package __init__.py"""
    try:
        import compilertools
    except ImportError:
        # Reverts back to classic import behavior if compilertools not available
        # or imported on a non compatible Python version.
        pass

The ``try`` ``except`` block ensures that the package is imported correctly even if compilertools is not available or
can't run. In this case, compiled modules will be imported in compatibility mode, without optimisations.

**Enabling compilertools on build**

To generate multiple optimized compiled modules, compilertools needs to be initialized in the ``setup.py`` of the
package.

This can be done by simply importing ``compilertools.build`` in setup.py just after used build library
(like ``setuptools``, ``distutils``, ...):

.. code-block:: python

    """setup.py file"""
    from setuptools import setup
    try:
        import compilertools.build
    except ImportError:
        # Reverts back to classic build behavior if compilertools imported
        # on a non compatible Python version.
        pass

Don't forget to add compilertools as requirement for the package in the ``install_requires`` argument of
inside ``setup.py``.

The ``try`` ``except`` block ensures that ``setup.py`` can still be used on Python versions that are not supported
by compilertools (Like Python 2). In this case, compiled modules will be build without optimization.

.. code-block:: python

    """setup.py file, continued..."""
    setup(
        # ...Others setup arguments...
        install_requires=['compilertools']
        )

**And next ?**

That's its, compilertools is enabled on the package. Its configuration can be tweaked (See below) if needed, but it
work with default value else.

You can now build the wheel package with ``setup.py bdist_wheel``. If an user uses this generated wheel,
Python will use the best optimized compiled file available inside the package for its machine.

If an user build your package with ``pip`` from source, it will get an automatically optimized file for its machine.

Configuring compilertools
-------------------------

Compilertools configuration is done with the ``compilertools.build.ConfigBuild`` object, simply by changing its
parameters to adjust compilertools behavior as needed directly in ``setup.py``:

.. code-block:: python

    """setup.py file"""
    try:
        import compilertools.build

        # Creates optimized compiled modules only for AVX2 and AVX512 CPU instructions.
        compilertools.build.ConfigBuild.suffixes_includes = ['avx2', 'avx512']
    except ImportError:
        pass

Read :doc:`ConfigBuild documentation<api_build>` for available parameters.
