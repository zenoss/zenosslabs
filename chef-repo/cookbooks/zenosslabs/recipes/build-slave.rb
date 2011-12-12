#
# Cookbook Name:: zenosslabs
# Recipe:: build-slave
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

#include_recipe "zenosslabs"

include_recipe "git"
include_recipe "java"
include_recipe "zenosslabs::jenkins-slave"
include_recipe "zenosslabs::zenoss"
