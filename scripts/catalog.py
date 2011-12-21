#!/usr/bin/env python
import logging
LOG = logging.getLogger()

import ast
import os
import re
import subprocess


# Define explicit maps from AUTHOR fields found in ZenPack setup.py files to
# a list of normalized author names.
AUTHOR_MAP = {
    '2NMS - Maarten Wallraf': ['Maarten Wallraf'],
    'Alexander Vorobiyov devnull@rzpost.ru': ['Alexander Vorobiyov'],
    'Andreas Falk, R.Esteve': ['Andreas Falk', 'R. Esteve'],
    'Ben Hirsch (bhirsch@zenoss.com)': ['Ben Hirsch'],
    'Chet Luther <cluther@zenoss.com>': ['Chet Luther'],
    'Chris Morrison - chris.morrison@sita.aero, R.Esteve': ['Chris Morrison', 'R. Esteve'],
    'David Buler (phonegi)': ['David Buler'],
    'J.B. Giraudeau <jbgiraudeau@gmail.com>': ['J.B. Giraudeau'],
    'Jason Carpenter - Peak6': ['Jason Carpenter'],
    'Johan Keskitalo & Andreas Falk, R.Esteve': ['Johan Keskitalo', 'Andreas Falk', 'R. Esteve'],
    'Johan Keskitalo,R.Esteve': ['Johan Keskitalo', 'R. Esteve'],
    'Joseph Hanson (Zenoss)': ['Joseph Hanson'],
    'Nick Anderson <nick@cmdln.org>': ['Nick Anderson'],
    'Peter Hunt <support@opengear.com>': ['Peter Hunt'],
    'Peter Mitsich': ['Peter Mistich'],
    'R.Esteve': ['R. Esteve'],
    'Robert Naylor <zenpack@pobice.co.uk>': ['Robert Naylor'],
    'Zenoss Inc.': ['Zenoss'],
    'Zenoss Inc. (Simon)': ['Simon Jakesch'],
    'Zenoss Team': ['Zenoss'],
    'Zenoss, Inc.': ['Zenoss'],
    'dcarmean@zenoss.com': ['David Carmean'],
    'zenoss': ['Zenoss'],
    }


def get_zenpack_metadata(setup_filename, attribute_names=None):
    """Extracts metadata from a ZenPack's setup.py.

    Uses AST to extract metadata from a ZenPack's setup.py without evaluating
    it. If `attribute_names` is not specified, all standard attributes will be
    extracted. If `attribute_names` is specified, only attributes by those
    names will be extracted.

    In the case that an attribute is missing, it will be set to `None` in the
    returned dictionary.

    :param setup_filename: path to ZenPack setup.py
    :type setup_filename: :class:`types.StringTypes`
    :param attribute_names: attribute names to return
    :type attribute_names: :class:`types.ListType` or :class:`types.NoneType`
    :rtype: :class:`types.DictType`

    """

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
                    items[name.id] = v.s.decode('latin-1')
                elif isinstance(v, (ast.Tuple, ast.List)):
                    items[name.id] = []
                    for e in v.elts:
                        if isinstance(e, ast.Str):
                            items[name.id].append(e.s.decode('latin-1'))

    for attribute_name in attribute_names:
        if attribute_name not in items:
            if attribute_name == 'INSTALL_REQUIRES':
                items[attribute_name] = []
            else:
                items[attribute_name] = None

    return items


def expand_author(author):
    """Expand a single author string into a list of authors.

    Uses a combination of splitting on r'\s+(?:/|and|&)\s+' and looking up in
    an exceptions dictionary.

    :param author: AUTHOR string taken from a ZenPack's setup.py
    :type author: :class:`types.StringTypes`
    :rtype: :class:`types.GeneratorType`

    """

    if not author:
        return

    authors = re.split(r'\s+(?:/|and|&)\s+', author)
    for part in authors:
        if part in AUTHOR_MAP:
            for expanded_author in AUTHOR_MAP[part]:
                yield expanded_author
        else:
            yield part


def vcs_from_url(url):
    """Determine the VCS (Version Control System) from a URL.

    The return value will either be `git` or `subversion`.

    :param url: URL to checkout or clone the repository
    :type url: :class:`types.StringTypes`
    :rtype: :class:`types.StringType`

    """
    if url.endswith('.git'):
        return "git"
    else:
        return "subversion"


def vcs_from_path(path):
    """Determine the VCS (Version Control System) from a path.

    The return value will either be `git` or `subversion`.

    :param path: base path to a checked out or cloned VCS repository
    :type path: :class:`types.StringTypes`
    :rtype: :class:`types.StringType`

    """

    if os.path.isdir(os.path.join(path, '.git')):
        return 'git'
    elif os.path.isdir(os.path.join(path, '.svn')):
        return 'subversion'


