#
# Cookbook Name:: zenosslabs
# Resource:: snapshot
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

actions :create

attribute :name, :kind_of => String, :name_attribute => true
attribute :version, :kind_of => String
