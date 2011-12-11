#
# Cookbook Name:: zenosslabs
# Recipe:: zenoss
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

dependencies = %w{mysql-server net-snmp net-snmp-utils gmp libgomp libgcj liberation-fonts}
dependencies.each do |pkg|
    yum_package pkg do
        action :install
    end
end

# cookbook_file "/tmp/#{node[:zenoss_rpm]}" do
#     source node[:zenoss_rpm]
# end

# package "zenoss" do
#     source "/tmp/#{node[:zenoss_rpm]}"
# end
