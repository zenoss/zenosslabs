#! /usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# Description:
# The purpose of this script is to offer basic AWS interaction for users.
#
# Version: 0.1
##############################################################################

import os
import sys
import time

from boto.ec2.connection import EC2Connection as ec2
from boto.vpc import VPCConnection as vpc


# Check to confirm critical information is set in environment
try:
    awsAccessKey = os.environ['AWS_ACCESS_KEY']
    awsSecretKey = os.environ['AWS_SECRET_KEY']
    username = os.environ['USER']
    customer = os.environ['DEPARTMENT']
    awsKeyName = os.environ['AWS_KEY_NAME']

except KeyError as envNotSet:
    print "\n" * 3
    print "******* ERROR *********"
    print "The following environment variables MUST be set"
    print ""
    print "AWS_ACCESS_KEY"
    print "AWS_SECRET_KEY"
    print "USER"
    print "DEPARTMENT"
    print "AWS_KEY_NAME"
    print ""
    print "Error Results:"
    print str(envNotSet)
    print "Not Set"
    sys.exit()

# List of AMI offered to user.
# Feel free to add more AMIs here
amiList = {
    1: ('Ubuntu Server 12.04.1 LTS', 'ami-3d4ff254'),
    2: ('Red Hat Enterprise Linux 6.3', 'ami-cc5af9a5'),
    }

# Limited list of instance types available. Many more exists but haven't been added here.
instanceList = {
    1: ('Micro', 't1.micro'),
    2: ('Small', 'm1.small'),
    3: ('Medium', 'm1.medium'),
    4: ('Large', 'm1.large'),
    }

envList = {
    1: ('Lab', 'Turn off every night at 8pm CST. No Weekend'),
    2: ('Production', 'Never turn off'),
    3: ('Temp', 'Destory at 8pm CST. *WARNING* Data will be lost'),
    4: ('Daily', 'Turn off every night at 8pm CST. Startup on Weekends')
    }

# List of jobs user can execute
jobsList = {
    1: 'List my instances',
    2: 'Stop my %s instances now' % (envList[1][0]),
    3: 'Start my %s instances now' % (envList[1][0]),
    4: 'Create new instance',
    5: 'Destroy instance',
    6: 'Exit',
    }

ec2conn = ec2(awsAccessKey, awsSecretKey)
vpcconn = vpc(awsAccessKey, awsSecretKey)


def listAll():
    filters = {'tag:Owner': username}
    getList = ec2conn.get_all_instances(filters=filters)

    print "*" * 60
    print "All instances that belong to %s" % (username)
    print "\n" * 3
    print "LINE -- NAME -- RUNNING STATE -- PRIVATE IP -- ENVIRONMENT"
    print ""
    instanceList = []
    intLineNumber = 1
    for i in getList:
        instanceList.append(i)
        print "%s -- %s -- %s -- %s -- %s" % (intLineNumber, i.instances[0].__dict__['tags']['Name'],
                                i.instances[0].state, i.instances[0].private_ip_address,
                                i.instances[0].__dict__['tags']['Environment'])
        intLineNumber += 1

    print "\n" * 3
    return instanceList


def destroy():

    instanceList = listAll()
    valid = False
    while valid == False:
        getDestroy = raw_input("What instance would you like to destroy? ")
        try:
            getDestroy = int(getDestroy)
            getDestroy = getDestroy - 1
            valid = True
            print "You want to destroy %s" % (instanceList[getDestroy].instances[0].__dict__['tags']['Name'])
            getConfirm = raw_input("Is this correct? Yes or No \"NOTE: You must spell Yes out exactly if you want to destroy\"")
            if getConfirm == 'Yes':
                ec2conn.terminate_instances(instanceList[getDestroy].instances[0].id)
                listAll()
        except:
            pass


def changeRunningState(state, status):

    filters = {'tag:Environment': envList[status][0], 'tag:Owner': username}
    getList = ec2conn.get_all_instances(filters=filters)

    idList = []

    for i in getList:
        idList.append(i.instances[0].id)

    if state == "start":
        getList = ec2conn.start_instances(idList)
    elif state == "stop":
        getList = ec2conn.stop_instances(idList)
    listAll()


