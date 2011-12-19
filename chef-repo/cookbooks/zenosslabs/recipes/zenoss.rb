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

    # Create a logical volume.
    zenosslabs_lvm_fs "zenoss/#{node[:zenoss][:version]}" do
        device "/dev/vdb"
        vg_name "zenoss"
        lv_name node[:zenoss][:version]
        size "2G"
        mount_point "/opt/zenoss"
        action [ :create, :format, :mount ]
    end

    # Install Zenoss.
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

    # Optionally install Core ZenPacks.
    if node[:zenoss][:core]
        zenoss_core_zenpacks_rpm = "#{node[:zenoss][:core_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zenoss_core_zenpacks_rpm}" do
            source zenoss_core_zenpacks_rpm
        end

        yum_package "zenoss-core-zenpacks" do
            source "/tmp/#{zenoss_core_zenpacks_rpm}"
            options "--nogpgcheck"
        end
    end

    # Install Enterprise ZenPacks
    if node[:zenoss][:enterprise]
        zenoss_enterprise_zenpacks_rpm = "#{node[:zenoss][:enterprise_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zenoss_enterprise_zenpacks_rpm}" do
            source zenoss_enterprise_zenpacks_rpm
        end

        yum_package "zenoss-enterprise-zenpacks" do
            source "/tmp/#{zenoss_enterprise_zenpacks_rpm}"
            options "--nogpgcheck"
        end
    end

    %w{zenoss mysqld snmpd}.each do |service_name|
        service service_name do
            action :stop
        end
    end

    # Create a snapshot and switch to it to keep base pristine.
    zenosslabs_snapshot "tmp" do
        vg_name "zenoss"
        base_lv_name node[:zenoss][:version]
        percent_of_origin 49
        mount_point "/opt/zenoss"
        action [ :create, :mount ]
    end

    %w{mysqld zenoss mysqld}.each do |service_name|
        service service_name do
            action :start
        end
    end
end
