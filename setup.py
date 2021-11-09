#! /usr/bin/env python3
"""Setup script

run "./setup.py --help-commands" for help.
"""
from datetime import datetime
from os.path import abspath, dirname, join

PACKAGE_INFO = dict(
    name="compilertools",
    description="A library for helping optimizing Python extensions compilation.",
    long_description_content_type="text/markdown; charset=UTF-8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="compiler distutils setuptools build_ext wheels setup build",
    author="J.Goutin",
    url="https://github.com/JGoutin/compilertools",
    project_urls={
        "Documentation": "http://compilertools.readthedocs.io/",
        "Download": "https://pypi.org/project/compilertools",
    },
    license="BSD",
    zip_safe=True,
    python_requires=">=3.6",
    setup_requires=["setuptools"],
    tests_require=["pytest-cov", "pytest-flake8", "pytest-black"],
    command_options={},
)

SETUP_DIR = abspath(dirname(__file__))

with open(join(SETUP_DIR, "compilertools/_version.py")) as file:
    for line in file:
        if line.rstrip().startswith("__version__"):
            PACKAGE_INFO["version"] = line.split("=", 1)[1].strip(" \"'\n")
            break

with open(join(SETUP_DIR, "readme.md")) as file:
    PACKAGE_INFO["long_description"] = file.read()

PACKAGE_INFO["command_options"]["build_sphinx"] = {
    "project": ("setup.py", PACKAGE_INFO["name"].capitalize()),
    "version": ("setup.py", PACKAGE_INFO["version"]),
    "release": ("setup.py", PACKAGE_INFO["version"]),
    "copyright": (
        "setup.py",
        "2017-%s, %s" % (datetime.now().year, PACKAGE_INFO["author"]),
    ),
}

if __name__ == "__main__":
    from os import chdir
    from sys import argv
    from setuptools import setup, find_packages

    if {"pytest", "test", "ptr"}.intersection(argv):
        PACKAGE_INFO["setup_requires"].append("pytest-runner")

    elif "build_sphinx" in argv:
        PACKAGE_INFO["setup_requires"] += ["sphinx", "sphinx_rtd_theme"]

    chdir(SETUP_DIR)
    setup(packages=find_packages(exclude=["tests", "doc"]), **PACKAGE_INFO)
