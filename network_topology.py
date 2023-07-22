#!/usr/bin/env python3

import time
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random
import pandas as pd
import threading


class OVSController(Controller):
    def start(self):
        "Overridden start() to run ovs-vsctl"
        self.cmd("ovs-vsctl --no-wait init")

    def stop(self):
        "Overridden stop() to stop ovs-vsctl"
        self.cmd("ovs-vsctl --no-wait exit")


def create_network():
    """Create a network with 10 hosts and one server."""
    net = Mininet(controller=OVSController, switch=OVSSwitch)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    server = net.addHost('server', ip='10.0.0.100')
    hosts = []
    for n in range(1, 12):
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
    i = 0
    for host in hosts:
        if i == len(hosts) - 1:
            break
        host.cmd('sudo ./main_client.py > ./dataFile/terminal_output/{}_output.txt &'.format(host.IP()))
        i += 1
    CLI(net)
    info('*** Stopping network')
    net.stop()


