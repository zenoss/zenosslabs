#!/bin/bash
wget -O - http://get.docker.io | sh
usermod -aG docker $USER
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7
echo "deb [ arch=amd64 ] http://unstable.zenoss.io/apt/ubuntu trusty universe" > /etc/apt/sources.list.d/zenoss.list
apt-get update
apt-get install -y ntp
apt-get install -y zenoss-resmgr-service
MHOST={{in_MHOST}}
sed -i -e '/SERVICED_MASTER=1/a\    export SERVICED_REGISTRY=1\n    export SERVICED_MASTER_IP='${MHOST}'\n    export SERVICED_ZK='${MHOST}':2181\n    export SERVICED_DOCKER_REGISTRY='${MHOST}':5000\n    export SERVICED_ENDPOINT='${MHOST}':4979\n    export SERVICED_LOG_ADDRESS='${MHOST}':5042\n    export SERVICED_LOGSTASH_ES='${MHOST}':9100\n    export SERVICED_STATS_PORT='${MHOST}':8443\n' \
    -e 's/SERVICED_MASTER=1/SERVICED_MASTER=0/g' \
    /etc/init/serviced.conf
start serviced
