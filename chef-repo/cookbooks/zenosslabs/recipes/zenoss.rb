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
    lv_name = "#{node[:zenoss][:version]}_#{node[:zenoss][:flavor]}"
    zenosslabs_lvm_fs "zenoss/#{lv_name}" do
        device "/dev/vdb"
        vg_name "zenoss"
        lv_name lv_name
        size "2G"
        mount_point "/opt/zenoss"
        action [ :create, :format, :mount ]
    end

    # Install Zenoss Platform.
    if %q(platform core enterprise).include? node[:zenoss][:flavor]
        zenoss_rpm = "#{node[:zenoss][:platform_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zenoss_rpm}" do
            source zenoss_rpm
        end

        rpm_package "zenoss" do
            source "/tmp/#{zenoss_rpm}"
            options "--nodeps --replacepkgs --replacefiles"
            not_if "test -f /opt/zenoss/.installed.#{zenoss_rpm}"
            action :install
        end

        file "/opt/zenoss/.installed.#{zenoss_rpm}"

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
    end

    # Optionally install Core ZenPacks.
    if %q(core enterprise).include? node[:zenoss][:flavor]
        zenoss_core_zenpacks_rpm = "#{node[:zenoss][:core_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zenoss_core_zenpacks_rpm}" do
            source zenoss_core_zenpacks_rpm
        end

        rpm_package "zenoss-core-zenpacks" do
            source "/tmp/#{zenoss_core_zenpacks_rpm}"
            options "--nodeps --replacepkgs --replacefiles"
            not_if "test -f /opt/zenoss/.installed.#{zenoss_core_zenpacks_rpm}"
            action :install
        end

        file "/opt/zenoss/.installed.#{zenoss_core_zenpacks_rpm}"
    end

    # Install Enterprise ZenPacks
    if %q(enterprise).include? node[:zenoss][:flavor]
        zenoss_enterprise_zenpacks_rpm = "#{node[:zenoss][:enterprise_zenpacks_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zenoss_enterprise_zenpacks_rpm}" do
            source zenoss_enterprise_zenpacks_rpm
        end

        rpm_package "zenoss-enterprise-zenpacks" do
            source "/tmp/#{zenoss_enterprise_zenpacks_rpm}"
            options "--nodeps --replacepkgs --replacefiles"
            not_if "test -f /opt/zenoss/.installed.#{zenoss_enterprise_zenpacks_rpm}"
            action :install
        end

        file "/opt/zenoss/.installed.#{zenoss_enterprise_zenpacks_rpm}"
    end

    # Shutdown and cleanup package database.
    %w{zenoss mysqld snmpd}.each do |service_name|
        service service_name do
            action :stop
        end
    end

    zenosslabs_lvm_fs "zenoss/#{lv_name}" do
        action :umount
    end

    if %q(enterprise).include? node[:zenoss][:flavor]
        rpm_package "zenoss-enterprise-zenpacks" do
            options "--justdb --nodeps --noscripts --notriggers"
            action :remove
        end
    end

    if %q(core enterprise).include? node[:zenoss][:flavor]
        rpm_package "zenoss-core-zenpacks" do
            options "--justdb --noscripts --notriggers"
            action :remove
        end
    end

    if %q(platform core enterprise).include? node[:zenoss][:flavor]
        rpm_package "zenoss" do
            options "--justdb --noscripts --notriggers"
            action :remove
        end
    end
end
