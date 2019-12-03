# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.4'  # For `sphinx.ext.imgmath`.

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.imgmath',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['.']

source_suffix = '.rst'
master_doc = 'index'
project = 'oemof.db'
year = '2019'
author = 'oemof developer group'
copyright = '2015-{0}, {1}'.format(year, author)
version = release = '0.0.6dev'

pygments_style = 'sphinx'
extlinks = {
    'issue': ('https://github.com/oemof/oemof.db/issues/%s', '#'),
    'pr': ('https://github.com/oemof/oemof.db/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

# Output file base name for HTML help builder.
htmlhelp_basename = 'oemof.db_doc'

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'oemof.db.tex', u'oemof.db Documentation', author, 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'oemof.db', u'oemof.db Documentation', [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'oemof.db', u'oemof.db Documentation', author, 'oemof.db',
   'Database related functionality of the open energy modelling framework, '
   'split out into a separate package.',
   'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'oemof.db'
epub_author = author
epub_publisher = author
epub_copyright = u'2015-{0}, {1}'.format(year, author)

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

