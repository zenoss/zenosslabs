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
    if node[:kernel][:machine] = "i686"
        rpm_arch = "i386"
    else
        rpm_arch = node[:kernel][:machine]
    end

    dependencies = %w{mysql-server net-snmp net-snmp-utils gmp libgomp libgcj liberation-fonts}
    dependencies.each do |pkg|
        yum_package pkg do
            action :install
        end
    end

    zenosslabs_loopback_fs "/opt/zenoss" do
        vg_name "zenoss"
        block_size 4096
        bytes 1073741824  # TODO: Increase to 2GB
        action :create
    end

    directory "/opt/zenoss" do
        owner "zenoss"
        group "zenoss"
    end

    zenoss_rpm = "#{node[:zenoss][:rpm]}-#{rpm_arch}.rpm"
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

    # Define "platform" snapshot resource.
    zenosslabs_snapshot "platform" do
        vg_name "zenoss"
        base_lv_name "base"
        percent_of_origin 20
        mount "/opt/zenoss"
        action :nothing
    end

    service "zenoss" do
        only_if "test -f /opt/zenoss/.fresh_install"
        action :start

        # Create the "platform" snapshot after installing.
        notifies :create, "zenosslabs_snapshot[platform]", :immediately

        # Switch to the "platform" snapshot after stopping Zenoss to use it as
        # the foundation for further snapshots.
        notifies :switch, "zenosslabs_snapshot[platform]", :immediately
    end


    # Install Core ZenPacks
    service "zenoss" do
        action :start
    end

    # Define "core" snapshot resource.
    zenosslabs_snapshot "core" do
        vg_name "zenoss"
        base_lv_name "platform"
        percent_of_origin 20
        mount "/opt/zenoss"
        action :nothing
    end

    zenoss_core_zenpacks_rpm = "#{node[:zenoss][:core_zenpacks_rpm]}-#{rpm_arch}.rpm"
    cookbook_file "/tmp/#{zenoss_core_zenpacks_rpm}" do
        source zenoss_core_zenpacks_rpm
    end

    yum_package "zenoss-core-zenpacks" do
        source "/tmp/#{zenoss_core_zenpacks_rpm}"
        options "--nogpgcheck"

        # Create the "core" snapshot after installing.
        notifies :create, "zenosslabs_snapshot[core]", :immediately

        # Switch to the "core" snapshot after stopping Zenoss to use it as the
        # foundation for further snapshots.
        notifies :switch, "zenosslabs_snapshot[core]", :immediately
    end


    # Install Enterprise ZenPacks
    service "zenoss" do
        action :start
    end

    # Define "enterprise" snapshot resource.
    zenosslabs_snapshot "enterprise" do
        vg_name "zenoss"
        base_lv_name "core"
        percent_of_origin 20
        mount "/opt/zenoss"
        action :nothing
    end

    # Define "working" snapshot resource.
    zenosslabs_snapshot "working" do
        vg_name "zenoss"
        base_lv_name "enterprise"
        percent_of_origin 20
        mount "/opt/zenoss"
        action :nothing
    end

    zenoss_enterprise_zenpacks_rpm = "#{node[:zenoss][:enterprise_zenpacks_rpm]}-#{rpm_arch}.rpm"
    cookbook_file "/tmp/#{zenoss_enterprise_zenpacks_rpm}" do
        source zenoss_enterprise_zenpacks_rpm
    end

    yum_package "zenoss-enterprise-zenpacks" do
        source "/tmp/#{zenoss_enterprise_zenpacks_rpm}"
        options "--nogpgcheck"

        # Create the "enterprise" snapshot after installing.
        notifies :create, "zenosslabs_snapshot[enterprise]", :immediately

        # When done, create and switch to a "working" snapshot so as to not
        # dirty the enterprise snapshot.
        notifies :create, "zenosslabs_snapshot[working]", :immediately
        notifies :switch, "zenosslabs_snapshot[working]", :immediately
    end
end
