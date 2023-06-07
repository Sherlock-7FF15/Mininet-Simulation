#!/usr/bin/env python3

import socket
import time
import psutil


def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Record the network throughput value
    io_counters = psutil.net_io_counters()
    pre_val = io_counters.packets_recv
    while True:
        # Update value and calculate throughput
        io_counters = psutil.net_io_counters()
        new_val = io_counters.packets_recv
        throughput = new_val - pre_val
        pre_val = new_val
        for i in range(1,11):
            target_ip = '10.0.0.{}'.format(i)
            c_socket.sendto(str(throughput), (target_ip, 9564))
        time.sleep(1)
client()