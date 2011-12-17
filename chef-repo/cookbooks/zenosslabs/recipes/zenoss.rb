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
    rpm_release = node[:kernel][:release].split('.')[-1]

    if node[:kernel][:machine] == "i686"
        rpm_arch = "i386"
    else
        rpm_arch = node[:kernel][:machine]
    end

    # Install dependencies.
    dependencies = %w{mysql-server net-snmp net-snmp-utils gmp libgomp libgcj liberation-fonts}
    dependencies.each do |pkg|
        yum_package pkg do
            action :install
        end
    end

    # Create an loopback file system using LVM for snapshots.
    zenosslabs_loopback_fs "/opt/zenoss" do
        vg_name "zenoss"
        block_size 4096
        bytes 2147483648
        action :create
    end


    # Install Zenoss platform.
    zenosslabs_snapshot "platform" do
        vg_name "zenoss"
        base_lv_name "base"
        percent_of_origin 20
        mount "/opt/zenoss"
        action [ :create, :switch ]
    end

    zenoss_rpm = "#{node[:zenoss][:rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
    cookbook_file "/tmp/#{zenoss_rpm}" do
        source zenoss_rpm
    end

    yum_package "zenoss" do
        source "/tmp/#{zenoss_rpm}"
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
        action [ :enable, :start ]
    end


    # Install Core ZenPacks.
    zenosslabs_snapshot "core" do
        vg_name "zenoss"
        base_lv_name "platform"
        percent_of_origin 20
        mount "/opt/zenoss"
        action [ :create, :switch ]
    end

    %w{mysqld zenoss}.each do |service_name|
        service service_name do
            action :start
        end
    end

    zenoss_core_zenpacks_rpm = "#{node[:zenoss][:core_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
    cookbook_file "/tmp/#{zenoss_core_zenpacks_rpm}" do
        source zenoss_core_zenpacks_rpm
    end

    yum_package "zenoss-core-zenpacks" do
        source "/tmp/#{zenoss_core_zenpacks_rpm}"
        options "--nogpgcheck"
    end


    # Install Enterprise ZenPacks
    zenosslabs_snapshot "enterprise" do
        vg_name "zenoss"
        base_lv_name "core"
        percent_of_origin 20
        mount "/opt/zenoss"
        action [ :create, :switch ]
    end

    %w{mysqld zenoss}.each do |service_name|
        service service_name do
            action :start
        end
    end

    zenoss_enterprise_zenpacks_rpm = "#{node[:zenoss][:enterprise_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
    cookbook_file "/tmp/#{zenoss_enterprise_zenpacks_rpm}" do
        source zenoss_enterprise_zenpacks_rpm
    end

    yum_package "zenoss-enterprise-zenpacks" do
        source "/tmp/#{zenoss_enterprise_zenpacks_rpm}"
        options "--nogpgcheck"
    end

    # Switch to a "working" snapshot to keep snapshots pristine.
    zenosslabs_snapshot "working" do
        vg_name "zenoss"
        base_lv_name "enterprise"
        percent_of_origin 20
        mount "/opt/zenoss"
        action [ :create, :switch ]
    end
end
