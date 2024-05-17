import subprocess
import os
import getpass

def is_mounted(partition):
    """Check if a partition is still mounted."""
    try:
        output = subprocess.check_output(['mount'])
        return partition.encode() in output
    except subprocess.CalledProcessError:
        print("Failed to check mount status")
        return False

def mount_partition(partition, mount_point):
    """Mount a specific partition to a given mount point."""
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['sudo', 'mount', partition, mount_point], check=True)

def unmount_partition(partition):
    """Unmount a specific partition."""
    subprocess.run(['sudo', 'umount', partition], stderr=subprocess.DEVNULL)

    # Verify that the partitions are indeed unmounted
    for part in partitions:
        part_path = f'{sd_card}{part}'
        if is_mounted(part_path):
            raise Exception(f"Failed to unmount {part_path}, still mounted.")

def prepare_partitions(sd_card):
    """Prepare and mount partitions for copying data."""
    boot_partition = f'{sd_card}1'
    root_partition = f'{sd_card}2'
    boot_mount = f'/media/{getpass.getuser()}/boot'
    root_mount = f'/media/{getpass.getuser()}/root'
    mount_partition(boot_partition, boot_mount)
    mount_partition(root_partition, root_mount)
    return boot_mount, root_mount


def is_partitioned(sd_card):
    """Check if the SD card has necessary partitions."""
    try:
        output = subprocess.check_output(['lsblk', '-f', sd_card])
        return b'vfat' in output and b'ext4' in output
    except subprocess.CalledProcessError:
        return False

def check_and_mount_sd_card(sd_card):
    """Check and mount the SD card boot partition."""
    boot_partition = f'{sd_card}1'
    mount_point = f'/media/{getpass.getuser()}/bootfs'
    if not os.path.ismount(mount_point):
        print(f"Mounting {boot_partition} to {mount_point}...")
        os.makedirs(mount_point, exist_ok=True)
        subprocess.run(['sudo', 'mount', boot_partition, mount_point], check=True)
    return mount_point

def create_partitions(sd_card):
    """Create and format partitions on the SD card."""
    print("Creating and formatting partitions...")
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mklabel', 'gpt'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'fat32', '1MiB', '257MiB'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'set', '1', 'boot', 'on'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'ext4', '257MiB', '100%'], check=True)
    subprocess.run(['sudo', 'mkfs.vfat', f'{sd_card}1'], check=True)
    subprocess.run(['sudo', 'mkfs.ext4', f'{sd_card}2'], check=True)


def setup_sd_card(sd_card):
    """Setup the SD card with partitions, formatting, and mounting."""
    if not is_partitioned(sd_card):
        print("Partitions not found, creating them...")
        create_partitions(sd_card)
    mount_point = check_and_mount_sd_card(sd_card)
    return mount_point


"""
def format_partitions(sd_card):
    print("Formatting partitions...")
    # Format the boot partition to FAT32
    subprocess.run(['sudo', 'mkfs.vfat', f'{sd_card}1'], check=True)
    # Format the main partition to EXT4
    subprocess.run(['sudo', 'mkfs.ext4', f'{sd_card}2'], check=True)

def create_partitions(sd_card):
    # Create partitions on the SD card after confirming it is bad-block free.
    print("Creating partition table and partitions...")
    # Creating a new GPT partition table
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mklabel', 'gpt'], check=True)

    # Creating a small FAT32 boot partition of 256MB
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'fat32', '1MiB', '257MiB'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'set', '1', 'boot', 'on'], check=True)  # Mark as bootable

    # Creating a larger Linux filesystem partition for the remaining space
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'ext4', '257MiB', '100%'], check=True)

    # Formatting the partitions
    format_partitions(sd_card)


    
"""
