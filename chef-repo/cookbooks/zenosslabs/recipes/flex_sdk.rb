# Recipe:: flex_sdk
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

flex = "flex_sdk_4.5.1.21328A"
flex_zip = "#{flex}.zip"
flex_url = "http://fpdownload.adobe.com/pub/flex/sdk/builds/flex4.5/#{flex_zip}"

remote_file "/opt/#{flex_zip}" do
    source flex_url
    action :create_if_missing
end

execute "unzip -q -d /opt/#{flex} /opt/#{flex_zip}" do
    creates "/opt/#{flex}/bin/compc"
end

execute "chmod -R +rx /opt/#{flex}"

link "/opt/flex_sdk" do
    to "/opt/#{flex}"
end
