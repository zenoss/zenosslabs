#!/usr/bin/env python
import logging
LOG = logging.getLogger()

import ast
import operator
import os
import re
import unicodedata
import subprocess


HTML_TEMPLATE = """<html>
    <head>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load("visualization", "1", {packages:["corechart"]});

            // Authorship Concentration
            google.setOnLoadCallback(drawAuthorshipConcentration);
            function drawAuthorshipConcentration() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'ZenPacks per Author');
                data.addColumn('number', 'Number of Authors');
                data.addRows([
                {%- for number, count in authorship_concentration %}
                    ['{{ number }} ZenPack{{ 's' if number != 1 }}', {{ count }}]{{ ',' if not loop.last }}
                {%- endfor %}
                ]);

                var options = {
                    title: 'Authorship Concentration',
                    titleTextStyle: {fontSize: 24},
                    width: 600,
                    height: 400
                };

                var chart = new google.visualization.PieChart(document.getElementById('authorship_concentration_div'));
                chart.draw(data, options);
            }

            // Top 10 Authors
            google.setOnLoadCallback(drawTopTenAuthors);
            function drawTopTenAuthors() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Author');
                data.addColumn('number', 'Number of ZenPacks');
                data.addRows([
                {%- for author, count in top_authors[:10] %}
                    ["{{ author }}", {{ count }}]{{ ',' if not loop.last }}
                {%- endfor %}
                ]);

                var options = {
                    title: 'Top 10 Authors',
                    titleTextStyle: {fontSize: 24},
                    width: 600,
                    height: 400
                };

                var chart = new google.visualization.PieChart(document.getElementById('top_ten_authors_div'));
                chart.draw(data, options);
            }

            // License Distribution
            google.setOnLoadCallback(drawLicenseDistribution);
            function drawLicenseDistribution() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'License');
                data.addColumn('number', 'Number of ZenPacks');
                data.addRows([
                {%- for license, count in license_distribution %}
                    ["{{ license }}", {{ count }}]{{ ',' if not loop.last }}
                {%- endfor %}
                ]);

                var options = {
                    title: 'License Distribution',
                    titleTextStyle: {fontSize: 24},
                    width: 600,
                    height: 400
                };

                var chart = new google.visualization.PieChart(document.getElementById('license_distribution_div'));
                chart.draw(data, options);
            }

            // Lines of Code
            google.setOnLoadCallback(drawLinesOfCode);
            function drawLinesOfCode() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Language');
                data.addColumn('number', 'Lines of Code');
                data.addRows([
                    ['Python', {{ lines_of_code[0] }}],
                    ['XML', {{ lines_of_code[1] }}],
                    ['ZCML', {{ lines_of_code[2] }}],
                    ['RPT', {{ lines_of_code[3] }}],
                    ['PT', {{ lines_of_code[4] }}],
                    ['JS', {{ lines_of_code[5] }}]
                ]);

                var options = {
                    title: 'Lines of Code',
                    titleTextStyle: {fontSize: 24},
                    width: 600,
                    height: 400
                };

                var chart = new google.visualization.PieChart(document.getElementById('lines_of_code_div'));
                chart.draw(data, options);
            }
        </script>
    </head>
    <body>
        <table>
            <tr>
                <td id="authorship_concentration_div"></td>
                <td id="top_ten_authors_div"></td>
            </tr><tr>
                <td id="license_distribution_div"></td>
                <td id="lines_of_code_div"></td>
            </tr>
    </body>
</html>
"""


TEXT_TEMPLATE = """ZenPacks Dashboard
------------------

Total ZenPacks: {{ total_zenpacks }}

Authorship Concentration:
{%- for number, count in authorship_concentration %}
    - {{ number }}: {{ count }}
{%- endfor %}
"""


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
                    items[name.id] = asciify(v.s)
                elif isinstance(v, (ast.Tuple, ast.List)):
                    items[name.id] = []
                    for e in v.elts:
                        if isinstance(e, ast.Str):
                            items[name.id].append(asciify(e.s))

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


def count_code_lines(path, extension):
    r = subprocess.check_output(
        "cd %s ; find ZenPacks/ -name \\*.%s -print0 | xargs -0 wc -l | tail -1 | awk '{ print $1 }'" % (path, extension),
        shell=True).rstrip()

    if r:
        return int(r)
    else:
        return 0


def update_repositories(config):
    for directory_id, directory in config.get('directories', {}).items():
        if 'url' not in directory:
            LOG.warn("No url specified for %s", directory_id)
            continue

        get_repository(directory_id, directory['url'])

    for zenpack_id, zenpack in config.get('zenpacks', {}).items():
        if 'url' not in zenpack:
            LOG.warn("No url specified for %s", zenpack_id)
            continue

        get_repository(zenpack_id, zenpack['url'])


