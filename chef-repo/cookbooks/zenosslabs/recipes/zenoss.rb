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
    managed_services = %w{snmpd}
    managed_packages = %w{net-snmp net-snmp-utils gmp libgomp liberation-fonts}

    # According to the Zenoss 4.1.1 installation documentation we need to
    # explicitely install the .x86_64 version of the libgcj package on x86_64
    # systems.
    if rpm_arch == "x86_64"
        managed_packages += %w{libgcj.x86_64}
    elsif rpm_arch == "i386"
        managed_packages += "libgcj"
    end

    # Zenoss 3
    if node[:zenoss][:version].start_with? '3'
        managed_packages += %w{mysql-server}
        managed_services += %w(mysql-server)

    # Zenoss 4
    elsif node[:zenoss][:version].start_with? '4'
        rpm_package "zenossdeps" do
            source "http://deps.zenoss.com/yum/zenossdeps.el5.noarch.rpm"
        end

        zends_rpm = "#{node[:zenoss][:zends_rpm]}.#{rpm_release}.#{rpm_arch}.rpm"
        cookbook_file "/tmp/#{zends_rpm}" do
            source zends_rpm
        end

        rpm_package "zends" do
            source "/tmp/#{zends_rpm}"
        end

        managed_package += %w{tk unixODBC erlang rabbitmq-server memcached perl-DBI libxslt}
        managed_services += %w{zends rabbitmq-server memcached}
    end

    managed_packages.each do |pkg|
        yum_package pkg
    end

    managed_services.each do |svc|
        service svc do
            action [ :disable, :start ]
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
    if %q(platform core enterprise resmgr).include? node[:zenoss][:flavor]
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

        # Alias wget to true so Zenoss startup doesn't have to wait for the
        # initial device add to timeout.
        execute "alias wget=true"

        service "zenoss" do
            action [ :disable, :start ]
        end

        execute "unalias wget"
    end

    # Optionally install Core ZenPacks.
    if %q(core enterprise resmgr).include? node[:zenoss][:flavor]
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
    if %q(enterprise resmgr).include? node[:zenoss][:flavor]
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

    service "zenoss" do
        action :stop
    end

    # Shutdown and cleanup package database.
    managed_services.each do |service_name|
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
