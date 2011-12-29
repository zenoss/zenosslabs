#
# Cookbook Name:: zenosslabs
# Role:: zenpack-build-server-411
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-build-server-411"
description "ZenPack Build Server for Zenoss 4.1.1"

run_list(
    "role[zenpack-builder-411-platform]",
    "role[zenpack-builder-411-resmgr]"
)
