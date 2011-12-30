#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-deps-321
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps"


# Attributes
node[:zenoss][:version] = "3.2.1"
node[:zenoss][:version_tag] = "321"
node[:zenoss][:flavor_tags] = %w{platform core enterprise}
node[:zenoss][:platform_rpm] = "zenoss-3.2.1-1326"
node[:zenoss][:core_zenpacks_rpm] = "zenoss-core-zenpacks-3.2.1-1326"
node[:zenoss][:enterprise_zenpacks_rpm] = "zenoss-enterprise-zenpacks-3.2.1-1326"
