#
# Cookbook Name:: zenosslabs
# Role:: zenpack-jenkins
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-jenkins"
description "ZenPack Build Master"

run_list(
    "recipe[git]",
    "recipe[java]",
    "recipe[zenosslabs::jenkins-master]"
)
