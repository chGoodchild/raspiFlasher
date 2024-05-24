import time
import sys
import subprocess
import os
import hashlib
import getpass
import yaml
from sdcard_management import setup_sd_card, unmount_sd_card, flash_action, list_partitions

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

def flash_sd_card(sd_card, image_path, expected_checksum):
    """Main function to flash the SD card with all configurations."""
    verify_image_checksum(image_path, expected_checksum)
    print("Available disk devices:")
    subprocess.run(['lsblk'])
    confirm = input(f"Are you sure you want to flash the SD card at {sd_card}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Flashing aborted.")
        return

    # test_sd_card_with_badblocks(sd_card)    

    # Ensure the SD card is not mounted before flashing
    unmount_sd_card(sd_card)

    # Flash the image to the SD card
    flash_action(image_path, sd_card)
    
    # Remount partitions after flashing for further configuration
    boot_mount, root_mount = prepare_partitions(sd_card)
    print(f"Mounted boot partition on {boot_mount} and root partition on {root_mount}")

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
        config['expected_checksum']
    )
    
    # End timing
    end_time = time.time()

    # Calculate the duration
    duration = end_time - start_time
    print(f"It took {duration} seconds to flash the image and set up the pi")

