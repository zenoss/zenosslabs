#!/usr/bin/env python
#
# Example script that scrapes metadata out of ZenPack setup.py files. It is
# assumed that the following subversion check outs have been made in the
# working directory.
#
#   svn co http://dev.zenoss.org/svnint/trunk/core/zenpacks core-zenpacks
#   svn co http://dev.zenoss.org/svnint/trunk/enterprise/zenpacks enterprise-zenpacks

import ast
import os


def get_zenpack_metadata(setup_filename, attribute_names=None):
    """Extracts metadata from a ZenPack's setup.py."""

    if attribute_names is None:
        attribute_names = (
            'NAME',
            'VERSION',
            'AUTHOR',
            'COPYRIGHT',
            'LICENSE',
            'COMPAT_ZENOSS_VERS',
            'INSTALL_REQUIRES',
            )

    items = {}

    f = open(setup_filename, 'r')
    t = compile(f.read(), setup_filename, 'exec', ast.PyCF_ONLY_AST)
    f.close()

    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and name.id in attribute_names:
                v = node.value

                if isinstance(v, ast.Str):
                    items[name.id] = v.s
                elif isinstance(v, (ast.Tuple, ast.List)):
                    items[name.id] = []
                    for e in v.elts:
                        if isinstance(e, ast.Str):
                            items[name.id].append(e.s)

    for attribute_name in attribute_names:
        if attribute_name not in items:
            items[attribute_name] = None

    return items


if __name__ == '__main__':
    for root in ('core-zenpacks', 'enterprise-zenpacks'):
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            setup_filename = os.path.join(path, 'setup.py')

            if not os.path.isdir(path) or \
                not entry.startswith('ZenPacks.') or \
                not os.path.isfile(setup_filename):
                continue

            zp_metadata = get_zenpack_metadata(setup_filename)
            from pprint import pprint
            pprint(zp_metadata)
            print
