/etc/init.d/network restart
/etc/init.d/firewall restart
/etc/init.d/opennds restart

logread | grep opennds
logread | grep firewall

ndsctl status

ip addr show guest
ip addr show eth0.3

		
service network restart
service firewall restart
service opennds restart
service dnsmasq restart

nft --version
# nftables v1.0.8 (Old Doc Yak #2)

opkg install nftables
# Package nftables-json (1.0.8-1) installed in root is up to date.


nft add table ip nds_nat
nft add chain ip nds_nat ndsOUT { type nat hook postrouting priority 100 \; }
nft add rule ip nds_nat ndsOUT ip daddr 192.168.3.1 tcp dport 2050 counter accept
nft add rule ip nds_nat ndsOUT tcp dport 80 counter dnat to 192.168.3.1:2050

opkg update
opkg install kmod-nf-nat kmod-ipt-tproxy



vi /etc/opkg/distfeeds.conf

# Set correct target and architecture for your system.
src/gz openwrt_core https://downloads.openwrt.org/releases/23.05.0/targets/bcm27xx/bcm2711/packages
src/gz openwrt_base https://downloads.openwrt.org/releases/23.05.0/packages/aarch64_cortex-a72/base
src/gz openwrt_luci https://downloads.openwrt.org/releases/23.05.0/packages/aarch64_cortex-a72/luci
src/gz openwrt_packages https://downloads.openwrt.org/releases/23.05.0/packages/aarch64_cortex-a72/packages
src/gz openwrt_routing https://downloads.openwrt.org/releases/23.05.0/packages/aarch64_cortex-a72/routing
src/gz openwrt_telephony https://downloads.openwrt.org/releases/23.05.0/packages/aarch64_cortex-a72/telephony


# Still getting Kernel errors
# root@OpenWrt:/etc/config# /etc/init.d/network restart; logread -f
# Sun Jun  2 16:18:17 2024 daemon.notice hostapd: phy0-ap0: AP-STA-CONNECTED ae:63:e2:65:9f:e7 auth_alg=open
# Sun Jun  2 16:18:17 2024 kern.err kernel: [  958.801942] ieee80211 phy0: brcmf_p2p_send_action_frame: Unknown Frame: category 0x8a, action 0x6
# Sun Jun  2 16:18:22 2024 daemon.warn odhcpd[2197]: No default route present, overriding ra_lifetime!
# Sun Jun  2 16:18:35 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: disassociated
# Sun Jun  2 16:18:35 2024 daemon.notice hostapd: phy0-ap0: AP-STA-DISCONNECTED ae:63:e2:65:9f:e7
# Sun Jun  2 16:18:43 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: associated


# brctl show
# brctl delif br-wwan eth0.3
# ifconfig br-wwan down
# ip link set br-wwan down
# brctl delbr br-wwan
# brctl addbr br-guest
# brctl addif br-guest eth0.3
# brctl addif br-guest phy0-ap0
# ifconfig br-guest up
# ifconfig br-guest 192.168.3.1 netmask 255.255.255.0


