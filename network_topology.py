#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def create_network():
    "Create a network with 20 hosts and one server."

    net = Mininet(controller=OVSController)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    server = net.addHost('server', ip='10.0.0.21')
    hosts = [net.addHost('h%d' % n, ip='10.0.0.%d' % n) for n in range(1, 11)]

    info('*** Adding switch\n')
    switch = net.addSwitch('s0')

    info('*** Creating links\n')
    for host in hosts:
        net.addLink(host, switch)
    net.addLink(server, switch)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    while True:
        command = input('input command')

    CLI(net)

    info('*** Stopping network')
    net.stop()