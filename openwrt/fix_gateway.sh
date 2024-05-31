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

nft --version
# nftables v1.0.8 (Old Doc Yak #2)

opkg install nftables
# Package nftables-json (1.0.8-1) installed in root is up to date.


