#
# Cookbook Name:: zenosslabs
# Role:: zenpack-build-server-321
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

name "zenpack-build-server-321"
description "ZenPack Build Server for Zenoss 3.2.1"

run_list(
    "role[zenpack-builder-321-platform]",
    "role[zenpack-builder-321-core]",
    "role[zenpack-builder-321-enterprise]"
)
