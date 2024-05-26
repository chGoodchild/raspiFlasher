#!/bin/bash

# Update package list and install Tailscale and iptables-nft
opkg update
opkg install tailscale iptables-nft

# Stop any running instance of Tailscale
/etc/init.d/tailscale stop

# Start Tailscale with cleanup disabled
tailscaled --cleanup=false &

# Wait for tailscaled to start
sleep 5

# Bring up Tailscale
tailscale up

# Output the status of Tailscale
tailscale status
