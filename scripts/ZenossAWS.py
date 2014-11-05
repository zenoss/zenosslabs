#!/usr/bin/env python

##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# Description:
# The purpose of this script is to offer basic AWS interaction for users.
#
##############################################################################

import os
import sys
import time
import optparse
from collections import namedtuple

from boto.ec2.connection import EC2Connection as ec2
from boto.vpc import VPCConnection as vpc

import socket

from getpass import getpass

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

# List of AMI offered to user.
# Feel free to add more AMIs here
AWS_AMI = namedtuple('AMI', ['description', 'id'])
AMI_LIST = (
    AWS_AMI('Ubuntu Server 12.04 LTS', 'ami-aae625c2'),
    AWS_AMI('Ubuntu Server 12.04 LTC VNC', 'ami-8af330e2'),
    AWS_AMI('Ubuntu Server 13.10', 'ami-87bab1ee'),
    AWS_AMI('Ubuntu Server 14.04 LTS', 'ami-6e5e9606'),
    AWS_AMI('Ubuntu Server 14.04 LTS VNC', 'ami-1ef13276'),
    AWS_AMI('Red Hat Enterprise Linux 6.3', 'ami-deeb28b6'),
    AWS_AMI('Red Hat Enterprise Linux 6.5', 'ami-d0e427b8'),
    #AWS_AMI('Red Hat Enterprise Linux 7.0', 'ami-40df6928'),
    AWS_AMI('CentOS 5.7 x86_64', 'ami-bbbbf5d2'),
    AWS_AMI('Centos 6.3 x86_64', 'ami-48da1920'),
    AWS_AMI('Centos 6.5 x86_64', 'ami-86e724ee'),
    AWS_AMI('Centos 6.5 x86_64 VNC', 'ami-10f33078'),
    AWS_AMI('CentOS 7.0 x86_64', 'ami-56e6683e'),
    AWS_AMI('Windows 2003 Server Domain', 'ami-62009f0b'),
    AWS_AMI('Windows 2008 Server Domain', 'ami-b8039cd1'),
    AWS_AMI('Windows 2008 Server', 'ami-98039cf1'),
    AWS_AMI('Windows 2012 Server', 'ami-e45c3b8d'),
)

EUROPA_AMI = AWS_AMI('Ubuntu Server 14.04 LTS', 'ami-6e5e9606')

# Limited list of instance types available. Many more exists but haven't been added here.
AWS_INSTANCE = namedtuple('AWS_INSTANCE', ['description', 'id'])
INSTANCE_LIST = (
    AWS_INSTANCE('Micro (1 CPU / 512MB / / Very Low Network) .02/hr - .24/day - 1.20/week - 5.20/month', 't1.micro'),
    AWS_INSTANCE('Small (1 CPU / 1.7GB / 160GB / Low Network) .04/hr - .48/day - 2.40/week - 10.40/month', 'm1.small'),
    AWS_INSTANCE('Medium (1 CPU / 3.75GB / 410GB/ Moderate Network) .09/hr - 1.08/day - 5.40/week - 23.40/month', 'm1.medium'),
    #AWS_INSTANCE('Medium SSD (1 CPU / 3.75GB / 4GB SSD / Moderate Network) .07/hr - .84/day - 4.20/week - 18.20/month', 'm3.medium'),
    AWS_INSTANCE('Large (2 CPU / 7.5GB / 2x420GB / Moderate Network) .18/hr - 2.26/day - 10.80/week - 46.80/month', 'm1.large'),
    #AWS_INSTANCE('Large SSD (2 CPU / 7.5GB / 32GB / Moderate Network) .14/hr - 1.68/day - 8.40/week - 36.40/month', 'm3.large'),
    #AWS_INSTANCE('Large SSD Mem Optimized (2 CPU / 15GB / 32GB / Moderate Network) .18/hr - 2.16/day - 10.80/week - 46.80/month', 'r3.large'),
    AWS_INSTANCE('X-Large (4 CPU / 15GB / 4x420GB / Moderate Network) .35/hr - 4.20/day - 21.00/week - 91.00/month', 'm1.xlarge'),
    AWS_INSTANCE('X-Large SSD (4 CPU / 15GB / 2x40GB / Moderate Network) .28/hr - 3.36/day - 16.80/week - 72.80/month', 'm3.xlarge'),
    #AWS_INSTANCE('X-Large SSD Mem Optimized (4 CPU / 30GB / 80GB / Moderate Network) .35/hr - 4.20/day - 21.00/week - 91.00/month', 'r3.xlarge'),
    AWS_INSTANCE('XX-Large (4 CPU / 34GB / 2x850GB / Moderate Network) .49/hr - 11.76/day - 82.32/week - 356.72/month', 'm2.2xlarge'),
    AWS_INSTANCE('XXXX-Large (8 CPU / 68GB / 2x840GB / High Netork) .98/hr - 23.52/day - 164.64/week - 713.44/month', 'm2.4xlarge'),
    AWS_INSTANCE('CentOS7 - XX-Large SSD Mem Optimized (8 CPU / 61GB / 160GB / High Network) .70/hr - 8.40/day - 42.00/week - 182/month', 'r3.2xlarge'), 
    #AWS_INSTANCE('RHEL 2xLarge (8 CPU/ 61GB / 2x800 SSD / High Network) 1.84/hr - 44.16/day - 309.12/week - 1339.52/month', 'i2.2xlarge'),
)


