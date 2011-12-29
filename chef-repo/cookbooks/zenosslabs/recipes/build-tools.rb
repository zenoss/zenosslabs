#
# Cookbook Name:: zenosslabs
# Recipe:: build-tools
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

cookbook_file "/usr/local/bin/test_zenpack.py" do
    source "test_zenpack.py"
end
