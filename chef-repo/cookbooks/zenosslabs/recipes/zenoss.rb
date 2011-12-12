#
# Cookbook Name:: zenosslabs
# Recipe:: zenoss
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

case node[:platform]
when "centos"
    dependencies = %w{mysql-server net-snmp net-snmp-utils gmp libgomp libgcj liberation-fonts}
    dependencies.each do |pkg|
        yum_package pkg do
            action :install
        end
    end

    cookbook_file "/tmp/#{node[:zenoss_rpm]}" do
        source node[:zenoss_rpm]
    end

    yum_package "zenoss" do
        source "/tmp/#{node[:zenoss_rpm]}"
        options "--nogpgcheck"
    end

    file "/opt/zenoss/etc/DAEMONS_TXT_ONLY" do
        owner "zenoss"
        group "zenoss"
        mode 0644
    end

    template "/opt/zenoss/etc/daemons.txt" do
        owner "zenoss"
        group "zenoss"
        mode 0644
        source "daemons.txt.erb"
    end

    service "zenoss" do
        action :start
    end
end
