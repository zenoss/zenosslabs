# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.viewcode']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Zenoss Labs'
copyright = u'2011, Zenoss Labs <labs@zenoss.com>'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'pyramid'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'sidebarwidth': '305',
    }

# Theme customizations not supported by options.
html_static_path = ['_static']
html_favicon = 'favicon.ico'
html_style = 'zenosslabs.css'
html_logo = '_static/new-zenoss-logo.png'

# Make sure the sidebar contains all of the sections we want.
html_copy_source = True
html_show_sourcelink = True

html_sidebars = {
    '**': ['localtoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'],
    }


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
    'classoptions': ',openany,oneside',  # eliminate blank pages
    'babel': '\\usepackage[english]{babel}',  # a babel option is required
    }

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'ZenossLabsDocumentation.tex', u'Zenoss Labs Documentation Documentation',
   u'Zenoss Labs \\textless{}labs@zenoss.com\\textgreater{}', 'manual'),
]


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'zenosslabsdocumentation', u'Zenoss Labs Documentation Documentation',
     [u'Zenoss Labs <labs@zenoss.com>'], 1)
]


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'ZenossLabsDocumentation', u'Zenoss Labs Documentation Documentation',
   u'Zenoss Labs <labs@zenoss.com>', 'ZenossLabsDocumentation', 'One line description of project.',
   'Miscellaneous'),
]


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'Zenoss Labs Documentation'
epub_author = u'Zenoss Labs <labs@zenoss.com>'
epub_publisher = u'Zenoss Labs <labs@zenoss.com>'
epub_copyright = u'2011, Zenoss Labs <labs@zenoss.com>'

