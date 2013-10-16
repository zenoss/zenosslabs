#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# Description:
# The purpose of this script is to offer connection testing and validation to
# Amazon Web Services
#
##############################################################################

import os
import sys
import optparse
import site

try:
    try:
        zenhome = os.environ['ZENHOME']
        if zenhome:
            # Try to import boto from AWS ZenPack
            zenawspath = "{0}/ZenPacks/ZenPacks.zenoss.AWS-2.0.0.egg/ZenPacks/zenoss/AWS/lib".format(zenhome)
            site.addsitedir(zenawspath)
    except KeyError:
        print "The ZENHOME environment variable does not exists"
    from boto.ec2.connection import EC2Connection as ec2
    from boto.exception import EC2ResponseError as ec2err
except ImportError:
    print "The boto module is not installed. Please install it and try to execute this method again"
    sys.exit(2)


def parse_options():
    usage = """\
ZenossAWSValidation.py [options...]

This utility is used to validate AWS environment connections."""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-a", "--aws-access-key", dest='aws_access_key',
                      help="AWS Access Key (environment variable: AWS_ACCESS_KEY)")
    parser.add_option("-s", "--aws-secret-key", dest='aws_secret_key',
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
    try:
        ec2conn = ec2(
                aws_access_key_id=options.aws_access_key,
                aws_secret_access_key=options.aws_secret_key,
                is_secure=True)
        print "A secure connection has been made to AWS"
    except:
        print "Sorry a secure connection has failed"
        try:
            ec2conn = ec2(
                aws_access_key_id=options.aws_access_key,
                aws_secret_access_key=options.aws_secret_key,
                is_secure=False)
            print "A non-secure connection has been made to AWS"
        except:
            print "Sorry no connection is possible to AWS"
            sys.exit(2)

    try:
        instancelist = ec2conn.get_all_instances()
        print "You have {0} instances".format(len(instancelist))
    except ec2err as e:
        print "You have the following error {0}".format(e)
    print "Script has completed"
