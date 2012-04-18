#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('zenpacks')

import os
import pkg_resources

from flask import Flask, abort, render_template, request, send_from_directory
from flaskext.xmlrpc import XMLRPCHandler


# Create Flask application.
app = Flask(__name__)

# These IP addresses are allowed to download private ZenPacks.
IP_WHITELIST = [
    '204.12.99.193',  # ZenPack Build Farm & artifacts.zenoss.loc
    ]

# Set defaults for Python version if Zenoss version is known.
PYTHON_VERSION_MAP = {
    '3.0': '2.6',
    '3.1': '2.6',
    '3.2': '2.6',
    '4.0': '2.6',
    '4.1': '2.7',
    '4.2': '2.7',
    }

# Zenoss uses a "prior-version.70" notation for beta releases.
BETA_VERSION_MAP = {
    '2.5.70': '3.0.0',
    '3.0.70': '3.1.0',
    '3.1.70': '4.0.0',
    '4.0.70': '4.1.0',
    '4.1.70': '4.2.0',
    }


PUBLIC_EGGS_PATH = '/srv/zenpacks/files/eggs'
PRIVATE_EGGS_PATH = '/srv/zenpacks/files/private_eggs'


###############################################################################

def matching_projects(key=None, zenoss_version=None):
    """Returns projects compatible with the passed parameters."""

    distributions = matching_distributions(
        key=key,
        zenoss_version=zenoss_version)

    projects = set()
    for distribution in distributions:
        projects.add(distribution.project_name)

    return list(projects)


def matching_releases(key=None, zenoss_version=None, project=None):
    """Returns releases compatible with the passed parameters."""

    distributions = matching_distributions(
        key=key,
        zenoss_version=zenoss_version,
        project=project)

    releases = []
    for distribution in distributions:
        releases.append((distribution.project_name, distribution.version))

    return releases


def matching_distributions(
    key=None, zenoss_version=None, platform=None, python=None, project=None,
    version=None):
    """Yields distributions compatible with the passed parameters.

    All parameters are optional and should be used to filter the full list
    of distributions.
    """

    # Python version can be inferred from Zenoss version.
    if zenoss_version and not python:
        zenoss_version = BETA_VERSION_MAP.get('zenoss_version', zenoss_version)
        z_major = '.'.join(zenoss_version.split('.')[:2])
        python = PYTHON_VERSION_MAP.get(z_major, None)

    search_path = [PUBLIC_EGGS_PATH]

    if request.remote_addr in IP_WHITELIST:
        search_path.append(PRIVATE_EGGS_PATH)

    environment = pkg_resources.Environment(
        search_path=search_path,
        platform=platform,
        python=python)

    for key in environment:
        if not key.startswith('zenpacks.'):
            continue

        if project and key != project.lower():
            continue

        for distribution in environment[key]:
            if version:
                requirement = pkg_resources.Requirement.parse(
                    "%s == %s" % (project, version))

                if distribution.version not in requirement:
                    continue

            if not zenoss_version:
                yield distribution
                continue

            # If the ZenPack doesn't have zenpack_info metadata, it can't define
            # compatZenossVers. We must assume it is compatible with all Zenoss
            # versions.
            if not distribution.has_metadata('zenpack_info'):
                yield distribution
                continue

            # Assume compatibility with the requested Zenoss version unless the
            # next loop finds this to not be the case.
            z_compatible = True

            # get_metadata can raise exceptions for improperly-formatted or
            # corrupt eggs.
            zenpack_info = None

            try:
                zenpack_info = distribution.get_metadata('zenpack_info')
            except Exception:
                continue

            for line in pkg_resources.yield_lines(zenpack_info):
                key, value = map(str.strip, line.split(':', 1))
                if key == 'compatZenossVers':
                    z_requirement = pkg_resources.Requirement.parse(
                        "Zenoss %s" % value)

                    if zenoss_version not in z_requirement:
                        z_compatible = False

            # Select the distribution unless it was found to be incompatible
            # with the requested Zenoss version.
            if z_compatible:
                yield distribution
                continue


