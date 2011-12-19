#!/usr/bin/env python
import logging
LOG = logging.getLogger()

import ast
import os
import subprocess
import yaml


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
    logging.basicConfig(level=logging.INFO)

    config_file = open("catalog.yaml", "r")
    config = yaml.load(config_file)
    config_file.close()

    zenpacks = {}

    for directory_id, directory in config.get('directories', {}).items():
        if 'url' not in directory:
            LOG.warn("No url specified for %s", directory_id)
            continue

        vcs = None
        if directory['url'].endswith('.git'):
            vcs = 'git'
        else:
            vcs = 'subversion'

        if vcs == 'subversion':
            r = subprocess.check_call(
                "svn checkout %s %s" % (directory['url'], directory_id),
                shell=True)

            if r != 0:
                LOG.warn("Failed to checkout %s", directory_id)
                continue

        elif vcs == 'git':
            r = None
            if os.path.isdir(os.path.join(directory_id, '.git')):
                r = subprocess.check_call(
                    "cd %s ; git pull" % directory_id,
                    shell=True,
                    )
            else:
                r = subprocess.check_call(
                    "git clone %s %s" % (directory['url'], directory_id),
                    shell=True)

            if r != 0:
                LOG.warn("Failed to clone or pull %s", directory_id)
                continue

            r = subprocess.check_call(
                "cd %s ; git submodule update --init" % directory_id,
                shell=True)

            if r != 0:
                LOG.warn("Failed to update submodules for %s", directory_id)
                continue

        for entry in os.listdir(directory_id):
            path = os.path.join(directory_id, entry)
            setup_filename = os.path.join(path, 'setup.py')

            if not os.path.isdir(path) or \
                not entry.startswith('ZenPacks.') or \
                not os.path.isfile(setup_filename):
                continue

            zp_metadata = get_zenpack_metadata(setup_filename)
            zp_metadata['url'] = directory['url']
            zenpacks[entry] = zp_metadata

    for zenpack_name in zenpacks.keys():
        from pprint import pprint
        pprint(zenpacks[zenpack_name])
        print
