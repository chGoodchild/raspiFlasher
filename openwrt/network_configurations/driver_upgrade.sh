#!/bin/bash

# Define variables
LOCAL_IMAGE_PATH="/home/pachai/Documents/raspiFlasher/openwrt/network_configurations/openwrt-23.05.0-bcm27xx-bcm2711-rpi-4-squashfs-sysupgrade.img.gz"
REMOTE_USER="root"
REMOTE_HOST="192.168.1.1"
REMOTE_IMAGE_PATH="/tmp/openwrt-23.05.0-bcm27xx-bcm2711-rpi-4-squashfs-sysupgrade.img.gz"

# Copy the sysupgrade image to the OpenWrt device
echo "Copying ${LOCAL_IMAGE_PATH} to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_IMAGE_PATH}"
scp "${LOCAL_IMAGE_PATH}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_IMAGE_PATH}"

if [ $? -eq 0 ]; then
    echo "Successfully copied the sysupgrade image to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_IMAGE_PATH}"
else
    echo "Failed to copy the sysupgrade image to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_IMAGE_PATH}"
    exit 1
fi

# Perform the sysupgrade on the OpenWrt device
echo "Initiating sysupgrade on the OpenWrt device"
ssh "${REMOTE_USER}@${REMOTE_HOST}" "sysupgrade ${REMOTE_IMAGE_PATH}"

if [ $? -eq 0 ]; then
    echo "Sysupgrade initiated successfully"
else
    echo "Failed to initiate sysupgrade"
    exit 1
fi

echo "Upgrade process started. The device will reboot automatically if the upgrade is successful."
