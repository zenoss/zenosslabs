#
# Cookbook Name:: zenosslabs
# Recipe:: maven
#
# Copyright 2011, Zenoss, Inc.
#

maven_tarball = "apache-maven-3.0.4-bin.tar.gz"
maven_url = "http://mirrors.axint.net/apache/maven/binaries/#{maven_tarball}"

remote_file "/opt/#{maven_tarball}" do
    source maven_url
    action :create_if_missing
end

execute "tar xf #{maven_tarball}" do
    cwd "/opt"
    creates "/opt/apache-maven-3.0.3/bin/mvn"
end

link "/opt/maven" do
    to "/opt/apache-maven-3.0.3"
end
