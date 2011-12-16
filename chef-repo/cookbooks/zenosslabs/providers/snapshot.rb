#
# Cookbook Name:: zenosslabs
# Provider:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

action :nothing do
    # Needed for initializing resources for later notification.
end

action :create do
    execute "create snapshot" do
        not_if "test -f /dev/mapper/#{new_resource.vg_name}-#{new_resource.name}"
        command "lvcreate -l#{new_resource.percent_of_origin}%ORIGIN -s -n #{new_resource.name} /dev/#{new_resource.vg_name}/#{new_resource.base_lv_name}"
    end
end

action :switch do
    %w{zenoss mysqld snmpd}.each do |service_name|
        service service_name do
            action :stop
        end
    end

    mount new_resource.mount do
        :unmount
    end

    mount new_resource.mount do
        device "/dev/mapper/#{new_resource.vg_name}-#{new_resource.name}"
        fstype "ext3"
    end

    %w{mysqld snmpd zenoss}.each do |service_name|
        service service_name do
            action :start
        end
    end
end