#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-deps-411
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps"


# Attributes
node[:zenoss][:version] = "4.1.1"
node[:zenoss][:version_tag] = "411"
node[:zenoss][:flavor_tags] = %w{platform resmgr}
node[:zenoss][:platform_rpm] = "zenoss-4.1.1-1396"
node[:zenoss][:core_zenpacks_rpm] = "zenoss-core-zenpacks-4.1.1-1396"
node[:zenoss][:enterprise_zenpacks_rpm] = "zenoss-enterprise-zenpacks-4.1.1-1396"