def html_projects_list(key, zenoss_version, projects):
    """PyPI-compatible HTML listing of projects."""

    links = []
    for project in sorted(projects):
        links.append('<a href="/pypi/%s/%s/%s">%s</a>' % (
            key, zenoss_version, project, project))

    if len(links) < 1:
        abort(404)

    return render_template('zenpacks_list.html', title='ZenPacks', items=links)


def html_releases_list(key, zenoss_version, releases):
    """PyPI-compatible HTML listing of releases for a project."""

    links = []
    for project, version in sorted(releases, reverse=True):
        links.append('<a href="/pypi/%s/%s/%s/%s">%s %s</a>' % (
            key, zenoss_version, project, version, project, version))

    if len(links) < 1:
        abort(404)

    return render_template('zenpacks_list.html', title='Releases', items=links)


def html_eggs_list(key, filenames):
    """PyPI-compatible HTML listing of projects."""

    links = []
    for filename in sorted(filenames):
        links.append(
            '<a href="/pypi/eggs/%(key)s/%(filename)s">%(filename)s</a>' % {
            'key': key,
            'filename': os.path.basename(filename)})

    if len(links) < 1:
        abort(404)

    return render_template('zenpacks_list.html', title='Eggs', items=links)


### PyPI Indexes ##############################################################

@app.route('/pypi/<key>/<zenoss_version>/')
def pypi_index(key=None, zenoss_version=None):
    """PyPI-compatible index page."""

    return html_projects_list(key, zenoss_version, matching_projects(
        key=key, zenoss_version=zenoss_version))


@app.route('/pypi/<key>/<zenoss_version>/<project>/')
def pypi_project_index(key=None, zenoss_version=None, project=None):
    """PyPI-compatible project index page."""

    return html_releases_list(key, zenoss_version, matching_releases(
        key=key, zenoss_version=zenoss_version, project=project))


@app.route('/pypi/<key>/<zenoss_version>/<project>/<version>/')
def pypi_project_version(key=None, zenoss_version=None, project=None, version=None):
    """PyPI-compatible project version index page."""

    distributions = matching_distributions(
        zenoss_version=zenoss_version,
        project=project,
        version=version)

    return html_eggs_list(key, (d.location for d in distributions))


### PyPI Eggs #################################################################

@app.route('/pypi/eggs/<key>/<filename>')
def download(key=None, filename=None):
    return send_from_directory(PUBLIC_EGGS_PATH, filename, as_attachment=True)


### PyPI XML-RPC API ##########################################################

handler = XMLRPCHandler('xmlrpc')
handler.connect(app, '/')


@handler.register
def search(spec=None, operator=None):
    """PyPI-compatible XML-RPC search API endpoint."""

    results = []
    for distribution in matching_distributions():
        for spec_name in spec['name']:
            if spec_name.lower() in distribution.key:
                results.append({
                    'name': distribution.project_name,
                    'version': distribution.version,
                    'summary': 'No summary for project.',
                    '_pypi_ordering': 100,
                    })

    return results


### Custom API ################################################################

@app.route('/api/download/<zenpack>')
def api_download(zenpack=None):
    """Custom API download for ZenPack build system."""

    search_path = [PUBLIC_EGGS_PATH]

    if request.remote_addr in IP_WHITELIST:
        search_path.append(PRIVATE_EGGS_PATH)

    zenoss_version = request.args.get('zenoss_version', None)
    platform = request.args.get('platform', None)
    python = request.args.get('python', None)

    if not zenoss_version or not platform or not python:
        abort(400)

    environment = pkg_resources.Environment(
        search_path=search_path,
        platform=platform,
        python=python)

    requirement = pkg_resources.Requirement.parse(zenpack)
    distribution = environment.best_match(
        requirement, pkg_resources.WorkingSet())

    if not distribution:
        abort(404)

    return send_from_directory(
        os.path.dirname(distribution.location),
        os.path.basename(distribution.location),
        as_attachment=True)


###############################################################################

if __name__ == '__main__':
    # For stand-alone operation.
    app.run(host='0.0.0.0', port=8888, debug=True)
else:
    # For WSGI operation.
    application = app
