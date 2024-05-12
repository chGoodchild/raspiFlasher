import sys
import subprocess
import os

def flash_sd_card(sd_card, image_path, ssid, wifi_password, country_code='US'):
    # Flash the SD card with the Raspberry Pi OS image
    print("Flashing the SD card with the image...")
    subprocess.run(['balena-etcher-cli', image_path, '--drive', sd_card, '--yes'], check=True)
    
    # Mount the boot partition (assumed to be the first partition)
    boot_partition = sd_card + '1'  # Adjust according to your system (e.g., /dev/sdb1)
    subprocess.run(['mount', boot_partition, '/mnt'], check=True)
    
    # Enable SSH access
    print("Enabling SSH access...")
    with open('/mnt/ssh', 'w') as ssh_file:
        pass  # Create an empty file named 'ssh'
    
    # Setup Wi-Fi
    print("Configuring Wi-Fi settings...")
    wpa_config = f"""
country={country_code}
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={{
    ssid="{ssid}"
    psk="{wifi_password}"
    key_mgmt=WPA-PSK
}}
"""
    with open('/mnt/wpa_supplicant.conf', 'w') as wpa_file:
        wpa_file.write(wpa_config)
    
    # Unmount the boot partition
    subprocess.run(['umount', '/mnt'], check=True)
    print("SD card is ready with the OS, SSH, and Wi-Fi configured.")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python flash_sd_card.py <SD_CARD> <IMAGE_PATH> <SSID> <WIFI_PASSWORD>")
        sys.exit(1)

    sd_card = sys.argv[1]
    image_path = sys.argv[2]
    ssid = sys.argv[3]
    wifi_password = sys.argv[4]

    flash_sd_card(sd_card, image_path, ssid, wifi_password)
