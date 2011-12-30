#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::zenpack-build-deps"

node[:zenoss][:version_tags].each do |version_tag|
    include_recipe "zenosslabs::zenpack-build-server-#{version_tag}"
end
