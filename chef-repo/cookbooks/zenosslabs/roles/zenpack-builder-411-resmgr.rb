#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-411-resmgr
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-411-resmgr"
description "ZenPack Build Server for Zenoss 4.1.1 Resource Manager"

run_list "role[zenpack-builder-411-platform]"
default_attributes(
    "zenoss" => {
        "flavor" => "resmgr",
        "core_zenpacks_rpm" => "zenos-core-zenpacks-4.1.1-1396",
        "enterprise_zenpacks_rpm" => "zenoss-enterprise-zenpacks-4.1.1-1396"
    }
)
