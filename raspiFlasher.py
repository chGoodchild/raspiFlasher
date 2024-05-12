import sys
import subprocess
import os
import hashlib

def verify_image_checksum(image_path, expected_checksum):
    print("Verifying image checksum...")
    sha256 = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    calculated_checksum = sha256.hexdigest()
    if calculated_checksum != expected_checksum:
        raise ValueError("Checksum verification failed: the image file may be corrupted or altered.")
    print("Checksum verification passed.")

def flash_sd_card(sd_card, image_path, ssid, wifi_password, expected_checksum, country_code='US'):
    # Verify the image checksum
    verify_image_checksum(image_path, expected_checksum)

    # Flash the SD card with the Raspberry Pi OS image using dd
    print("Flashing the SD card with the image...")
    dd_command = f"sudo dd if={image_path} of={sd_card} bs=4M conv=fsync"
    subprocess.run(dd_command, shell=True, check=True)
    
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
    if len(sys.argv) != 6:
        print("Usage: python flash_sd_card.py <SD_CARD> <IMAGE_PATH> <SSID> <WIFI_PASSWORD> <EXPECTED_CHECKSUM>")
        sys.exit(1)

    sd_card = sys.argv[1]
    image_path = sys.argv[2]
    ssid = sys.argv[3]
    wifi_password = sys.argv[4]
    expected_checksum = sys.argv[5]

    flash_sd_card(sd_card, image_path, ssid, wifi_password, expected_checksum)
