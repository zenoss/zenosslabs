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


def asciify(string):
    """Brute-force conversion of any encoding to ASCII."""
    return unicodedata.normalize(
        'NFKD', string.decode('latin-1')).encode('ASCII', 'ignore')


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


def commits_from_path(path):
    vcs = vcs_from_path(path)

    command = None
    matcher = None

    if vcs == 'subversion':
        command = "cd %s ; svn log -q | grep -v '^---'"
        matcher = re.compile(r'^\S+ \| \S+ \| (\S+ \S+)').search
    elif vcs == 'git':
        command = "cd %s ; git log --date=iso | grep '^Date'"
        matcher = re.compile(r'^Date:\s+(\S+ \S+)').search
    else:
        return []

    commits = []
    r = subprocess.check_output(command % path, shell=True)
    for line in r.split('\n'):
        match = matcher(line)
        if match:
            commits.append(match.group(1))

    # We want chronological order.
    commits.reverse()

    return commits


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


def discover_zenpacks(config):
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

            zenpack = get_zenpack_metadata(setup_filename)
            zenpack['PATH'] = path
            yield zenpack

    for zenpack_id, zenpack in config.get('zenpacks', {}).items():
        if 'url' not in zenpack:
            LOG.warn("No url specified for %s", zenpack_id)
            continue

        setup_filename = os.path.join(zenpack_id, 'setup.py')
        if not os.path.isfile(setup_filename):
            continue

        zenpack = get_zenpack_metadata(setup_filename)
        zenpack['PATH'] = zenpack_id
        yield zenpack


def create_database(config):
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

    c.execute(
        "CREATE TABLE zenpack_commits ("
        "  zenpack TEXT,"
        "  feature TEXT,"
        "  date TEXT"
        ")")

    for zenpack in discover_zenpacks(config):
        c.execute("INSERT INTO zenpacks VALUES (?, ?, ?, ?, ?, ?)", (
            zenpack['NAME'],
            zenpack['LICENSE'] and zenpack['LICENSE'] or None,
            zenpack['COPYRIGHT'],
            zenpack['VERSION'],
            zenpack['COMPAT_ZENOSS_VERS'],
            url_from_path(zenpack['PATH']),
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
            count_code_lines(zenpack['PATH'], 'py'),
            count_code_lines(zenpack['PATH'], 'xml'),
            count_code_lines(zenpack['PATH'], 'zcml'),
            count_code_lines(zenpack['PATH'], 'rpt'),
            count_code_lines(zenpack['PATH'], 'pt'),
            count_code_lines(zenpack['PATH'], 'js'),
            ))

        commits = commits_from_path(zenpack['PATH'])
        for i, commit in enumerate(commits):
            if i == 0:
                c.execute("INSERT INTO zenpack_commits VALUES (?, ?, ?)", (
                    zenpack['NAME'],
                    'first',
                    commit,
                    ))

            if i == len(commits) - 1:
                c.execute("INSERT INTO zenpack_commits VALUES (?, ?, ?)", (
                    zenpack['NAME'],
                    'last',
                    commit,
                    ))

            c.execute("INSERT INTO zenpack_commits VALUES (?, ?, ?)", (
                zenpack['NAME'],
                'incremental',
                commit,
                ))

    conn.commit()
    c.close()


