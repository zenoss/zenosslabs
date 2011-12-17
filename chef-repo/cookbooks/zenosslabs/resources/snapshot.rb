#
# Cookbook Name:: zenosslabs
# Resource:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

actions :create, :switch

attribute :name, :kind_of => String, :name_attribute => true
attribute :vg_name, :kind_of => String
attribute :base_lv_name, :kind_of => String
attribute :percent_of_origin, :kind_of => Integer, :default => 16
attribute :mount, :kind_of => String