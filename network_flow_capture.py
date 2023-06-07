#!/usr/bin/env python3

import argparse
from scapy.all import *
import pcapy
from struct import *
import time
import threading
from datetime import datetime


def packet_capture(dev, ti):
    # print(dev)
    pc = pcapy.open_live(dev, 65536, 1, 0)
    start_time = time.time()
    while True:
        if time.time() - start_time > ti:
            break
        try:
            (header, packet) = pc.next()
            parsed_packet = Ether(packet)  # decode the original packet to scapy packet
            if IP in parsed_packet:
                ip_layer = parsed_packet[IP]
                packet_info = {
                    'packet_length': len(packet),
                    'packet_frame_len': len(parsed_packet),
                    'source_ip': ip_layer.src,
                    'destination_ip': ip_layer.dst,
                    'source_port': ip_layer.sport if TCP in ip_layer or UDP in ip_layer else None,
                    'destination_port': ip_layer.dport if TCP in ip_layer or UDP in ip_layer else None,
                    'received_time': datetime.fromtimestamp(header.getts()[0]).strftime('%Y-%m-%d %H:%M:%S'),
                    'ttl': ip_layer.ttl,
                    'protocol': ip_layer.proto
                }
                print(packet_info)
        except pcapy.PcapError:
            continue


def network_capture(ti):
    device = pcapy.findalldevs()
    print(device)
    for dev in device:
        t = threading.Thread(target=packet_capture, args=(dev, ti))
        t.start()


if __name__ == '__main__':
    # network_flow_capture.py [-h] [--time TIME]
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=int, default=10)
    args = parser.parse_args()
    network_capture(args.time)
