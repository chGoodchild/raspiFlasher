#!/bin/bash

# Define variables
REMOTE_USER="root"
REMOTE_HOST="192.168.1.1"

# Reboot the OpenWrt device
echo "Rebooting the OpenWrt device"
ssh "${REMOTE_USER}@${REMOTE_HOST}" "reboot"

if [ $? -eq 0 ]; then
    echo "Reboot command sent successfully"
else
    echo "Failed to send reboot command"
    exit 1
fi

# Wait for the device to reboot
echo "Waiting for the device to reboot..."

while true; do
    # Try to connect to the OpenWrt device
    ssh -o ConnectTimeout=5 "${REMOTE_USER}@${REMOTE_HOST}" "echo 'Device is up!'"
    
    if [ $? -eq 0 ]; then
        echo "The device has rebooted successfully and is now up!"
        break
    else
        echo "Device is still rebooting... checking again in 5 seconds."
        sleep 5
    fi
done

