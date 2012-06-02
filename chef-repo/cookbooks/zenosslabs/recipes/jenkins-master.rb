#
# Cookbook Name:: zenosslabs
# Recipe:: jenkins-master
#
# Copyright 2011, Zenoss, Inc.
#

%w{git java jenkins}.each do |recipe|
    include_recipe recipe
end

package "subversion" do
    action :install
end

include_recipe "zenosslabs::jenkins-common"

# Install Jenkins.
include_recipe "jenkins"

# Install Jenkins plugins.
%w(git analysis-core analysis-collector bulk-builder htmlpublisher warnings publish-over-ssh).each do |plugin|
    if not FileTest.exist?("/var/lib/jenkins/plugins/#{plugin}.hpi")
        jenkins_cli "install-plugin #{plugin}"
        jenkins_cli "safe-restart"
    end
end

# Install scripts and configuration file to discover Jenkins jobs.
cookbook_file "/usr/local/bin/discover_zenpacks" do
    source "discover_zenpacks"
    mode "0755"
end

template "/var/lib/jenkins/jobs.yaml" do
    owner "jenkins"
    group "jenkins"
    mode 0644
    source "jobs.yaml.erb"
    variables(
        :discovery_jobs => node[:zenosslabs][:jenkins_jobs][:discovery_jobs],
        :zenpack_jobs => node[:zenosslabs][:jenkins_jobs][:zenpack_jobs]
    )
end
