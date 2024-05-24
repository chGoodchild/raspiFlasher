import subprocess
import os
import getpass

def list_partitions(sd_card):
    """List all partitions for the given SD card."""
    try:
        result = subprocess.run(['lsblk', '-nlo', 'NAME', sd_card], capture_output=True, text=True, check=True)
        partitions = result.stdout.strip().split()
        # Include the full path for partitions and exclude the entire device
        partitions = [f'/dev/{p}' for p in partitions if p.startswith(sd_card.split('/')[-1]) and p != sd_card.split('/')[-1]]
        return partitions
    except subprocess.CalledProcessError as e:
        print(f"Error listing partitions: {e}")
        return []

def is_mounted(mount_point):
    """Check if a mount point is already mounted."""
    try:
        output = subprocess.check_output(['mount'])
        return mount_point.encode() in output
    except subprocess.CalledProcessError:
        print("Failed to check mount status")
        return False

def mount_partition(partition, mount_point):
    """Mount a specific partition to a given mount point."""
    os.makedirs(mount_point, exist_ok=True)
    print(f"Mounting {partition} to {mount_point}...")
    if not is_mounted(mount_point):
        try:
            subprocess.run(['sudo', 'mount', partition, mount_point], check=True)
            print(f"Mounted {partition} to {mount_point}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to mount {partition}: {e}")
    else:
        print(f"{mount_point} is already mounted.")

def prepare_partitions(sd_card):
    """Prepare and mount partitions for copying data."""
    partitions = list_partitions(sd_card)
    
    if len(partitions) < 2:
        print("Not enough partitions found on the SD card. Creating partitions...")
        create_partitions(sd_card)
        partitions = list_partitions(sd_card)
        if len(partitions) < 2:
            raise ValueError("Failed to create the necessary partitions on the SD card.")

    # Assuming the first partition is the boot partition and the second is the root partition
    boot_partition = partitions[0]
    root_partition = partitions[1]
    
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
    partitions = list_partitions(sd_card)
    if not partitions:
        print("No partitions found on the SD card.")
        return None
    
    # Assuming the boot partition is the first one in the list
    boot_partition = partitions[0]
    mount_point = f'/media/{getpass.getuser()}/boot'
    
    if not is_mounted(mount_point):
        print(f"Mounting {boot_partition} to {mount_point}...")
        os.makedirs(mount_point, exist_ok=True)
        subprocess.run(['sudo', 'mount', boot_partition, mount_point], check=True)
    else:
        print(f"{mount_point} is already mounted.")
    
    return mount_point

def create_partitions(sd_card):
    """Create and format partitions on the SD card."""
    print("Creating and formatting partitions...")

    # Determine the partition naming scheme
    if 'mmcblk' in sd_card:
        boot_partition = f'{sd_card}p1'
        root_partition = f'{sd_card}p2'
    else:
        boot_partition = f'{sd_card}1'
        root_partition = f'{sd_card}2'

    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mklabel', 'gpt'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'fat32', '1MiB', '257MiB'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'set', '1', 'boot', 'on'], check=True)
    subprocess.run(['sudo', 'parted', '-s', sd_card, 'mkpart', 'primary', 'ext4', '257MiB', '100%'], check=True)
    subprocess.run(['sudo', 'mkfs.vfat', boot_partition], check=True)
    subprocess.run(['sudo', 'mkfs.ext4', root_partition], check=True)

def setup_sd_card(sd_card):
    """Setup the SD card with partitions, formatting, and mounting."""
    if not is_partitioned(sd_card):
        print("Partitions not found, creating them...")
        create_partitions(sd_card)
    mount_point = check_and_mount_sd_card(sd_card)
    return mount_point

def unmount_sd_card(sd_card):
    """Attempt to unmount all partitions of the SD card."""
    print(f"Unmounting all partitions on {sd_card}")

    partitions = list_partitions(sd_card)

    for partition in partitions:
        if os.path.exists(partition):  # Check if the partition exists
            subprocess.run(['sudo', 'umount', partition], stderr=subprocess.DEVNULL)

