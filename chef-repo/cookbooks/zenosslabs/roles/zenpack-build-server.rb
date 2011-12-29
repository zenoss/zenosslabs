#
# Cookbook Name:: zenosslabs
# Role:: zenpack-build-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-build-server"
description "ZenPack Build Server"

run_list(
    "role[zenpack-build-server-321]",
    "role[zenpack-build-server-411]"
)
