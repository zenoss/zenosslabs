#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger('zenpack.test')

import os
import sys

from subprocess import Popen, PIPE


class ShellError(Exception):
    pass


def shell(command):
    """Helper method to get the output from a command."""
    LOG.debug("Running '%s'", command)
    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()

    if stdout:
        LOG.debug("--- STDOUT ---")
        for line in stdout.split('\n'):
            LOG.debug(line)

    if stderr:
        LOG.debug("--- STDERR ---")
        for line in stderr.split('\n'):
            LOG.debug(line)

    if p.returncode != 0:
        raise ShellError("'%s' returned non-zero exit status %s" % (
            command, p.returncode))

    return stdout


class ZenossManager(object):
    def setup(self, zenoss_configuration):
        self.tear_down()

        try:
            shell("sudo /sbin/service mysqld start")
            shell("sudo /sbin/service zends start")
        except ShellError:
            pass

        lv_name = "zenoss/%s" % zenoss_configuration
        lv_device = "/dev/%s" % lv_name

        if not os.path.exists(lv_device):
            raise Exception("%s doesn't exist." % lv_device)

        try:
            shell("sudo /usr/sbin/lvcreate -l25%%ORIGIN -s -n sandbox %s" % lv_name)
        except ShellError:
            pass

        try:
            shell("sudo mount /dev/zenoss/sandbox /opt/zenoss")
            shell("sudo /sbin/service zenoss start")
        except ShellError, ex:
            LOG.error(ex)

    def tear_down(self):
        commands = (
            "sudo /sbin/service zenoss stop",
            "sudo umount /opt/zenoss",
            "sudo /usr/sbin/lvremove -f zenoss/sandbox",
            )

        for command in commands:
            try:
                shell(command)
            except ShellError:
                pass


class ZenPackBuilder(object):
    zenpack_name = None
    zenpack_directory = None

    def __init__(self):
        self.zenpack_directory = os.getcwd()
        self.zenpack_name = os.path.basename(self.zenpack_directory)

    def run_all(self):
        self.build_egg()

        self.test_install()
        self.test_unittests()

    def build_egg(self):
        try:
            shell("sudo chown -R zenoss:jenkins .")
            shell("sudo rm -Rf build dist *.egg-info")
            shell("sudo -u zenoss -i 'cd %s ; python setup.py bdist_egg'" % (
                self.zenpack_directory))

            shell("sudo -u zenoss -i mkdir -p /opt/zenoss/zenpack_eggs")
            shell("sudo mv dist/*.egg /opt/zenoss/zenpack_eggs/")
        except ShellError, ex:
            LOG.error(ex)

    def test_install(self):
        try:
            shell(
                "sudo -u zenoss -i zenpack --install "
                "/opt/zenoss/zenpack_eggs/%s-*.egg" % (
                    self.zenpack_name))
        except ShellError, ex:
            LOG.error(ex)

    def test_unittests(self):
        try:
            # TODO: Move to nose. It's ridiculously faster and feature-rich.
            # shell(
            #     "sudo -u zenoss -i nosetests --nologcapture -w %s %s.tests" % (
            #     self.zenpack_name, self.zenpack_name))

            shell("sudo -u zenoss -i runtests %s" % self.zenpack_name)
        except ShellError, ex:
            LOG.error(ex)


def main():
    build_tag = os.environ.get('BUILD_TAG', None)
    if not build_tag:
        print >> sys.stderr, "BUILD_TAG environment variable not set."
        sys.exit(1)

    build_labels = dict(
        x.split('=') for x in build_tag.split('-')[1].split(','))

    zenoss_configuration = build_labels.get('zenoss_configuration', None)
    if not zenoss_configuration:
        print >> sys.stderr, "BUILD_TAG doesn't contain zenoss_configuration."
        sys.exit(1)

    if not os.path.isfile('setup.py'):
        print >> sys.stderr, "setup.py doesn't exist."
        sys.exit(1)

    zman = ZenossManager()
    zman.setup(zenoss_configuration)

    try:
        tester = ZenPackBuilder()
        tester.run_all()
    finally:
        zman.tear_down()


if __name__ == '__main__':
    main()
