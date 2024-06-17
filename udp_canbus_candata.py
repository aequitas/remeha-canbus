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

can_ids = defaultdict(str)

next = time.time()+3

while True:
    # if can_id =
    if time.time() > next:
        for can_id in can_ids:
            print(f"{can_id:<16}", end=" ")
        print()

    #     total = 0
    #     for can_id, count in sorted(can_ids.items()):
    #         if count:
    #             print(f"{can_id:4} [{count:2}]",end=" ")
    #         else:
    #             print(f"{can_id:4}     ",end=" ")
    #         total += count
    #         can_ids[can_id] = 0
    #     print(f"total: {total}")
        next = time.time()+10

    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    packet = struct.unpack("<IB8s", data)

    can_id = packet[0]
    size = packet[1]
    candata = packet[2][:size]
    hex_data = ''.join(format(x, '02x') for x in candata)

    canopen_function_code = can_id & 0x780
    canopen_node_id = can_id & 0x7F

    # if canopen_function_code == 0x80:
    #     for can_id in can_ids:
    #         print(f"{can_id:<16}", end=" ")
    #     print()

    if not size:
        continue

    if can_id in [118]:
        continue

    if hex_data in ["05", "00dc0a1800", "0300000001000000", "0000000000000000", "59053c2d08000b01", "6000000000000000", "7000000000000000", "00000000ffffff00", "0300000000000000", "0000ffffff0004", "510b000000800000"]:
        continue

    can_ids[f"{can_id:<4} {canopen_function_code:<4} {canopen_node_id:<4}"] = hex_data

    for can_id in can_ids:
        print(f"{can_ids[can_id]:<16}", end=" ")
    print()
