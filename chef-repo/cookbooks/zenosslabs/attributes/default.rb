#
# Cookbook Name:: zenosslabs
# Attribute:: default
#
# Copyright 2011, Zenoss, Inc.
#
# All rights reserved - Do Not Redistribute
#

default[:zenoss] = {
    :versions => [
        {
            :name => "3.2.1",

            :database => {
                :name => "mysql",
                :service => "mysqld",
                :datadir => "/var/lib/mysql",
                :package => {
                    :name => "mysql-server"
                }
            },

            :daemons => ['zeoctl'],

            :flavors => [
                {
                    :name => "platform",
                    :packages => [
                        {
                            :name => "zenoss",
                            :rpm_prefix => "zenoss-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        }
                    ]
                },{
                    :name => "core",
                    :packages => [
                        {
                            :name => "zenoss",
                            :rpm_prefix => "zenoss-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        },{
                            :name => "zenoss-core-zenpacks",
                            :rpm_prefix => "zenoss-core-zenpacks-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        }
                    ]
                },{
                    :name => "enterprise",
                    :packages => [
                        {
                            :name => "zenoss",
                            :rpm_prefix => "zenoss-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        },{
                            :name => "zenoss-core-zenpacks",
                            :rpm_prefix => "zenoss-core-zenpacks-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        },{
                            :name => "zenoss-enterprise-zenpacks",
                            :rpm_prefix => "zenoss-enterprise-zenpacks-3.2.1-1326",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/"
                        }
                    ]
                }
            ]
        },

        {
            :name => "4.1.1",

            :database => {
                :name => "zends",
                :datadir => "/opt/zends/data",
                :service => "zends",
                :package => {
                    :name => "zends",
                    :rpm_prefix => "zends-5.5.15-1.r51230",
                    :url_prefix => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/"
                }
            },

            :daemons => ['zeneventserver', 'zeneventd'],

            :flavors => [
                {
                    :name => "resmgr",
                    :packages => [
                        {
                            :name => "zenoss",
                            :rpm_prefix => "zenoss-4.1.1-1396",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/"
                        },{
                            :name => "zenoss-core-zenpacks",
                            :rpm_prefix => "zenoss-core-zenpacks-4.1.1-1396",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/"
                        },{
                            :name => "zenoss-enterprise-zenpacks",
                            :rpm_prefix => "zenoss-enterprise-zenpacks-4.1.1-1396",
                            :url_prefix => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/"
                        }
                    ]
                }
            ]
        }
    ]
}
