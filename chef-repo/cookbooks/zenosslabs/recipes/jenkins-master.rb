#
# Cookbook Name:: zenosslabs
# Recipe:: jenkins-master
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

include_recipe "zenosslabs::jenkins-common"

# Install Jenkins.
include_recipe "jenkins"

# Create an example job.
cookbook_file "/tmp/ZenPacks.zenoss.SolarisMonitor.job.xml" do
    source "jenkins-jobs/ZenPacks.zenoss.SolarisMonitor.job.xml"
    mode 0644
    owner "jenkins"
    group "jenkins"
end

jenkins_job "ZenPacks.zenoss.SolarisMonitor" do
    not_if "test -f /var/lib/jenkins/jobs/#{name}/config.xml"
    config "/tmp/ZenPacks.zenoss.SolarisMonitor.job.xml"
    action :create
end

# Install Jenkins plugins.
%w(git).each do |plugin|
    if not FileTest.exist?("/var/lib/jenkins/plugins/#{plugin}.hpi")
        jenkins_cli "install-plugin #{plugin}"
        jenkins_cli "safe-restart"
    end
end
