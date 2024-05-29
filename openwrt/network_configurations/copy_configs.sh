#!/bin/bash

# Define variables
LOCAL_PATH="/home/pachai/Documents/raspiFlasher/openwrt/network_configurations/opennds"
REMOTE_USER="root"
REMOTE_HOST="192.168.2.1"
REMOTE_PATH="/etc/config"

# Define the mapping of local files to remote files
declare -A FILE_MAP
FILE_MAP=(
    ["etc_config_dhcp"]="dhcp"
    ["etc_config_network"]="network"
    ["etc_config_wireless"]="wireless"
)

# Iterate over each file and copy it to the OpenWrt device
for LOCAL_FILE in "${!FILE_MAP[@]}"; do
    REMOTE_FILE="${REMOTE_PATH}/${FILE_MAP[$LOCAL_FILE]}"
    
    echo "Copying ${LOCAL_PATH}/${LOCAL_FILE} to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}"
    scp "${LOCAL_PATH}/${LOCAL_FILE}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}"
    
    if [ $? -eq 0 ]; then
        echo "Successfully copied ${LOCAL_PATH}/${LOCAL_FILE} to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}"
    else
        echo "Failed to copy ${LOCAL_PATH}/${LOCAL_FILE} to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILE}"
        exit 1
    fi
done

echo "All files copied successfully!"
