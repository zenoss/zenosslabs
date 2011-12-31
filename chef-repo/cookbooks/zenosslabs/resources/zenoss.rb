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
attribute :packages, :kind_of => Array
