#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import network_flow_capture


def create_network():
    "Create a network with 10 hosts and one server."

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

    info('*** Running socket server\n')

    for node in hosts:
        node.cmd('python3 ./node_udp_server.py &')
        node.cmd('python3 ./node_udp_client.py &')


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