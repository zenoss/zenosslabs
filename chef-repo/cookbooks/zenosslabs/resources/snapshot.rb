#
# Cookbook Name:: zenosslabs
# Resource:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

actions :create, :mount

attribute :name, :kind_of => String, :name_attribute => true
attribute :vg_name, :kind_of => String
attribute :base_lv_name, :kind_of => String
attribute :percent_of_origin, :kind_of => Integer, :default => 15
attribute :mount_point, :kind_of => String
