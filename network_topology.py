#!/usr/bin/env python3
import time

from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random

import pandas as pd
import threading


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
        node.cmd('python3 ./network_flow_capture.py ')
    # Sharing packet volume within past 1 second. This code will be executed forever.
    for node in hosts:
        node.cmd('python3 ./node_udp_server.py &')
        node.cmd('python3 ./node_udp_client.py --t 5 &')

    info('*** Running CLI\n')
    threads = []
    while True:
        command = input('Input Command> ')
        if command == 'start':
            # Start simulation
            t = threading.Thread(target=node_time_control, args=(hosts, 0.5))
            t.start()
            threads.append(t)
        if command == 'exit':
            for t in threads:
                t.join()
            break
        if command == 'CLI':
            CLI(net)
    info('*** Stopping network')
    net.stop()


def node_time_control(hosts, time_interval):
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
        for node in hosts:
            if act_dic[node][clk] == 1:
                node.cmd('sudo ./benign_behavior.py --time 1 --n 10 --sleep 0.1')
            # print(node, act_dic[node][clk])
            # print(clk)
        # print('----------------------------')
        time.sleep(time_interval)


def ddos_attack(hosts, perc):
    nums = random.sample(range(len(hosts)), int(perc*len(hosts)))
    selected_nodes = []
    for i in nums:
        selected_nodes.append(hosts[i])
    for node in selected_nodes:
        node.cmd('sudo ./ddos_attack_simulation.py')