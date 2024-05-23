import time
import sys
import subprocess
import os
import hashlib
import getpass
import uuid
import shutil
import yaml
from sdcard_management import setup_sd_card, check_and_mount_sd_card, create_partitions, prepare_partitions

def flash_action(image_path, sd_card):
    print("Flashing the SD card with the image...")
    dd_command = f"sudo dd if={image_path} of={sd_card} bs=4M conv=fsync status=progress"

    with subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stderr:
            print(f"\r{line.strip()}", end='')  # Print and overwrite the same line
        process.wait()  # Wait for the dd command to finish

    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, dd_command)

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def configure_user(sd_card, username, plain_password):
    # Encrypt the password
    from subprocess import Popen, PIPE
    process = Popen(['openssl', 'passwd', '-6'], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    encrypted_password, _ = process.communicate(input=plain_password)

    # Path to userconf.txt on the boot partition
    mount_point = check_and_mount_sd_card(sd_card)
    print("mount_point, ", mount_point)
    userconf_path = os.path.join(mount_point, 'userconf.txt')
    with open(userconf_path, 'w') as f:
        f.write(f'{username}:{encrypted_password.strip()}')

def configure_wifi(sd_card, ssid, wifi_password, boot_mount, root_mount):
    # Generate a UUID for the connection
    connection_uuid = str(uuid.uuid4())
    
    wifi_config = f"""
[connection]
id=my-wifi
uuid={connection_uuid}
type=wifi
interface-name=wlan0
autoconnect=true

[wifi]
mode=infrastructure
ssid={ssid}

[wifi-security]
key-mgmt=wpa-psk
psk={wifi_password}

[ipv4]
method=auto
dhcp-client-id=mac
dhcp-send-hostname=true

[ipv6]
method=auto
    """
    wifi_config_path = os.path.join(root_mount, 'etc', 'NetworkManager', 'system-connections', 'my-wifi.nmconnection')
    
    os.makedirs(os.path.dirname(wifi_config_path), exist_ok=True)
    with open(wifi_config_path, 'w') as f:
        f.write(wifi_config)
    
    # Set permissions
    subprocess.run(['sudo', 'chmod', '600', wifi_config_path], check=True)
    subprocess.run(['sudo', 'chown', 'root:root', wifi_config_path], check=True)

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

def flash_sd_card(sd_card, image_path, ssid, wifi_password, expected_checksum, pi_username, pi_password, country_code='US'):
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

    # The image already contains two partitions, so `of` doesn't need
    # to point at individual partitions in dd
    flash_action(image_path, sd_card)
    
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

    configure_user(sd_card, pi_username, pi_password)
    configure_wifi(sd_card, ssid, wifi_password, boot_mount, root_mount)

    # Copy the first-boot-setup.sh script to the boot partition
    first_boot_script_path = os.path.join(os.path.dirname(__file__), 'first-boot-setup.sh')
    dest_first_boot_script_path = os.path.join(boot_mount, 'first-boot-setup.sh')
    shutil.copy(first_boot_script_path, dest_first_boot_script_path)
    print(f"Copied first-boot-setup.sh to {dest_first_boot_script_path}")

    # Ensure the script is executable
    subprocess.run(['sudo', 'chmod', '+x', dest_first_boot_script_path], check=True)
    print("Made first-boot-setup.sh executable")

    # Modify rc.local to run the first-boot-setup.sh on boot
    rc_local_path = os.path.join(root_mount, 'etc', 'rc.local')
    with open(rc_local_path, 'r+') as rc_local_file:
        rc_local_content = rc_local_file.read()
        # Ensure rc.local ends with 'exit 0' and call the setup script before it
        if 'first-boot-setup.sh' not in rc_local_content:
            rc_local_content = rc_local_content.replace('exit 0', 'bash /boot/first-boot-setup.sh\nexit 0')
            rc_local_file.seek(0)
            rc_local_file.write(rc_local_content)
            rc_local_file.truncate()
            print(f"Modified {rc_local_path} to include first-boot-setup.sh")

    print("SD card is ready with the OS, SSH, and Wi-Fi configured.")

def is_root():
    return os.geteuid() == 0

if not is_root():
    print("Script not running as root. Trying to elevate privileges...")
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

if __name__ == '__main__':

    
    # Start timing
    start_time = time.time()


    config = load_config()
    
    flash_sd_card(
        config['sd_card'], 
        config['image_path'], 
        config['ssid'], 
        config['wifi_password'], 
        config['expected_checksum'],
        config['pi_username'], 
        config['pi_password']
    )
    
    # End timing
    end_time = time.time()

    # Calculate the duration
    duration = end_time - start_time
    print(f"It took {duration} seconds to flash the image and set up the pi")

