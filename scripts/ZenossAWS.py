#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# Description:
# The purpose of this script is to offer basic AWS interaction for users.
#
# Version: 0.3
# Added Create AMI Image of instance.
# Added command line arguments
#   list = Will list all instances then exit
#
#
#
# Version: 0.2
# 5 - Stop/Start fail when no instances
# 10 - Filter out Terminated instances
# 6 - Error when trying to start/stop with terminated instances
# 3 - Can't cancel out of destroy screen
# 7 - Need to allow single instance start/stop
#
# Version: 0.1
# Initial Release
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
    sys.exit(1)

# List of AMI offered to user.
# Feel free to add more AMIs here
AMI_LIST = (
    ('Ubuntu Server 12.04.1 LTS', 'ami-3d4ff254'),
    ('Red Hat Enterprise Linux 6.3', 'ami-cc5af9a5'),
)

# Limited list of instance types available. Many more exists but haven't been added here.
INSTANCE_LIST = (
    ('Micro', 't1.micro'),
    ('Small', 'm1.small'),
    ('Medium', 'm1.medium'),
    ('Large', 'm1.large'),
)

ENV_LIST = (
    ('Production', 'Never turn off'),
    ('Daily', 'Turn off every night at 8pm CST. Startup on Weekends'),
    ('Lab', 'Turn off every night at 8pm CST. No Weekend'),
    ('Temporary', 'Destroy at 8pm CST. *WARNING* Data will be lost'),
    ('Short Use', 'Destroy after an hour of run time. *WARNING* Data will be lost')
)

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

ec2conn = ec2(awsAccessKey, awsSecretKey)
vpcconn = vpc(awsAccessKey, awsSecretKey)

def promptVal(prompt, convert_fn=None, valid_fn=None, exit_values=()):
    """
    Prompts for a value from stdin. Uses convert_fn to convert
    the value to another format. If valid_fn is specified, it
    is passed the converted value to determine if the value is
    valid. If the value is invalid, it is discarded and the user
    is prompted again. If exit_values is specified, it contains
    a list of (lowercase) values which can short-circuit the loop
    and cause promptVal to return None. Returns the converted value
    from stdin, or None if the input matched exit_values.
    """
    if not valid_fn:
        valid_fn = lambda x: True
    if not convert_fn:
        convert_fn = lambda x: x
    while True:
        input = raw_input(prompt)
        if input.lower() in exit_values:
            return None
        value = convert_fn(input)
        if valid_fn(value):
            return value

def promptInt(prompt, min_val=None, max_val=None, **kwargs):
    """
    Prompts for an integer value from stdin. If min_val is
    specified, the value must be greater or equal to the
    specified value. If max_val is specified, the value must
    be less than the specified value. Returns the value from
    the user converted to an int.
    """
    def valid_int_range(val):
        return (min_val is None or val >= min_val) and \
               (max_val is None or val < max_val)
    kwargs['convert_fn'] = int
    kwargs['valid_fn'] = valid_int_range
    return promptVal(prompt, **kwargs)

def promptList(prompt, list_val, **kwargs):
    """
    Prompts for a choice in a list. Returns the list item at the selected
    index.

    :param prompt: Prompt to show the user.
    :param list_val: The list that the user should select from.
    :param kwargs: Arguments to promptVal.
    :return: object or None
    """
    index_offset = 1
    kwargs['min_val'] = index_offset
    kwargs['max_val'] = len(list_val) + index_offset
    index_val = promptInt(prompt, **kwargs)
    if index_val is not None:
        return list_val[index_val - index_offset]

def promptListMultiple(prompt, list_val, **kwargs):
    """
    Prompts for multiple selections in a list. Returns the list items at
    the selected index.

    :param prompt: Prompt to show the user.
    :param list_val: The list the user should select from.
    :param kwargs: Arguments to promptVal.
    :return: A list of selected values or None.
    """
    index_offset = 1
    def valid_indexes(val):
        for idx in val:
            if idx < index_offset or idx >= len(list_val) + index_offset:
                return False
        return True
    kwargs['convert_fn'] = lambda x: set(map(int, x.split(',')))
    kwargs['valid_fn'] = valid_indexes
    selected_idxs = promptVal(prompt, **kwargs)
    if selected_idxs is not None:
        return [list_val[idx - index_offset] for idx in selected_idxs]

