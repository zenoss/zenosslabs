#!/bin/bash
apt-get install btrfs-tools
parted -s /dev/xvdb mklabel msdos
parted -s /dev/xvdb mkpartfs primary ext2 0 102400
mkfs.btrfs -f /dev/xvdb1
mkdir -p /var/lib/docker
echo -e "#!/bin/bash" >> /etc/init.d/ebs-init-mount
echo -e "mount -o rw,noatime,nodatacow /dev/xvdb1 /var/lib/docker" >> /etc/init.d/ebs-init-mount
chmod +x /etc/init.d/ebs-init-mount
/etc/init.d/ebs-init-mount
update-rc.d ebs-init-mount defaults
echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list
printf "\n%s %s\n" `ifconfig eth0 | grep "inet addr" | tr ":" " " | awk {'print $3'}` `hostname` >> /etc/hosts
apt-key adv --keyserver keys.gnupg.net --recv-keys AA5A1AD7
echo "deb [ arch=amd64 ] http://unstable.zenoss.io/apt/ubuntu trusty universe" > /etc/apt/sources.list.d/zenoss.list
apt-get update
apt-get install -y ntp
apt-get install -y --force-yes zenoss-resmgr-service
usermod -aG docker zenny
usermod -aG sudo zenny
MHOST={{in_MHOST}}
EXT=$(date +"%j-%T")
sudo sed -i.${EXT} -e 's|^#[^H]*\(HOME=/root\)|\1|' \
 -e 's|^#[^S]*\(SERVICED_REGISTRY=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_AGENT=\).|\11|' \
 -e 's|^#[^S]*\(SERVICED_MASTER=\).|\10|' \
 -e 's|^#[^S]*\(SERVICED_MASTER_IP=\).*|\1'${MHOST}'|' \
 -e '/=$SERVICED_MASTER_IP/ s|^#[^S]*||' \
 /etc/default/serviced
start serviced
