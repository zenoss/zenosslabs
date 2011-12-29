#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-411-platform
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-411-platform"
description "ZenPack Build Server for Zenoss 4.1.1"

run_list "role[zenpack-builder-411]"

default_attributes(
    "zenoss" => {
        "flavor" => "platform",
        "platform_rpm" => "zenoss-4.1.1-1396"
    }
)
