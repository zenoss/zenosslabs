#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321-core
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps-321"


# Attributes
node[:zenoss][:flavor] = "core"


# Run List
include_recipe "zenosslabs::zenoss"
