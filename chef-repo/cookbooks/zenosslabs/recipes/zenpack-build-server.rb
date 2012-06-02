#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-server
#
# Copyright 2011, Zenoss, Inc.
#

# Attributes
node[:authorization] = {
    "sudo" => {
        "env_keep" => ['WORKSPACE', 'BUILD_TAG'],
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
%w{lsof python-devel openldap-devel pcre-devel autoconf}.each do |pkg_name|
    package pkg_name
end

%w{zenoss_manager zenpack_harness}.each do |script|
    cookbook_file "/usr/local/bin/#{script}" do
        source script
        mode "0755"
    end
end

node[:zenoss][:versions].each do |version|
    version[:flavors].each do |flavor|
        installed_file = "/.installed.#{version[:name]}_#{flavor[:name]}"

        zenosslabs_zenoss "#{version[:name]} #{flavor[:name]}" do
            not_if "test -f #{installed_file}"
            version version[:name]
            flavor flavor[:name]
            database version[:database]
            daemons version[:daemons]
            extra_daemons flavor[:extra_daemons] or []
            packages flavor[:packages]
            action :install
        end

        # This speeds up repeated runs considerably. However, if something is
        # changed within the zenoss resource provider, these install files will
        # need to be manually deleted.
        file installed_file
    end
end

template "/home/zenoss/.bashrc" do
    owner "zenoss"
    group "zenoss"
    mode 0644
    source "zenoss_bashrc.erb"
end

directory "/home/zenoss/.m2" do
    owner "zenoss"
    group "zenoss"
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

# Make jenkins and zenoss members of each other's groups. This is done because
# ZenPack source lives under the Jenkins workspace, but must be built by zenoss.
group "jenkins" do
    members ["zenoss"]
end

group "zenoss" do
    members ["jenkins"]
end

# The jenkins workspace can get quite large. Mount it on secondary storage.
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
