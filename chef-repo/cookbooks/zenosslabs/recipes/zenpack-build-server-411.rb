#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-411
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::zenpack-build-deps"

%w{platform resmgr}.each do |flavor|
    include_recipe "zenosslabs::zenpack-build-server-411-#{flavor}"
end
