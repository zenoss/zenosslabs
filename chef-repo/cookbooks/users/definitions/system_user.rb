define :system_user, :userid => nil, :ssh_key => nil do

  #define some commonly used vars
  userid = params[:userid]
  ssh_key = params[:ssh_key]
  home_dir = "/home/#{userid}"
  Chef::Log.info("Creating user directory #{home_dir}")
  ushell = "/bin/bash"

  # fixes CHEF-1699
  ruby_block "reset group list" do
    block do
      Etc.endgrent
    end
    action :nothing
  end

  user userid do
    shell ushell
    supports :manage_home => true
    home home_dir
    #fix the bug (see above)
    notifies :create, "ruby_block[reset group list]", :immediately
  end

  directory "#{home_dir}/.ssh" do
    owner userid
    group userid
    mode "0700"
  end

  template "#{home_dir}/.ssh/authorized_keys" do
    source "authorized_keys.erb"
    owner userid
    group userid
    mode "0600"
    variables :ssh_keys => ssh_key
  end
  
  Chef::Log.info("Completed creation of system user #{userid}")
  
end
