#!/bin/bash

# Prompt the user for the password
read -sp "Enter password for root@192.168.8.181: " PASSWORD
echo

# Define the OpenWrt device's IP address and the user
OPENWRT_IP="192.168.8.181"
USER="root"

# Define the source directory where your local configuration files are stored
SOURCE_DIR="./hotplug"

# Define the destination directory on the OpenWrt device
DEST_DIR="/etc/config"

# List of configuration files to copy
FILES=("10-eth0-detect" "20-wifi-detect" "dhcp" "dropbear" "firewall" "luci" "network" "rpcd" "system" "tailscale" "ucitrack" "uhttpd" "wireless")

# Copy each file to the OpenWrt device
for FILE in "${FILES[@]}"; do
    sshpass -p "${PASSWORD}" scp "${SOURCE_DIR}/${FILE}" "${USER}@${OPENWRT_IP}:${DEST_DIR}/"
    if [ $? -eq 0 ]; then
        echo "Successfully copied ${FILE} to ${OPENWRT_IP}:${DEST_DIR}"
    else
        echo "Failed to copy ${FILE} to ${OPENWRT_IP}:${DEST_DIR}"
    fi
done

# Correct the paths for the hotplug scripts
sshpass -p "${PASSWORD}" ssh ${USER}@${OPENWRT_IP} "mv /etc/config/10-eth0-detect /etc/hotplug.d/iface/10-eth0-detect"
sshpass -p "${PASSWORD}" ssh ${USER}@${OPENWRT_IP} "mv /etc/config/20-wifi-detect /etc/hotplug.d/iface/20-wifi-detect"

# Restart network services to apply new configurations
sshpass -p "${PASSWORD}" ssh ${USER}@${OPENWRT_IP} "/etc/init.d/network restart"
sshpass -p "${PASSWORD}" ssh ${USER}@${OPENWRT_IP} "/etc/init.d/dnsmasq restart"

# Optional: Reboot the device to ensure all settings are applied
# Uncomment the following line if you want to reboot the device
# sshpass -p "${PASSWORD}" ssh ${USER}@${OPENWRT_IP} "reboot"
