#
# Cookbook Name:: zenosslabs
# Recipe:: build-master
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "git"
include_recipe "java"
include_recipe "zenosslabs::jenkins-master"