def enumerate_with_offset(iterable, offset=1):
    for i, val in enumerate(iterable):
        yield i+offset, val

def listAll(state=None, status=None):
    #state = State of machine pending | running | shutting-down | terminated | stopping | stopped
    #status = Environment Tag value instance deployed to

    filters = {'tag:Owner': username}
    if status:
        filters.update({'tag:Environment': ENV_LIST[status][0]})
    if state:
        filters.update({'instance-state-name': state})

    instanceList = ec2conn.get_all_instances(filters=filters)

    print "*" * 60
    print "All instances that belong to %s" % username
    print "\n" * 3
    print "LINE -- NAME -- RUNNING STATE -- PRIVATE IP -- ENVIRONMENT"
    print ""
    for i, instance in enumerate_with_offset(instanceList):
        if instance.instances[0].state != 'terminated':
            print "%s -- %s -- %s -- %s -- %s" % (i, instance[0].tags['Name'],
                                instance[0].state, instance[0].private_ip_address,
                                instance[0].tags['Environment'])

    print "\n" * 3
    return instanceList


def destroy():
    instanceList = listAll()
    print "Or Type \"EXIT\" to quit"

    instance = promptList("What instance would you like to destroy? ",
                          instanceList, exit_values=('exit',))
    if instance is None:
        return

    print "You want to destroy %s" % instance.instances[0].tags['Name']
    getConfirm = raw_input("Is this correct? Yes or No \"NOTE: You must spell Yes out exactly if you want to destroy\"")
    if getConfirm == 'Yes':
        ec2conn.terminate_instances(instance.instances[0].id)
        listAll()


def changeRunningState(targetstate, fromstate=None, status=None, instanceID=None):
    #state = State of machine pending | running | shutting-down | terminated | stopping | stopped
    #status = Environment Tag value instance deployed to
    #instanceID = List of instance id

    filters = {'tag:Owner': username}
    if status:
        filters['tag:Environment'] = ENV_LIST[status][0]
    if fromstate:
        filters['instance-state-name'] = fromstate

    if instanceID:
        getList = ec2conn.get_all_instances(instance_ids=instanceID, filters=filters)
    else:
        getList = ec2conn.get_all_instances(filters=filters)

    idList = [i.instances[0].id for i in getList]
    if idList:
        if targetstate == "start":
            ec2conn.start_instances(idList)
        elif targetstate == "stop":
            ec2conn.stop_instances(idList)
    listAll()


def selectInstances(targetstate, fromstate=None, status=None):
    #state = State of machine pending | running | shutting-down | terminated | stopping | stopped
    #status = Environment Tag value instance deployed to

    if fromstate:
        instanceList = listAll(state=fromstate)
    elif fromstate and status:
        instanceList = listAll(state=fromstate, status=status)
    elif status:
        instanceList = listAll(status=status)
    else:
        instanceList = listAll()

    print "Or Type \"EXIT\" to quit"

    selectedInstances = promptListMultiple("Which instances would you like to %s? " % targetstate,
                                           instanceList)
    if selectedInstances:
        instance_ids = [instance.instances[0].id for instance in selectedInstances]
        if status:
            changeRunningState(targetstate=targetstate, status=status, instanceID=instance_ids)
        else:
            changeRunningState(targetstate=targetstate, instanceID=instance_ids)

        listAll()


def createAMIInstance():
    instanceList = listAll()

    print "Or Type \"EXIT\" to quit"
    instance = promptList("What instance would you like to create AMI Image? ",
                          instanceList, exit_values=('exit',))
    if instance is None:
        return
    getName = promptVal("What name would you like to set for the new AMI name? ",
                        valid_fn=bool)
    instance_id = instance.instances[0].id
    newID = ec2conn.create_image(instance_id=instance_id, name=getName, no_reboot=True)
    print "New ID=" + newID
    listAll()


