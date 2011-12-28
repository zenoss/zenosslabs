#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-321-platform
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-321-platform"
description "ZenPack Build Server for Zenoss 3.2.1"

run_list "role[zenpack-builder-321]"

default_attributes(
    "zenoss" => {
        "flavor" => "platform",
        "platform_rpm" => "zenoss-3.2.1-1326"
    }
)
