#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-321-core
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-321-core"
description "ZenPack Build Server for Zenoss 3.2.1 Core"

run_list "role[zenpack-builder-321-platform]"

default_attributes(
    "zenoss" => {
        "flavor" => "core",
        "core_zenpacks_rpm" => "zenoss-core-zenpacks-3.2.1-1326"
    }
)
