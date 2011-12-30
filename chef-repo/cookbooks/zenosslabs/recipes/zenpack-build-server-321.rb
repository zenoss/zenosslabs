#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server-321
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::zenpack-build-deps-321"

node[:zenoss][:flavor_tags].each do |flavor_tag|
    include_recipe "zenosslabs::zenpack-build-server-#{node[:zenoss][:version_tag]}-#{flavor_tag}"
end
