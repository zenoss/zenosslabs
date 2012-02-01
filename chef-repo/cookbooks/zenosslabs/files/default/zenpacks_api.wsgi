#!/usr/bin/env python
import os
import pkg_resources

from bottle import (
    abort, debug, default_app, get, request, route, run, static_file,
    )


FILES_PATH = '/srv/zenpacks/files'

EXAMPLE_ZENOSS_VERSION = "3.2"
EXAMPLE_PLATFORM = 'linux-x86_64'
EXAMPLE_PYTHON = '2.7'
EXAMPLE_QUERY = 'OpenStack'

# Set defaults for Python version if Zenoss version is known.
PYTHON_VERSION_MAP = {
    '3.0': '2.6',
    '3.1': '2.6',
    '3.2': '2.6',
    '4.0': '2.6',
    '4.1': '2.7',
    '4.2': '2.7',
    }


class APIException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class ZenPackEnvironment(object):
    zenoss_version = None
    platform = None
    python = None

    # pkg_resources stuff
    environment = None
    working_set = None

    def __init__(self, zenoss_version, platform, python=None, key=None):
        if not zenoss_version:
            raise APIException(
                400, "Missing parameter: zenoss_version. Example: %s" % (
                    EXAMPLE_ZENOSS_VERSION))
        else:
            zenoss_version_parts = \
                request.query.zenoss_version.split('.') + ['0', '0']

            self.zenoss_version = '.'.join(zenoss_version_parts[:2])

        eggs_path = os.path.join(FILES_PATH, zenoss_version)
        if not os.path.isdir(eggs_path):
            abort(404, "No ZenPacks available for Zenoss %s" % (
                request.query.zenoss_version))

        if not platform:
            raise APIException(
                400, "Missing parameter: platform. Example: %s" % (
                    EXAMPLE_PLATFORM))
        else:
            self.platform = platform

        if not python:
            self.python = PYTHON_VERSION_MAP.get(self.zenoss_version, None)

            if not self.python:
                raise APIException(
                    400, "Missing parameter: python. Example: %s" % (
                        EXAMPLE_PYTHON))

        self.environment = pkg_resources.Environment(
            search_path=[eggs_path],
            platform=self.platform,
            python=self.python)

        egg_paths = (os.path.join(eggs_path, x) \
            for x in os.listdir(eggs_path) if x.endswith('.egg'))

        self.working_set = pkg_resources.WorkingSet(entries=egg_paths)

    def search(self, query):
        for ep in self.working_set.iter_entry_points('zenoss.zenpacks'):
            if query in ep.name:
                yield ep.name

    def best_match(self, requirement):
        return self.environment.best_match(requirement, self.working_set)

    @classmethod
    def from_query(cls, query):
        return ZenPackEnvironment(
            query.zenoss_version,
            query.platform,
            query.python,
            query.key)


@route('/')
def default():
    abort(404, "API endpoint not found.")


@route('/search')
def search():
    if not request.query.query:
        abort(400, "Missing parameter: query. Example: %s" % (EXAMPLE_QUERY))

    try:
        env = ZenPackEnvironment.from_query(request.query)
    except APIException, ex:
        abort(ex.code, ex.message)

    return {
        'result': list(env.search(request.query.query)),
        }


@get('/download/<name>')
def download(name=None):
    if not name:
        abort(400, "/<name> must be appended to the URL.")

    try:
        env = ZenPackEnvironment.from_query(request.query)
    except APIException, ex:
        abort(ex.code, ex.message)

    requirement = pkg_resources.Requirement.parse(name)
    package = env.best_match(requirement)

    if not package:
        abort(404, "No ZenPack found meeting your criteria.")

    return static_file(
        os.path.basename(package.location),
        root=os.path.dirname(package.location),
        download=True)


@get('/resolve/<name>')
def resolve(name=None):
    if not name:
        abort(400, "/<name> must be appended to the URL.")

    try:
        env = ZenPackEnvironment.from_query(request.query)
    except APIException, ex:
        abort(ex.code, ex.message)

    dependencies = []

    requirement = pkg_resources.Requirement.parse(name)
    for egg in env.working_set.resolve([requirement]):
        dependencies.append(egg.project_name)

    return {'result': dependencies}


if __name__ == '__main__':
    # For stand-alone operation.
    debug(True)
    run(host='0.0.0.0', port=8888)
else:
    # For running under mod_wsgi.
    application = default_app()
