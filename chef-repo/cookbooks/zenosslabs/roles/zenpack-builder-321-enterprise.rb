#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-321-enterprise
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-321-enterprise"
description "ZenPack Build Server for Zenoss 3.2.1 Enterprise"

run_list "role[zenpack-builder-321-core]"
default_attributes(
    "zenoss" => {
        "flavor" => "enterprise",
        "enterprise_zenpacks_rpm" => "zenoss-enterprise-zenpacks-3.2.1-1326"
    }
)
