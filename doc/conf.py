"""Sphinx documentation."""

from os.path import abspath, dirname
from datetime import datetime
import tomllib
import sys

# Ensure package can be imported
sys.path.insert(0, abspath(dirname(dirname(__file__))))

# Load information from pyproject.toml
with open(f"{abspath(dirname(dirname(__file__)))}/pyproject.toml", "rb") as _file:
    pyproject = tomllib.load(_file)["tool"]["poetry"]

# Sphinx configuration
project = pyproject["name"].capitalize()
version = pyproject["version"]
author = pyproject["authors"][0]
copyright = "2017-%s, %s" % (datetime.now().year, author)
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
man_pages = [(master_doc, pyproject["name"], f"{project} Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        pyproject["description"],
        "Miscellaneous",
    )
]
