#!/bin/bash
apt-get install btrfs-tools
parted -s /dev/xvdb mklabel msdos
parted -s /dev/xvdb mkpartfs primary ext2 0 51200
parted -s /dev/xvdb mkpartfs primary ext2 51200 102400
mkfs.btrfs -f /dev/xvdb1
mkfs.btrfs -f /dev/xvdb2
mkdir -p /var/lib/docker
mkdir -p /opt/serviced/var
echo -e "#!/bin/bash" >> /etc/init.d/ebs-init-mount
echo -e "mount /dev/xvdb1 /var/lib/docker" >> /etc/init.d/ebs-init-mount
echo -e "mount /dev/xvdb2 /opt/serviced/var" >> /etc/init.d/ebs-init-mount
chmod +x /etc/init.d/ebs-init-mount
/etc/init.d/ebs-init-mount
update-rc.d ebs-init-mount defaults
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list
apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7
echo "deb [ arch=amd64 ] http://unstable.zenoss.io/apt/ubuntu trusty universe" > /etc/apt/sources.list.d/zenoss.list
apt-get update
apt-get install -y ntp
apt-get install -y --force-yes zenoss-resmgr-service
usermod -aG docker zenny
usermod -aG sudo zenny
docker login -u {{DOCKER_USERNAME}} -p {{DOCKER_PASSWORD}} -e {{DOCKER_EMAIL}}
mv /.dockercfg /root
EXT=$(date +"%j-%H%M%S")
sed -i.${EXT} \
 -e 's|^#[^S]*\(SERVICED_FS_TYPE=\).*$|\1btrfs|' \
 /etc/default/serviced
start serviced
rm /var/lib/cloud/instance/user-data.txt
rm /var/lib/cloud/instance/user-data.txt.i

