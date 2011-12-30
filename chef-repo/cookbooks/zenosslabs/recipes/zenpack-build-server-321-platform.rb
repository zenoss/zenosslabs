#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321-platform
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps-321"


# Resources
zenosslabs_zenoss "3.2.1 platform" do
    version "3.2.1"
    flavor "platform"
    platform_rpm "zenoss-3.2.1-1326"
    action :install
end
