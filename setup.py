"""compilertools setup"""
from setuptools import setup, find_packages
from datetime import datetime

# Set Package informations
PACKAGE_INFOS = dict(
    name='compilertools',
    description='A library for helping optimizing Python extensions compilation.',
    long_description_content_type='text/markdown; charset=UTF-8',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    packages=find_packages(exclude=['tests', 'doc']),
    zip_safe=True,
    python_requires='>=3.4',
    extras_require={'tests': ['pytest']},
    )

# Get package __version__ from package
with open('compilertools/_version.py') as file:
    for line in file:
        if line.rstrip().startswith('__version__'):
            PACKAGE_INFOS['version'] = line.split('=', 1)[1].strip(" \"\'\n")
            break

# Get long description from readme
with open('readme.md') as file:
    PACKAGE_INFOS['long_description'] = file.read()

# Sphinx configuration
PACKAGE_INFOS['command_options']['build_sphinx'] = {
    'project': ('setup.py', PACKAGE_INFOS['name'].capitalize()),
    'version': ('setup.py', PACKAGE_INFOS['version']),
    'release': ('setup.py', PACKAGE_INFOS['version']),
    'copyright': ('setup.py', '2017-%s, %s' % (
        datetime.now().year, PACKAGE_INFOS['author'])),
    }

# Run setup
if __name__ == '__main__':
    from os import chdir
    from os.path import dirname, abspath
    chdir(abspath(dirname(__file__)))
    setup(**PACKAGE_INFOS)
