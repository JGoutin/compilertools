#!/usr/bin/env python3
"""Sphinx documentation"""

from os.path import abspath, dirname
import sys

sys.path.insert(0, abspath(dirname(dirname(__file__))))

# -- General configuration ------------------------------------------------
from setup import PACKAGE_INFO  # noqa: E402

SPHINX_INFO = PACKAGE_INFO["command_options"]["build_sphinx"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]
source_suffix = ".rst"
master_doc = "index"
project = SPHINX_INFO["project"][1]
copyright = SPHINX_INFO["copyright"][1]
author = PACKAGE_INFO["author"]
version = SPHINX_INFO["version"][1]
release = SPHINX_INFO["release"][1]
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "default"
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_rtd_theme"

# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = "%sdoc" % project

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}
latex_documents = [
    (master_doc, "%s.tex" % project, "%s Documentation" % project, author, "manual"),
]

# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, PACKAGE_INFO["name"], "%s Documentation" % project, [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        project,
        "%s Documentation" % project,
        author,
        project,
        PACKAGE_INFO["description"],
        "Miscellaneous",
    ),
]
