#!/bin/bash
parted -s /dev/xvdb mklabel msdos
parted -s /dev/xvdb mkpart primary ext2 0 51200
parted -s /dev/xvdb mkpart primary ext2 51200 102400
mkfs.btrfs -f /dev/xvdb1
mkfs.btrfs -f /dev/xvdb2
mkdir -p /var/lib/docker
mkdir -p /opt/serviced/var/volumes
echo -e '#!/bin/bash' >> /etc/init.d/ebs-init-mount
echo -e "# chkconfig: 345 99 01" >> /etc/init.d/ebs-init-mount
echo -e "# description: some startup script" >> /etc/init.d/ebs-init-mount
echo -e "mount /dev/xvdb1 /var/lib/docker" >> /etc/init.d/ebs-init-mount
echo -e "mount /dev/xvdb2 /opt/serviced/var/volumes" >> /etc/init.d/ebs-init-mount
chmod +x /etc/init.d/ebs-init-mount
/etc/init.d/ebs-init-mount
chkconfig --add ebs-init-mount
chkconfig ebs-init-mount on
cat >/etc/yum.repos.d/docker.repo <<-EOF
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
printf "\n%s %s\n" `ifconfig eth0 | grep "inet " | tr ":" " " | awk {'print $2'}` `hostname` >> /etc/hosts
yum --enablerepo=zenoss-unstable install -y zenoss-resmgr-service
systemctl start docker
docker login -u {{DOCKER_USERNAME}} -p {{DOCKER_PASSWORD}} -e {{DOCKER_EMAIL}}
echo 'DOCKER_OPTS="-s devicemapper --dns=172.17.42.1"' >> /etc/sysconfig/docker
systemctl stop docker && systemctl start docker
EXT=$(date +"%j-%H%M%S") sed -i.${EXT}  -e 's|^#[^S]*\(SERVICED_FS_TYPE=\).*$|\btrfs|' /etc/default/serviced
systemctl start serviced
sudo usermod -aG docker zenny
usermod -aG wheel zenny
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i
