#!/bin/bash

# Redirect all output to a log file for debugging
exec > /var/log/first-boot-setup.log 2>&1
set -x  # Enable script debugging

echo "Starting first-boot-setup.sh script..."

# Ensure dhcpcd5 is installed
echo "Updating package list and installing dhcpcd5..."
sudo apt-get update
sudo apt-get install -y dhcpcd5

# Append network priorities to dhcpcd.conf
echo "Configuring network priorities..."
echo "
interface eth0
metric 300

interface wlan0
metric 200
" | sudo tee -a /etc/dhcpcd.conf

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $(whoami)

# Install Tailscale
echo "Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sudo sh

# Enable the first-boot-setup systemd service to run at next boot
echo "Enabling first-boot-setup service..."
sudo systemctl enable first-boot-setup.service

# Disable this script from running on next boot
echo "Disabling first-boot-setup.sh from running on next boot..."
sudo sed -i '/first-boot-setup.sh/d' /etc/rc.local

# Reboot the system
echo "Rebooting the system..."
sudo reboot