def print_csv_normalized(config):
    import csv

    zenpacks_writer = csv.writer(open('zenpacks.csv', 'wb'))
    zenpacks_writer.writerow([
        'Name', 'License', 'Copyright', 'Version', 'Compatible Zenoss Version',
        'URL'])

    zenpack_authors_writer = csv.writer(open('zenpack_authors.csv', 'wb'))
    zenpack_authors_writer.writerow(['ZenPack', 'Author'])

    zenpack_codelines_writer = csv.writer(open('zenpack_codelines.csv', 'wb'))
    zenpack_codelines_writer.writerow([
        'ZenPack', 'XML', 'Python', 'JavaScript', 'PT', 'RPT', 'ZCML'])

    zenpack_commits_writer = csv.writer(open('zenpacks_commits.csv', 'wb'))
    zenpack_commits_writer.writerow(['ZenPack', 'Feature', 'Date'])

    zenpack_dependencies_writer = csv.writer(
        open('zenpack_dependencies.csv', 'wb'))

    zenpack_dependencies_writer.writerow(['ZenPack', 'Dependency', 'Version'])

    for zenpack in discover_zenpacks(config):
        zenpacks_writer.writerow([
            zenpack['NAME'],
            zenpack['LICENSE'] is None and '' or zenpack['LICENSE'],
            zenpack['COPYRIGHT'],
            zenpack['VERSION'],
            zenpack['COMPAT_ZENOSS_VERS'],
            url_from_path(zenpack['PATH']),
            ])

        for author in set(expand_author(zenpack['AUTHOR'])):
            zenpack_authors_writer.writerow([
                zenpack['NAME'],
                author,
                ])

        for dependency in zenpack['INSTALL_REQUIRES']:
            parts = re.split(r'([><=]+)', dependency, maxsplit=1)

            version = None
            if len(parts) == 1:
                version = ""
            else:
                version = ''.join(parts[1:])

            zenpack_dependencies_writer.writerow([
                zenpack['NAME'],
                parts[0],
                version,
                ])

        zenpack_codelines_writer.writerow([
            zenpack['NAME'],
            count_code_lines(zenpack['PATH'], 'xml'),
            count_code_lines(zenpack['PATH'], 'py'),
            count_code_lines(zenpack['PATH'], 'js'),
            count_code_lines(zenpack['PATH'], 'pt'),
            count_code_lines(zenpack['PATH'], 'rpt'),
            count_code_lines(zenpack['PATH'], 'zcml'),
            ])

        commits = commits_from_path(zenpack['PATH'])
        for i, commit in enumerate(commits):
            feature = None
            if i == 0:
                feature = 'first'
            elif i == len(commits) - 1:
                feature = 'last'

            zenpack_commits_writer.writerow([
                zenpack['NAME'],
                feature,
                commit,
                ])


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


def denormalized_generator():
    conn = sqlite3.connect("catalog.db")
    c = conn.cursor()

    c.execute(
        "SELECT name, license, copyright, version, compat_zenoss_vers, url "
        "  FROM zenpacks"
        )

    for zenpack, license, copyright, version, compat_zenoss_vers, url in c.fetchall():
        c.execute(
            "SELECT py, xml, zcml, rpt, pt, js "
            "  FROM zenpack_codelines "
            " WHERE zenpack = ?",
            (zenpack,)
            )

        lines_py, lines_xml, lines_zcml, lines_rpt, lines_pt, lines_js = c.fetchone()

        c.execute(
            "SELECT author "
            "  FROM zenpack_authors "
            " WHERE zenpack = ?",
            (zenpack,)
            )

        authors = c.fetchall()
        if len(authors) < 1:
            authors = [(None,)]

        for author, in authors:
            c.execute(
                "SELECT dependency, version "
                "  FROM zenpack_dependencies "
                " WHERE zenpack = ?",
                (zenpack,)
                )

            dependencies = c.fetchall()
            if len(dependencies) < 1:
                dependencies = [(None, None)]

            for dependency, dependency_version in dependencies:
                c.execute(
                    "SELECT feature, date "
                    "  FROM zenpack_commits "
                    " WHERE zenpack = ?",
                    (zenpack,)
                    )

                commits = c.fetchall()
                if len(commits) < 1:
                    commits = [(None, None)]

                for feature, date in commits:
                    if feature is None or date is None:
                        continue

                    yield {
                        'zenpack': zenpack,
                        'license': license,
                        'copyright': copyright,
                        'version': version,
                        'compat_zenoss_vers': compat_zenoss_vers,
                        'url': url,
                        'lines_xml': lines_xml,
                        'lines_py': lines_py,
                        'lines_js': lines_js,
                        'lines_pt': lines_pt,
                        'lines_rpt': lines_rpt,
                        'lines_zcml': lines_zcml,
                        'author': author,
                        'dependency': dependency,
                        'dependency_version': dependency_version,
                        'commit_type': feature,
                        'commit_year': date.split('-')[0],
                        'commit_timestamp': date,
                        }


def print_csv_denormalized():
    import csv

    writer = csv.writer(open('zenpacks_denormalized.csv', 'wb'))
    writer.writerow([
        'zenpack', 'license', 'copyright', 'version', 'compat_zenoss_vers',
        'url', 'lines_xml', 'lines_py', 'lines_js', 'lines_pt', 'lines_rpt',
        'lines_zcml', 'author', 'dependency', 'dependency_version',
        'commit_type', 'commit_year', 'commit_timestamp',
        ])

    for row in denormalized_generator():
        writer.writerow([
            row['zenpack'],
            row['license'],
            row['copyright'],
            row['version'],
            row['compat_zenoss_vers'],
            row['url'],
            row['lines_xml'],
            row['lines_py'],
            row['lines_js'],
            row['lines_pt'],
            row['lines_rpt'],
            row['lines_zcml'],
            row['author'],
            row['dependency'],
            row['dependency_version'],
            row['commit_type'],
            row['commit_year'],
            row['commit_timestamp'],
            ])


