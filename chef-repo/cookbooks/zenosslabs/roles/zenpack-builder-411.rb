#
# Cookbook Name:: zenosslabs
# Role:: zenpack-builder-411
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-builder-411"
description "ZenPack Build Server for Zenoss 4.1.1"

run_list "role[zenpack-builder]"

default_attributes(
    "zenoss" => {
        "version" => "4.1.1"
    }
)
