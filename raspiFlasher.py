import sys
import subprocess
import os
import hashlib
import getpass
from sdcard_management import setup_sd_card, check_and_mount_sd_card, create_partitions, prepare_partitions

def configure_user(sd_card, username, plain_password):
    # Encrypt the password
    from subprocess import Popen, PIPE
    process = Popen(['openssl', 'passwd', '-6'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    encrypted_password, _ = process.communicate(input=plain_password)

    # Path to userconf.txt on the boot partition
    mount_point = check_and_mount_sd_card(sd_card)
    userconf_path = os.path.join(mount_point, 'userconf.txt')
    with open(userconf_path, 'w') as f:
        f.write(f'{username}:{encrypted_password.strip()}')


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

    print("No bad blocks found, proceeding to partition the SD card.")
    create_partitions(sd_card)
    check_and_mount_sd_card(sd_card)


def flash_sd_card(sd_card, image_path, ssid, wifi_password, expected_checksum, country_code='US'):
    """Main function to flash the SD card with all configurations."""
    # verify_image_checksum(image_path, expected_checksum)
    print("Available disk devices:")
    subprocess.run(['lsblk'])
    confirm = input(f"Are you sure you want to flash the SD card at {sd_card}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Flashing aborted.")
        return

    # test_sd_card_with_badblocks(sd_card)    

    # Ensure the SD card is not mounted before flashing
    unmount_sd_card(sd_card)

    print("lsblk before flashing:")
    subprocess.run(['lsblk'])

    # The image already contains two partitions, so `of` doesn't need
    # to point at individual partitions in dd
    print("Flashing the SD card with the image...")
    dd_command = f"sudo dd if={image_path} of={sd_card} bs=4M conv=fsync status=progress"
    subprocess.run(dd_command, shell=True, check=True)
    
    print("lsblk after flashing:")
    subprocess.run(['lsblk'])

    # Remount partitions after flashing for further configuration
    boot_mount, root_mount = prepare_partitions(sd_card)
    print(f"Mounted boot partition on {boot_mount} and root partition on {root_mount}")

    # Enable SSH access
    username = getpass.getuser()  # Gets the current system's username
    print("Enabling SSH access...")
    ssh_file_path = f'/media/{username}/boot/ssh'  # Use the dynamic path
    with open(ssh_file_path, 'w') as ssh_file:
        pass  # Create an empty file named 'ssh'

    # Setup Wi-Fi
    print("Configuring Wi-Fi settings...")
    wpa_file_path = f'/media/{username}/boot/wpa_supplicant.conf'
    wpa_config = f"""
country={country_code}
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={{
    ssid="{ssid}"
    psk="{wifi_password}"
    key_mgmt=WPA-PSK
    disabled=0
    priority=1
}}
    """
    with open(wpa_file_path, 'a') as wpa_file:
        wpa_file.write(wpa_config)

    # Example usage in your main script
    username = input("Enter the desired username for Raspberry Pi: ")
    password = getpass.getpass("Enter the desired password for Raspberry Pi: ")
    configure_user(sd_card, username, password)

    print("SD card is ready with the OS, SSH, and Wi-Fi configured.")

def is_root():
    return os.geteuid() == 0

if not is_root():
    print("Script not running as root. Trying to elevate privileges...")
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python flash_sd_card.py <SD_CARD> <IMAGE_PATH> <SSID> <WIFI_PASSWORD> <EXPECTED_CHECKSUM>")
        sys.exit(1)

    is_root()

    flash_sd_card(*sys.argv[1:])