ENVIRONMENT = namedtuple('ENVIRONMENT', ['name', 'description'])
#ENV_LIST = (
#    ENVIRONMENT('Production', 'Never turn off'),

ENV_LIST = (
    ENVIRONMENT('Lab', 'Turn off every night at 8pm CST M-F.'),
    ENVIRONMENT('Temporary', 'Destroy at 8pm CST. *WARNING* Data will be lost'),
    ENVIRONMENT('Short Use', 'Destroy after an hour of run time. *WARNING* Data will be lost'),
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

    def __str__(self):
        return self.description

    __repr__ = __str__

EXIT_VALUES = ('exit',)


def promptVal(prompt, convert_fn=None, valid_fn=None, allow_exit=False):
    """
    Prompts for a value from stdin. Uses convert_fn to convert
    the value to another format. If valid_fn is specified, it
    is passed the converted value to determine if the value is
    valid. If the value is invalid, it is discarded and the user
    is prompted again. If allow_exit is specified, it allows the
    loop to be short-circuited and return None if the input from the
    user is 'exit'. Returns the converted value from stdin, or None
    if allow_exit is True and the user chose to exit.
    """
    if not valid_fn:
        valid_fn = lambda x: True
    if not convert_fn:
        convert_fn = lambda x: x
    while True:
        input = raw_input(prompt)
        if input:
            if allow_exit and input.lower() in EXIT_VALUES:
                return None
            try:
                value = convert_fn(input)
                if valid_fn(value):
                    return value
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                print >> sys.stderr, "Invalid value: %s" % input


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
        yield i + offset, val


def listAll(state=None, status=None):
    #state = State of machine pending | running | shutting-down | terminated | stopping | stopped
    #status = Environment Tag value instance deployed to

    filters = {'tag:Owner': options.aws_username}
    if status:
        filters.update({'tag:Environment': ENV_LIST[status][0]})
    if state:
        filters.update({'instance-state-name': state})

    instanceList = ec2conn.get_all_instances(filters=filters)

    print "*" * 60
    print "All instances that belong to %s" % options.aws_username
    print "\n" * 3
    print "LINE -- NAME -- RUNNING STATE -- PRIVATE IP -- ENVIRONMENT"
    print ""
    for i, reservation in enumerate_with_offset(instanceList):
        instance = reservation.instances[0]
        if instance.state != 'terminated':
            print "%s -- %s -- %s -- %s -- %s" % (i, instance.tags['Name'],
                                instance.state, instance.private_ip_address,
                                instance.tags['Environment'])

    print "\n" * 3
    return instanceList


def destroy():
    instanceList = listAll()
    print "Or Type \"EXIT\" to quit"

    instance = promptList("What instance would you like to destroy? ",
                          instanceList, allow_exit=True)
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

    filters = {'tag:Owner': options.aws_username}
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


def changeTag(tagName='ExtraTime'):
    instanceList = listAll()

    print "Or Type \"EXIT\" to quit"

    if tagName == 'ExtraTime':
        selectedInstances = promptListMultiple("Which instances would you like to extend the usage on? ",
                                           instanceList, allow_exit=True)

    if tagName == 'Environment':
        selectedInstances = promptListMultiple("Which instances would you like to change the Environment on? ",
                                           instanceList, allow_exit=True)

    if selectedInstances:
        instance_ids = [instance.instances[0].id for instance in selectedInstances]

        if tagName == 'ExtraTime':
            selectedVal = promptInt("How many hours would you like to add? ", min_val=1, max_val=24)

        if tagName == 'Environment':
            print "\n" * 5
            for i, env in enumerate_with_offset(ENV_LIST):
                print "%s - %s - %s" % (i, env.name, env.description)
            print "\n" * 2
            selectedVal = promptList("How do you classify this machine? ", ENV_LIST)
            selectedVal = selectedVal[0]

        ec2conn.create_tags(instance_ids, {tagName: selectedVal})


def selectInstances(targetstate, fromstate=None, status=None):
    #state = State of machine pending | running | shutting-down | terminated | stopping | stopped
    #status = Environment Tag value instance deployed to

    instanceList = listAll(state=fromstate, status=status)

    print "Or Type \"EXIT\" to quit"

    selectedInstances = promptListMultiple("Which instances would you like to %s? " % targetstate,
                                           instanceList, allow_exit=True)
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
                          instanceList, allow_exit=True)
    if instance is None:
        return
    getName = promptVal("What name would you like to set for the new AMI name? ",
                        valid_fn=bool)

    getDescription = promptVal("What description would you like to provide? ",
                        valid_fn=bool)

    instance_id = instance.instances[0].id
    newID = ec2conn.create_image(instance_id=instance_id, name=getName, description=getDescription, no_reboot=True)

    #Need to assign tag information
    print "Working... Please wait"
    time.sleep(4)

    newTags = {
        'Name': getName,
        'Customer': options.department,
        'Owner': options.aws_username,
        'Description': getDescription,
        }
    ec2conn.create_tags(newID, newTags)

    print "New ID=" + newID
    listAll()


