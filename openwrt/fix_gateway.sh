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


