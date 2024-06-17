#!/usr/bin/env python3

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

rxpdo = "0x00"

while True:
    # if int(time.time()*50)%2:
    #     print()
    data, addr = sock.recvfrom(13) # buffer size is 1024 bytes
    packet = struct.unpack("<IB8s", data)
    # print(packet)
    can_id = packet[0]
    size = packet[1]
    candata = packet[2][:size]
    hex_data = ''.join(format(x, '02x') for x in candata)

    canopen_function_code = can_id & 0x780
    canopen_node_id = can_id & 0x7F

    print(f"canbus canid: {can_id:<4} co_id: {canopen_node_id:<2} fc: {canopen_function_code:<4} ({canopen_function_code:04x}), size: {size}, data: {hex_data}")
    #continue

    if candata == 0:
        continue

    if canopen_function_code == 0x0:
        continue
        log.debug("canopen NMT node control")
    elif canopen_function_code == 0x80:
        print()
        log.info("canopen sync")
    elif canopen_function_code == 0x700:
        continue
        log.debug(f"canopen hearthbeat node id: {canopen_node_id}")
    elif canopen_function_code == 0x100:
        timestamp = struct.unpack("<LH", candata)
        date = datetime.datetime.fromisoformat('1984-01-01') + datetime.timedelta(days=timestamp[1], milliseconds=timestamp[0])
        log.debug(f"canopen timestamp: {timestamp}, {date}")
    elif canopen_function_code >= 0x71 and canopen_function_code <= 0x76:
        continue
        log.debug("canopen flying master")
    elif canopen_function_code in [0x180, 0x280, 0x380, 0x480]:
        log.debug(f"canopen TxPDO node id: {canopen_node_id:02d}, data: {hex_data}")
        if canopen_node_id == 1 and len(candata) == 7:
            unpacked = struct.unpack("<bbbbbbb", candata)
            log.info(f"Status: {unpacked[0]}, Substatus: {unpacked[1]}, rest: {unpacked[2:]}, hexdata: {hex_data}")
        if canopen_node_id == 1 and len(candata) == 8:
            unpacked = struct.unpack("<Hbbbbbb", candata)
            log.info(f"Outside: {unpacked[0]*0.01:.2f} °C")
        if canopen_node_id == 65 and len(candata) == 8 and candata[0:2] == b'\x00\x07':
            unpacked = struct.unpack("<bbbHBH", candata)
            # print(hex_data)
            # log.info(f"Fan rpm: {unpacked[3]}, Fan setpoint: {unpacked[4]}")
            # log.info(f"Aanvoer temp: {unpacked[-1]*0.01}")
            log.info(f"Aanvoer temp: {unpacked[5]*0.01:.2f}, retour temp?: {unpacked[3]*0.01:.2f}, druk: {unpacked[4]/10:.2f}, rest: {unpacked[:-1]}, hexdata: {hex_data}")
        # if canopen_node_id == 2 and len(candata) == 5:
        #     unpacked = struct.unpack(">Hbbb", candata)
        #     log.info(f"unknown: {unpacked[0]}")



        # DEBUG:__main__:canopen TxPDO node id: 65, data: 000701210b115a14  12 waterdruk? (1.8)
        # DEBUG:__main__:canopen RxPDO node id: 65, data: 7000000000000000
        # DEBUG:__main__:canopen TxPDO node id: 65, data: 1002dc13bc167104 13 waterdruk? (1.9)

    elif canopen_function_code in [0x200,0x300,0x400, 0x500]:
        log.debug(f"canopen RxPDO node id: {canopen_node_id:02d}, data: {hex_data}")
        if canopen_node_id == 65:
            rxpdo = candata
    elif canopen_function_code in [0x580]:
        log.info(f"canopen TxSDO node id: {canopen_node_id:02d}, data: {hex_data}")
    elif canopen_function_code in [0x600]:
        log.info(f"canopen RxSDO node id: {canopen_node_id:02d}, data: {hex_data}")



    # print("received message: %s" % data)