def deregisterAMIImage():

    COMB_AMI_LIST = []
    amiListStart = 1
    USER_AMI_LIST = ec2conn.get_all_images(filters={'tag:Owner': options.aws_username})

    for i in USER_AMI_LIST:
        COMB_AMI_LIST.append(
            {'description': i.description,
             'id': i.id})
        print "%s - %s" % (amiListStart, i.description)
        amiListStart += 1

    print "\n" * 2
    selectedAMI = promptList("What image would you like to remove? ", COMB_AMI_LIST)
    ec2conn.deregister_image(image_id=selectedAMI['id'])
    listAll()


def deploy():
    #Instance Name
    getName = promptVal("What name would you like to assign to this instance? ",
                        valid_fn=lambda x: len(x) > 1)
    print "\n" * 3

    #Environment
    for i, env in enumerate_with_offset(ENV_LIST):
        print "%s - %s - %s" % (i, env.name, env.description)

    print "\n" * 2
    selectedEnv = promptList("How do you classify this machine? ", ENV_LIST)

    print "\n" * 5

    #Get users list of AMI Images
    print "Working on retrieving list of AMI Images... Please wait"

    USER_AMI_LIST = ec2conn.get_all_images(filters={'tag:Owner': options.aws_username})
    print "\n" * 5

    COMB_AMI_LIST = []

    amiListStart = 1
    for i in USER_AMI_LIST:
        COMB_AMI_LIST.append(
            {'description': i.description,
             'id': i.id})
        print "%s - %s" % (amiListStart, i.description)
        amiListStart += 1

    #AMI
    for i, ami in enumerate_with_offset(AMI_LIST, offset=amiListStart):
        COMB_AMI_LIST.append(
            {'description': ami.description,
             'id': ami.id})
        print "%s - %s" % (i, ami.description)

    print "\n" * 2
    selectedAMI = promptList("What image would you like to deploy? ", COMB_AMI_LIST)

    print "\n" * 5

    #Instance Type
    for i, instance in enumerate_with_offset(INSTANCE_LIST):
        print "%s - %s" % (i, instance.description)

    print "\n" * 2
    selectedInstance = promptList("What size instance would you like to deploy? ",
                                  INSTANCE_LIST)

    print "\n" * 5

    #Security Groups
    """
    awsSecGroups = filter(lambda x: x.name in ['LocalQANetwork'],
                          ec2conn.get_all_security_groups())
    for i, secgroup in enumerate_with_offset(awsSecGroups):
        print "%s - %s \"%s\"" % (i, secgroup.name, secgroup.description)
    print "\n" * 2
    selectedSecGroup = promptList("What Security Group would you like to assign to this instance? ",
                                  awsSecGroups)
    vpcID = selectedSecGroup.vpc_id
    print "\n" * 5

    #VPC Subnets
    filters = {'tag:Owner': 'qa'}
    filters['vpcId'] = vpcID
    """
    sgfilter = ['sg-09544f6b']

    selectedSecGroup = ec2conn.get_all_security_groups(group_ids=sgfilter)[0]

    filters = {'tag:Owner': options.department}
    filters['vpcId'] = 'vpc-92b4bff0'

    awsSubnets = filter(lambda x: x.available_ip_address_count > 0,
                        vpcconn.get_all_subnets(filters=filters))

    if len(awsSubnets) == 0:
        print "*" * 60
        print "*" * 60
        print "Well sorry about that but you don't have any subnets assigned to you"
        print "in this VPC. Either select another VPC or ask the administrator"
        print "for a subnet assignment."
        print "*" * 60
        print "*" * 60
        return

    for i, subnet in enumerate_with_offset(awsSubnets):
        netname = subnet.tags.get('Name', '')
        print "%s - %s \"%s\" -- %s" % (i, subnet.id, subnet.cidr_block, netname)

    print "\n" * 2
    selectedSubnet = promptList("What Subnet would you like to assign this instance? ",
                                awsSubnets)
    print "\n" * 5

    #Deploy new instance
    print options.aws_key_name
    sendSecGroupID = str(selectedSecGroup.id)
    sendInstanceID = selectedInstance.id
    sendSubnet = str(selectedSubnet.id)
    sendAMI = selectedAMI['id']

    print sendAMI
    print sendSecGroupID
    print sendInstanceID
    print sendSubnet

    newInstance = ec2conn.run_instances(image_id=sendAMI,
            key_name=options.aws_key_name,
            instance_initiated_shutdown_behavior='stop',
            security_group_ids=[sendSecGroupID],
            instance_type=sendInstanceID,
            subnet_id=sendSubnet)
    """
    newInstance = ec2conn.run_instances(image_id=sendAMI,
            key_name='DefaultZenoss',
            instance_initiated_shutdown_behavior='stop',
            security_group_ids=[sendSecGroupID],
            instance_type=sendInstanceID,
            subnet_id=sendSubnet)
    """
    print "Working... Please wait"
    time.sleep(4)

    newTags = {
        'Name': getName,
        'Environment': selectedEnv.name,
        'Customer': options.department,
        'Owner': options.aws_username,
        'ExtraTime': 0, 
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


def getDockerUserPassEmail():
    username = raw_input("Please enter your Docker Hub username: ")
    password1, password2 = "a", "b"
    while password1 != password2:
        password1 = getpass("Please enter your Docker Hub password: ")
        password2 = getpass("Please enter your Docker Hub password (again): ")
        if password1 != password2:
            print "Passwords do not match."
    email = raw_input("Please enter the email address associated with your Docker Hub account: ")
    return username, password1, email


def deployEuropaSingleHostMaster():
    #Docker Login
    username, password, email = getDockerUserPassEmail()

    #Instance Name
    getName = promptVal("What name would you like to assign to this instance? ",
                        valid_fn=lambda x: len(x) > 1)
    print "\n" * 3

    #Environment
    for i, env in enumerate_with_offset(ENV_LIST):
        print "%s - %s - %s" % (i, env.name, env.description)

    print "\n" * 2
    selectedEnv = promptList("How do you classify this machine? ", ENV_LIST)

    print "\n" * 5

    #Instance Type
    for i, instance in enumerate_with_offset(INSTANCE_LIST):
        print "%s - %s" % (i, instance.description)

    print "\n" * 2
    selectedInstance = promptList("What size instance would you like to deploy? ",
                                  INSTANCE_LIST)

    print "\n" * 5

    #Security Groups
    sgfilter = ['sg-09544f6b']

    selectedSecGroup = ec2conn.get_all_security_groups(group_ids=sgfilter)[0]

    filters = {'tag:Owner': options.department}
    filters['vpcId'] = 'vpc-92b4bff0'

    awsSubnets = filter(lambda x: x.available_ip_address_count > 0,
                        vpcconn.get_all_subnets(filters=filters))

    if len(awsSubnets) == 0:
        print "*" * 60
        print "*" * 60
        print "Well sorry about that but you don't have any subnets assigned to you"
        print "in this VPC. Either select another VPC or ask the administrator"
        print "for a subnet assignment."
        print "*" * 60
        print "*" * 60
        return

    for i, subnet in enumerate_with_offset(awsSubnets):
        netname = subnet.tags.get('Name', '')
        print "%s - %s \"%s\" -- %s" % (i, subnet.id, subnet.cidr_block, netname)

    print "\n" * 2
    selectedSubnet = promptList("What Subnet would you like to assign this instance? ",
                                awsSubnets)
    print "\n" * 5

    #Deploy new instance
    print options.aws_key_name
    sendSecGroupID = str(selectedSecGroup.id)
    sendInstanceID = selectedInstance.id
    sendSubnet = str(selectedSubnet.id)
    sendAMI = EUROPA_AMI.id

    print sendAMI
    print sendSecGroupID
    print sendInstanceID
    print sendSubnet

    userdata = open(os.path.join(ROOT_PATH, "europa-singlehost-install.sh"), 'r').read()
    userdata = userdata.replace("{{DOCKER_USERNAME}}", username)
    userdata = userdata.replace("{{DOCKER_PASSWORD}}", password)
    userdata = userdata.replace("{{DOCKER_EMAIL}}", email)

    newInstance = ec2conn.run_instances(image_id=sendAMI,
            key_name=options.aws_key_name,
            instance_initiated_shutdown_behavior='stop',
            security_group_ids=[sendSecGroupID],
            user_data=userdata,
            instance_type=sendInstanceID,
            subnet_id=sendSubnet)
    print "Working... Please wait"
    time.sleep(4)

    newTags = {
        'Name': getName,
        'Environment': selectedEnv.name,
        'Customer': options.department,
        'Owner': options.aws_username,
        'ExtraTime': 0, 
    }

    newInstanceID = newInstance.instances[0].id
    tagresult = ec2conn.create_tags(newInstanceID, newTags)

    if not tagresult:
        print "We had a problem creating your instance. Not sure what happened so you will need to contact the Zenoss AWS Administrator for your department."
        return

    print "Provisioning has commenced. Go to https://%s to see the Control Center. It may take a few minutes before it is up." % newInstance.instances[0].private_ip_address


def deployEuropaMultihost():
    #Docker Login
    username, password, email = getDockerUserPassEmail()

    #Number of agent instances.
    nInstances = promptInt("How many agents do you want? (minimum of one) ", min_val = 1)
    print "\n" * 3

    #Instance Name
    getName = promptVal("What name prefix would you like to assign to these instances? ",
                        valid_fn=lambda x: len(x) > 1)
    print "\n" * 3

    #Environment
    for i, env in enumerate_with_offset(ENV_LIST):
        print "%s - %s - %s" % (i, env.name, env.description)

    print "\n" * 2
    selectedEnv = promptList("How do you classify these machines? ", ENV_LIST)

    print "\n" * 5

    #Instance Type
    for i, instance in enumerate_with_offset(INSTANCE_LIST):
        print "%s - %s" % (i, instance.description)

    print "\n" * 2
    selectedInstance = promptList("What size instances would you like to deploy? ", INSTANCE_LIST)

    print "\n" * 5

    #Security Groups
    sgfilter = ['sg-09544f6b']

    selectedSecGroup = ec2conn.get_all_security_groups(group_ids=sgfilter)[0]

    filters = {'tag:Owner': options.department}
    filters['vpcId'] = 'vpc-92b4bff0'

    awsSubnets = filter(lambda x: x.available_ip_address_count > 0,
                        vpcconn.get_all_subnets(filters=filters))

    if len(awsSubnets) == 0:
        print "*" * 60
        print "*" * 60
        print "Well sorry about that but you don't have any subnets assigned to you"
        print "in this VPC. Either select another VPC or ask the administrator"
        print "for a subnet assignment."
        print "*" * 60
        print "*" * 60
        return

    for i, subnet in enumerate_with_offset(awsSubnets):
        netname = subnet.tags.get('Name', '')
        print "%s - %s \"%s\" -- %s" % (i, subnet.id, subnet.cidr_block, netname)

    print "\n" * 2
    selectedSubnet = promptList("What Subnet would you like to assign these instances? ",
                                awsSubnets)
    print "\n" * 5

    #Deploy new instance
    print options.aws_key_name
    sendSecGroupID = str(selectedSecGroup.id)
    sendInstanceID = selectedInstance.id
    sendSubnet = str(selectedSubnet.id)
    sendAMI = EUROPA_AMI.id

    print sendAMI
    print sendSecGroupID
    print sendInstanceID
    print sendSubnet

    userdata = open(os.path.join(ROOT_PATH, "europa-multihost-master-install.sh"), 'r').read()
    userdata = userdata.replace("{{DOCKER_USERNAME}}", username)
    userdata = userdata.replace("{{DOCKER_PASSWORD}}", password)
    userdata = userdata.replace("{{DOCKER_EMAIL}}", email)

    newInstance1 = ec2conn.run_instances(image_id=sendAMI,
            key_name=options.aws_key_name,
            instance_initiated_shutdown_behavior='stop',
            security_group_ids=[sendSecGroupID],
            user_data=userdata,
            instance_type=sendInstanceID,
            subnet_id=sendSubnet)
    print "Working... Please wait"
    time.sleep(4)

    newTags = {
        'Name': getName + "-master",
        'Environment': selectedEnv.name,
        'Customer': options.department,
        'Owner': options.aws_username,
        'ExtraTime': 0, 
    }
    tagresult = ec2conn.create_tags(newInstance1.instances[0].id, newTags)
    if not tagresult:
        print "We had a problem creating your instances. Not sure what happened so you will need to contact the Zenoss AWS Administrator for your department."
        return

    print "Waiting for master ip address..."
    while newInstance1.instances[0].private_ip_address == None:
        time.sleep(1)
        newInstance1.instances[0].update()

    userdata = open(os.path.join(ROOT_PATH, "europa-multihost-minion-install.sh"), 'r').read()
    userdata = userdata.replace("{{in_MHOST}}", newInstance1.instances[0].private_ip_address)

    for i in range(nInstances):

        agent = ec2conn.run_instances(image_id=sendAMI,
                key_name=options.aws_key_name,
                instance_initiated_shutdown_behavior='stop',
                security_group_ids=[sendSecGroupID],
                user_data=userdata,
                instance_type=sendInstanceID,
                subnet_id=sendSubnet)
        print "Working on agent %d... Please wait" % (i + 1)
        time.sleep(4)
        newTags = {
            'Name': "%s-agent-%02d" % (getName, i + 1),
            'Environment': selectedEnv.name,
            'Customer': options.department,
            'Owner': options.aws_username,
            'ExtraTime': 0, 
        }
        tagresult = ec2conn.create_tags(agent.instances[0].id, newTags)
        if not tagresult:
            print "We had a problem creating your instances. Not sure what happened so you will need to contact the Zenoss AWS Administrator for your department."
            return

    print "Provisioning has commenced. Go to https://%s to see the Control Center. It may take a few minutes before it is up." % newInstance1.instances[0].private_ip_address


def jobList():
    # List of jobs user can execute
    jobsList = [
        Job('List my instances', listAll),
        Job('Start all of my %s instances now' % ENV_LIST[2].name,
            changeRunningState,
            targetstate="start",
            fromstate="stopped",
            status=2
        ),
        Job('Stop all of my %s instances now' % ENV_LIST[2].name,
            changeRunningState,
            targetstate="stop",
            fromstate="running",
            status=2
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
        Job('Extend Time of instance',
            changeTag
        ),
        Job('Change Environment',
            changeTag,
            tagName="Environment"
        ),
        Job('Destroy instance', destroy),
        Job('Create new instance', deploy),
        Job('Create new Europa single host master instance', deployEuropaSingleHostMaster),
        Job('Create new Europa multihost environment', deployEuropaMultihost),
        Job('Create AMI from instance', createAMIInstance),
        Job('Destroy AMI', deregisterAMIImage),
        Job('Exit', sys.exit),
    ]

    while True:
        print "*" * 60
        print "\n"

        for i, job in enumerate_with_offset(jobsList):
            print "%s - %s" % (i, job)

        print "\n" * 2
        job = promptList("What would you like to do? ", jobsList, allow_exit=True)
        job.execute()


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
        'username': env_get('AWS_USERNAME', cfg_get('username', env_get('USER'))),
        'department': env_get('DEPARTMENT', cfg_get('department')),
        'key_name': env_get('AWS_KEY_NAME', cfg_get('key_name')),
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
    parser.add_option("-u", "--aws-username", dest='aws_username',
                      default=defaults['username'],
                      help="AWS Username (environment variable: AWS_USERNAME/USER)")
    parser.add_option("-d", "--department", dest='department',
                      default=defaults['department'],
                      help="Department Name (environment variable: DEPARTMENT)")
    parser.add_option("-k", "--aws-key-name", dest='aws_key_name',
                      default=defaults['key_name'],
                      help="AWS Key Name (environment variable: AWS_KEY_NAME)")
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
        jobList()
    except (KeyboardInterrupt, EOFError):
        print

