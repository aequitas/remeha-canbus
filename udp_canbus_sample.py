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
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    packet = struct.unpack("<IB8s", data)

    can_id = packet[0]
    size = packet[1]
    candata = packet[2][:size]
    hex_data = ''.join(format(x, '02x') for x in candata)

    canopen_function_code = can_id & 0x780
    canopen_node_id = can_id & 0x7F

    if can_id in [451]:
        print(f"can_id: {can_id} canopen function code: {canopen_function_code:<4} ({canopen_function_code:04x}), size: {size}, data: {hex_data}")
