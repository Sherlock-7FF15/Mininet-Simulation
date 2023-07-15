#!/usr/bin/env python3

import argparse
from scapy.all import *
import pcapy
from struct import *
import time
import threading
from datetime import datetime

import csv

from scapy.layers.inet import TCP, UDP
from scapy.layers.l2 import Ether


def packet_capture(dev, file_name):
    # print(dev)
    pc = pcapy.open_live(dev, 65536, 1, 0)
    path = '/home/ee597/Desktop/MiniTest/dataFile/output_data/{}.csv'.format(file_name)
    prev_packet_time = None

    # check whether the target file exist
    try:
        with open(path, 'w') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=['packet_length', 'packet_frame_len', 'source_ip', 'destination_ip',
                                                'source_port', 'destination_port', 'received_time', 'time_difference',
                                                'ttl', 'protocol'])
            writer.writeheader()
    except FileExistsError:
        pass

    while True:
        try:
            (header, packet) = pc.next()
            parsed_packet = Ether(packet)
            if IP in parsed_packet:
                ip_layer = parsed_packet[IP]
                current_packet_time = header.getts()[0]
                time_diff = current_packet_time - prev_packet_time if prev_packet_time is not None else None

                packet_info = {
                    'packet_length': len(packet),
                    'packet_frame_len': len(parsed_packet),
                    'source_ip': ip_layer.src,
                    'destination_ip': ip_layer.dst,
                    'source_port': ip_layer.sport if TCP in ip_layer or UDP in ip_layer else None,
                    'destination_port': ip_layer.dport if TCP in ip_layer or UDP in ip_layer else None,
                    'received_time': datetime.fromtimestamp(current_packet_time).strftime('%Y-%m-%d %H:%M:%S'),
                    'time_difference': time_diff,
                    'ttl': ip_layer.ttl,
                    'protocol': ip_layer.proto
                }
                # print(packet_info)
                # write data into csv
                with open(path, 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=['packet_length', 'packet_frame_len', 'source_ip',
                                                              'destination_ip', 'source_port', 'destination_port',
                                                              'received_time', 'time_difference', 'ttl', 'protocol'])
                    writer.writerow(packet_info)

                prev_packet_time = current_packet_time

        except pcapy.PcapError:
            continue


def network_capture(node):
    device = pcapy.findalldevs()
    print(device)
    for dev in device:
        t = threading.Thread(target=packet_capture, args=(dev, node))
        t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", type=str, default='10.0.0.0')
    args = parser.parse_args()
    network_capture(args.node)
