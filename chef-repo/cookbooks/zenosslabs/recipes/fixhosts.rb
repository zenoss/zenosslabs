#
# Cookbook Name:: zenosslabs
# Recipe:: fixhosts
#
# Copyright 2011, Zenoss, Inc.
#

# RabbitMQ won't work without a resolvable hostname.
ruby_block "edit etc hosts" do
    block do
        rc = Chef::Util::FileEdit.new("/etc/hosts")
        rc.search_file_replace_line(
            /^127\.0\.0\.1\s+localhost\.localdomain\s+localhost$/,
            "127.0.0.1\t#{node[:fqdn]} #{node[:hostname]} localhost.localdomain localhost")

        rc.write_file
    end
end
