#!/bin/bash
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
wget -O - http://get.docker.io | sh
usermod -aG docker $USER
docker login -u {{DOCKER_USERNAME}} -p {{DOCKER_PASSWORD}} -e {{DOCKER_EMAIL}}
mv /.dockercfg /root
apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7
echo "deb [ arch=amd64 ] http://unstable.zenoss.io/apt/ubuntu trusty universe" > /etc/apt/sources.list.d/zenoss.list
apt-get update
apt-get install -y ntp
apt-get install -y zenoss-resmgr-service
start serviced
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i
