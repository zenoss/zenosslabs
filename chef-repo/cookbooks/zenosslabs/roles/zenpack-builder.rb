#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder"
description "ZenPack Build Server"

run_list(
    "recipe[git]",
    "recipe[java]",
    "recipe[zenosslabs::jenkins-slave]",
    "recipe[zenosslabs::zenoss]"
)
