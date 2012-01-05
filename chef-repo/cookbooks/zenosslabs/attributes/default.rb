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

default[:zenosslabs] = {
    :jenkins_jobs => {
        :discovery_jobs => [
            {
                :name => 'Discovery - Core ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/core/zenpacks'
            },{
                :name => 'Discovery - Community ZenPacks',
                :scm => 'git',
                :url => 'git@github.com:zenoss/Community-ZenPacks-SubModules.git'
            },{
                :name => 'Discovery - Enterprise ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/enterprise/zenpacks'
            },{
                :name => 'Discovery - Reporting ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/enterprise/reporting/zenpacks'
            },{
                :name => 'Discovery - Customer ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/customer/zenpacks'
            },{
                :name => 'Discovery - ClientServices ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/ClientServices/ZenPacks'
            }
        ],

        :zenpack_jobs => [
            {
                :name => 'ZenPacks.Blizzard.Custom',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.Blizzard.Custom.git'
            },{
                :name => 'ZenPacks.zenoss.AutoTune',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.AutoTune.git'
            },{
                :name => 'ZenPacks.zenoss.CalculatedPerformance',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.CalculatedPerformance.git'
            },{
                :name => 'ZenPacks.zenoss.CallManagerMonitor',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.CallManagerMonitor.git'
            },{
                :name => 'ZenPacks.zenoss.CloudFoundry',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.CloudFoundry.git'
            },{
                :name => 'ZenPacks.zenoss.CloudStack',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.CloudStack.git'
            },{
                :name => 'ZenPacks.zenoss.Demo',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.Demo.git'
            },{
                :name => 'ZenPacks.zenoss.DeviceClassServices',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.DeviceClassServices.git'
            },{
                :name => 'ZenPacks.zenoss.GOM',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.GOM.git'
            },{
                :name => 'ZenPacks.zenoss.Memcached',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.Memcached.git'
            },{
                :name => 'ZenPacks.zenoss.NeoCatalog',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.NeoCatalog.git'
            },{
                :name => 'ZenPacks.zenoss.OpenStack',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.OpenStack.git'
            },{
                :name => 'ZenPacks.zenoss.OpenStackSwift',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.OpenStackSwift.git'
            },{
                :name => 'ZenPacks.zenoss.OpenVZ',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.OpenVZ.git'
            },{
                :name => 'ZenPacks.zenoss.PostgreSQL',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.PostgreSQL.git'
            },{
                :name => 'ZenPacks.zenoss.Puppet',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.Puppet.git'
            },{
                :name => 'ZenPacks.zenoss.RabbitMQ',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.RabbitMQ.git'
            },{
                :name => 'ZenPacks.zenoss.RRDtoolReports',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.RRDtoolReports.git'
            },{
                :name => 'ZenPacks.zenoss.ScrutinizerIntegrator',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.ScrutinizerIntegrator.git'
            },{
                :name => 'ZenPacks.zenoss.ServiceNowIntegrator',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.ServiceNowIntegrator.git'
            },{
                :name => 'ZenPacks.zenoss.SolarisMonitor',
                :scm => 'git',
                :url => 'git@github.com:zenoss/ZenPacks.zenoss.SolarisMonitor.git'
            }
        ]
    }
}
