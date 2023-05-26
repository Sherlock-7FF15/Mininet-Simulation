import socket


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
    print('UDP server listening on {}:{}'.format(host, port))
    # Udp Server Listen
    while True:
        data, address = s_socket.recvfrom(1024)
        print ('Received data from {} : {}'.format(address, data.decode()))


node_ip = get_ip_address()
node_port = 9564
print ('{}:9564'.format(node_ip))
udp_server(node_ip, node_port)