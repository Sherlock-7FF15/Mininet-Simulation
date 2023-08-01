#!/usr/bin/env python3
import time

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSController
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
    server = net.addHost('server', ip='10.0.0.100')
    hosts = []
    for n in range(1, 52):
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
    k_para = [5, 10]
    ratio = [1]
    duration = [10, 20]
    data_set = ['training', 'testing', 'validation']
    for k in k_para:
        for r in ratio:
            for t in duration:
                for memo in data_set:
                    i = 0
                    for host in hosts:
                        if i == len(hosts) - 1:
                            time.sleep(60)
                            print('Experiment {} {} {} {} Start'.format(k, r, t, memo))
                            host.cmd('sudo ./main_server.py --k {} --ratio {} --duration {} --memo {} '
                                     '> ./dataFile/terminal_output/{}_output.txt'
                                     .format(k, r, t, memo, host.IP()))
                            break
                        host.cmd('sudo ./main_client.py > ./dataFile/terminal_output/{}_output.txt &'.format(host.IP()))
                        i += 1
                    time.sleep(200)
    # CLI(net)
    info('*** Stopping network')
    net.stop()
