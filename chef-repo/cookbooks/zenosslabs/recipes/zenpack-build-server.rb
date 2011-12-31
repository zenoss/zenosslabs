#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Attributes
node[:authorization] = {
    "sudo" => {
        "users" => ["jenkins"],
        "passwordless" => true
    }
}

node[:java] = {
    "install_flavor" => "sun"
}


# Recipes
include_recipe "selinux::disabled"
include_recipe "git"
include_recipe "java"
include_recipe "zenosslabs::fixhosts"
include_recipe "zenosslabs::jenkins-slave"
include_recipe "sudo"


# Resources
cookbook_file "/usr/local/bin/test_zenpack.py" do
    source "test_zenpack.py"
    mode "0755"
end

node[:zenoss][:versions].each do |version|
    version[:flavors].each do |flavor|
        zenosslabs_zenoss "#{version} #{flavor}" do
            version version
            flavor flavor
            packages flavor[:packages]
            action :install
        end
    end
end

group "jenkins" do
    members ["zenoss"]
end

group "zenoss" do
    members ["jenkins"]
end