def create_database(config):
    discovered_zenpacks = {}

    for directory_id, directory in config.get('directories', {}).items():
        if 'url' not in directory:
            LOG.warn("No url specified for %s", directory_id)
            continue

        for entry in os.listdir(directory_id):
            path = os.path.join(directory_id, entry)
            setup_filename = os.path.join(path, 'setup.py')

            if not os.path.isdir(path) or \
                not entry.startswith('ZenPacks.') or \
                not os.path.isfile(setup_filename):
                continue

            zp_metadata = get_zenpack_metadata(setup_filename)
            zp_metadata['URL'] = url_from_path(path)
            zp_metadata['LINES_PY'] = count_code_lines(path, 'py')
            zp_metadata['LINES_XML'] = count_code_lines(path, 'xml')
            zp_metadata['LINES_ZCML'] = count_code_lines(path, 'zcml')
            zp_metadata['LINES_RPT'] = count_code_lines(path, 'rpt')
            zp_metadata['LINES_PT'] = count_code_lines(path, 'pt')
            zp_metadata['LINES_JS'] = count_code_lines(path, 'js')

            discovered_zenpacks[entry] = zp_metadata

    for zenpack_id, zenpack in config.get('zenpacks', {}).items():
        if 'url' not in zenpack:
            LOG.warn("No url specified for %s", zenpack_id)
            continue

        setup_filename = os.path.join(zenpack_id, 'setup.py')
        if not os.path.isfile(setup_filename):
            continue

        zp_metadata = get_zenpack_metadata(setup_filename)
        zp_metadata['URL'] = url_from_path(zenpack_id)
        zp_metadata['LINES_PY'] = count_code_lines(zenpack_id, 'py')
        zp_metadata['LINES_XML'] = count_code_lines(zenpack_id, 'xml')
        zp_metadata['LINES_ZCML'] = count_code_lines(zenpack_id, 'zcml')
        zp_metadata['LINES_RPT'] = count_code_lines(zenpack_id, 'rpt')
        zp_metadata['LINES_PT'] = count_code_lines(zenpack_id, 'pt')
        zp_metadata['LINES_JS'] = count_code_lines(zenpack_id, 'js')

        discovered_zenpacks[zenpack_id] = zp_metadata

    if os.path.isfile("catalog.db"):
        os.unlink("catalog.db")

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

    c.execute(
        "CREATE TABLE zenpack_codelines ("
        "  zenpack TEXT,"
        "  py INTEGER,"
        "  xml INTEGER,"
        "  zcml INTEGER,"
        "  rpt INTEGER,"
        "  pt INTEGER,"
        "  js INTEGER"
        ")")

    for zenpack in discovered_zenpacks.values():
        c.execute("INSERT INTO zenpacks VALUES (?, ?, ?, ?, ?, ?)", (
            zenpack['NAME'],
            zenpack['LICENSE'] and zenpack['LICENSE'] or None,
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

        c.execute("INSERT INTO zenpack_codelines VALUES (?, ?, ?, ?, ?, ?, ?)", (
            zenpack['NAME'],
            zenpack['LINES_PY'],
            zenpack['LINES_XML'],
            zenpack['LINES_ZCML'],
            zenpack['LINES_RPT'],
            zenpack['LINES_PT'],
            zenpack['LINES_JS'],
            ))

    conn.commit()
    c.close()


def asciify(string):
    return unicodedata.normalize(
        'NFKD', string.decode('latin-1')).encode('ASCII', 'ignore')


def render(template_name):
    import jinja2

    template = jinja2.Template(template_name)
    context = get_render_context()
    print template.render(context)


def get_render_context():
    context = {}

    conn = sqlite3.connect("catalog.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM zenpacks")
    context['total_zenpacks'] = c.fetchone()[0]

    c.execute(
        "SELECT author, COUNT(*) "
        "  FROM zenpack_authors "
        " GROUP BY author "
        " ORDER BY COUNT(*) DESC "
        )

    authorship_concentration = {}
    context['top_authors'] = []

    for row in c:
        authorship_concentration.setdefault(row[1], 0)
        authorship_concentration[row[1]] += 1
        context['top_authors'].append((row[0], row[1]))

    context['authorship_concentration'] = sorted(
        authorship_concentration.items(),
        key=operator.itemgetter(1),
        reverse=True)

    c.execute(
        "SELECT IFNULL(license, 'Undefined'), COUNT(*) "
        "  FROM zenpacks "
        " GROUP BY license "
        " ORDER BY COUNT(*) DESC "
        )

    context['license_distribution'] = c.fetchall()

    c.execute(
        "SELECT SUM(py), SUM(xml), SUM(zcml), SUM(rpt), SUM(pt), SUM(js) "
        "  FROM zenpack_codelines "
        )

    context['lines_of_code'] = c.fetchone()

    c.close()

    return context


if __name__ == '__main__':
    import sqlite3
    import sys
    import yaml

    logging.basicConfig(
        format="%(levelname)s| %(message)s",
        level=logging.INFO)

    valid_commands = (
        'update_repos',
        'create_database',
        'render_text',
        'render_html',
        )

    commands = []
    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: %s <command>\n" % sys.argv[0]
        print >> sys.stderr, "Valid commands: %s" % ', '.join(valid_commands)
        sys.exit(1)

    command = None
    if len(sys.argv) == 1:
        commands.append('render_text')
    else:
        commands = sys.argv[1:]

    for command in commands:
        if command not in valid_commands:
            print >> sys.stderr, "%s is not a valid command.\n" % command
            print >> sys.stderr, "Valid commands: %s" % (
                ', '.join(valid_commands),)
            sys.exit(1)

    config_file = open("catalog.yaml", "r")
    config = yaml.load(config_file)
    config_file.close()

    for command in commands:
        if command == 'update_repos':
            update_repositories(config)
        elif command == 'create_database':
            create_database(config)
        elif command == 'render_text':
            render(TEXT_TEMPLATE)
        elif command == 'render_html':
            render(HTML_TEMPLATE)
