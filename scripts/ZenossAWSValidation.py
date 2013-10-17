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
import hashlib
import hmac
import base64
import urllib
import site
import datetime

from twisted.web.client import getPage

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
except ImportError:
    print "The boto module is not installed. Please install it and try to execute this method again"
    sys.exit(2)


def iso8601(seconds_ago=0):
    '''
    Return a ISO8601 date and time representation of now adjusted by
    seconds_ago in UTC.
    '''
    utcnow = datetime.datetime.utcnow()
    if seconds_ago == 0:
        utc = utcnow
    else:
        utc = utcnow - datetime.timedelta(seconds=seconds_ago)

    return utc.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def awsUrlSign(
        httpVerb='GET',
        hostHeader=None,
        uriRequest="/",
        httpRequest=None,
        awsKeys=None):

    """
    Method that will take the URL requst and provide a signed
    API query string.

    httpVerb = GET, PUT, POST
    hostHeader - example: monitoring.us-east-1.amazonaws.com
    uriRequest - example: /client/api (default / )
    httpRequest - example: {'Action': 'ListMetrics', ...}
    awsKeys - example: ('MYACCESSKEY', 'MYSECRETKEY')
    """

    # Set time of request for key signing
    httpRequest['Timestamp'] = iso8601()

    accesskey = awsKeys[0]
    secretkey = awsKeys[1]

    httpRequest['AWSAccessKeyId'] = accesskey

    # The query string needs to be url encoded prior to signing
    queryString = urllib.urlencode(httpRequest)

    # The query string needs to be in byte order
    splitQuery = queryString.split('&')
    splitQuery.sort()

    # Now rejoin key/values for query string to sign
    new_query_line = '&'.join(splitQuery)

    signme = '\n'.join([httpVerb, hostHeader, uriRequest, new_query_line])

    # Get key signing has setup.
    new_hmac = hmac.new(secretkey, digestmod=hashlib.sha256)
    new_hmac.update(signme)

    sig = {'Signature': base64.b64encode(new_hmac.digest())}

    signature = urllib.urlencode(sig)

    return '%s/?%s&%s' % (hostHeader, new_query_line, signature)


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
        instancelist = ec2conn.get_all_instances()
        print "You have {0} instances".format(len(instancelist))
        print "A secure connection has been made to AWS"
    except:
        print "Sorry a secure connection has failed"
        try:
            ec2conn = ec2(
                aws_access_key_id=options.aws_access_key,
                aws_secret_access_key=options.aws_secret_key,
                is_secure=False)
            instancelist = ec2conn.get_all_instances()
            print "You have {0} instances".format(len(instancelist))
            print "A non-secure connection has been made to AWS"
        except:
            try:
                httpVerb = 'GET'
                uriRequest = '/'

                baseRequest = {}
                baseRequest['SignatureMethod'] = 'HmacSHA256'
                baseRequest['SignatureVersion'] = '2'
                baseRequest['Action'] = 'DescribeInstances'
                baseRequest['Version'] = '2012-12-01'

                hostHeader = 'ec2.us-eas-1.amazonaws.com'

                getURL = awsUrlSign(
                    httpVerb,
                    hostHeader,
                    uriRequest,
                    baseRequest,
                    (options.aws_access_key, options.aws_secret_key))
                getURL = 'http://%s' % getURL
                result = getPage(getURL)
                print result
            except:
                print "Sorry no connection is possible to AWS"
                sys.exit(2)