def url_from_path(path):
    """Determine the VCS URL for a path.

    :param path: base path to a checked out or cloned VCS repository
    :type path: :class:`types.StringTypes`
    :rtype: :class:`types.StringType`

    """
    vcs = vcs_from_path(path)

    if vcs == "git":
        return subprocess.check_output(
            "cd %s ; git config --get remote.origin.url" % path,
            shell=True).rstrip()
    elif vcs == 'subversion':
        return subprocess.check_output(
            "cd %s ; svn info | grep URL | cut -d ' ' -f2" % path,
            shell=True).rstrip()


def get_repository(label, url):
    """Clone or checkout a repository.

    :param label: label for the repository
    :type label: :class:`types.StringType`
    :param url: URL to checkout or clone the repository
    :type url: :class:`types.StringTypes`
    :rtype: :class:`types.NoneType`

    """
    vcs = vcs_from_url(url)
    if vcs == "subversion":
        LOG.info("%s: subversion checkout", label)
        r = subprocess.check_call(
            "svn checkout %s %s" % (url, label),
            shell=True)

        if r != 0:
            LOG.warn("Failed to checkout %s", label)

    elif vcs == 'git':
        r = None
        if os.path.isdir(os.path.join(label, '.git')):
            LOG.info("%s: git pull", label)
            r = subprocess.check_call(
                "cd %s ; git pull" % label,
                shell=True,
                )
        else:
            LOG.info("%s: git clone", label)
            r = subprocess.check_call(
                "git clone %s %s" % (url, label),
                shell=True)

        if r != 0:
            LOG.warn("Failed to clone or pull %s", label)
            return

        LOG.info("%s: git submodule update --init", label)
        r = subprocess.check_call(
            "cd %s ; git submodule update --init" % label,
            shell=True)

        if r != 0:
            LOG.warn("Failed to update submodules for %s", label)
            return


if __name__ == '__main__':
    import sqlite3
    import yaml

    logging.basicConfig(
        format="%(levelname)s| %(message)s",
        level=logging.INFO)

    config_file = open("catalog.yaml", "r")
    config = yaml.load(config_file)
    config_file.close()

    discovered_zenpacks = {}

    for directory_id, directory in config.get('directories', {}).items():
        if 'url' not in directory:
            LOG.warn("No url specified for %s", directory_id)
            continue

        # get_repository(directory_id, directory['url'])

        for entry in os.listdir(directory_id):
            path = os.path.join(directory_id, entry)
            setup_filename = os.path.join(path, 'setup.py')

            if not os.path.isdir(path) or \
                not entry.startswith('ZenPacks.') or \
                not os.path.isfile(setup_filename):
                continue

            zp_metadata = get_zenpack_metadata(setup_filename)
            zp_metadata['URL'] = url_from_path(path)

            discovered_zenpacks[entry] = zp_metadata

    for zenpack_id, zenpack in config.get('zenpacks', {}).items():
        if 'url' not in zenpack:
            LOG.warn("No url specified for %s", zenpack_id)
            continue

        # get_repository(zenpack_id, zenpack['url'])

        setup_filename = os.path.join(zenpack_id, 'setup.py')
        if not os.path.isfile(setup_filename):
            continue

        zp_metadata = get_zenpack_metadata(setup_filename)
        zp_metadata['URL'] = url_from_path(zenpack_id)

        discovered_zenpacks[zenpack_id] = zp_metadata

    conn = sqlite3.connect("catalog.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE zenpacks ("
        "  name TEXT,"
        "  license TEXT,"
        "  copyright TEXT,"
        "  version TEXT,"
        "  compat_zenoss_vers TEXT,"
        "  url TEXT"
        ")")

    c.execute(
        "CREATE TABLE zenpack_authors ("
        "  zenpack TEXT,"
        "  author TEXT"
        ")")

    c.execute(
        "CREATE TABLE zenpack_dependencies ("
        "  zenpack TEXT,"
        "  dependency TEXT,"
        "  version TEXT"
        ")")

    for zenpack in discovered_zenpacks.values():
        c.execute("INSERT INTO zenpacks VALUES (?, ?, ?, ?, ?, ?)", (
            zenpack['NAME'],
            zenpack['LICENSE'],
            zenpack['COPYRIGHT'],
            zenpack['VERSION'],
            zenpack['COMPAT_ZENOSS_VERS'],
            zenpack['URL'],
            ))

        for author in set(expand_author(zenpack['AUTHOR'])):
            c.execute("INSERT INTO zenpack_authors VALUES (?, ?)", (
                zenpack['NAME'],
                author,
                ))

        for dependency in zenpack['INSTALL_REQUIRES']:
            parts = re.split(r'([><=]+)', dependency, maxsplit=1)

            version = None
            if len(parts) == 1:
                version = ""
            else:
                version = ''.join(parts[1:])

            c.execute("INSERT INTO zenpack_dependencies VALUES (?, ?, ?)", (
                zenpack['NAME'],
                parts[0],
                version,
                ))

    conn.commit()
    c.close()
