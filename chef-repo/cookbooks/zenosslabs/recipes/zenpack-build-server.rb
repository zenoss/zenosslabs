#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::zenpack-build-server-deps"

%w{3.2.1 4.1.1}.each do |version|
    version_tag = version.gsub('.', '')

    include_recipe "zenosslabs::zenpack-build-server-#{version_tag}"
end
