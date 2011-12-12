#
# Cookbook Name:: zenosslabs
# Provider:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

require 'chef/mixin/shell_out'
include Chef::Mixin::ShellOut


action :create do
    image_directory = "/var/lib/diskimages"
    image_file = "#{image_directory}/#{new_resource.name}.img"
    loop_dev = shell_out("losetup -f").stdout.chomp
    vg_name = new_resource.name
    lv_name = "#{vg_name}/base"
    lv_dev = "/dev/mapper/#{vg_name}-base"

    case node[:platform]
    when "centos", "redhat"
        zenhome = "/opt/zenoss"
    else
        log "Not currently supported on #{node[:platform]}"
    end

    directory image_directory do
        owner "root"
        group "root"
        mode "0755"
        recursive true
        action :create
    end

    execute "create image" do
        not_if "test -f #{image_file}"
        command "dd if=/dev/zero of=#{image_file} bs=4096 count=524288"
    end

    execute "loop image" do
        not_if { shell_out("losetup -a").stdout.include?(image_file) }
        command "losetup #{loop_dev} #{image_file}"
    end

    # The image might already be looped under a different device.
    loop_dev = shell_out("losetup -a | grep '#{image_file}'").stdout.split(':')[0]
    
    execute "create lvm physical volume" do
        not_if "pvdisplay -s #{loop_dev} || false"
        command "pvcreate #{loop_dev}"
    end

    execute "create lvm volume group" do
        not_if "vgdisplay -s #{vg_name}"
        command "vgcreate #{vg_name} #{loop_dev}"
    end

    execute "import lvm volume group" do
        only_if "vgdisplay -c 2>&1 | grep 'Volume group #{vg_name} is exported'"
        command "vgimport #{vg_name}"
    end

    execute "make lvm volume group available" do
        not_if "lvdisplay -C | grep base | grep #{vg_name} | grep -- '-wi-a-'"
        command "vgchange -ay #{vg_name}"
    end

    execute "create lvm base logical volume" do
        not_if "lvdisplay -c #{lv_name}"
        command "lvcreate -L1069547520B -n base #{vg_name}"
    end

    execute "format base logical volume" do
        not_if "fsck -n #{lv_dev}"
        command "mkfs.ext3 #{lv_dev}"
    end

    directory zenhome do
        owner "root"
        group "root"
        mode "0755"
        recursive true
        action :create
    end

    execute "mount base filesystem" do
        not_if "mount | grep #{lv_dev} | grep #{zenhome}"
        command "mount #{lv_dev} #{zenhome}"
    end

    ###########################################################################

    # TODO: The real work of installing Zenoss.

    ###########################################################################

    execute "unmount base filesystem" do
        only_if "mount | grep #{lv_dev} | grep #{zenhome}"
        command "umount #{zenhome}"
    end

    execute "make lvm volume group unavailable" do
        only_if "lvdisplay -C | grep base | grep #{vg_name} | grep -- '-wi-a-'"
        command "vgchange -an #{vg_name}"
    end

    execute "export lvm volume group" do
        not_if "vgdisplay -c 2>&1 | grep 'Volume group #{vg_name} is exported'"
        command "vgexport #{vg_name}"
    end

    execute "unloop image" do
        only_if { shell_out("losetup -a").stdout.include?(image_file) }
        command "losetup -d #{loop_dev}"
    end
end
