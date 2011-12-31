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
            :flavors => [
                {
                    :name => "platform",
                    :packages => [
                        "zenoss-3.2.1-1326"
                    ]
                },

                {
                    :name => "core",
                    :packages => [
                        "zenoss-3.2.1-1326",
                        "zenoss-core-zenpacks-3.2.1-1326"
                    ]
                },

                {
                    :name => "enterprise",
                    :packages => [
                        "zenoss-3.2.1-1326",
                        "zenoss-core-zenpacks-3.2.1-1326",
                        "zenoss-enterprise-zenpacks-3.2.1-1326"
                    ]
                }
            ]
        },

        {
            :name => "4.1.1",
            :flavors => [
                {
                    :name => "resmgr",
                    :packages => [
                        "zends-5.5.15-1.r51230",
                        "zenoss-4.1.1-1396",
                        "zenoss-core-zenpacks-4.1.1-1396",
                        "zenoss-enterprise-zenpacks-4.1.1-1396"
                    ]
                }
            ]
        }
    ],

    :packages => {
        "zenoss-3.2.1-1326" => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/",
        "zenoss-core-zenpacks-3.2.1-1326" => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/",
        "zenoss-enterprise-zenpacks-3.2.1-1326" => "http://artifacts.zenoss.loc/releases/3.2.1/1326/enterprise/",

        "zends-5.5.15-1.r51230" => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/",

        "zenoss-4.1.1-1396" => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/",
        "zenoss-core-zenpacks-4.1.1-1396" => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/",
        "zenoss-enterprise-zenpacks-4.1.1-1396" => "http://artifacts.zenoss.loc/releases/4.1.1/1396/resmgr/"
    }
}
