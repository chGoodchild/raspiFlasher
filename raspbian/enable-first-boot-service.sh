#!/bin/bash

# Enable the first-boot-setup.service
systemctl enable first-boot-setup.service

# Remove this script after enabling the service
rm /boot/enable-first-boot-service.sh
