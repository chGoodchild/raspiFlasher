

opkg update
opkg install opennds
# nano /etc/opennds/opennds.conf
/etc/init.d/opennds enable
/etc/init.d/opennds start
/etc/init.d/opennds status

opkg update
opkg install iptables-legacy
opkg install ip6tables-legacy
update-alternatives --set iptables /usr/sbin/iptables-legacy
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

ln -sf /usr/sbin/iptables-legacy /usr/sbin/iptables
ln -sf /usr/sbin/iptables-legacy-save /usr/sbin/iptables-save
ln -sf /usr/sbin/iptables-legacy-restore /usr/sbin/iptables-restore

ln -sf /usr/sbin/ip6tables-legacy /usr/sbin/ip6tables
ln -sf /usr/sbin/ip6tables-legacy-save /usr/sbin/ip6tables-save
ln -sf /usr/sbin/ip6tables-legacy-restore /usr/sbin/ip6tables-restore

opkg update
opkg remove dnsmasq
opkg install dnsmasq-full
