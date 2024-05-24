#!/bin/bash
# Initial setup and system configuration

sudo apt update -y
sudo apt upgrade -y

# Install necessary packages
sudo apt-get install -y qemu-user-static binfmt-support meld


# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $(whoami)

# Install Tailscale
echo "Installing Tailscale..."
curl -fsSL https://tailscale.com/install.sh | sudo sh

# Download and run the manual setup script
# wget https://raw.githubusercontent.com/chGoodchild/raspiFlasher/master/manual_setup.sh
# chmod +x manual_setup.sh
# ./manual_setup.sh

