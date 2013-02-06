#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# Description:
# This script scans the AWS environment for environments that need to be
# shutdown.
#
# Version: 0.1
# Initial Release
##############################################################################

import os
import sys
import optparse
import time

from datetime import datetime

from boto.ec2.connection import EC2Connection as ec2
from boto.vpc import VPCConnection as vpc


class Job(object):
    def __init__(self, description, fn, *args, **kwargs):
        self.description = description
        if not callable(fn):
            raise ValueError("Not callable: %r" % fn)
        self.fn = fn
        self.fn_args = args
        self.fn_kwargs = kwargs

    def execute(self):
        return self.fn(*self.fn_args, **self.fn_kwargs)

    def __str__(self):
        return self.description

    __repr__ = __str__


def changeState(targetstate='stop', fromstate=None,  envTag='lab'):

    """
    targetstate = stop, start, destroy
    envTag = Lab, Daily, Temporary, Short Use
    """
    amazonTimeFormat = '%Y-%m-%dT%H:%M:%S.000z'

    filters = {}
    if fromstate:
        filters['instance-state-name'] = fromstate

    filters['tag:Environment'] = envTag
    selectedInstances = ec2conn.get_all_instances(filters=filters)

    instanceList = []

    for i in selectedInstances:
        dt1 = datetime.strptime(i.instances[0].launch_time, amazonTimeFormat)
        instanceRunTime = datetime.now() - dt1
        extraTime = int(i.instances[0].tags['ExtraTime'])
        if extraTime == 0:
            if instanceRunTime.seconds > 90:
                instanceList.append(i.instances[0].id)
        else:
            newTime = extraTime - 1
            ec2conn.create_tags([i.instances[0].id], {'ExtraTime': newTime})

    if instanceList:
        if targetstate == 'start':
            ec2conn.start_instances(instanceList)
        elif targetstate == 'stop':
            ec2conn.stop_instances(instanceList)
        elif targetstate == 'destroy':
            ec2conn.stop_instances(instanceList)
            #ec2conn.terminate_instances(i.instances[0].id)


def autoJob():

    #Environment Lables

    weekdayEnv = ['Lab', 'Daily']
    weekendEnv = 'Daily'
    tempEnv = 'Temporary'
    shortuseEnv = 'Short Use'

    jobsList = [
         Job('Weekday Night Job',
            changeState,
            targetstate='stop',
            fromstate='running',
            envTag=weekdayEnv),
         Job('Weekday Morning Job',
            changeState,
            targetstate='start',
            fromstate='stopped',
            envTag=weekdayEnv),
         Job('Weekend Night Job',
            changeState,
            targetstate='stop',
            fromstate='running',
            envTag=weekendEnv),
         Job('Weekend Morning Job',
            changeState,
            targetstate='start',
            fromstate='stopped',
            envTag=weekendEnv),
         Job('Temporary Destroy Job',
            changeState,
            targetstate='destroy',
            envTag=tempEnv),
         Job('Short Use Destroy Job',
            changeState,
            targetstate='destroy',
            envTag=shortuseEnv),
         ]

    weekday = False

    if time.strftime("%a").lower() in ['mon', 'tue', 'wed', 'thu', 'fri']:
        weekday = True

    if int(time.strftime("%H", time.gmtime())) == 4:
        if weekday:
            jobsList[0].execute()
        else:
            jobsList[2].execute()

        jobsList[4].execute()

    elif int(time.strftime("%H", time.gmtime())) == 14:
        if weekday:
            jobsList[1].execute()
        else:
            jobsList[3].execute()
    jobsList[5].execute()


def get_defaults():
    from ConfigParser import SafeConfigParser, DEFAULTSECT
    cfg = SafeConfigParser()
    cfg_file = os.path.expanduser("~/.zenoss_aws.cfg")
    if os.path.exists(cfg_file):
        # Fake out SafeConfigParser by writing a default section
        cfg_contents = "[%s]\n" % DEFAULTSECT
        with open(cfg_file) as f:
            cfg_contents += f.read()
        from cStringIO import StringIO
        cfg.readfp(StringIO(cfg_contents))

    def cfg_get(key, default=None):
        if cfg.has_option(DEFAULTSECT, key):
            return cfg.get(DEFAULTSECT, key)
        return default

    #
    # Option precedence:
    #
    #   Config File -> Environment -> Command-line Options
    #
    # in all cases except for the 'USER' env var, which will always be set so
    # we prefer the config file setting before looking at the USER env var.
    #
    env_get = os.environ.get
    return {
        'access_key': env_get('AWS_ACCESS_KEY', cfg_get('access_key')),
        'secret_key': env_get('AWS_SECRET_KEY', cfg_get('secret_key')),
    }


def parse_options():
    usage = """\
ZenossAWS.py [options...]

This utility is used to manage EC2 instances in the Zenoss AWS environment."""
    parser = optparse.OptionParser(usage=usage)
    defaults = get_defaults()
    parser.add_option("-a", "--aws-access-key", dest='aws_access_key',
                      default=defaults['access_key'],
                      help="AWS Access Key (environment variable: AWS_ACCESS_KEY)")
    parser.add_option("-s", "--aws-secret-key", dest='aws_secret_key',
                      default=defaults['secret_key'],
                      help="AWS Secret Key (environment variable: AWS_SECRET_KEY)")

    options, _ = parser.parse_args()
    # All options are required
    for option in parser.option_list:
        if not option.dest:
            continue
        if not getattr(options, option.dest, None):
            parser.print_help()
            print >> sys.stderr, "\nRequired option %s not specified" % option
            sys.exit(2)
    return options

if __name__ == '__main__':
    options = parse_options()
    ec2conn = ec2(options.aws_access_key, options.aws_secret_key)
    vpcconn = vpc(options.aws_access_key, options.aws_secret_key)
    try:
        autoJob()
    except (KeyboardInterrupt, EOFError):
        print
