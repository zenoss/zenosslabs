# nova-manage user create testuser
# nova-manage project add sales testuser
# nova-manage project zipfile sales testuser --file /tmp/blah.zip

define :nova_user, :userid => nil, :project => "sales" do

    #user credentials and environment settings
    userid = params[:userid]
    project = params[:project]
    home_dir = "/home/#{userid}"
    nova_auth_dir = "#{home_dir}/.nova_auth"
    nova_auth_file = "#{nova_auth_dir}/nova_#{userid}.zip"
    Chef::Log.info("Creating nove user #{userid} on project #{project}")
    Chef::Log.info("Cred file at #{nova_auth_file}")
    

    #create the user & assign the user to a project
    execute "nova-manage user create #{userid}; nova-manage project add #{project} #{userid}" do
        not_if "nova-manage user exports #{userid}"
    end
        
    #setup authentication dir
    directory nova_auth_dir do
      owner userid
      group userid
      mode "0755"
      action :create
    end
    
    #create auth zip
    execute "nova-manage project zipfile #{project} #{userid} --file=#{nova_auth_file}" do
        not_if {File.exists?("#{nova_auth_file}")}
    end
    
    #unzip auth zip
    execute "unzip -o #{nova_auth_file} -d #{nova_auth_dir}/" do
      user userid
      group userid
      not_if {File.exists?("#{nova_auth_dir}/novarc")}
    end
    
    #setup user environment
    template "#{home_dir}/.bash_profile" do
      source "bash_profile.erb"
      owner userid
      group userid
      mode "0644"
      variables ({
        :nova_auth => ". #{nova_auth_dir}/novarc",
        :nova_details_script => "/etc/nova.motd.sh"
      })
    end
    
    
    # add the users public key to nova by default
    execute "su - #{userid} -c 'nova keypair-add #{userid}_key.pub --pub_key #{home_dir}/.ssh/authorized_keys'" do
        not_if "su - #{userid} -c 'nova keypair-list' | grep \"| #{userid}_key.pub |\""
    end
end


