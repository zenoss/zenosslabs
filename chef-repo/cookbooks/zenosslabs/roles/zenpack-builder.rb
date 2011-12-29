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
    "recipe[selinux::disabled]",
    "recipe[git]",
    "recipe[java]",
    "recipe[zenosslabs::fixhosts]",
    "recipe[zenosslabs::jenkins-slave]",
    "recipe[zenosslabs::zenoss]"
)

default_attributes(
    "java" => {
        "install_flavor" => "sun"
    },

    "zenoss" => {
        "zends_rpm" => "zends-5.5.15-1.r51230"
    }
)
