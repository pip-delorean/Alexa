#!/usr/bin/env python
# https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/

import socket

# msg = """
#     M-SEARCH * HTTP/1.1
#     HOST:239.255.255.250:1900
#     MAN:"ssdp:discover"
#     MX:2
#     ST:upnp:rootdevice
#     """

msg = """
	M-SEARCH * HTTP/1.1
	HOST: 239.255.255.250:1900
	MAN: "ssdp:discover"
	MX: 15
	ST: urn:Belkin:device:**
	"""

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(5)
s.sendto(msg, ('239.255.255.250', 1900) )

try:
    while True:
        data, addr = s.recvfrom(65507)
        print addr, data
except socket.timeout:
    pass