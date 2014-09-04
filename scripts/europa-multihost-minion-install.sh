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
sed -i -e 's|^# *\(export HOME=/root\)|\1|' \
  -e 's|^# *\(export SERVICED_REGISTRY=\).|\11|' \
  -e 's|^# *\(export SERVICED_AGENT=\).|\11|' \
  -e 's|^# *\(export SERVICED_MASTER=\).|\10|' \
  -e 's|^# *\(export SERVICED_MASTER_IP=\).*|\1'${MHOST}'|' \
  -e '/=$SERVICED_MASTER_IP/ s|^# *||' \
  /etc/default/serviced 
start serviced
