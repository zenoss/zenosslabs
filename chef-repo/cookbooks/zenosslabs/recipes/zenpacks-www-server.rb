#
# Cookbook Name:: zenosslabs
# Recipe:: zenpacks-www-server
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

%w{apache2 apache2::mod_autoindex apache2::mod_wsgi}.each do |recipe|
    include_recipe recipe
end

web_app "zenpacks.zenosslabs.com" do
    template "zenpacks_www.conf.erb"
    server_name "zenpacks.zenosslabs.com"
    server_aliases [node['hostname'], node['fqdn'], node['ipaddress']]
    docroot "/srv/www/zenpacks"
end
