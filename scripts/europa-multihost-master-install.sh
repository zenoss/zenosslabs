#!/bin/bash
echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7
echo "deb [ arch=amd64 ] http://unstable.zenoss.io/apt/ubuntu trusty universe" > /etc/apt/sources.list.d/zenoss.list
apt-get update
apt-get install -y ntp
apt-get install -y --force-yes zenoss-resmgr-service
usermod -aG docker zenny
usermod -aG sudo zenny
docker login -u {{DOCKER_USERNAME}} -p {{DOCKER_PASSWORD}} -e {{DOCKER_EMAIL}}
mv /.dockercfg /root
EXT=$(date +"%j-%T")
sed -i.${EXT} -e 's|^#[^H]*\(HOME=/root\)|\1|' \
 -e 's|^#[^S]*\(SERVICED_REGISTRY=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_AGENT=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_MASTER=\).|\11|' \
 /etc/default/serviced
start serviced
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i
