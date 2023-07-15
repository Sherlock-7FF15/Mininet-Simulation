#!/usr/bin/env python3
import socket
import csv
import time
from datetime import datetime


def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.0.0.21", 80))
        ip_address = sock.getsockname()[0]
        return ip_address
    except socket.error:
        return None
    finally:
        sock.close()


def udp_server(host, port):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_socket.bind((host, port))
    path = '/home/ee597/Desktop/MiniTest/dataFile/packet_volume/{}.csv'.format(host)
    print('UDP server listening on {}:{}'.format(host, port))
    # check whether the target file exist
    try:
        with open(path, 'w') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=['data', 'address', 'time'])
            writer.writeheader()
    except FileExistsError:
        pass
    # Udp Server Listen
    while True:
        data, address = s_socket.recvfrom(1024)
        formatted_time = datetime.now()
        packet_info = {
            'data': data.decode(),
            'address': address[0],
            'time': formatted_time
        }
        print('Received data from {} : {}'.format(address, data.decode()))
        with open(path, 'a') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=['data', 'address', 'time'])
            writer.writerow(packet_info)


if __name__ == '__main__':
    node_ip = get_ip_address()
    node_port = 9564
    print('{}:9564'.format(node_ip))
    udp_server(node_ip, node_port)