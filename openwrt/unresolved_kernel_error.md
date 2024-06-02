root@OpenWrt:/etc/config# iw dev
phy#0
	Interface phy0-ap0
		ifindex 3
		wdev 0x1
		addr de:a6:32:50:40:d7
		ssid TollGate
		type AP
		channel 36 (5180 MHz), width: 20 MHz, center1: 5180 MHz
		txpower 31.00 dBm
root@OpenWrt:/etc/config# brctl addbr br-guest
root@OpenWrt:/etc/config# brctl addif br-guest eth0.3
brctl: bridge br-guest: Resource busy
root@OpenWrt:/etc/config# brctl addif br-guest phy0-ap0
root@OpenWrt:/etc/config# brctl addif br-guest eth0.3
brctl: bridge br-guest: Resource busy
root@OpenWrt:/etc/config# ifconfig br-guest up
root@OpenWrt:/etc/config# ifconfig br-guest 192.168.3.1 netmask 255.255.255.0
root@OpenWrt:/etc/config# ifconfig br-guest
br-guest  Link encap:Ethernet  HWaddr DE:A6:32:50:40:D7  
          inet addr:192.168.3.1  Bcast:192.168.3.255  Mask:255.255.255.0
          inet6 addr: fe80::e08a:38ff:fe5a:2aa/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
