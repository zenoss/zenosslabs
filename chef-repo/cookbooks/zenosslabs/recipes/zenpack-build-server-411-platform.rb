#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-411-platform
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-server-deps"


# Resources
zenosslabs_zenoss "4.1.1 platform" do
    version "4.1.1"
    flavor "platform"
    zends_rpm "zends-5.5.15-1.r51230"
    platform_rpm "zenoss-4.1.1-1396"
    action :install
end
