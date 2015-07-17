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
MHOST={{in_MHOST}}
echo "HOME=/root" >> /etc/default/serviced
echo "SERVICED_REGISTRY=1" >> /etc/default/serviced
echo "SERVICED_AGENT=1" >> /etc/default/serviced
echo "SERVICED_MASTER=0" >> /etc/default/serviced
echo "SERVICED_STATS_PORT=$MHOST:8443" >> /etc/default/serviced
echo "SERVICED_LOGSTASH_ES=$MHOST:9100" >> /etc/default/serviced
echo "SERVICED_LOG_ADDRESS=$MHOST:5042" >> /etc/default/serviced
echo "SERVICED_ENDPOINT=$MHOST:4979" >> /etc/default/serviced
echo "SERVICED_DOCKER_REGISTRY=$MHOST:5000" >> /etc/default/serviced
echo "SERVICED_ZK=$MHOST:2181" >> /etc/default/serviced
systemctl start serviced
sudo usermod -aG docker zenny
usermod -aG wheel zenny
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i
