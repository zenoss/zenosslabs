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
                :name => 'Discovery - Core ZenPacks (zenoss-4.1)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/core/zenoss-4.1.x/zenpacks'
            },{
                :name => 'Discovery - Core ZenPacks (zenoss-3.2)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/core/zenoss-3.2.x/zenpacks'
            },

            {
                :name => 'Discovery - Enterprise ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/enterprise/zenpacks'
            },{
                :name => 'Discovery - Enterprise ZenPacks (zenoss-4.1)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/zenoss-4.1.x/zenpacks'
            },{
                :name => 'Discovery - Enterprise ZenPacks (zenoss-3.2)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/zenoss-3.2.x/zenpacks'
            },

            {
                :name => 'Discovery - Reporting ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/enterprise/reporting/zenpacks'
            },{
                :name => 'Discovery - Reporting ZenPacks (zenoss-4.1)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/zenoss-4.1.x/reporting/zenpacks'
            },{
                :name => 'Discovery - Reporting ZenPacks (zenoss-3.1)',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/branches/zenoss-3.1.x/reporting/zenpacks'
            },

            {
                :name => 'Discovery - Customer ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/trunk/customer/zenpacks'
            },{
                :name => 'Discovery - ClientServices ZenPacks',
                :scm => 'subversion',
                :url => 'http://dev.zenoss.org/svnint/ClientServices/ZenPacks'
            },{
                :name => 'Discovery - Accenture ZenPacks',
                :scm => 'subversion',
                :url => 'https://dev.zenoss.com/svn-accenture'
            },

            {
                :name => 'Discovery - GitHub Public ZenPacks',
                :scm => 'git',
                :url => 'git@github.com:zenoss/zenpacks.git'
            },{
                :name => 'Discovery - GitHub Private ZenPacks',
                :scm => 'git',
                :url => 'git@github.com:zenoss/private-zenpacks.git'
            },{
                :name => 'Discovery - Community ZenPacks',
                :scm => 'git',
                :url => 'git@github.com:zenoss/Community-ZenPacks-SubModules.git'
            }
        ]
    }
}
