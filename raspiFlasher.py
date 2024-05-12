import sys
import subprocess
import os
import hashlib
import getpass

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

def unmount_sd_card(sd_card):
    """Attempt to unmount all partitions of the SD card."""
    print(f"Unmounting all partitions on {sd_card}")
    for part in ['1', '2']:  # Extend this list if there are more partitions
        subprocess.run(['sudo', 'umount', f'{sd_card}{part}'], stderr=subprocess.DEVNULL)

def test_sd_card_with_badblocks(sd_card):
    
    unmount_sd_card(sd_card)

    print("Testing SD card for bad blocks...")
    try:
        subprocess.run(['sudo', 'badblocks', '-wsv', sd_card], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Bad blocks were found on the SD card.")

def flash_sd_card(sd_card, image_path, ssid, wifi_password, expected_checksum, country_code='US'):
    # Verify the image checksum
    verify_image_checksum(image_path, expected_checksum)

    # List available disk devices and ask for user confirmation
    print("Available disk devices:")
    subprocess.run(['lsblk'])
    confirm = input(f"Are you sure you want to flash the SD card at {sd_card}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Flashing aborted.")
        return

    # Test the SD card for bad blocks in destructive mode
    test_sd_card_with_badblocks(sd_card)

    # Flash the SD card with the Raspberry Pi OS image using dd
    print("Flashing the SD card with the image...")
    dd_command = f"sudo dd if={image_path} of={sd_card} bs=4M conv=fsync status=progress"
    subprocess.run(dd_command, shell=True, check=True)
    
    # Enable SSH access
    username = getpass.getuser()  # Gets the current system's username
    print("Enabling SSH access...")
    ssh_file_path = f'/media/{username}/bootfs/ssh'  # Use the dynamic path
    with open(ssh_file_path, 'w') as ssh_file:
        pass  # Create an empty file named 'ssh'

    # Setup Wi-Fi
    print("Configuring Wi-Fi settings...")
    wpa_file_path = f'/media/{username}/bootfs/wpa_supplicant.conf'
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
    with open(wpa_file_path, 'a') as wpa_file:
        wpa_file.write(wpa_config)

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

