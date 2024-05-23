#!/bin/bash

# Ensure dhcpcd5 is installed
apt-get update
apt-get install -y dhcpcd5

# Append network priorities to dhcpcd.conf
echo "
interface eth0
metric 300

interface wlan0
metric 200
" >> /etc/dhcpcd.conf

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker $(whoami)

curl -fsSL https://tailscale.com/install.sh | sh

# Disable this script from running on next boot
sed -i '/first-boot-setup.sh/d' /etc/rc.local

# Reboot the system
reboot
