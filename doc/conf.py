"""Sphinx documentation"""

from os.path import abspath, dirname
import sys

sys.path.insert(0, abspath(dirname(dirname(__file__))))

from setup import PACKAGE_INFO  # noqa: E402

SPHINX_INFO = PACKAGE_INFO["command_options"]["build_sphinx"]

project = SPHINX_INFO["project"][1]
copyright = SPHINX_INFO["copyright"][1]
author = PACKAGE_INFO["author"]
version = SPHINX_INFO["version"][1]
release = SPHINX_INFO["release"][1]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "default"
html_theme = "sphinx_rtd_theme"
htmlhelp_basename = f"{project}doc"
latex_elements = {}  # type: ignore
latex_documents = [
    (master_doc, f"{project}.tex", f"{project} Documentation", author, "manual")
]
man_pages = [
    (master_doc, PACKAGE_INFO["name"], f"{project} Documentation", [author], 1)
]
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        PACKAGE_INFO["description"],
        "Miscellaneous",
    )
]
