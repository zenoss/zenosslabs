#
# Cookbook Name:: zenosslabs
# Recipe:: jenkins-common
#
# Copyright 2011, Zenoss, Inc.
#

# Create jenkins user.
user "jenkins" do
    comment "Jenkins"
    home "/var/lib/jenkins"
end

# Jenkins directory needs to be group-executable.
directory "/var/lib/jenkins" do
    mode "0750"
end

# Setup keys and trust.
directory "/var/lib/jenkins/.ssh" do
    owner "jenkins"
    group "jenkins"
    mode "0700"
    action :create
end

# Templatize the .bashrc.
template "/var/lib/jenkins/.bashrc" do
    owner "jenkins"
    group "jenkins"
    mode 0644
    source "jenkins_bashrc.erb"
end

%w{id_rsa id_rsa.pub known_hosts authorized_keys}.each do |file|
    case file
    when "id_rsa", "authorized_leys"
        mode = 0600
    else
        mode = 0644
    end

    cookbook_file "/var/lib/jenkins/.ssh/#{file}" do
        source "jenkins.ssh/#{file}"
        mode { mode }
        owner "jenkins"
        group "jenkins"
    end
end
