#!/bin/bash

# Define variables
REMOTE_USER="root"
REMOTE_HOST="192.168.1.1"

# Define the commands to be run on the OpenWrt device
COMMANDS="
echo '### System Information ###';
uname -a;
echo '';

echo '### Available Hardware ###';
lshw -short;
echo '';

echo '### Network Interfaces ###';
ip link show;
echo '';

echo '### Wireless Configuration ###';
cat /etc/config/wireless;
echo '';

echo '### Network Configuration ###';
cat /etc/config/network;
echo '';

echo '### DHCP Configuration ###';
cat /etc/config/dhcp;
echo '';

echo '### DHCP Leases ###';
cat /tmp/dhcp.leases;
echo '';

echo '### Current Network Status ###';
ifconfig;
echo '';

echo '### Wireless Status ###';
iw dev;
echo '';

echo '### Wireless Stations ###';
iwinfo;
echo '';

echo '### Active Connections ###';
netstat -tuln;
echo '';

echo '### Routing Table ###';
route -n;
echo '';
"

# Execute the commands on the remote OpenWrt device and display the output
ssh "${REMOTE_USER}@${REMOTE_HOST}" "${COMMANDS}"

# Optionally, you can save the output to a file
ssh "${REMOTE_USER}@${REMOTE_HOST}" "${COMMANDS}" > openwrt_status_report.txt
