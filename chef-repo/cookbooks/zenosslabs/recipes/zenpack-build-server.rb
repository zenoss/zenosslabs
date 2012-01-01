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
cookbook_file "/usr/local/bin/zenpack_harness" do
    source "zenpack_harness"
    mode "0755"
end

node[:zenoss][:versions].each do |version|
    version[:flavors].each do |flavor|
        zenosslabs_zenoss "#{version[:name]} #{flavor[:name]}" do
            version version[:name]
            flavor flavor[:name]
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
