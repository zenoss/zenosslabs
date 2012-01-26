#!/usr/bin/env python
import os
import pkg_resources

from bottle import abort, default_app, get, request, route, run, static_file


FILES_PATH = '/srv/zenpacks/files'

EXAMPLE_ZENOSS_VERSION = "3.2"
EXAMPLE_PLATFORM = 'linux-x86_64'
EXAMPLE_PYTHON = '2.7'

# Set defaults for Python version if Zenoss version is known.
PYTHON_VERSION_MAP = {
    '3.0': '2.6',
    '3.1': '2.6',
    '3.2': '2.6',
    '4.0': '2.6',
    '4.1': '2.7',
    '4.2': '2.7',
    }


@route('/')
def default():
    abort(404, "API endpoint not found. Try /download/<zenpack_name> instead.")


@get('/download/<name>')
def download(name=None):
    if not name:
        abort(400, "/<name> must be appended to the URL.")

    if not request.query.zenoss_version:
        abort(400,
            "Missing parameter: zenoss_version. Example: %s" % (
            EXAMPLE_ZENOSS_VERSION))

    zenoss_version_parts = request.query.zenoss_version.split('.') + ['0', '0']
    zenoss_version = '.'.join(zenoss_version_parts[:2])

    eggs_path = os.path.join(FILES_PATH, zenoss_version)
    if not os.path.isdir(eggs_path):
        abort(404,
            "No ZenPacks available for Zenoss %s" % (
            request.query.zenoss_version))

    if not request.query.platform:
        abort(400,
            "Missing parameter: platform. Example: %s" % EXAMPLE_PLATFORM)

    python_version = request.query.python
    if not python_version:
        python_version = PYTHON_VERSION_MAP.get(zenoss_version, None)

    if not python_version:
        abort(400,
            "Missing parameter: python. Example: %s" % EXAMPLE_PYTHON)

    environment = pkg_resources.Environment(
        search_path=[eggs_path],
        platform=request.query.platform,
        python=python_version)

    requirement = pkg_resources.Requirement.parse('ZenPacks.zenoss.CloudStack')
    working_set = pkg_resources.WorkingSet(entries=[eggs_path])
    package = environment.best_match(requirement, working_set)

    return static_file(
        os.path.basename(package.location),  # filename
        root=eggs_path,
        download=True)


if __name__ == '__main__':
    # For stand-alone operation.
    run(host='0.0.0.0', port=8888)
else:
    # For running under mod_wsgi.
    application = default_app()
