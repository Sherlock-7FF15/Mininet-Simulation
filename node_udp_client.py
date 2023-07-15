#!/usr/bin/env python3
import argparse
import socket
import time
import psutil


def client(int_time):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Record the network throughput value
    io_counters = psutil.net_io_counters()
    pre_val = io_counters.packets_recv + io_counters.packets_sent
    while True:
        # Update value and calculate throughput
        io_counters = psutil.net_io_counters()
        new_val = io_counters.packets_recv + io_counters.packets_sent
        throughput = new_val - pre_val
        pre_val = new_val
        for i in range(1,11):
            target_ip = '10.0.0.{}'.format(i)
            c_socket.sendto(str(throughput).encode('utf-8'), (target_ip, 9564))
        time.sleep(int_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", type=int, default=1)
    args = parser.parse_args()
    client(args.t)