def deploy():
    awsSecGroups = filter(lambda x: x != 'default',
                          ec2conn.get_all_security_groups())

    #Instance Name
    getName = promptVal("What name would you like to assign to this instance? ",
                        valid_fn=lambda x: len(x) > 1)
    print "\n" * 3

    #Environment
    for i, env in enumerate_with_offset(ENV_LIST):
        print "%s - %s - %s" % (i, env[0], env[1])

    print "\n" * 2
    selectedEnv = promptList("How do you classify this machine? ", ENV_LIST)

    print "\n" * 5

    #AMI
    for i, ami in enumerate_with_offset(AMI_LIST):
        print "%s - %s" % (i, AMI_LIST[i][0])

    print "\n" * 2
    selectedAMI = promptList("What image would you like to deploy? ", AMI_LIST)

    print "\n" * 5

    #Instance Type
    for i, instance in enumerate_with_offset(INSTANCE_LIST):
        print "%s - %s" % (i, instance[0])
    print "\n" * 2
    selectedInstance = promptList("What size instance would you like to deploy? ",
                                  INSTANCE_LIST)

    print "\n" * 5

    #Security Groups
    for i, secgroup in enumerate_with_offset(awsSecGroups):
        print "%s - %s \"%s\"" % (i, secgroup.name, secgroup.description)
    print "\n" * 2
    selectedSecGroup = promptList("What Security Group would you like to assign to this instance? ",
                                  awsSecGroups)
    vpcID = selectedSecGroup.vpc_id
    print "\n" * 5

    #VPC Subnets
    awsSubnets = filter(lambda x: x.available_ip_address_count > 0,
                        vpcconn.get_all_subnets(filters=[('vpcId', vpcID)]))
    for i, subnet in enumerate_with_offset(awsSubnets):
        netname = subnet.tags.get('Name', '')

        print "%s - %s \"%s\" -- %s" % (i, subnet.id, subnet.cidr_block, netname)
    print "\n" * 2
    selectedSubnet = promptList("What Subnet would you like to assign this instance? ",
                                awsSubnets)
    print "\n" * 5

    #Deploy new instance
    print awsKeyName
    sendSecGroupID = str(selectedSecGroup.id)
    sendInstanceID = str(selectedInstance[1])
    sendSubnet = str(selectedSubnet.id)
    sendAMI = selectedAMI[1]

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
        'Environment': selectedEnv[0],
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
        print "The IP Address of your instance is: %s" % newInstance.instances[0].private_ip_address
        print "The public key that was used is: %s" % newInstance.instances[0].key_name
    else:
        print "We had a problem creating your instance. Not sure what happened so you will need to contact the Zenoss AWS Administrator for your department."


def jobList():
    # List of jobs user can execute
    jobsList = [
        Job('List my instances', listAll),
        Job('Start all of my %s instances now' % (ENV_LIST[3][0]),
            changeRunningState,
            targetstate="start",
            fromstate="stopped",
            status=3
        ),
        Job('Stop all of my %s instances now' % (ENV_LIST[3][0]),
            changeRunningState,
            targetstate="stop",
            fromstate="running",
            status=3
        ),
        Job('Start instance',
            selectInstances,
            targetstate="start",
            fromstate="stopped"
        ),
        Job('Stop instance',
            selectInstances,
            targetstate="stop",
            fromstate="running"
        ),
        Job('Destroy instance', destroy),
        Job('Create new instance', deploy),
        Job('Create AMI from instance', createAMIInstance),
        Job('Exit', sys.exit),
    ]

    while True:
        print "*" * 60
        print "\n"

        for i, job in enumerate_with_offset(jobsList):
            print "%s - %s" % (i, job)

        print "\n" * 2
        job = promptList("What would you like to do? ", jobsList)
        job.execute()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for i in sys.argv:
            argT = i.split("=")

            if argT[0] == "list":
                listAll()
                sys.exit()
    jobList()
