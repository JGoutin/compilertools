# coding=utf-8
"""Test build and import with real files and compilers"""


C_SOURCE = '''
#include <Python.h>

static PyObject *
ctsrcex_test(PyObject *self, PyObject *args) {
    return PyLong_FromLong(1);
}

static PyMethodDef CtsrcexMethods[] = {
    {"test", ctsrcex_test, METH_VARARGS,
     "Used for test compilertools."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef ctsrcexmodule = {
    PyModuleDef_HEAD_INIT, "ctsrcex", NULL, -1,  CtsrcexMethods
};

PyMODINIT_FUNC
PyInit_ctsrcex(void) {
    return PyModule_Create(&ctsrcexmodule);
}
'''


PYX_SOURCE = '''
# cython: language_level=3

def test():
    return 1
'''


TEST_SCRIPT = '''
import sys
sys.path.extend(%s)

import compilertools
import ctsrcex

from os.path import basename
print(basename(ctsrcex.__file__), ctsrcex.test(), end='')
'''


def _build_and_import(
        setup, extension, ext_function=None,
        source_ext='module.c', source_content=C_SOURCE):
    """Test build with true files and compiler,
    and then import generated files."""
    from os import listdir, remove, getcwd
    from os.path import join, isfile
    from sys import executable
    from subprocess import Popen, PIPE
    from tempfile import TemporaryDirectory

    # This import also enable compilertools build patches
    from compilertools.build import get_build_compile_args
    from compilertools.imports import ARCH_SUFFIXES
    from compilertools._config_build import ConfigBuild

    # Compile all possibilities
    ConfigBuild.suffixes_includes.clear()
    ConfigBuild.suffixes_excludes.clear()

    # Build
    with TemporaryDirectory() as tmp:
        # Create source
        source = join(tmp, 'ctsrcex%s' % source_ext)
        build = join(tmp, 'build_exts')
        with open(source, 'wt') as file:
            file.write(source_content)

        # Create extensions
        extension = [extension('ctsrcex', [source])]
        if ext_function is not None:
            extension = ext_function(extension)

        # Compile
        try:
            setup(name='ctsrcex', ext_modules=extension,
                  script_args=['build_ext', '-t', tmp, '-b', build])

        # Handle setup errors
        except SystemExit as exception:
            message = exception.args[0]
            # Excepted exception if compiler not found by Distutils
            if ('Unable to find vcvarsall.bat' in message or
                    # Or not found by Setuptools
                    ('Microsoft Visual C++ ' in message and
                     ' is required.' in message)):
                from pytest import xfail
                xfail(message)
            # re-raise other exceptions
            raise

        # Check files presence
        assert set(listdir(build)) == {
            'ctsrcex%s' % suffix for suffix in
            get_build_compile_args()}

        # Create import test script
        script = join(tmp, 'test.py')
        with open(script, 'wt') as file:
            file.write(TEST_SCRIPT % str([build, getcwd()]))

        # Test suffixes imports
        if not ARCH_SUFFIXES:
            from pytest import xfail
            xfail('ARCH_SUFFIXES is empty on current environment')

        for suffix in ARCH_SUFFIXES:
            # Ignore file not existing
            path = join(build, 'ctsrcex%s' % suffix)
            if not isfile(path):
                continue

            # Import using import test script
            process = Popen(
                [executable, script], stdout=PIPE, stderr=PIPE, shell=False)
            stdout, stderr = process.communicate()

            # Check result printed by import test script
            assert (stdout or stderr).decode() == 'ctsrcex%s 1' % suffix

            # Remove imported file for forcing importing another in next loop
            print('"%s" imported successfully' % suffix)
            remove(path)


def tests_build_distutils():
    """Test compatibility with distutils only"""
    from distutils.core import setup, Extension
    _build_and_import(setup, Extension)


def tests_build_setuptools():
    """Test compatibility with Setuptools"""
    try:
        from setuptools import setup, Extension
    except ImportError:
        from pytest import skip
        skip('"setuptools" package not available')
    _build_and_import(setup, Extension)


def tests_build_numpy_distutils():
    """Tests compatibility with numpy.distutils"""
    try:
        from numpy.distutils.core import setup, Extension
    except ImportError:
        from pytest import skip
        skip('"numpy.distutils" package not available')

    _build_and_import(setup, Extension)


def tests_build_cython():
    """Test compatibility with Cython"""
    from distutils.core import setup, Extension
    try:
        from Cython.Build import cythonize
    except ImportError:
        from pytest import skip
        skip('"cython" package not available')

    _build_and_import(
        setup, Extension, ext_function=cythonize,
        source_ext='.pyx', source_content=PYX_SOURCE)
