#
# Cookbook Name:: zenosslabs
# Resource:: zenoss
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

actions :install

attribute :name, :kind_of => String, :name_attribute => true
attribute :version, :kind_of => String
attribute :flavor, :kind_of => String
attribute :zends_rpm, :kind_of => String, :default => nil
attribute :platform_rpm, :kind_of => String, :default => nil
attribute :core_zenpacks_rpm, :kind_of => String, :default => nil
attribute :enterprise_zenpacks_rpm, :kind_of => String, :default => nil
