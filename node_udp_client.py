import socket
import time
import psutil

def client():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pre_val = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    while True:
        new_val = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        throughput = new_val - pre_val
        pre_val = new_val
        for i in range(1,11):
            target_ip = '10.0.0.{}'.format(i)
            c_socket.sendto(str(throughput), (target_ip, 9564))
        time.sleep(1)
client()