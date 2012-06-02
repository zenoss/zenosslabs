#
# Cookbook Name:: zenosslabs
# Recipe:: ant
#
# Copyright 2011, Zenoss, Inc.
#

ant_tarball = "apache-ant-1.8.2-bin.tar.gz"
ant_url = "http://mirrors.axint.net/apache/ant/binaries/#{ant_tarball}"

remote_file "/opt/#{ant_tarball}" do
    source ant_url
    action :create_if_missing
end

execute "tar xf #{ant_tarball}" do
    cwd "/opt"
    creates "/opt/apache-ant-1.8.2/bin/ant"
end

link "/opt/ant" do
    to "/opt/apache-ant-1.8.2"
end
