#!/usr/bin/env python3

import pyshark
import time
import argparse


def capture_and_analysis(capture_time):
    capture = pyshark.LiveCapture()
    start_time = time.time()

    for packet in capture.sniff_continuously():
        try:
            packet_length = packet.ip.len
            packet_frame_len = packet.length
            source_ip = packet.ip.src
            destination_ip = packet.ip.dst
            source_port = packet.tcp.srcport if 'tcp' in packet else packet.udp.srcport
            destination_port = packet.tcp.dstport if 'tcp' in packet else packet.udp.dstport
            received_time = packet.sniff_time.strftime('%Y-%m-%d %H:%M:%S')
            protocol = packet.transport_layer
            ttl = packet.ip.ttl
            print([packet_length, packet_frame_len, source_ip, destination_ip, source_port, destination_port, received_time, ttl, protocol])
            if time.time() - start_time > capture_time:
                capture.close()
                break
        except AttributeError:
            continue


if __name__ == '__main__':

    # network_flow_capture.py [-h] [--time TIME]
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=int, default=5)
    args = parser.parse_args()
    capture_and_analysis(args.time)
