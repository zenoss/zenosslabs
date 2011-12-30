#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321-enterprise
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Inheritance
include_recipe "zenosslabs::zenpack-build-deps-321"


# Resources
zenosslabs_zenoss "3.2.1 enterprise" do
    version "3.2.1"
    flavor "enterprise"
    platform_rpm "zenoss-3.2.1-1326"
    core_zenpacks_rpm "zenoss-core-zenpacks-3.2.1-1326"
    enterprise_zenpacks_rpm "zenoss-enterprise-zenpacks-3.2.1-1326"
    action :install
end
