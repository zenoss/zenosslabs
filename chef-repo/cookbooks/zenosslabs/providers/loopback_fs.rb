#
# Cookbook Name:: zenosslabs
# Provider:: loopback_fs
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

require 'chef/mixin/shell_out'
include Chef::Mixin::ShellOut


action :create do
    vg_name = new_resource.vg_name
    image_directory = "/var/lib/diskimages"
    image_file = "#{image_directory}/#{vg_name}.img"
    loop_dev = "/dev/loop0"
    lv_name = "#{vg_name}/base"
    lv_dev = "/dev/mapper/#{vg_name}-base"

    # Double the blocks to leave room for LVM snapshots.
    blocks = (new_resource.bytes / new_resource.block_size) * 2

    directory image_directory do
        owner "root"
        group "root"
        mode "0755"
        recursive true
        action :create
    end

    execute "create image" do
        not_if "test -f #{image_file}"
        command "dd if=/dev/zero of=#{image_file} bs=#{new_resource.block_size} count=#{blocks}"
    end

    execute "loop image" do
        not_if { shell_out("losetup -a").stdout.include?(image_file) }
        command "losetup #{loop_dev} #{image_file}"
    end

    execute "create lvm physical volume" do
        not_if "pvdisplay -s #{loop_dev} || false"
        command "pvcreate #{loop_dev}"
    end

    execute "create lvm volume group" do
        not_if "vgdisplay -s #{vg_name}"
        command "vgcreate #{vg_name} #{loop_dev}"
    end

    execute "create lvm base logical volume" do
        not_if "lvdisplay -c #{lv_name}"
        command "lvcreate -L#{new_resource.bytes}B -n base #{vg_name}"
    end

    execute "format base logical volume" do
        not_if "file -sL #{lv_dev} | grep 'ext3 filesystem data'"
        command "mkfs.ext3 #{lv_dev}"
    end

    directory new_resource.name do
        owner "root"
        group "root"
        mode "0755"
        recursive true
        action :create
    end

    mount new_resource.name do
        device lv_dev
        fstype "ext3"
    end
end
