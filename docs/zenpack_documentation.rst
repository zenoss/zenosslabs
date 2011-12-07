===============================================================================
ZenPack Documentation
===============================================================================

ZenPacks must be documented using reStructuredText. The minimum documentation
requirement is that each ZenPack have a ``README.rst`` located in its top-level
directory.

An optional top-level ``docs/`` directory containing at least one file named
``index.rst`` can also be created to suplement the ``README.rst``. This would
be the recommended approach if a ZenPack's documentation requires the
additional complexity of additional structure, files, or Sphinx extensions.

Contents:

.. toctree::
   :maxdepth: 2

   Standards <zenpack_standards_guide>
   Template <zenpack_documentation_template>
   Example <zenpack_documentation_example>
