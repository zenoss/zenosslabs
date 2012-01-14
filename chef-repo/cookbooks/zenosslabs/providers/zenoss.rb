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

        if new_resource.version.start_with? '4'
            managed_packages += %w{tk unixODBC erlang rabbitmq-server memcached libxslt}
            managed_services += %w{rabbitmq-server memcached}
        end

        # ZenDS will be installed later as one of the packages in
        # new_resource.packages.
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


        # Each Zenoss configuration needs to have its database (MySQL or ZenDS)
        # data isolated.
        service new_resource.database[:service] do
            action :stop
        end

        if new_resource.database[:package][:url_prefix].nil?
            package new_resource.database[:package][:name] do
                action :install
            end

            execute "yum -y reinstall #{new_resource.database[:package][:name]}" do
                not_if "test -f /opt/zenoss/.installed.#{new_resource.database[:package][:name]}"
            end
        else
            rpm_filename = "#{new_resource.database[:package][:rpm_prefix]}.#{rpm_release}.#{rpm_arch}.rpm"

            remote_file "/tmp/#{rpm_filename}" do
                source "#{new_resource.database[:package][:url_prefix]}#{rpm_filename}"
                action :create_if_missing
            end

            package "perl-DBI"

            rpm_package new_resource.database[:package][:name] do
                source "/tmp/#{rpm_filename}"
                options "--nodeps --replacepkgs --replacefiles"
                not_if "test -f /opt/zenoss/.installed.#{new_resource.database[:package][:name]}"
            end

            template "/opt/zends/etc/zends.cnf" do
                owner "root"
                group "root"
                mode 0644
                source "zends.cnf.erb"
            end
        end

        file "/opt/zenoss/.installed.#{new_resource.database[:package][:name]}"

        execute "rpm -e #{new_resource.database[:package][:name]} --justdb --nodeps --noscripts --notriggers" do
            only_if "rpm -q #{new_resource.database[:package][:name]}"
        end

        execute "mv #{new_resource.database[:datadir]} /opt/zenoss/datadir" do
            not_if "test -d /opt/zenoss/datadir"
        end

        link new_resource.database[:datadir] do
            to "/opt/zenoss/datadir"
        end

        service new_resource.database[:service] do
            action [ :disable, :start ]
        end


        # Install Zenoss.
        new_resource.packages.each do |zenoss_pkg|
            rpm_filename = "#{zenoss_pkg[:rpm_prefix]}.#{rpm_release}.#{rpm_arch}.rpm"

            remote_file "/tmp/#{rpm_filename}" do
                source "#{zenoss_pkg[:url_prefix]}#{rpm_filename}"
                action :create_if_missing
            end

            rpm_package zenoss_pkg[:name] do
                source "/tmp/#{rpm_filename}"
                options "--nodeps --replacepkgs --replacefiles"
                not_if "test -f /opt/zenoss/.installed.#{rpm_filename}"
            end

            file "/opt/zenoss/.installed.#{rpm_filename}"

            execute "rpm -e #{zenoss_pkg[:name]} --justdb --nodeps --noscripts --notriggers" do
                only_if "rpm -q #{zenoss_pkg[:name]}"
            end

            # Installation steps specific to the main zenoss package.
            if zenoss_pkg[:name] == "zenoss"
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
                        :daemons => new_resource.daemons
                    )
                end

                if new_resource.daemons.include? 'zeneventd'
                    template "/opt/zenoss/etc/zeneventd.conf" do
                        owner "zenoss"
                        group "zenoss"
                        mode 0644
                        source "zeneventd.conf.erb"
                    end
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
                    to "/bin/true"
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

        execute "su - zenoss -c 'pip install pyflakes'" do
            creates "/opt/zenos/bin/pyflakes"
        end

        execute "su - zenoss -c 'pip install pep8'" do
            creates "/opt/zenos/bin/pep8"
        end


        # Shutdown Zenoss and related services and unmout logical volume.
        execute "service zenoss stop" do
            returns [0,1,2,3,4,5,6,7,8,9]
        end

        ([new_resource.database[:service]] + managed_services).each do |service_name|
            service service_name do
                action :stop
            end
        end

        # Somehow MySQL files are becoming owned by the zenoss user during this
        # process. Fixing it with a sledgehammer.
        if new_resource.database[:name] == 'mysql'
            execute "chown -R mysql:mysql /opt/zenoss/datadir"
        end

        zenosslabs_lvm_fs "zenoss/#{lv_name}" do
            action :umount
        end
    end
end
