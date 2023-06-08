#!/usr/bin/env python3
import time

from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

import pandas as pd

def create_network():
    """Create a network with 10 hosts and one server."""
    net = Mininet(controller=OVSController)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    server = net.addHost('server', ip='10.0.0.21')
    hosts = []
    for n in range(1, 11):
        host_name = 'h{}'.format(n)
        host_ip = '10.0.0.{}'.format(n)
        host = net.addHost(host_name, ip=host_ip)
        hosts.append(host)

    info('*** Adding switch\n')
    switch = net.addSwitch('s0')

    info('*** Creating links\n')
    for host in hosts:
        net.addLink(host, switch)
    net.addLink(server, switch)

    info('*** Starting network\n')
    net.start()

    info('*** Running socket server\n')

    for node in hosts:
        node.cmd('python3 ./node_udp_server.py &')
        node.cmd('python3 ./node_udp_client.py &')

    node_time_control(hosts, 1)


    info('*** Running CLI\n')
    while True:
        command = input('Input Command> ')
        # if command == 'start':
        #     for node in hosts:
        #         # This can be replaced with DDoS attack code
        #         node.cmd('ping -c 50 10.0.0.21 &')
        # if command == 'start track':
        #     for node in hosts:
        #         node.cmd('sudo python3 ./network_flow_capture.py --time {} &'.format(5))
        if command == 'exit':
            break
        CLI(net)
    info('*** Stopping network')
    net.stop()


def node_time_control(hosts, sleep_time):
    act_dic = dict()
    file_path = '/home/ee597/Desktop/MiniTest/dataFile/NODE_{}.csv'
    file_list = ['1152', '13101', '23093', '25668', '27068', '27638', '28381', '31867', '31973', '33925']
    file_path_list = []
    for path in file_list:
        file_path_list.append(file_path.format(path))
    i = 0
    for node in hosts:
        data_frame = pd.read_csv(file_path_list[i])
        act_list = data_frame['ACTIVE'].to_list()
        act_dic[node] = act_list
        i += 1
    # print(act_dic)
    start_time = time.time()
    clk = 0
    while True:
        if start_time - time.time() > 300:
            break
        clk += 1
        print(clk)
        for node in hosts:
            print(node, act_dic[node][clk])
        print('----------------------------')
        time.sleep(sleep_time)