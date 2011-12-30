#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-411-resmgr
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps-411"


# Attributes
node[:zenoss][:flavor] = "resmgr"


# Run List
include_recipe "zenosslabs::zenoss"
