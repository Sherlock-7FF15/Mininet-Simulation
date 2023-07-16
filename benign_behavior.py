#!/usr/bin/env python3
import argparse
import random
import string
import time
from scapy.layers.inet import IP, ICMP
from scapy.all import *
import socket


def udp_send(act_time, sleep_time):
    start_time = time.time()
    count = 0
    while True:
        if time.time() - start_time > act_time:
            break
        ip_list = [
            '10.0.0.100'
        ]
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        length = random.randint(40, 60)
        random_content = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        c_socket.sendto(random_content.encode('utf-8'), (random.choice(ip_list), 9567))
        count += 1
        time.sleep(sleep_time)
    print('send {} packets within {} seconds'.format(count, act_time))


if __name__ == "__main__":
    #  benign_behavior.py [-h] [--time TIME] [--n N] [--sleep SLEEP]
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=float, default=5)
    parser.add_argument("--sleep", type=float, default=0.2)
    args = parser.parse_args()
    udp_send(args.time, args.sleep)
