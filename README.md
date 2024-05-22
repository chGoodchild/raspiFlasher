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


------------

Steps to Configure Wi-Fi Using NetworkManager on Raspberry Pi OS Bookworm:

root/etc/NetworkManager/system-connections/my-wifi.nmconnection

[connection]
id=my-wifi
uuid=YOUR-UUID-HERE  # Generate a UUID using uuidgen command
type=wifi
interface-name=wlan0
autoconnect=true

[wifi]
mode=infrastructure
ssid=your_SSID

[wifi-security]
key-mgmt=wpa-psk
psk=your_password

[ipv4]
method=auto

[ipv6]
method=auto



sudo chmod 600 /mnt/root/etc/NetworkManager/system-connections/my-wifi.nmconnection
sudo chown root:root /mnt/root/etc/NetworkManager/system-connections/my-wifi.nmconnection
