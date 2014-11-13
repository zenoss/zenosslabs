#!/bin/bash
#
# Copyright 2014 The Serviced Authors.
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
###############################################################################
#
# Requires about 5G of free space in ~/
#
# Requires script to be run as root
# Requires that all specified hostnames are resolvable to IPs via host command
# Requires passwordless ssh to all specified hosts
# Requires that btrfs filesystem is partitioned and mounted at /opt/serviced/var
#
# Instructions to run on master as root user:
#    download this script to $HOME
#    chmod +rx ~/install-resmgr-5.sh
#    ~/install-resmgr-5.sh MASTER_HOSTNAME REMOTE_HOSTNAME REMOTE2_HOSTNAME ...
#
# Log files are stored in $HOME/resmgr/
# 
###############################################################################

export INSTALL_RESMGR_VERSION="0.1"
export WORKDIR="$(\cd $HOME; /bin/pwd)"   # full path to temp work dir

#==============================================================================
function usage
{
    cat <<EOF
Usage: $0 master|remote MASTER_HOSTNAME REMOTE_HOSTNAME [OTHER_REMOTE_HOSTNAMES...]
    install resmgr 5 on master and remote host(s)

Example(s):
    $0 master zenoss-master zenoss-remote1 zenoss-remote2   # called on master host

    $0 remote zenoss-master zenoss-remote1 zenoss-remote2   # called on remote host(s)

EOF
    exit 1
}

#==============================================================================
function die
{
    echo "ERROR: ${*}" >&2
    exit 1
}

#==============================================================================
function logError
{
    echo "ERROR: ${*}" >&2
}

#==============================================================================
function logWarning
{
    echo "WARNING: ${*}" >&2
}

#==============================================================================
function logInfo
{
    echo "INFO: ${*}" >&2
}

#==============================================================================
function logSummary
{
    echo "INFO: ${*}" >&2
    echo "================================================================================" >&2
}

#==============================================================================
function getLinuxDistro 
{               
    local linux_distro=$([ -f "/etc/redhat-release" ] && echo RHEL || echo DEBIAN; [ "0" = $PIPESTATUS ] && true || false)
    local result=$?

    echo $linux_distro
    return $result
}

#==============================================================================
function checkPrereqs
{
    logInfo "Checking prereqs"

    local numErrors=0

    # check btrfs
    for path in \
        "/opt/serviced/var" \
        "/var/lib/docker" \
    ; do
        if ! df -H $path; then
            logError "df was not able to find dir: $dir"
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        # TODO: check that each path is btrfs
    done

    logSummary "checked prereqs - found $numErrors errors"

    return $numErrors
}

#==============================================================================
function duplicateOutputToLogFile
{
    local logfile="$1"

    local logdir=$(dirname $logfile)
    if [ ! -d "$logdir" ]; then
        \mkdir -p $logdir
    fi

    exec &> >(tee -a $logfile)
    echo -e "\n################################################################################" >> $logfile
    return $?
}

#==============================================================================
function main
{
    INITPWD=$(pwd)
    local errors=0
    if [[ $# -lt 3 ]]; then
        usage
    fi
    local role="$1"; shift
    local master="$1"; shift
    local remotes="$@"

    # ---- Check environment
    [ "root" != "$(whoami)" ] && die "user is not root - run this script as 'root' user"

    local logdir="$HOME/log"
    [ ! -d "$logdir" ] && mkdir -p "$logdir"

    \cd $logdir || die "could not cd to logdir: $logdir"

    duplicateOutputToLogFile "$logdir/$(basename -- $0).log"

    logInfo "$(basename -- $0)  date:$(date +'%Y-%m-%d-%H%M%S-%Z')  uname-rm:$(uname -rm)"
    logInfo "installing as $cmd role with master $master with remotes: $remotes"

    # ---- Check prereqs
    checkPrereqs || die "prereqs not configured"

    # TODO: check that each host is ip/hostname resolvable

    # ---- Show date and version of os

    # TODO: install on remote
    #   for each remote
    #       scp this script to each
    #       ssh and nohup launch the script with 'remote'

    # TODO: install on master
    #   install zenoss-resmgr
    #          follow most of this
    #          https://github.com/control-center/serviced/wiki/Install-a-Build:-Ubuntu,-Master
    #   add appropriate pools
    #   add hosts to pools
    #   wait for remote by continuously adding host and waiting for success
    #   add template
    #   start zenoss
    #   wait for services to start
    #   use dc-admin to add remote collector to collector pool

    #   install zenoss-resmgr
    #          follow most of this
    #          https://github.com/control-center/serviced/wiki/Install-a-Build:-Ubuntu,-Pool
    #          

    # ---- return with number of errors
    return $errors
}

#==============================================================================
# MAIN

if [ "install-resmgr-5.sh" = "$(basename -- $0)" ]; then
    main "$@"
    exit $?
fi

###############################################################################


