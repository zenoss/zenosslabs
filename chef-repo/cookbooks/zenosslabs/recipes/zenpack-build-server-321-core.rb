#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321-core
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-server-deps"


# Resources
zenosslabs_zenoss "3.2.1 core" do
    version "3.2.1"
    flavor "core"
    platform_rpm "zenoss-3.2.1-1326"
    core_zenpacks_rpm "zenoss-core-zenpacks-3.2.1-1326"
    action :install
end
