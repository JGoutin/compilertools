# coding=utf-8
"""compilertools setup"""
from datetime import datetime
from os.path import abspath, dirname, join

# Set Package information
PACKAGE_INFO = dict(
    name='compilertools',
    description='A library for helping optimizing Python extensions compilation.',
    long_description_content_type='text/markdown; charset=UTF-8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
        ],
    keywords='compiler distutils setuptools build_ext wheels setup build',
    author='J.Goutin',
    url='https://github.com/JGoutin/compilertools',
    license='BSD',
    zip_safe=True,
    python_requires='>=3.4',
    setup_requires=['setuptools'],
    tests_require=['pytest'],
    command_options={},
    )

SETUP_DIR = abspath(dirname(__file__))

# Get package __version__ from package
with open(join(SETUP_DIR, 'compilertools/_version.py')) as file:
    for line in file:
        if line.rstrip().startswith('__version__'):
            PACKAGE_INFO['version'] = line.split('=', 1)[1].strip(" \"\'\n")
            break

# Get long description from readme
with open(join(SETUP_DIR, 'readme.md')) as file:
    PACKAGE_INFO['long_description'] = file.read()

# Sphinx configuration
PACKAGE_INFO['command_options']['build_sphinx'] = {
    'project': ('setup.py', PACKAGE_INFO['name'].capitalize()),
    'version': ('setup.py', PACKAGE_INFO['version']),
    'release': ('setup.py', PACKAGE_INFO['version']),
    'copyright': ('setup.py', '2017-%s, %s' % (
        datetime.now().year, PACKAGE_INFO['author'])),
    }

# Run setup
if __name__ == '__main__':
    from os import chdir
    from sys import argv
    from setuptools import setup, find_packages

    # Add pytest_runner requirement if needed
    if {'pytest', 'test', 'ptr'}.intersection(argv):
        PACKAGE_INFO['setup_requires'].append('pytest-runner')

    # Add Sphinx requirements if needed
    elif 'build_sphinx' in argv:
        PACKAGE_INFO['setup_requires'] += ['sphinx', 'sphinx_rtd_theme']

    # Run setup
    chdir(SETUP_DIR)
    setup(packages=find_packages(exclude=['tests', 'doc']),
          **PACKAGE_INFO)
