#
# Cookbook Name:: zenosslabs
# Recipe:: buildslave
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::default"

# You must manually find jdk-6u25-ea-linux-amd64.rpm and place it in the
# java cookbook's files/default/ directory. The Sun JDK is required to build
# some ZenPacks.
include_recipe "java::sun"


# Install SSH keys for GitHub.
# cookbook_file "/var/lib/jenkins/.ssh/id_rsa" do
#     source "jenkins.ssh/id_rsa"
#     mode 0600
#     owner "jenkins"
#     group "jenkins"
# end

# cookbook_file "/var/lib/jenkins/.ssh/id_rsa.pub" do
#     source "jenkins.ssh/id_rsa.pub"
#     mode 0644
#     owner "jenkins"
#     group "jenkins"
# end

# cookbook_file "/var/lib/jenkins/.ssh/known_hosts" do
#     source "jenkins.ssh/known_hosts"
#     mode 0644
#     owner "jenkins"
#     group "jenkins"
# end
