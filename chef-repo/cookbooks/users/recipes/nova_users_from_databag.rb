#
# Cookbook Name:: users
# Recipe:: sysadmins
#
# Copyright 2009-2011, Opscode, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# TODO:
# - deal with user deletion
# - update databag with novakeys

search(:systemusers) do |u|
  new_userid = u['id']
  new_sshkey = u['ssh_keys']
  new_userproject = u['nova_project']
  Chef::Log.info("Creating user #{new_userid}")
  Chef::Log.info("Using sshkey #{new_sshkey}")
  
  #create a regular user
  system_user new_userid do
    userid new_userid
    ssh_key new_sshkey
  end
  
  #create a nova user
  nova_user new_userid do
    userid new_userid
    project new_userproject
  end
  
end
