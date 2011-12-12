#
# Cookbook Name:: zenosslabs
# Recipe:: default
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

# Setting "UseDNS no" in /etc/ssh/sshd_config makes logins faster.
execute "nodns" do
    not_if 'grep "^UseDNS no" /etc/ssh/sshd_config'
    command 'echo "UseDNS no" >> /etc/ssh/sshd_config'
end