root@OpenWrt:/etc/config# brctl show
bridge name	bridge id		STP enabled	interfaces
br-guest		8000.dea6325040d7	no		phy0-ap0
br-wwan		7fff.dca6325040d5	no		eth0.3
br-lan		7fff.dca6325040d5	no		eth0
root@OpenWrt:/etc/config# /etc/init.d/network restart; logread -f
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.708695] device phy0-ap0 left promiscuous mode
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.713490] br-guest: port 1(phy0-ap0) entered disabled state
Sun Jun  2 16:17:46 2024 daemon.warn netifd: You have delegated IPv6-prefixes but haven't assigned them to any interface. Did you forget to set option ip6assign on your lan-interfaces?
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.856842] bcmgenet fd580000.ethernet: configuring instance for external RGMII (RX delay)
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.865450] bcmgenet fd580000.ethernet eth0: Link is Up - 100Mbps/Full - flow control rx/tx
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.873866] br-lan: port 1(eth0) entered blocking state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.879132] br-lan: port 1(eth0) entered disabled state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.884500] device eth0 entered promiscuous mode
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.890272] br-lan: port 1(eth0) entered blocking state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.895509] br-lan: port 1(eth0) entered forwarding state
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'lan' is enabled
Sun Jun  2 16:17:46 2024 daemon.notice netifd: bridge 'br-lan' link is up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'lan' has link connectivity
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'lan' is setting up now
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.923359] br-wwan: port 1(eth0.3) entered blocking state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.928860] br-wwan: port 1(eth0.3) entered disabled state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.934699] device eth0.3 entered promiscuous mode
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.940674] br-wwan: port 1(eth0.3) entered blocking state
Sun Jun  2 16:17:46 2024 kern.info kernel: [  927.946184] br-wwan: port 1(eth0.3) entered forwarding state
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'wwan' is enabled
Sun Jun  2 16:17:46 2024 daemon.notice netifd: bridge 'br-wwan' link is up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'wwan' has link connectivity
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'wwan' is setting up now
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'wwan' is now up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: VLAN 'eth0.3' link is up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'loopback' is enabled
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'loopback' is setting up now
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'loopback' is now up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Network device 'eth0' link is up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Network device 'lo' link is up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Interface 'loopback' has link connectivity
Sun Jun  2 16:17:46 2024 daemon.notice netifd: lan (27443): udhcpc: started, v1.36.1
Sun Jun  2 16:17:46 2024 daemon.notice netifd: radio0 (27442): WARNING: Variable 'data' does not exist or is not an array/object
Sun Jun  2 16:17:46 2024 daemon.notice netifd: lan (27443): udhcpc: broadcasting discover
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: Set new config for phy phy0:
Sun Jun  2 16:17:46 2024 daemon.notice wpa_supplicant[1849]: Set new config for phy phy0
Sun Jun  2 16:17:46 2024 daemon.notice netifd: radio0 (27442): command failed: I/O error (-5)
Sun Jun  2 16:17:46 2024 daemon.notice wpa_supplicant[1849]: Set new config for phy phy0
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: Set new config for phy phy0: /var/run/hostapd-phy0.conf
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: Restart interface for phy phy0
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: Configuration file: data: driver=nl80211 logger_syslog=127 logger_syslog_level=2 logger_stdout=127 logger_stdout_level=2 country_code=US ieee80211d=1 ieee80211h=1 hw_mode=a beacon_int=100 chanlist=36 tx_queue_data2_burst=2.0 #num_global_macaddr=1 ieee80211n=1 ht_coex=0 ht_capab=[SHORT-GI-20][SHORT-GI-40][DSSS_CCK-40] ieee80211ac=1 vht_oper_chwidth=0 vht_oper_centr_freq_seg0_idx= vht_capab=[SHORT-GI-80][SU-BEAMFORMEE][MAX-A-MPDU-LEN-EXP0] channel=36  interface=phy0-ap0 bssid=dc:a6:32:50:40:d6 ctrl_interface=/var/run/hostapd ap_isolate=1 bss_load_update_period=60 chan_util_avg_period=600 disassoc_low_ack=1 skip_inactivity_poll=0 preamble=1 wmm_enabled=1 ignore_broadcast_ssid=0 uapsd_advertisement_enabled=1 utf8_ssid=1 multi_ap=0 auth_algs=1 wpa=0 ssid=TollGate qos_map_set=0,0,2,16,1,1,255,255,18,22,24,38,40,40,44,46,48,56 #default_macaddr nas_identifier=dca6325040d6  (phy phy0) --> new PHY
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: phy0-ap0: interface state UNINITIALIZED->COUNTRY_UPDATE
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: exiting on receipt of SIGTERM
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: started, version 2.90 cachesize 150
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: compile time options: IPv6 GNU-getopt no-DBus UBus no-i18n no-IDN DHCP DHCPv6 no-Lua TFTP conntrack no-ipset nftset auth cryptohash DNSSEC no-ID loop-detect inotify dumpfile
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: UBus support enabled: connected to system bus
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for test
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for onion
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for localhost
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for local
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for invalid
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: using only locally-known addresses for bind
Sun Jun  2 16:17:46 2024 daemon.warn dnsmasq[1]: no servers found in /tmp/resolv.conf.d/resolv.conf.auto, will retry
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: read /etc/hosts - 7 names
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: read /tmp/hosts/dhcp.cfg01411c - 0 names
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: read /tmp/hosts/dhcp.cfg05411c - 0 names
Sun Jun  2 16:17:46 2024 daemon.info dnsmasq[1]: read /tmp/hosts/odhcpd - 0 names
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: phy0-ap0: interface state COUNTRY_UPDATE->ENABLED
Sun Jun  2 16:17:46 2024 daemon.notice hostapd: phy0-ap0: AP-ENABLED
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Wireless device 'radio0' is now up
Sun Jun  2 16:17:46 2024 daemon.notice netifd: Network device 'phy0-ap0' link is up
Sun Jun  2 16:17:49 2024 daemon.notice netifd: lan (27443): udhcpc: broadcasting discover
Sun Jun  2 16:17:49 2024 daemon.notice netifd: lan (27443): udhcpc: broadcasting select for 192.168.8.231, server 192.168.8.1
Sun Jun  2 16:17:49 2024 daemon.notice netifd: lan (27443): udhcpc: lease of 192.168.8.231 obtained from 192.168.8.1, lease time 43200
Sun Jun  2 16:17:49 2024 daemon.notice netifd: Interface 'lan' is now up
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: reading /tmp/resolv.conf.d/resolv.conf.auto
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using nameserver 192.168.8.1#53
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for test
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for onion
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for localhost
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for local
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for invalid
Sun Jun  2 16:17:49 2024 daemon.info dnsmasq[1]: using only locally-known addresses for bind
Sun Jun  2 16:17:50 2024 user.notice firewall: Reloading firewall due to ifup of lan (br-lan)
Sun Jun  2 16:17:50 2024 daemon.warn odhcpd[2197]: No default route present, overriding ra_lifetime!
Sun Jun  2 16:17:51 2024 daemon.info dnsmasq[1]: read /etc/hosts - 7 names
Sun Jun  2 16:17:51 2024 daemon.info dnsmasq[1]: read /tmp/hosts/dhcp.cfg01411c - 0 names
Sun Jun  2 16:17:51 2024 daemon.info dnsmasq[1]: read /tmp/hosts/dhcp.cfg05411c - 0 names
Sun Jun  2 16:17:51 2024 daemon.info dnsmasq[1]: read /tmp/hosts/odhcpd - 0 names
Sun Jun  2 16:17:51 2024 daemon.crit dnsmasq[1]: failed to create listening socket for 192.168.8.231: Address in use
Sun Jun  2 16:17:51 2024 daemon.crit dnsmasq[1]: FAILED to start up
Sun Jun  2 16:17:56 2024 daemon.crit dnsmasq[1]: failed to create listening socket for 192.168.8.231: Address in use
Sun Jun  2 16:17:56 2024 daemon.crit dnsmasq[1]: FAILED to start up
Sun Jun  2 16:18:01 2024 daemon.crit dnsmasq[1]: failed to create listening socket for 192.168.8.231: Address in use
Sun Jun  2 16:18:01 2024 daemon.crit dnsmasq[1]: FAILED to start up
Sun Jun  2 16:18:06 2024 daemon.crit dnsmasq[1]: failed to create listening socket for 192.168.8.231: Address in use
Sun Jun  2 16:18:06 2024 daemon.crit dnsmasq[1]: FAILED to start up
Sun Jun  2 16:18:06 2024 daemon.warn odhcpd[2197]: No default route present, overriding ra_lifetime!
Sun Jun  2 16:18:11 2024 daemon.crit dnsmasq[1]: failed to create listening socket for 192.168.8.231: Address in use
Sun Jun  2 16:18:11 2024 daemon.crit dnsmasq[1]: FAILED to start up
Sun Jun  2 16:18:11 2024 daemon.info procd: Instance dnsmasq::cfg01411c s in a crash loop 6 crashes, 1 seconds since last crash
Sun Jun  2 16:18:17 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: associated
Sun Jun  2 16:18:17 2024 daemon.notice hostapd: phy0-ap0: AP-STA-CONNECTED ae:63:e2:65:9f:e7 auth_alg=open
Sun Jun  2 16:18:17 2024 kern.err kernel: [  958.801942] ieee80211 phy0: brcmf_p2p_send_action_frame: Unknown Frame: category 0x8a, action 0x6
Sun Jun  2 16:18:22 2024 daemon.warn odhcpd[2197]: No default route present, overriding ra_lifetime!
Sun Jun  2 16:18:35 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: disassociated
Sun Jun  2 16:18:35 2024 daemon.notice hostapd: phy0-ap0: AP-STA-DISCONNECTED ae:63:e2:65:9f:e7
Sun Jun  2 16:18:43 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: associated
Sun Jun  2 16:18:43 2024 daemon.notice hostapd: phy0-ap0: AP-STA-CONNECTED ae:63:e2:65:9f:e7 auth_alg=open
Sun Jun  2 16:18:43 2024 kern.err kernel: [  984.780196] ieee80211 phy0: brcmf_p2p_send_action_frame: Unknown Frame: category 0x8a, action 0x6
Sun Jun  2 16:19:01 2024 daemon.info hostapd: phy0-ap0: STA ae:63:e2:65:9f:e7 IEEE 802.11: disassociated
Sun Jun  2 16:19:01 2024 daemon.notice hostapd: phy0-ap0: AP-STA-DISCONNECTED ae:63:e2:65:9f:e7
Sun Jun  2 16:19:05 2024 daemon.warn odhcpd[2197]: No default route present, overriding ra_lifetime!


I seem to be getting Kernel errors when I try to connect to the interface via wifi. What am I doing wrong? 



