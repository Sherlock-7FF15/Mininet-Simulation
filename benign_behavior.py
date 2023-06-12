#!/usr/bin/env python3

import argparse
import random
import string
import time
from scapy.layers.inet import IP, ICMP
from scapy.all import *


def send_random_data(ip_addr):
    # Generate random content
    print(ip_addr)
    random_content = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
    ben_packet = IP(dst=ip_addr) / ICMP() / random_content
    send(ben_packet)


def choose_and_send(act_time, host_num, sleep_time):
    start_time = time.time()
    while True:
        if time.time() - start_time > act_time:
            break
        ip_list = []
        for n in range(1, host_num + 1):
            host_ip = '10.0.0.{}'.format(n)
            ip_list.append(host_ip)
        send_random_data(random.choice(ip_list))
        time.sleep(sleep_time)


if __name__ == "__main__":
    #  benign_behavior.py [-h] [--time TIME] [--n N] [--sleep SLEEP]
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=float, default=10)
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=1)
    args = parser.parse_args()
    choose_and_send(args.time, args.n, args.sleep)
