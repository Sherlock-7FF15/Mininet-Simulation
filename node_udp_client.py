import socket
import time


def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        for i in range(1,11):
            target_ip = '10.0.0.{}'.format(i)
            c_socket.sendto('10', (target_ip, 9564))
        time.sleep(1)
client()