def deploy():
    awsSecGroups = ec2conn.get_all_security_groups()

    valid = False

    #Instance Name
    while valid == False:
        getName = raw_input("What name would you like to assign to this instance? ")
        if len(getName) > 1:
            valid = True
    print "\n" * 3

    #Environment
    intLineNumber = 1
    for i in envList:
        print "%s - %s - %s" % (str(intLineNumber), envList[i][0], envList[i][1])
        intLineNumber += 1

    print "\n" * 2
    valid = False
    while valid == False:
        getEnv = raw_input("How do you classify this machine? ")
        try:
            getEnv = int(getEnv)
            if getEnv < intLineNumber:
                valid = True
        except:
            pass

    print "\n" * 5

    #AMI
    intLineNumber = 1
    for i in amiList:
        print "%s - %s" % (str(intLineNumber), amiList[i][0])
        intLineNumber += 1

    print "\n" * 2
    valid = False
    while valid == False:
        getAMI = raw_input("What image would you like to deploy? ")
        try:
            getAMI = int(getAMI)
            if getAMI < intLineNumber:
                valid = True
        except:
            pass

    print "\n" * 5

    #Instance Type
    intLineNumber = 1
    for i in instanceList:
        print "%s - %s" % (str(intLineNumber), instanceList[i][0])
        intLineNumber += 1
    print "\n" * 2
    valid = False
    while valid == False:
        getInstance = raw_input("What size instance would you like to deploy? ")
        try:
            getInstance = int(getInstance)
            if getInstance < intLineNumber:
                valid = True
        except:
            pass

    print "\n" * 5

    #Security Groups
    intLineNumber = 1
    secgroupList = []
    for i in awsSecGroups:
        if i.name != 'default':
            secgroupList.append(i)
            print "%s - %s \"%s\"" % (str(intLineNumber), i.name, i.description)
            intLineNumber += 1
    print "\n" * 2
    valid = False
    while valid == False:
        getSecGroup = raw_input("What Security Group would you like to assign to this instance? ")
        try:
            getSecGroup = int(getSecGroup)
            if getSecGroup < intLineNumber:
                valid = True
        except:
            pass

    vpcID = secgroupList[int(getSecGroup) - 1].vpc_id
    print "\n" * 5

    #VPC Subnets
    awsSubnets = vpcconn.get_all_subnets(filters={'vpcId': vpcID})
    intLineNumber = 1
    subnetList = []
    for i in awsSubnets:
        if i.available_ip_address_count > 0:
            subnetList.append(i)
            print "%s - %s \"%s\"" % (str(intLineNumber), i.id, i.cidr_block)
            intLineNumber += 1
    print "\n" * 2
    valid = False
    while valid == False:
        getSubnet = raw_input("What Subnet would you like to assign this instance? ")
        try:
            getSubnet = int(getSubnet)
            if getSubnet < intLineNumber:
                valid = True
        except:
            pass

    print "\n" * 5

    #Deploy new instance
    print awsKeyName
    sendSecGroupID = str(secgroupList[int(getSecGroup) - 1].id)
    sendInstanceID = str(instanceList[int(getInstance)][1])
    sendSubnet = str(subnetList[int(getSubnet) - 1].id)
    sendAMI = amiList[int(getAMI)][1]

    print sendAMI
    print sendSecGroupID
    print sendInstanceID
    print sendSubnet

    newInstance = ec2conn.run_instances(image_id=sendAMI,
            key_name=awsKeyName,
            instance_initiated_shutdown_behavior='stop',
            security_group_ids=[sendSecGroupID],
            instance_type=sendInstanceID,
            subnet_id=sendSubnet)

    print "Working... Please wait"
    time.sleep(4)

    newTags = {
        'Name': getName,
        'Environment': envList[int(getEnv)][0],
        'Customer': customer,
        'Owner': username
        }

    newInstanceID = newInstance.instances[0].id
    #ec2conn.modify_instance_attribute(newInstanceID, attribute='groupSet', value=['sg-8b6c9de4'])
    tagresult = ec2conn.create_tags(newInstanceID, newTags)

    if tagresult:
        print "\n" * 5
        print "*" * 60
        print ""
        print "Your instance has been deployed. It may take a few minutes before you can login."
        print "The IP Address of your instance is: %s" % (newInstance.instances[0].private_ip_address)
        print "The public key that was used is: %s" % (newInstance.instances[0].key_name)
    else:
        print "We had a problem creating your instance. Not sure what happened so you will need to contact the Zenoss AWS Administrator for your department."


def jobList():
    print "*" * 60
    print "\n"

    intLineNumber = 1
    for i in jobsList:
        print "%s - %s" % (str(intLineNumber), jobsList[i])
        intLineNumber += 1

    print "\n" * 2
    valid = False
    while valid == False:
        strJob = raw_input("What would you like to do? ")
        try:
            strJob = int(strJob)
            if strJob < intLineNumber:
                valid = True
        except:
            pass

    if strJob == 1:
        #List my instances
        listAll()

    elif strJob == 2:
        #Shutdown all my instances
        changeRunningState("stop", 1)

    elif strJob == 3:
        #Start my Lab instances
        changeRunningState("start", 1)

    elif strJob == 4:
        #Deploy New Instance
        deploy()

    elif strJob == 5:
        #Destory Instance
        destroy()

    elif strJob == 6:
        #Exit Script
        sys.exit()
    jobList()


jobList()
