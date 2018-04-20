# -*- coding: utf-8 -*-
"""
    pip install -U sphinx
    pip install sphinx_issues
    pip install sphinx_rtd_theme
"""
from __future__ import print_function

import inspect
import re
import evernode

# Project --------------------------------------------------------------

project = 'EverNode'
copyright = '2016-2018 AtomHash'
author = 'AtomHash'
issues_github_path = 'AtomHash/evernode'
version = release = evernode.__version__

# General --------------------------------------------------------------

master_doc = 'index'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}

# HTML -----------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_sidebars = {
    'index': [
        'project.html',
        'versions.html',
        'searchbox.html',
    ],
    '**': [
        'localtoc.html',
        'relations.html',
        'versions.html',
        'carbon_ads.html',
        'searchbox.html',
    ]
}
html_static_path = ['_static']
html_favicon = '_static/evernode-blue-favicon.ico'
html_logo = '_static/evernode-white-logo.png'
html_show_sourcelink = False

# linkcheck ------------------------------------------------------------

linkcheck_anchors = False

# Local Extensions -----------------------------------------------------


_internal_mark_re = re.compile(r'^\s*:internal:\s*$(?m)', re.M)


def skip_internal(app, what, name, obj, skip, options):
    docstring = inspect.getdoc(obj) or ''

    if skip or _internal_mark_re.search(docstring) is not None:
        return True


def cut_module_meta(app, what, name, obj, options, lines):
    """Remove metadata from autodoc output."""
    if what != 'module':
        return

    lines[:] = [
        line for line in lines
        if not line.startswith((':copyright:', ':license:'))
    ]


def setup(app):
    app.connect('autodoc-skip-member', skip_internal)
    app.connect('autodoc-process-docstring', cut_module_meta)
