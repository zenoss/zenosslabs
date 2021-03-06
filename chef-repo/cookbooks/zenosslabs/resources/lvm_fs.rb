#
# Cookbook Name:: zenosslabs
# Resource:: lvm_fs
#
# Copyright 2011, Zenoss, Inc.
#

actions :create, :format, :mount, :umount

attribute :name, :kind_of => String, :name_attribute => true
attribute :device, :kind_of => String
attribute :vg_name, :kind_of => String
attribute :lv_name, :kind_of => String
attribute :size, :kind_of => String, :default => "1G"
attribute :mount_point, :kind_of => String