#
# Cookbook Name:: zenosslabs
# Recipe:: slave
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

["3.2.1", "4.1.0"].each do |version|
    zenosslabs_snapshot "#{version}" do
        version "#{version}"
        action :create
    end
end
