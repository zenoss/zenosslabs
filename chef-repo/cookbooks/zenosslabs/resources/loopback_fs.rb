#
# Cookbook Name:: zenosslabs
# Resource:: loopback_fs
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

actions :create

attribute :name, :kind_of => String, :name_attribute => true
attribute :block_size, :kind_of => Integer, :default => 4096
attribute :bytes, :kind_of => Integer
attribute :vg_name, :kind_of => String
