#
# Cookbook Name:: zenosslabs
# Recipe:: zenpacks-www-server
#
# Copyright 2011, Zenoss, Inc.
#

user "zenpacks" do
    home "/srv/zenpacks"
    # password "$1$m/1RGn/l$p01/HA0h04t2xLWW0Ayes/"
end

%w{files wsgi-scripts/templates}.each do |dir|
    directory "/srv/zenpacks/#{dir}" do
        owner "zenpacks"
        group "zenpacks"
        mode 0755
        recursive true
        action :create
    end
end

# Using Flask as the Python web micro-framework.
execute "pip install flask" do
    creates "/usr/local/lib/python2.6/dist-packages/flask/__init__.py"
end

execute "pip install Flask-XML-RPC" do
    creates "/usr/local/lib/python2.6/dist-packages/flaskext/xmlrpc.py"
end

%w{zenpacks_server.wsgi templates/zenpacks_list.html}.each do |wsgi|
    cookbook_file "/srv/zenpacks/wsgi-scripts/#{wsgi}" do
        source wsgi
        owner "zenpacks"
        group "zenpacks"
        mode 0755
    end
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
