# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CAAIS'
copyright = '2026 Digitální a informační agentura'
author = 'Richard Chudoba (DIA); Milan Babic (NAKIT)'
release = '2.18'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx_design",
  "sphinx_copybutton",
]

#templates_path = ['_templates']
exclude_patterns = []

language = 'cs'

autosectionlabel_prefix_document = True
smartquotes = False
numfig = True

numfig_format = {
    'table': 'Tabulka %s: ',
    'figure': 'Obrázek %s: ',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = [
    '_static',
]
html_css_files = [
    'custom.css',
]
