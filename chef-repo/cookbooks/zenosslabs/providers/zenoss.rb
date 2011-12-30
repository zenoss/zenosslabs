#
# Cookbook Name:: zenosslabs
# Provider:: zenoss
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

action :install do
    case node[:platform]
    when "centos"
        rpm_release = node[:kernel][:release].split('.')[-1]

        if node[:kernel][:machine] == "i686"
            rpm_arch = "i386"
        else
            rpm_arch = node[:kernel][:machine]
        end

        zenoss_daemons = []

        # Install dependencies.
        managed_services = %w{snmpd}
        managed_packages = %w{net-snmp net-snmp-utils gmp libgomp liberation-fonts}

        # According to the Zenoss 4.1.1 installation documentation we need to
        # explicitly install the .x86_64 version of the libgcj package on x86_64
        # systems.
        if rpm_arch == "x86_64"
            managed_packages += %w{libgcj.x86_64}
        elsif rpm_arch == "i386"
            managed_packages += "libgcj"
        end

        # Zenoss 3
        if new_resource.version.start_with? '3'
            zenoss_daemons += %w{zeoctl}
            managed_packages += %w{mysql-server}
            managed_services += %w(mysqld)

        # Zenoss 4
        elsif new_resource.version.start_with? '4'
            zenoss_daemons += %w{zeneventserver zeneventd}

            # perl-DBI is a dependency for zends.
            yum_package "perl-DBI"

            zends_rpm = "#{new_resource.zends_rpm}.#{rpm_release}.#{rpm_arch}.rpm"
            cookbook_file "/tmp/#{zends_rpm}" do
                source zends_rpm
            end

            rpm_package "zends" do
                source "/tmp/#{zends_rpm}"
            end

            # This requires either EPEL or deps.zenoss.com be added to yum.repos.d.
            managed_packages += %w{tk unixODBC erlang rabbitmq-server memcached libxslt}
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
        lv_name = "#{new_resource.version}_#{new_resource.flavor}"
        zenosslabs_lvm_fs "zenoss/#{lv_name}" do
            device "/dev/vdb"
            vg_name "zenoss"
            lv_name lv_name
            size "2G"
            mount_point "/opt/zenoss"
            action [ :create, :format, :mount ]
        end

        # Install Zenoss Platform.
        if %q(platform core enterprise resmgr).include? new_resource.flavor
            zenoss_rpm = "#{new_resource.platform_rpm}.#{rpm_release}.#{rpm_arch}.rpm"
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
                variables(
                    :daemons => zenoss_daemons
                )
            end

            # Alias wget to true so Zenoss startup doesn't have to wait for the
            # initial device add to timeout.
            link "/usr/local/bin/wget" do
                to "/bin/true"
                only_if "test -f /opt/zenoss/.fresh_install || test -f /opt/zenoss/.upgraded"
                action :create
            end

            service "zenoss" do
                only_if "test -f /opt/zenoss/.fresh_install || test -f /opt/zenoss/.upgraded"
                action [ :disable, :start ]
            end

            link "/usr/local/bin/wget" do
                action :delete
            end
        end

        # Optionally install Core ZenPacks.
        if %q(core enterprise resmgr).include? new_resource.flavor
            zenoss_core_zenpacks_rpm = "#{new_resource.core_zenpacks_rpm}.#{rpm_release}.#{rpm_arch}.rpm"
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
        if %q(enterprise resmgr).include? new_resource.flavor
            zenoss_enterprise_zenpacks_rpm = "#{new_resource.enterprise_zenpacks_rpm}.#{rpm_release}.#{rpm_arch}.rpm"
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
        service "zenoss" do
            action :stop
        end

        managed_services.each do |service_name|
            service service_name do
                action :stop
            end
        end

        if %q(enterprise resmgr).include? new_resource.flavor
            rpm_package "zenoss-enterprise-zenpacks" do
                options "--justdb --nodeps --noscripts --notriggers"
                action :remove
            end
        end

        if %q(core enterprise resmgr).include? new_resource.flavor
            rpm_package "zenoss-core-zenpacks" do
                options "--justdb --noscripts --notriggers"
                action :remove
            end
        end

        if %q(platform core enterprise resmgr).include? new_resource.flavor
            rpm_package "zenoss" do
                options "--justdb --noscripts --notriggers"
                action :remove
            end
        end


        # Extra Python tools required for building and testing must be
        # installed into each Zenoss configuration because Zenoss bundles its
        # own Python.
        execute "su - zenoss -c 'easy_install pip'" do
            creates "/opt/zenoss/bin/pip"
        end

        execute "su - zenoss -c 'pip install nose'" do
            creates "/opt/zenoss/bin/nosetests"
        end

        execute "su - zenoss -c 'pip install coverage'" do
            creates "/opt/zenoss/bin/coverage"
        end


        # Unmount or logical volume.
        zenosslabs_lvm_fs "zenoss/#{lv_name}" do
            action :umount
        end
    end
end
