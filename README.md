# Setting Up Raspberry Pi SD Card Flasher

This README provides guidance on configuring your `config.yaml` file with the correct SD card device path, and retrieving your current network SSID and Wi-Fi password.

## Finding the Correct SD Card Device Path

To identify the correct device path for your SD card to use in your `config.yaml`, you can follow these steps:

1. **Insert your SD card into your computer.**
2. Open a terminal.
3. Run the command `lsblk` before and after inserting your SD card. Note any new device that appears in the list; this is likely your SD card.
4. Identify your SD card based on its size and the fact it typically won't have any mount points if it's freshly inserted or not automatically mounted.

For example, from your output, if `sdb` appears after inserting an SD card, and assuming no partitions are listed under it (or it's a new device showing up in the list), `sdb` is likely your SD card.

**Example Entry for config.yaml:**

```yaml
sd_card: "/dev/sdb"
```

**Important:** Make sure to replace `/dev/sdb` with the actual device path from your `lsblk` output. Using the wrong device path can lead to data loss if directed at the wrong storage device.

## Finding Your Current Network SSID and Wi-Fi Password

### Finding SSID

To find out which Wi-Fi network your machine is currently connected to, you can use the following command in the terminal:

```bash
nmcli -t -f active,ssid dev wifi | egrep '^yes' | cut -d':' -f2
```

This command lists active network connections and extracts the SSID of the currently active Wi-Fi network.

### Finding Wi-Fi Password

To retrieve the password for the Wi-Fi network you're currently connected to, you can use the following command:

```bash
for file in /etc/NetworkManager/system-connections/*; do
    echo "Checking $file for Wi-Fi password:"
    sudo grep psk= "$file" | cut -d'=' -f2
done
```

This command accesses the network configuration files managed by NetworkManager and extracts the password. Note that you may need superuser privileges to view these files.

**Note:** These commands assume you are using NetworkManager, which is common in many Linux distributions. If your distribution does not use NetworkManager, you'll need to locate your Wi-Fi configuration details in the specific configuration files or tools your system uses.

## Updating config.yaml

Once you have the SD card path, SSID, and Wi-Fi password, update your `config.yaml` accordingly:

```yaml
sd_card: "/dev/sdb"
image_url: "https://downloads.raspberrypi.com/raspios_armhf/images/raspios_armhf-2024-03-15/2024-03-15-raspios-bookworm-armhf.img.xz"
image_path: "./2024-03-15-raspios-bookworm-armhf.img.xz"
ssid: "Your Wifi User Name"
wifi_password: "Your Wifi Password"
expected_checksum: "52a807d37a894dfcb09274382762f8274c7044ce3d98040aba474e0af93b85ab"
```

Replace each placeholder with the actual data from your environment.

## Workflow

```bash
$ python3 yaml_launcher.py 
Launching the SD card flashing script...
Script not running as root. Trying to elevate privileges...
Available disk devices:
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0    7:0    0     4K  1 loop /snap/bare/5
loop1    7:1    0 161,2M  1 loop /snap/chromium/2842
loop2    7:2    0 161,2M  1 loop /snap/chromium/2846
loop3    7:3    0  55,7M  1 loop /snap/core18/2812
loop4    7:4    0  55,7M  1 loop /snap/core18/2823
loop5    7:5    0  63,9M  1 loop /snap/core20/2264
loop6    7:6    0  63,9M  1 loop /snap/core20/2318
loop7    7:7    0  74,2M  1 loop /snap/core22/1122
loop8    7:8    0  74,2M  1 loop /snap/core22/1380
loop9    7:9    0  66,1M  1 loop /snap/cups/1044
loop10   7:10   0  66,1M  1 loop /snap/cups/1047
loop11   7:11   0 269,6M  1 loop /snap/firefox/4209
loop12   7:12   0 164,8M  1 loop /snap/gnome-3-28-1804/161
loop13   7:13   0 164,8M  1 loop /snap/gnome-3-28-1804/198
loop14   7:14   0   219M  1 loop /snap/gnome-3-34-1804/77
loop15   7:15   0 218,4M  1 loop /snap/gnome-3-34-1804/93
loop16   7:16   0 346,3M  1 loop /snap/gnome-3-38-2004/115
loop17   7:17   0 349,7M  1 loop /snap/gnome-3-38-2004/143
loop18   7:18   0 504,2M  1 loop /snap/gnome-42-2204/172
loop19   7:19   0 505,1M  1 loop /snap/gnome-42-2204/176
loop20   7:20   0  65,2M  1 loop /snap/gtk-common-themes/1519
loop21   7:21   0  91,7M  1 loop /snap/gtk-common-themes/1535
loop22   7:22   0   118M  1 loop /snap/slack/147
loop23   7:23   0   118M  1 loop /snap/slack/149
loop24   7:24   0  12,9M  1 loop /snap/snap-store/1113
loop25   7:25   0  12,3M  1 loop /snap/snap-store/959
loop26   7:26   0  39,1M  1 loop /snap/snapd/21184
loop27   7:27   0  38,7M  1 loop /snap/snapd/21465
loop28   7:28   0   476K  1 loop /snap/snapd-desktop-integration/157
sda      8:0    0 465,8G  0 disk 
├─sda1   8:1    0   512M  0 part /boot/efi
├─sda2   8:2    0     1K  0 part 
└─sda5   8:5    0 465,3G  0 part /var/snap/firefox/common/host-hunspell
                                 /
sdb      8:16   1  29,7G  0 disk 
├─sdb1   8:17   1   512M  0 part /media/[username]/bootfs
└─sdb2   8:18   1   4,6G  0 part /media/[username]/rootfs
Are you sure you want to flash the SD card at /dev/sdb? (yes/no): yes
Unmounting all partitions on /dev/sdb
Flashing the SD card with the image...
5427429376 bytes (5,4 GB, 5,1 GiB) copied, 83,3035 s, 65,2 MB/sMounted boot partition on /media/root/boot and root partition on /media/root/root
Enabling SSH access...
Configuring Wi-Fi settings...
Password: 
Verifying - Password: 
Mounting /dev/sdb1 to /media/root/bootfs...
mount_point,  /media/root/bootfs
Copied first-boot-setup.sh to /media/root/boot/first-boot-setup.sh
Made first-boot-setup.sh executable
Modified /media/root/root/etc/rc.local to include first-boot-setup.sh
SD card is ready with the OS, SSH, and Wi-Fi configured.
It took 92.92427706718445 seconds to flash the image and set up the pi
```


## Manual dependency installation

```bash
wget https://raw.githubusercontent.com/chGoodchild/raspiFlasher/master/manual_setup.sh
chmod +x manual_setup.sh
./manual_setup.sh
```

## OpenWRT

Only works if raspbian is flashed just before flashing OpenWRT.

Have to figure out why this is the case...