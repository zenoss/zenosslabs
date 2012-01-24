#
# Cookbook Name:: zenosslabs
# Provider:: lvm_fs
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

action :create do
    device = new_resource.device
    vg_name = new_resource.vg_name
    lv_name = new_resource.lv_name
    size = new_resource.size

    fq_lv_name = "#{vg_name}/#{lv_name}"


    execute "pvcreate #{device}" do
        not_if "pvdisplay #{device}"
    end

    execute "vgcreate #{vg_name} #{device}" do
        not_if "vgdisplay #{vg_name}"
    end

    execute "lvcreate -L#{size} -n #{lv_name} #{vg_name}" do
        not_if "lvdisplay #{fq_lv_name}"
    end
end

action :format do
    lv_device = "/dev/mapper/#{new_resource.vg_name}-#{new_resource.lv_name}"


    execute "mkfs.ext3 #{lv_device}" do
        not_if "file -sL #{lv_device} | grep 'ext3 filesystem data'"
    end
end

action :mount do
    mount_point = new_resource.mount_point

    lv_device = "/dev/mapper/#{new_resource.vg_name}-#{new_resource.lv_name}"


    directory mount_point do
        recursive true
        action :create
    end

    mount mount_point do
        device lv_device
        fstype "ext3"
    end
end

action :umount do
    mount_point = new_resource.mount_point

    lv_device = "/dev/mapper/#{new_resource.vg_name}-#{new_resource.lv_name}"

    execute "kill -9 $(lsof -Fp /opt/zenoss | cut -b2-)"

    mount mount_point do
        device lv_device
        fstype "ext3"
        action :umount
    end    
end