def print_gviz_json_denormalized():
    import gviz_api

    data_table = gviz_api.DataTable({
        'zenpack': ('string', 'ZenPack'),
        'license': ('string', 'License'),
        'copyright': ('string', 'Copyright'),
        'version': ('string', 'Version'),
        'compat_zenoss_vers': ('string', 'Compatible Zenoss Version'),
        'url': ('string', 'URL'),
        'lines_xml': ('number', 'Lines of XML'),
        'lines_py': ('number', 'Lines of Python'),
        'lines_js': ('number', 'Lines of JavaScript'),
        'lines_pt': ('number', 'Lines of Page Template'),
        'lines_rpt': ('number', 'Lines of Report Template'),
        'lines_zcml': ('number', 'Lines of ZCML'),
        'author': ('string', 'Author'),
        'dependency': ('string', 'Dependency'),
        'dependency_version': ('string', 'Depedency Version'),
        'commit_type': ('string', 'Commit Type'),
        'commit_year': ('string', 'Commit Year'),
        'commit_timestamp': ('string', 'Commit Timestamp'),
        })

    for row in denormalized_generator():
        data_table.AppendData([{
            'zenpack': row['zenpack'],
            'license': row['license'],
            'copyright': row['copyright'],
            'version': row['version'],
            'compat_zenoss_vers': row['compat_zenoss_vers'],
            'url': row['url'],
            'lines_xml': row['lines_xml'],
            'lines_py': row['lines_py'],
            'lines_js': row['lines_js'],
            'lines_pt': row['lines_pt'],
            'lines_rpt': row['lines_rpt'],
            'lines_zcml': row['lines_zcml'],
            'author': row['author'],
            'dependency': row['dependency'],
            'dependency_version': row['dependency_version'],
            'commit_type': row['commit_type'],
            'commit_year': row['commit_year'],
            'commit_timestamp': row['commit_timestamp'],
            }])

    print data_table.ToJSon()


def push_gspreadsheet_denormalized():
    import gdata.spreadsheet.service

    username = os.environ.get('GDATA_USERNAME')
    password = os.environ.get('GDATA_PASSWORD')

    # https://docs.google.com/spreadsheet/ccc?key=0AjERpIICRnb0dGMyOWNhREd2R2JPeFJ4QlBxam05WlE&hl=en_US#gid=0
    spreadsheet_key = '0AjERpIICRnb0dGMyOWNhREd2R2JPeFJ4QlBxam05WlE'
    worksheet_id = '1'

    gs_client = gdata.spreadsheet.service.SpreadsheetsService()
    gs_client.email = username
    gs_client.password = password
    gs_client.source = 'ZenPack Cataloger'
    gs_client.ProgrammaticLogin()

    for row in denormalized_generator():
        gs_client.InsertRow({
            'zenpack': row['zenpack'],
            'license': row['license'],
            'copyright': row['copyright'],
            'version': row['version'],
            'compatzenossvers': row['compat_zenoss_vers'],
            'url': row['url'],
            'linesxml': str(row['lines_xml']),
            'linespy': str(row['lines_py']),
            'linesjs': str(row['lines_js']),
            'linespt': str(row['lines_pt']),
            'linesrpt': str(row['lines_rpt']),
            'lineszcml': str(row['lines_zcml']),
            'author': row['author'],
            'dependency': row['dependency'],
            'dependencyversion': row['dependency_version'],
            'committype': row['commit_type'],
            'commityear': row['commit_year'],
            'committimestamp': row['commit_timestamp'],
            }, spreadsheet_key, worksheet_id)


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

        'print_csv_normalized',

        'print_csv_denormalized',
        'print_gviz_json_denormalized',
        'push_gspreadsheet_denormalized',
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

        elif command == 'print_csv_normalized':
            print_csv_normalized(config)

        elif command == 'print_csv_denormalized':
            print_csv_denormalized()
        elif command == 'print_gviz_json_denormalized':
            print_gviz_json_denormalized()
        elif command == 'push_gspreadsheet_denormalized':
            push_gspreadsheet_denormalized()
