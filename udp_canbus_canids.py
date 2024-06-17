#!/usr/bin/env python3

from collections import defaultdict
import socket
import struct
import datetime
import logging
import sys
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 1337

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG if '-v' in sys.argv else logging.INFO)

can_ids = defaultdict(int)

next = time.time()+5

while True:
    if time.time() > next:
        total = 0
        for can_id, count in sorted(can_ids.items()):
            if count:
                print(f"{can_id:4} [{count:2}]",end=" ")
            else:
                print(f"{can_id:4}     ",end=" ")
            total += count
            can_ids[can_id] = 0
        print(f"total: {total}")
        next = time.time()+5

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    packet = struct.unpack("<IB8s", data)

    can_id = packet[0]
    size = packet[1]
    candata = packet[2][:size]
    hex_data = ''.join(format(x, '02x') for x in candata)

    can_ids[can_id] += 1
