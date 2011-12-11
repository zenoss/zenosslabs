#
# Cookbook Name:: zenosslabs
# Recipe:: jenkins-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::default"

# Install Jenkins server.
include_recipe "jenkins"

# Create an example job.
cookbook_file "/tmp/ZenPacks.zenoss.SolarisMonitor.job.xml" do
    source "jenkins-jobs/ZenPacks.zenoss.SolarisMonitor.job.xml"
    mode 0644
    owner "jenkins"
    group "jenkins"
end

jenkins_job "ZenPacks.zenoss.SolarisMonitor" do
    config "/tmp/ZenPacks.zenoss.SolarisMonitor.job.xml"
    action :create
end

# Install Jenkins plugins.
%w(git).each do |plugin|
    jenkins_cli "install-plugin #{plugin}"
    jenkins_cli "safe-restart"
end


# Install SSH keys for GitHub.
cookbook_file "/var/lib/jenkins/.ssh/id_rsa" do
    source "jenkins.ssh/id_rsa"
    mode 0600
    owner "jenkins"
    group "jenkins"
end

cookbook_file "/var/lib/jenkins/.ssh/id_rsa.pub" do
    source "jenkins.ssh/id_rsa.pub"
    mode 0644
    owner "jenkins"
    group "jenkins"
end

cookbook_file "/var/lib/jenkins/.ssh/known_hosts" do
    source "jenkins.ssh/known_hosts"
    mode 0644
    owner "jenkins"
    group "jenkins"
end
