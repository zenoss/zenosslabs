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


        # Prepare dependencies.
        zenoss_daemons = []
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

        if new_resource.version.start_with? '3'
            zenoss_daemons += %w{zeoctl}
            managed_packages += %w{mysql-server}
            managed_services += %w{mysqld}
        elsif new_resource.version.start_with? '4'
            zenoss_daemons += %w{zeneventserver zeneventd}
            managed_packages += %w{tk unixODBC erlang rabbitmq-server memcached libxslt perl-DBI}
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


        # Create and mount a logical volume to hold this Zenoss configuration.
        lv_name = "#{new_resource.version}_#{new_resource.flavor}"
        zenosslabs_lvm_fs "zenoss/#{lv_name}" do
            device "/dev/vdb"
            vg_name "zenoss"
            lv_name lv_name
            size "2G"
            mount_point "/opt/zenoss"
            action [ :create, :format, :mount ]
        end


        # Install Zenoss.
        new_resource.packages.each do |zenoss_pkg|
            rpm_filename = "#{zenoss_pkg}.#{rpm_release}.#{rpm_arch}.rpm"

            remote_file "/tmp/#{rpm_filename}" do
                source "#{node[:zenoss][:packages][zenoss_pkg]}#{rpm_filename}"
                action :create_if_missing
            end

            rpm_package zenoss_pkg do
                source "/tmp/#{rpm_filename}"
                options "--nodeps --replacepkgs --replacefiles"
                not_if "test -f /opt/zenoss/.installed.#{rpm_filename}"
            end

            # Remove the package from the database because we're going to be
            # installing many versions on the same system.
            if zenoss_pkg.start_with? 'zenoss-'
                file "/opt/zenoss/.installed.#{zenoss_rpm}"

                execute "rpm -e #{pkg_name} --justdb --nodeps --noscripts --notriggers" do
                    only_if "rpm -q #{pkg_name}"
                end
            end

            # Installation steps specific to the main zenoss package.
            if zenoss_pkg =~ /zenoss-\d/
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

                # Alias wget to true so Zenoss startup doesn't have to wait for
                # the initial device add to timeout.
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


        # Shutdown Zenoss and related services and unmout logical volume.
        (%w{zenoss} + managed_services).each do |service_name|

            # When zends is running it can cause mysqld's stop to error out.
            service "zends" do
                action :stop
            end

            service service_name do
                action :stop
            end
        end

        zenosslabs_lvm_fs "zenoss/#{lv_name}" do
            action :umount
        end
    end
end
