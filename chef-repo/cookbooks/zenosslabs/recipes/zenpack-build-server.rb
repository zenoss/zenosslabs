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
include_recipe "zenosslabs::ant"
include_recipe "zenosslabs::maven"
include_recipe "zenosslabs::flex_sdk"
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
            database version[:database]
            daemons version[:daemons]
            packages flavor[:packages]
            action :install
        end
    end
end

template "/home/zenoss/.bashrc" do
    owner "zenoss"
    group "zenoss"
    mode 0644
    source "zenoss_bashrc.erb"
end

directory "/home/zenoss/.m2" do
    mode 0755
    action :create
end

template "/home/zenoss/.m2/settings.xml" do
    owner "zenoss"
    group "zenoss"
    mode 0644
    source "m2_settings.xml.erb"
    variables(
        :repositories => [
            {
                :id => 'central',
                :url => 'http://cmrepo.zenoss.loc/nexus/content/groups/public'
            },{
                :id => 'releases',
                :url => 'http://cmrepo.zenoss.loc/nexus/content/repositories/releases'
            },{
                :id => 'snapshots',
                :url => 'http://cmrepo.zenoss.loc/nexus/content/repositories/snapshots'
            }
        ],

        :plugin_repositories => [
            {
                :id => 'zenoss.plugins',
                :url => 'http://cmrepo.zenoss.loc/nexus/content/repositories/public'
            }
        ]
    )
end

group "jenkins" do
    members ["zenoss"]
end

group "zenoss" do
    members ["jenkins"]
end

# The jenkins workspace can get quite large. Mount it elsewhere.
directory "/var/lib/jenkins/workspace" do
    owner "jenkins"
    group "jenkins"
    mode "0755"
    action :create
end

zenosslabs_lvm_fs "zenoss/workspace" do
    device "/dev/vdb"
    vg_name "zenoss"
    lv_name "workspace"
    size "10G"
    mount_point "/var/lib/jenkins/workspace"
    action [ :create, :format, :mount ]
end
