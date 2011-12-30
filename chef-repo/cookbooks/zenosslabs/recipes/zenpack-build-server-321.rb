#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::zenpack-build-deps"

%w{platform core enterprise}.each do |flavor|
    include_recipe "zenosslabs::zenpack-build-server-321-#{flavor}"
end
