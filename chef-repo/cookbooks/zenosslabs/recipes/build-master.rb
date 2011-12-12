#
# Cookbook Name:: zenosslabs
# Recipe:: build-master
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs"

include_recipe "git"
include_recipe "java"
include_recipe "zenosslabs::jenkins-master"


# Host files needed by build slaves.
include_recipe "apache2"

# Files needed by the slaves need to be manually dropped into this directory.
directory "/srv/www/chef" do
    owner "root"
    group "root"
    mode 0755
    recursive true
    action :create
end

web_app "chef_web" do
  server_name "chef.zenosslabs.com"
  docroot "/srv/www/chef"
  template "chef_web.conf.erb"
end
