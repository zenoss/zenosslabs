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
# Requires about 5G of free space in root's $HOME
#
# Requires script to be run as root
# Requires that all specified hostnames are resolvable to IPs via host command
# Requires passwordless ssh to all specified hosts
# Requires that btrfs filesystem is partitioned and mounted at:
#    /var/lib/docker     # all hosts
#    /opt/serviced/var   # only master
# Requires config settings in $HOME/.install-resmgr-5.rc
#
# Instructions to run on master as root user:
#    download this script to $HOME of the root user
#    chmod +rx ~root/install-resmgr-5.sh
#    ~root/install-resmgr-5.sh genconf
#       # edit and modify ~root/.install-resmgr-5.rc
#    ~root/install-resmgr-5.sh master
#
# Log files are stored in $HOME/resmgr/
# 
###############################################################################

export INSTALL_RESMGR_VERSION="0.1"

#==============================================================================
function usage
{
    cat <<EOF
Usage:
    $0 genconf 
        generate modifiable config file to $RCFILE

    $0 master
        install resmgr 5 on master and remote host(s) based on config file

Default config file:
EOF
    genconf /dev/stderr

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
function duplicateOutputToLogFile
{
    local logfile="$1"
    local logdir=$(dirname $logfile)
    [[ ! -d "$logdir" ]] && \mkdir -p $logdir

    exec &> >(tee -a $logfile)
    echo -e "\n################################################################################" >> $logfile
    return $?
}

#==============================================================================
function set_LINUX_DISTRO 
{               
    export LINUX_DISTRO=$([ -f "/etc/redhat-release" ] && echo RHEL || echo DEBIAN; [ "0" = $PIPESTATUS ] && true || false)
    local result=$?

    return $result
}

#==============================================================================
function importConf
{
    logInfo "Import required config"
    local rcfile="$1"
    local numErrors=0

    if [[ ! -f "$rcfile" ]]; then
        logError "unable to find config file: $rcfile"
        return 1
    fi

    logInfo "sourcing config file: $rcfile"
    source "$rcfile"

    for var in \
        "SERVICED_USERS" \
        "DOCKERHUB_USER" \
        "DOCKERHUB_EMAIL" \
        "DOCKERHUB_PASS" \
        "MASTER" \
    ; do
        if [[ -z "${!var}" ]] ; then
            logError "var $var is not set"
            numErrors=$(( numErrors + 1 ))
            continue
        fi
    done

    if [[ -z "${!COLLECTORS_OF_POOL[*]}" ]]; then
        logError "associative array COLLECTORS_OF_POOL is not set"
        numErrors=$(( numErrors + 1 ))
    fi
    for pool in ${!COLLECTORS_OF_POOL[*]}; do
        if [[ -z "${COLLECTORS_OF_POOL[${pool}]}" ]]; then
            logError "associative array COLLECTORS_OF_POOL[$pool] is not set"
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        REMOTES="$REMOTES ${COLLECTORS_OF_POOL[${pool}]}"
    done

    logSummary "imported required config - found $numErrors errors"

    return $numErrors
}


#==============================================================================
function checkFilesystems
{
    logInfo "Checking filesystems"
    local numErrors=0
    local wantedFSType="$1"; shift
    local paths="$@"

    for path in $paths; do
        logInfo "checking that path $path is of the required type: $wantedFSType"

        if ! df -H $path; then
            logError "df was not able to find dir: $dir"
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        if ! mount | grep "on $path type $wantedFSType"; then
            logError "filesystem at path: $path is not $wantedFSType"
            numErrors=$(( numErrors + 1 ))
            continue
        fi
    done

    logSummary "checked filesystems - found $numErrors errors"

    return $numErrors
}

#==============================================================================
function checkHostsResolvable
{
    local hosts="$@"
    logInfo "Checking that hosts are resolvable: $hosts"
    local numErrors=0

    for host in $hosts; do
        if ! host $host; then
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        logInfo "host $host is a valid host"
    done

    logSummary "checked that hosts are resolvable - found $numErrors errors"

    return $numErrors
}

#==============================================================================
function checkHostsSsh
{
    local hosts="$@"
    logInfo "Checking that hosts have passwordless ssh: $hosts"
    local numErrors=0

    for host in $hosts; do
        if ! ssh $host id >/dev/null; then
            numErrors=$(( numErrors + 1 ))
            continue
        fi
    done

    logSummary "checked that hosts have passwordless ssh - found $numErrors errors"

    return $numErrors
}

#==============================================================================
function installRemotes
{
    local master="$1"; shift
    local remotes="$@"
    logInfo "Installing remotes with master: $master and remotes: $remotes"
    local numErrors=0

    # scp and launch script
    for host in $remotes; do
        if ! scp $SCRIPT $host:; then
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        nohup ssh $host ~/$(basename -- $SCRIPT) remote $master &>/dev/null &
        if [[ $? != 0 ]] ; then
            numErrors=$(( numErrors + 1 ))
            continue
        fi

        logInfo "scped and launched script on $remote"
    done

    logSummary "installed remotes - found $numErrors errors"

    return $numErrors
}

#==============================================================================
function installHostSoftware
{
    logInfo "Installing software"
    local numErrors=0
    local users="$@"

    ufw disable

    if test -f /etc/selinux/config && grep '^SELINUX=enforcing' /etc/selinux/config; then
        EXT=$(date +'%Y%m%d-%H%M%S-%Z')
        sudo sed -i.${EXT} -e 's/^SELINUX=.*/SELINUX=permissive/g' \
              /etc/selinux/config && \
              grep '^SELINUX=' /etc/selinux/config

        die "SElinux was found and set to permissive - reboot server and rerun this script on master"
    fi

    set -e

    curl -sSL https://get.docker.io/ubuntu/ | sh

    for user in $users; do
        usermod -aG docker "$user"
    done

    apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7

    REPO=http://testing.zenoss.io/apt/ubuntu
    REPO=http://unstable.zenoss.io/apt/ubuntu   # TODO: use testing instead
    sh -c 'echo "deb [ arch=amd64 ] '${REPO}' trusty universe" \
          > /etc/apt/sources.list.d/zenoss.list'

    apt-get update

    apt-get install -y ntp

    apt-get install -y zenoss-resmgr-service

    set +e

    logSummary "installed software"

    return $numErrors
}

#==============================================================================
function configureCredentials
{
    logInfo "Configuring credentials"
    local numErrors=0

    set -e

    if [[ "RHEL" = $LINUX_DISTRO ]]; then
        for user in $SERVICED_USERS; do
            usermod -aG wheel "$user"
        done
    else
        for user in $SERVICED_USERS; do
            usermod -aG sudo "$user"
        done
    fi

    (export HISTCONTROL=ignorespace; \
        docker login -u "$DOCKERHUB_USER" -e "$DOCKERHUB_EMAIL" -p "$DOCKERHUB_PASS")

    set +e

    logSummary "configured credentials"

    return $numErrors
}

#==============================================================================
function configureMaster
{
    logInfo "Configuring master"
    local numErrors=0

    set -e

    EXT=$(date +'%Y%m%d-%H%M%S-%Z')
    sed -i.${EXT} \
          -e 's|^#[^S]*\(SERVICED_FS_TYPE=\).*$|\1btrfs|' \
            /etc/default/serviced

    sed -i.${EXT} -e 's|^#[^H]*\(HOME=/root\)|\1|' \
          -e 's|^#[^S]*\(SERVICED_REGISTRY=\).|\11|' \
          -e 's|^#[^S]*\(SERVICED_AGENT=\).|\11|' \
          -e 's|^#[^S]*\(SERVICED_MASTER=\).|\11|' \
                /etc/default/serviced

    MYOPT="\nDOCKER_OPTS=\"--insecure-registry $(hostname -s):5000\""
    sed -i.${EXT} -e '/DOCKER_OPTS=/ s|$|'"${MYOPT}"'|' \
      /etc/default/docker
    stop docker; start docker

    start serviced

    set +e

    logSummary "configured master"

    return $numErrors
}

#==============================================================================
function configureRemote
{
    logInfo "Configuring remote"
    local master="$1"
    local numErrors=0

    set -e

    EXT=$(date +'%Y%m%d-%H%M%S-%Z')

    MHOST=$(set -o pipefail; host $master | awk '{print $NF}')

    test ! -z "${MHOST}" && \
    sed -i.${EXT} -e 's|^#[^H]*\(HOME=/root\)|\1|' \
      -e 's|^#[^S]*\(SERVICED_REGISTRY=\).|\11|' \
      -e 's|^#[^S]*\(SERVICED_AGENT=\).|\11|' \
      -e 's|^#[^S]*\(SERVICED_MASTER=\).|\10|' \
      -e 's|^#[^S]*\(SERVICED_MASTER_IP=\).*|\1'${MHOST}'|' \
      -e '/=$SERVICED_MASTER_IP/ s|^#[^S]*||' \
      /etc/default/serviced

    start serviced

    set +e

    logSummary "configured remote"

    return $numErrors
}

#==============================================================================
function retry
{
    local timeout=$1; shift
    local name=$1; shift
    local command="$@"

    local result=1
    until [[ $timeout -lt 1 ]]; do
        $command; result=$?; [[ $result = 0 ]] && return 0 
        
        logInfo "$name not ready yet (countdown:$timeout). Checking again in 10 seconds."
        sleep 10
        timeout=$(( $timeout - 10 ))
    done

    return $result
}

function test_serviced_ready
{
    local rpcport=$1
    wget http://localhost:$rpcport &>/dev/null
    return $?
}

function host_add
{
    local pool="$1"; shift
    local rpcport="$1"; shift
    local host="$1"
    serviced host add $host:$rpcport $pool
    serviced host list | grep "$pool.*$host.*$rpcport" &>/dev/null
    return $?
}

function wait_for_all_running
{
    serviced service status | awk '$1 != "NAME" && $3 != "" && $3 != "Running"{ notrunning++} END{exit notrunning}'
    return $?
}


#==============================================================================
function addPoolAndHosts
{
    logInfo "add pool and hosts"
    local timeout="$1"; shift
    local pool="$1"; shift
    local rpcport="$1"; shift
    local hosts="$@"
    local numErrors=0

    serviced pool add $pool 0
    if ! serviced pool list $pool |grep '"ID":.*"'$pool'"' >/dev/null; then
        logError "unable to add pool $pool"
        return 1
    fi

    for host in $hosts; do
        retry $timeout "add host to pool" host_add $pool $rpcport $host || die "timed out adding host $host on rpcport $rpcport to pool $pool"
    done

    logSummary "added pool $pool on rpcport with hosts: $hosts"
    return $numErrors
}

#==============================================================================
function deployTemplateAndStart
{
    logInfo "deploy and start template"
    local template="$1"

    local id=$(serviced template list | awk '/'$template'/{print $1; exit}')

    if [[ -z "$id" ]]; then
        logError "unable to find template $template"
        return 1
    fi
    serviced template deploy "$id" default zenoss

    serviced service start $template

    logSummary "deployed and started template"
    return $numErrors
}

#==============================================================================
function addZenossCollector
{
    logInfo "add zenoss collector"
    local pool="$1"; shift
    local numErrors=0

    serviced service attach zope/0 su - zenoss -c "dc-admin add-hub --pool $pool $pool"
    serviced service attach zope/0 su - zenoss -c "dc-admin add-collector --pool $pool --src-hub $pool $pool"

    logSummary "added zenoss collector $collector to pool $pool"
    return $numErrors
}

#==============================================================================
function genconf
{
    local file="$1"
    [[ "/dev/stderr" != $file ]] && logInfo "generate config file: $file"
    local numErrors=0

    cat <<-EOF >$file
    SERVICED_USERS=""                       # host username(s) allowed to log into CC UI
    DOCKERHUB_USER=""                       # username to be supplied to docker login
    DOCKERHUB_EMAIL="customer@example.com"  # email to be supplied to docker login
    DOCKERHUB_PASS=""                       # password to be supplied to docker login

    MASTER=$(hostname -s)                          # hostname of serviced master

    # define pools
    declare -A COLLECTORS_OF_POOL
    COLLECTORS_OF_POOL["pool1"]="remote-collector-hostname1 remote-collector-hostname2"
EOF

    [[ "/dev/stderr" != $file ]] && logSummary "generated config file"
    return $numErrors
}

#==============================================================================
function main
{
    INITPWD=$(pwd)
    SCRIPT="$(\cd $(dirname $0); \pwd)/$(basename -- $0)"
    RCFILE=~/".$(basename -- $0 .sh).rc"

    [[ $# -lt 1 ]] && usage
    local role="$1"; shift

    # ---- Check environment
    [[ "root" != "$(whoami)" ]] && die "user is not root - run this script as 'root' user"

    if [[ "genconf" = "$role" ]]; then
        genconf "$RCFILE"
        exit $?
    fi

    local errors=0
    local logdir="$HOME/resmgr"
    [[ ! -d "$logdir" ]] && mkdir -p "$logdir"
    \cd $logdir || die "could not cd to logdir: $logdir"

    duplicateOutputToLogFile "$logdir/$(basename -- $0).log"

    # ---- Show date and version of os
    logInfo "$(basename -- $0)  date:$(date +'%Y%m%d-%H%M%S-%Z')  uname-rm:$(uname -rm)"

    set_LINUX_DISTRO 

    # ---- install on master and remotes
    case "$role" in
        "master")
            importConf "$RCFILE" || die "failed to satisfy required configuration variables"
            logInfo "installing as '$role' role with master $MASTER with remotes: $REMOTES"

            checkHostsResolvable $MASTER $REMOTES || die "failed to satisfy resolvable hosts prereq"

            checkFilesystems "btrfs" "/var/lib/docker" "/opt/serviced/var" || die "failed to satisfy filesystem prereq"

            checkHostsSsh $MASTER $REMOTES || die "failed to satisfy passwordless ssh prereq"

            installRemotes $MASTER $REMOTES

            installHostSoftware $SERVICED_USERS

            configureCredentials

            configureMaster

            local timeout=1800
            local UIPORT=443
            retry $timeout serviced test_serviced_ready $UIPORT || die "serviced failed to be ready within $timeout seconds"

            local RPCPORT=4979
            serviced host add $MASTER:$RPCPORT default

            source "$RCFILE"  # workaround for declare -A COLLECTORS_OF_POOL being local to function
            for pool in ${!COLLECTORS_OF_POOL[*]}; do
                local remotes="${COLLECTORS_OF_POOL[${pool}]}"
                addPoolAndHosts $timeout $pool $RPCPORT $remotes || die "unable to add pool $pool and hosts: $remotes"
            done

            deployTemplateAndStart "Zenoss.resmgr"

            retry $timeout services-running wait_for_all_running || die "timed out waiting for all services to be running"

            for pool in ${!COLLECTORS_OF_POOL[*]}; do
                addZenossCollector $pool || die "unable to add collector to $pool"
            done

            logSummary "software is installed, deployed, and started on master"
            ;;

        "remote")
            local MASTER="$1"
            logInfo "installing as '$role' role with master $MASTER"

            checkHostsResolvable $MASTER || die "failed to satisfy resolvable hosts prereq"

            checkFilesystems "btrfs" "/var/lib/docker" || die "failed to satisfy filesystem prereq"

            installHostSoftware $SERVICED_USERS

            configureRemote $MASTER

            logSummary "software is installed, deployed, and started on remote"
            ;;

        *)
            die "prereqs not configured"
            ;;
    esac

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


