#
# Cookbook Name:: zenosslabs
# Recipe:: zenpacks-www-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

user "zenpacks" do
    home "/srv/zenpacks"
    # password "$1$m/1RGn/l$p01/HA0h04t2xLWW0Ayes/"
end

%w{files wsgi-scripts}.each do |dir|
    directory "/srv/zenpacks/#{dir}" do
        owner "zenpacks"
        group "zenpacks"
        mode 0755
        recursive true
        action :create
    end
end

# Using bottle as the Python web micro-framework.
execute "pip install bottle" do
    creates "/usr/local/bin/bottle.py"
end

cookbook_file "/srv/zenpacks/wsgi-scripts/zenpacks_api.wsgi" do
    source "zenpacks_api.wsgi"
    owner "zenpacks"
    group "zenpacks"
    mode 0755
end

%w{apache2 apache2::mod_autoindex apache2::mod_wsgi}.each do |recipe|
    include_recipe recipe
end

web_app "zenpacks.zenosslabs.com" do
    template "zenpacks_www.conf.erb"
    server_name "zenpacks.zenosslabs.com"
    server_aliases [node['hostname'], node['fqdn'], node['ipaddress']]
    docroot "/srv/zenpacks/files"
end
