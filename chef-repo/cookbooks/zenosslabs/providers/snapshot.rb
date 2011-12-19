#
# Cookbook Name:: zenosslabs
# Provider:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

action :create do
    name = new_resource.name
    vg_name = new_resource.vg_name
    percent_of_origin = new_resource.percent_of_origin
    base_lv_name = new_resource.base_lv_name

    execute "lvcreate -l#{percent_of_origin}%ORIGIN -s -n #{name} #{vg_name}/#{base_lv_name}" do
        not_if "test -b /dev/mapper/#{vg_name}-#{name}"
    end
end

action :mount do
    name = new_resource.name
    vg_name = new_resource.vg_name
    mount_point = new_resource.mount_point

    lv_device = "/dev/mapper/#{vg_name}-#{name}"


    mount mount_point do
        action :umount
    end

    mount mount_point do
        device lv_device
        fstype "ext3"
        action :mount
    end
end
