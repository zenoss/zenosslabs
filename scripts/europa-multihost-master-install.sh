#!/bin/bash
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
rpm -ivh http://get.zenoss.io/yum/zenoss-repo-1-1.x86_64.rpm
yum clean all
yum --enablerepo=zenoss-unstable install -y zenoss-resmgr-service
systemctl start docker
docker login -u {{DOCKER_USERNAME}} -p {{DOCKER_PASSWORD}} -e {{DOCKER_EMAIL}}
mv /.dockercfg /root
echo 'DOCKER_OPTS="-s devicemapper --dns=172.17.42.1"' >> /etc/sysconfig/docker
systemctl stop docker && systemctl start docker
EXT=$(date +"%j-%T")
sed -i.${EXT} -e 's|^#[^H]*\(HOME=/root\)|\1|' \
 -e 's|^#[^S]*\(SERVICED_REGISTRY=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_AGENT=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_MASTER=\).|\11|' \
 /etc/default/serviced
EXT=$(date +"%j-%H%M%S") sed -i.${EXT}  -e 's|^#[^S]*\(SERVICED_FS_TYPE=\).*$|\btrfs|' /etc/default/serviced
systemctl start serviced
sudo usermod -aG docker zenny
usermod -aG wheel zenny
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i
