#
# Cookbook Name:: zenosslabs
# Recipe:: zenpack-build-deps
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

node[:zenoss] = {
    "zends_rpm" => "zends-5.5.15-1.r51230",
    "version_tags" => %w{321 411}
}


# Run List
recipes = [
    "selinux::disabled",
    "git",
    "java",
    "zenosslabs::fixhosts",
    "zenosslabs::jenkins-slave",
    "sudo",
    "zenosslabs::build-tools"
]

recipes.each do |recipe|
    include_recipe recipe
end
